import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Art Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]


def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Drama Society"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
