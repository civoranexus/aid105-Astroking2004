from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
import json
from pathlib import Path
from contextlib import asynccontextmanager

from src.models.inference import score_schemes

DATA_DIR = Path(__file__).resolve().parents[2] / "src" / "data"
SCHEMES_FILE = DATA_DIR / "sample_schemes.json"

# Initialize SCHEMES to ensure variable exists before lifespan runs
SCHEMES = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup/shutdown. Loads schemes into memory."""
    global SCHEMES
    try:
        SCHEMES = json.loads(SCHEMES_FILE.read_text())
    except Exception:
        SCHEMES = []
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


# Schemes are loaded during application lifespan startup


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/schemes")
def get_schemes():
    return SCHEMES


@app.post("/recommendations")
def recommendations(user: UserProfile, top_k: int = 5):
    # Use model_dump for Pydantic v2 compatibility
    user_data = user.model_dump() if hasattr(user, "model_dump") else user.dict()
    results = score_schemes(user_data, SCHEMES)
    return {
        "user": user.dict(),
        "results": results[:top_k],
    }
