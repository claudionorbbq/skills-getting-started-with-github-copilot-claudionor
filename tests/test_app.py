from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import app, activities


def test_signup_rejects_duplicate_email_for_same_activity():
    original = deepcopy(activities)
    try:
        activities.clear()
        activities.update({
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            }
        })

        client = TestClient(app)
        response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
        assert len(activities["Chess Club"]["participants"]) == 2
    finally:
        activities.clear()
        activities.update(original)


def test_signup_rejects_when_activity_is_full():
    original = deepcopy(activities)
    try:
        activities.clear()
        activities.update({
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 2,
                "participants": ["one@mergington.edu", "two@mergington.edu"],
            }
        })

        client = TestClient(app)
        response = client.post("/activities/Chess Club/signup?email=three@mergington.edu")

        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is full"
        assert len(activities["Chess Club"]["participants"]) == 2
    finally:
        activities.clear()
        activities.update(original)
