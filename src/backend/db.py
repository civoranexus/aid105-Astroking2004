import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./schemeassist.db")

# Render provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Synchronous engine for simplicity
if DATABASE_URL.startswith("sqlite:"):
    # Ensure directory for SQLite DB exists (supports paths like sqlite:///./.data/db.sqlite)
    try:
        # Extract file path after scheme: sqlite:///path/to/file
        path = DATABASE_URL.split("sqlite:///")[1]
        dirpath = os.path.dirname(path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
    except Exception:
        pass

# Production database settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour (for production stability)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Try to create tables automatically for local/test environments
try:
    # import here to avoid circular imports at module import time
    from src.backend import models_db

    models_db.Base.metadata.create_all(engine)
except Exception:
    pass
