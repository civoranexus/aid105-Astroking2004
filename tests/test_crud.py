from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_create_user_and_get():
    payload = {
        "id": "u100",
        "name": "Bob",
        "age": 40,
        "income": 15000,
        "state": "Karnataka",
        "needs": ["training"]
    }
    r = client.post("/users", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "id" in body
    user_id = body["id"]

    r2 = client.get(f"/users/{user_id}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["name"] == "Bob"


def test_create_scheme_and_recommend():
    scheme = {
        "scheme_id": "T-100",
        "title": "Test Scheme",
        "description": "A test scheme",
        "eligible_income_min": 0,
        "eligible_income_max": 20000,
        "eligible_states": ["karnataka"],
        "tags": ["training"],
        "benefits": ["grant"],
        "documents": ["id_proof"]
    }
    r = client.post("/schemes/db", json=scheme)
    assert r.status_code == 200
    body = r.json()
    assert body.get("scheme_id") == "T-100"

    # Now call recommendations for a user matching scheme
    user = {"name": "Charlie", "income": 10000, "state": "Karnataka", "needs": ["training"]}
    r2 = client.post("/recommendations", json=user)
    assert r2.status_code == 200
    res = r2.json()
    assert isinstance(res, list)
