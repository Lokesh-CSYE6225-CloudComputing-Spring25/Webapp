import sys
import os

# Add the parent directory to sys.path to make app.py accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from app.routes import app  # ✅ Import app directly (avoid multiple initializations)

@pytest.fixture
def client():
    """Creates a test client for the Flask app"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check_success(client):
    """Test if /healthz endpoint returns HTTP 200"""
    response = client.get("/healthz")
    assert response.status_code == 200

def test_health_check_with_body(client):
    """Test if /healthz rejects requests with a body (should return 400)"""
    response = client.get("/healthz", json={"key": "value"})
    assert response.status_code == 400

def test_invalid_endpoint(client):
    """Test if an invalid endpoint returns HTTP 404"""
    response = client.get("/invalid_endpoint")
    assert response.status_code == 404

def test_method_not_allowed(client):
    """Test if using POST on /healthz returns HTTP 405"""
    response = client.post("/healthz")
    assert response.status_code == 405
