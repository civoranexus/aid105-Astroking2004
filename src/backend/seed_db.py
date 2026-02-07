import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.backend.db import SessionLocal
from src.backend import models_db

DATA_DIR = Path(__file__).resolve().parents[2] / "src" / "data"
SCHEMES_FILE = DATA_DIR / "sample_schemes.json"

def seed():
    if not SCHEMES_FILE.exists():
        print("No sample_schemes.json found to seed.")
        return

    db = SessionLocal()
    try:
        schemes_data = json.loads(SCHEMES_FILE.read_text())
        for item in schemes_data:
            # Handle both 'id' (from JSON) and 'scheme_id'
            sid = item.get('scheme_id') or item.get('id')
            # Check if exists
            exists = db.query(models_db.Scheme).filter_by(scheme_id=sid).first()
            if not exists:
                new_scheme = models_db.Scheme(
                    scheme_id=sid,
                    title=item.get('title'),
                    description=item.get('description'),
                    eligibility=item.get('eligibility'),
                    application=item.get('application'),
                    level=item.get('level'),
                    scheme_category=item.get('schemeCategory'),
                    tags=item.get('tags', []),
                    benefits=item.get('benefits', []),
                    documents=item.get('documents', []),
                    metadata_json={
                        "eligible_income_min": item.get("eligible_income_min"),
                        "eligible_income_max": item.get("eligible_income_max"),
                        "eligible_age_min": item.get("eligible_age_min"),
                        "eligible_age_max": item.get("eligible_age_max"),
                        "eligible_states": item.get("eligible_states"),
                    }
                )
                db.add(new_scheme)
        db.commit()
        print(f"Successfully seeded {len(schemes_data)} schemes.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()