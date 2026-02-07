from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import logging
from pathlib import Path
from contextlib import asynccontextmanager
import sys
import os

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.inference import score_schemes
from src.models.ai_service import generate_chat_response, MODEL_NAME
from src.backend.db import get_db, engine
from src.backend import models_db
from sqlalchemy.orm import Session

DATA_DIR = Path(__file__).resolve().parents[2] / "src" / "data"
SCHEMES_FILE = DATA_DIR / "sample_schemes.json"

# Initialize SCHEMES to ensure variable exists before lifespan runs
SCHEMES = []
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup/shutdown. Loads schemes into memory and ensures DB tables."""
    global SCHEMES
    app.state.schemes = []
    try:
        logger.info(f"Looking for schemes file at: {SCHEMES_FILE}")
        if SCHEMES_FILE.exists():
            content = SCHEMES_FILE.read_text()
            if not content.strip():
                logger.warning(f"Schemes file exists but is empty: {SCHEMES_FILE}")
            else:
                app.state.schemes = json.loads(content)
                SCHEMES = app.state.schemes
                logger.info(f"✓ Loaded {len(app.state.schemes)} schemes from JSON.")
        else:
            logger.error(f"✗ Schemes file not found at: {SCHEMES_FILE}")
            logger.info("Please run: python import_schemes.py")
    except json.JSONDecodeError as e:
        logger.error(f"✗ Invalid JSON in {SCHEMES_FILE}: {e}")
    except Exception as e:
        logger.error(f"✗ Failed to load schemes: {e}")

    # Ensure DB tables exist for local/dev
    try:
        models_db.Base.metadata.create_all(engine)
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    yield


app = FastAPI(title="SchemeAssist AI - Backend", version="0.1", lifespan=lifespan)

# CORS configuration for Render deployment
origins = [
    "http://localhost:5173",  # Local development - Vite default
    "http://localhost:3000",  # Alternative local dev port
    "http://localhost:8000",  # Local backend
    "https://*.onrender.com",  # Render services
    os.getenv("FRONTEND_URL", ""),  # Custom frontend URL from environment
]

# Remove empty strings from origins
origins = [origin for origin in origins if origin]

# Parse ALLOW_ALL_ORIGINS as an explicit boolean
allow_all_env = os.getenv("ALLOW_ALL_ORIGINS", "").strip().lower()
allow_all = allow_all_env in ("1", "true", "yes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfile(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    income: Optional[float] = None
    state: Optional[str] = None
    district: Optional[str] = None
    needs: List[str] = Field(default_factory=list)


class SchemeIn(BaseModel):
    scheme_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    eligibility: Optional[str] = None
    application: Optional[str] = None
    level: Optional[str] = None
    schemeCategory: Optional[str] = None
    eligible_income_min: Optional[float] = None
    eligible_income_max: Optional[float] = None
    eligible_states: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    documents: Optional[List[str]] = None


class ChatRequest(BaseModel):
    query: str


# Schemes are loaded during application lifespan startup


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/debug")
def health_debug(request: Request):
    """Debug endpoint to check app state"""
    schemes = getattr(request.app.state, "schemes", [])
    return {
        "status": "ok",
        "schemes_loaded": len(schemes),
        "schemes_file_exists": SCHEMES_FILE.exists(),
        "data_dir": str(DATA_DIR),
        "schemes_file_path": str(SCHEMES_FILE),
    }


@app.get("/")
def root():
    return {"message": "SchemeAssist API is running", "docs": "/docs"}


@app.get("/schemes")
def get_schemes(request: Request):
    try:
        schemes = getattr(request.app.state, "schemes", [])
        if not schemes:
            logger.error("No schemes available - check if import_schemes.py was run")
            # Try loading from file as fallback
            if SCHEMES_FILE.exists():
                try:
                    content = SCHEMES_FILE.read_text()
                    schemes = json.loads(content)
                    logger.info(f"Loaded {len(schemes)} schemes from file as fallback")
                except Exception as e:
                    logger.error(f"Failed to load schemes from file: {e}")
                    raise HTTPException(status_code=503, detail="Schemes data not loaded. Run import_schemes.py.")
            else:
                raise HTTPException(status_code=503, detail="Schemes data not loaded. Run import_schemes.py.")
        def scheme_richness(s: dict) -> int:
            score = 0
            if s.get("eligibility"):
                score += 2
            if s.get("application"):
                score += 2
            if s.get("level"):
                score += 1
            if s.get("schemeCategory"):
                score += 1
            if s.get("tags"):
                score += 1
            if s.get("benefits"):
                score += 1
            if s.get("documents"):
                score += 1
            description = s.get("description") or ""
            if len(description) > 120:
                score += 1
            return score

        schemes_sorted = sorted(schemes, key=scheme_richness, reverse=True)
        return schemes_sorted
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /schemes endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/recommendations")
def recommendations(user: UserProfile, request: Request, top_k: int = 5, include_central: bool = True):
    # Standardize on model_dump for Pydantic v2
    user_data = user.model_dump()
    
    # Normalize user data for better matching
    if user_data.get("state"):
        user_data["state"] = user_data["state"].lower()

    user_name = user_data.get('name')
    user_income = user_data.get('income')
    user_state = user_data.get('state')
    user_needs = user_data.get('needs', [])
    logger.info(
        f"Processing recommendations for user: {user_name} "
        f"(Income: {user_income}, State: {user_state}, Needs: {user_needs}, Include Central: {include_central})"
    )

    # Use JSON schemes loaded in memory (primary source)
    json_schemes = getattr(request.app.state, "schemes", [])
    logger.info(f"Found {len(json_schemes)} schemes in app state.")
    
    # Standardize JSON schemes to use 'scheme_id' instead of 'id'
    standardized_json = []
    for s in json_schemes:
        s_copy = s.copy()
        if "id" in s_copy:
            s_copy["scheme_id"] = s_copy.pop("id")
        standardized_json.append(s_copy)

    all_schemes = standardized_json
    logger.info(f"Total schemes to score: {len(all_schemes)}")
    
    results = score_schemes(user_data, all_schemes, include_central=include_central)
    logger.info(f"Found {len(results)} recommendations")
    
    # Transform results to match frontend expectations
    transformed = []
    for r in results[:top_k]:
        transformed.append({
            "id": r.get("scheme_id") or r.get("id"),
            "title": r.get("title"),
            "description": r.get("description"),
            "eligibility": r.get("eligibility"),
            "application": r.get("application"),
            "level": r.get("level"),
            "schemeCategory": r.get("schemeCategory"),
            "tags": r.get("tags"),
            "benefits": r.get("benefits"),
            "documents": r.get("documents")
        })
    
    return transformed


@app.post("/users")
def create_user(user: UserProfile, db: Session = Depends(get_db)):
    data = user.model_dump()
    db_user = models_db.User(
        external_id=data.get("id"),
        name=data.get("name"),
        age=data.get("age"),
        income=data.get("income"),
        state=data.get("state"),
        district=data.get("district"),
        needs=data.get("needs"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "external_id": db_user.external_id}


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(models_db.User).filter_by(id=user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    income_value = u.income if u.income is not None else None
    return {
        "id": u.id,
        "external_id": u.external_id,
        "name": u.name,
        "age": u.age,
        "income": float(income_value) if income_value is not None else None,
        "state": u.state,
        "district": u.district,
        "needs": u.needs,
    }


@app.post("/schemes/db")
def create_scheme(scheme: SchemeIn, db: Session = Depends(get_db)):
    data = scheme.model_dump()
    db_scheme = models_db.Scheme(
        scheme_id=data.get("scheme_id"),
        title=data.get("title"),
        description=data.get("description"),
        eligibility=data.get("eligibility"),
        application=data.get("application"),
        level=data.get("level"),
        scheme_category=data.get("schemeCategory"),
        metadata_json={
            "eligible_income_min": data.get("eligible_income_min"),
            "eligible_income_max": data.get("eligible_income_max"),
            "eligible_age_min": data.get("eligible_age_min"),
            "eligible_age_max": data.get("eligible_age_max"),
            "eligible_states": data.get("eligible_states"),
        },
        tags=data.get("tags"),
        benefits=data.get("benefits"),
        documents=data.get("documents"),
    )
    db.add(db_scheme)
    db.commit()
    db.refresh(db_scheme)
    return {"id": db_scheme.id, "scheme_id": db_scheme.scheme_id}


@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """AI-powered chat endpoint to answer questions about schemes."""
    # Fetch some schemes to provide context to the AI
    db_schemes = db.query(models_db.Scheme).limit(10).all()
    schemes_context = [
        {"title": s.title, "description": s.description} 
        for s in db_schemes
    ]
    
    response = await generate_chat_response(request.query, schemes_context)
    return {"query": request.query, "response": response, "model": MODEL_NAME}
