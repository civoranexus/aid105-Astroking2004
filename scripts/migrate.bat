@echo off
setlocal
if "%DATABASE_URL%"=="" (
  echo Please set DATABASE_URL environment variable before running.
  exit /b 1
)
python -m alembic upgrade head
