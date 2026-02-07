"""Smoke test to verify SQLAlchemy, psycopg2 and models load correctly.
Creates a temporary SQLite DB and attempts to create tables from models_db.Base.
"""
import os
import sys
from pathlib import Path

sys.path.append("src")

print("PYTHON PATH:", sys.executable)

try:
    import sqlalchemy
    print("sqlalchemy ok", sqlalchemy.__version__)
except Exception as e:
    print("sqlalchemy import failed:", e)
    raise

try:
    import psycopg2
    print("psycopg2 ok", psycopg2.__version__)
except Exception as e:
    print("psycopg2 import failed:", e)
    raise

from backend.models_db import Base
from sqlalchemy import create_engine

data_dir = Path(".data")
data_dir.mkdir(exist_ok=True)
db_path = data_dir / "smoke_test.db"
engine = create_engine(f"sqlite:///{db_path}")

print("Creating tables into", db_path)
Base.metadata.create_all(engine)
print("Tables created successfully")
