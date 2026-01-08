#!/bin/sh
set -e

# Wait for DB to be reachable (best-effort)
python /app/wait_for_db.py || true

# Run migrations (best-effort)
python /app/apply_migrations.py || true

# Start the Uvicorn server
exec uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
