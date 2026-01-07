import sys
from fastapi.testclient import TestClient

# Ensure src package is importable
sys.path.append("src")

from backend.main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_recommendations():
    user = {
        "id": "u1",
        "name": "Test User",
        "age": 30,
        "income": 8000,
        "state": "Karnataka",
        "needs": ["training"]
    }
    r = client.post("/recommendations", json=user)
    assert r.status_code == 200
    body = r.json()
    assert "results" in body
    assert isinstance(body["results"], list)
    # top result should be a dict with keys scheme and score
    if body["results"]:
        top = body["results"][0]
        assert "scheme" in top and "score" in top
