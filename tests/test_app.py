import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "teststudent@example.com"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_not_found():
    activity_name = "Chess Club"
    email = "missingstudent@example.com"

    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
