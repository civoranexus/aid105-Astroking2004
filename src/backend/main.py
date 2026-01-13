from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from pathlib import Path
from contextlib import asynccontextmanager

from src.models.inference import score_schemes
from src.models.ai_service import generate_chat_response
from src.backend.db import get_db, engine
from src.backend import models_db
from sqlalchemy.orm import Session

DATA_DIR = Path(__file__).resolve().parents[2] / "src" / "data"
SCHEMES_FILE = DATA_DIR / "sample_schemes.json"

# Initialize SCHEMES to ensure variable exists before lifespan runs
SCHEMES = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup/shutdown. Loads schemes into memory and ensures DB tables."""
    global SCHEMES
    try:
        SCHEMES = json.loads(SCHEMES_FILE.read_text())
    except Exception:
        SCHEMES = []

    # Ensure DB tables exist for local/dev
    try:
        models_db.Base.metadata.create_all(engine)
    except Exception:
        pass

    yield


app = FastAPI(title="SchemeAssist AI - Backend", version="0.1", lifespan=lifespan)


class UserProfile(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    income: Optional[float] = None
    state: Optional[str] = None
    district: Optional[str] = None
    needs: List[str] = Field(default_factory=list)


class SchemeIn(BaseModel):
    scheme_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    eligible_income_min: Optional[float] = None
    eligible_income_max: Optional[float] = None
    eligible_states: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    documents: Optional[List[str]] = None
    apply_url: Optional[str] = None


class ChatRequest(BaseModel):
    query: str


# Schemes are loaded during application lifespan startup


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/schemes")
def get_schemes():
    return SCHEMES


@app.post("/recommendations")
def recommendations(user: UserProfile, top_k: int = 5, db: Session = Depends(get_db)):
    # Use model_dump for Pydantic v2 compatibility
    user_data = user.model_dump() if hasattr(user, "model_dump") else user.dict()
    
    # Combine JSON schemes with DB schemes for a comprehensive search
    db_schemes = db.query(models_db.Scheme).all()
    formatted_db_schemes = []
    for s in db_schemes:
        meta = s.metadata_json or {}
        formatted_db_schemes.append({
            "scheme_id": s.scheme_id,
            "title": s.title,
            "description": s.description,
            "eligible_income_min": meta.get("eligible_income_min"),
            "eligible_income_max": meta.get("eligible_income_max"),
            "eligible_states": meta.get("eligible_states"),
            "tags": s.tags,
            "benefits": s.benefits
        })

    all_schemes = SCHEMES + formatted_db_schemes
    results = score_schemes(user_data, all_schemes)
    
    return {
        "user": user_data,
        "results": results[:top_k],
    }


@app.post("/users")
def create_user(user: UserProfile, db: Session = Depends(get_db)):
    data = user.model_dump() if hasattr(user, "model_dump") else user.dict()
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
    return {
        "id": u.id,
        "external_id": u.external_id,
        "name": u.name,
        "age": u.age,
        "income": float(u.income) if u.income is not None else None,
        "state": u.state,
        "district": u.district,
        "needs": u.needs,
    }


@app.post("/schemes/db")
def create_scheme(scheme: SchemeIn, db: Session = Depends(get_db)):
    data = scheme.model_dump() if hasattr(scheme, "model_dump") else scheme.dict()
    db_scheme = models_db.Scheme(
        scheme_id=data.get("scheme_id"),
        title=data.get("title"),
        description=data.get("description"),
        metadata_json={
            "eligible_income_min": data.get("eligible_income_min"),
            "eligible_income_max": data.get("eligible_income_max"),
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
    return {"query": request.query, "response": response}
