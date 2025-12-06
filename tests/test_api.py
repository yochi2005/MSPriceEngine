"""Basic API tests."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "MSPriceEngine" in response.json()["name"]


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_search_empty():
    """Test search with no results."""
    response = client.get("/search?q=nonexistentproduct12345")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["products"] == []


def test_get_stores_empty():
    """Test get stores when database is empty."""
    response = client.get("/stores")
    assert response.status_code == 200
    assert response.json() == []


def test_get_product_not_found():
    """Test get product that doesn't exist."""
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
