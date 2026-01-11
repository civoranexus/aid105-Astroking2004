# SchemeAssist AI — Backend (src)

Quick start (local):

1. Create a Python 3.10 virtualenv and install dependencies:

See the top-level `README.md` for consolidated project setup and quickstart instructions.

Backend quick commands:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r src/backend/requirements.txt
uvicorn src.backend.main:app --reload
```
