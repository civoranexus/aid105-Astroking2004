import json
from pathlib import Path
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
            # Check if exists
            exists = db.query(models_db.Scheme).filter_by(scheme_id=item['scheme_id']).first()
            if not exists:
                new_scheme = models_db.Scheme(
                    scheme_id=item['scheme_id'],
                    title=item.get('title'),
                    description=item.get('description'),
                    tags=item.get('tags', []),
                    benefits=item.get('benefits', []),
                    metadata_json={
                        "eligible_income_min": item.get("eligible_income_min"),
                        "eligible_income_max": item.get("eligible_income_max"),
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