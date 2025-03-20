import sys
import os

# Add the parent directory to sys.path to make app.py accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from app import create_app
from app.models import db  # Ensure SQLAlchemy is correctly initialized

@pytest.fixture(scope="module")  # Changed scope to module
def app():
    """Creates and configures a test Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Creates a test client for the Flask app."""
    return app.test_client()

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