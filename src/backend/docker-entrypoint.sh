#!/bin/sh
set -e

echo "Waiting for database..."
python /app/wait_for_db.py || true

echo "Running migrations..."
cd /app
python -m alembic upgrade head || true

echo "Starting application..."
exec uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
