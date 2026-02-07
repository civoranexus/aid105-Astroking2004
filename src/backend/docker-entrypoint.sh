#!/bin/sh
set -e

echo "Waiting for database..."
python /app/wait_for_db.py

echo "Running migrations..."
cd /app
python -m alembic -c /app/alembic.ini upgrade head

echo "Starting application..."
exec uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
