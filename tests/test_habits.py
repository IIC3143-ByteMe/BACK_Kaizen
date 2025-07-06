def test_create_habit_missing_fields_returns_422(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/habits/", json={}, headers=headers)
    assert resp.status_code == 422


def test_create_and_get_habit_success(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    payload = {
        "title": "New Habit",
        "description": "Desc",
        "icon": "icon",
        "color": "blue",
        "grupo": "G1",
        "type": "personal",
        "goal_period": "daily",
        "goal_value": 1,
        "goal_value_unit": "times",
        "task_days": "Mon,Tue",
        "reminders": "09:00",
        "ikigai_category": "Life",
    }
    r = client.post("/habits/", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == payload["title"]

    # GET para asegurarnos
    r2 = client.get(f"/habits/{data['id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["id"] == data["id"]
