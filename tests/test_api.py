import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.main import app
from src.backend.db import get_db
from src.backend.models_db import Base

# Use an in-memory SQLite database for testing to avoid touching production data
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create tables in the test database
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up after tests
    Base.metadata.drop_all(bind=engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_user_lifecycle_and_recommendation():
    # 1. Create a user
    user_payload = {
        "id": "user_001",
        "name": "Test User",
        "age": 30,
        "income": 45000.0,
        "state": "Karnataka",
        "district": "Bangalore",
        "needs": ["education", "finance"]
    }
    create_res = client.post("/users", json=user_payload)
    assert create_res.status_code == 200
    db_id = create_res.json()["id"]

    # 2. Verify user retrieval
    get_res = client.get(f"/users/{db_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Test User"

    # 3. Add a scheme to the DB that matches the user
    scheme_payload = {
        "scheme_id": "SCH_TEST_01",
        "title": "Education Grant",
        "eligible_income_max": 50000,
        "eligible_states": ["Karnataka"],
        "tags": ["education"]
    }
    scheme_res = client.post("/schemes/db", json=scheme_payload)
    assert scheme_res.status_code == 200

    # 4. Get recommendations
    reco_res = client.post("/recommendations", json=user_payload)
    assert reco_res.status_code == 200
    results = reco_res.json()
    
    # Check if our added scheme is in the results
    scheme_ids = [s["id"] for s in results]
    assert "SCH_TEST_01" in scheme_ids

def test_get_user_not_found():
    """Verify 404 error for non-existent users."""
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_recommendations_no_matches():
    """Verify that an empty list is returned when no schemes match criteria."""
    # User with very high income that should fail all sample filters
    user_payload = {"income": 9999999, "state": "Mars", "needs": ["nothing"]}
    response = client.post("/recommendations", json=user_payload)
    assert response.status_code == 200
    assert len(response.json()) == 0