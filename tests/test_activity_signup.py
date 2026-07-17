import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"],
        }
    }
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_signup_participant_adds_them_to_activity(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=student@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student@mergington.edu for Chess Club"
    assert "student@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_them_from_activity(client):
    response = client.delete(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
