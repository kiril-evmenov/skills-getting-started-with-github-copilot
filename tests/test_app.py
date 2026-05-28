import pytest


def test_get_activities_returns_200_and_structure(client):
    # Arrange - none

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    first_activity = next(iter(data.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)


def test_signup_adds_participant_and_prevents_duplicate(client):
    # Arrange
    activity_name = "Art Club"
    email = "tester@example.com"

    # ensure email not present
    resp = client.get("/activities")
    participants = resp.json()[activity_name]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: sign up
    resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert resp.status_code == 200

    # Assert: participant added
    data_after = client.get("/activities").json()
    assert email in data_after[activity_name]["participants"]

    # Act: duplicate signup
    resp_dup = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: duplicate prevented
    assert resp_dup.status_code == 400
    assert "Student already signed up" in resp_dup.json().get("detail", "")
