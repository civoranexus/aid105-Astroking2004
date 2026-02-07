import os
import sys

# Test environment bootstrap: set SQLite DB and ensure package path
DB_PATH = "./.data/test_app.db"
os.environ["DATABASE_URL"] = f"sqlite:///{DB_PATH}"
try:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
except Exception:
    pass

# Ensure src is importable for tests
sys.path.insert(0, "src")
