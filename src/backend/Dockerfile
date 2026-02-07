FROM python:3.10-slim

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install build dependencies
COPY src/backend/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
	pip install --no-cache-dir -r /app/requirements.txt

# Copy Alembic config and migration scripts so alembic can run
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

# Copy application code
COPY src /app/src

# Add entrypoint script
COPY src/backend/docker-entrypoint.sh /app/docker-entrypoint.sh
COPY src/backend/wait_for_db.py /app/wait_for_db.py
RUN chmod +x /app/docker-entrypoint.sh

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser && \
	chown -R appuser:appuser /app

USER appuser
WORKDIR /app/src/backend
EXPOSE 8000
ENTRYPOINT ["/app/docker-entrypoint.sh"]
