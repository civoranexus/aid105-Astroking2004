from fastapi.testclient import TestClient
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
        "income": 8000,
        "state": "Karnataka",
        "needs": ["training"]
    }
    r = client.post("/recommendations", json=user)
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    # top result should be a dict with keys id and name
    if body:
        top = body[0]
        assert "scheme_id" in top and "match_score" in top
