import csv
import json
from pathlib import Path
from typing import List

# Define paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "src" / "data" / "sample_schemes.json"
CSV_FILE = BASE_DIR / "updated_data.csv"

def parse_list(value: str) -> List[str]:
    """Helper to parse comma-separated strings into lists."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

def import_csv_to_json():
    if not CSV_FILE.exists():
        print(f"Error: {CSV_FILE} not found. Please create it first.")
        return

    new_schemes = []
    
    print(f"Reading from {CSV_FILE}...")
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows or rows missing critical identifiers
                if not row.get("slug") or not row.get("scheme_name"):
                    continue

                # Convert CSV row to Scheme format
                scheme = {
                    "id": row.get("slug", "").strip(),
                    "title": row.get("scheme_name", "").strip(),
                    "description": row.get("details", "").strip(),
                    "eligible_income_min": 0,
                    "eligible_income_max": None,
                    "eligible_age_min": 0,
                    "eligible_age_max": None,
                    "eligible_states": [],
                    "tags": parse_list(row.get("tags", "")),
                    "benefits": [row.get("benefits", "").strip()] if row.get("benefits", "").strip() else [],
                    "documents": parse_list(row.get("documents", "")),
                    "apply_url": "",
                    "eligibility": row.get("eligibility", "").strip(),
                    "application": row.get("application", "").strip(),
                    "level": row.get("level", "").strip(),
                    "schemeCategory": row.get("schemeCategory", "").strip()
                }
                new_schemes.append(scheme)
                
        print(f"Parsed {len(new_schemes)} schemes from CSV.")

        # Load existing schemes
        existing_schemes = []
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    existing_schemes = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Existing JSON file was corrupted or empty. Starting fresh.")
        
        # Append new schemes (checking for duplicate IDs could be added here)
        existing_ids = {s["id"] for s in existing_schemes}
        for scheme in new_schemes:
            if scheme["id"] not in existing_ids:
                existing_schemes.append(scheme)
                existing_ids.add(scheme["id"])
        
        # Write back to JSON
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_schemes, f, indent=2)
            print(f"Successfully updated {DATA_FILE}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import_csv_to_json()