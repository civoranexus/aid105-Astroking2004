# SchemeAssist AI — Backend (src)

Quick start (local):

1. Create a Python 3.10 virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r src/backend/requirements.txt
```

2. Run the app:

```bash
uvicorn src.backend.main:app --reload
```

Endpoints:
- `GET /health` — health check
- `GET /schemes` — list sample schemes
- `POST /recommendations` — body: user profile JSON, returns ranked schemes
