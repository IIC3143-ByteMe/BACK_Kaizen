def test_create_habit_missing_fields_returns_422(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/habits/", json={}, headers=headers)
    assert resp.status_code == 422


def test_create_and_get_habit_success(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    payload = {
        "title": "Dormir bien",
        "description": "Dormir 8 horas",
        "icon": "😴",
        "color": "blue",
        "group": "salud",
        "type": "sleep",
        "ikigai_category": "wellbeing",
        "goal": {
            "target": 8,
            "unit": "hours",
            "period": "daily",
            "type": "check" 
        },
        "task_days": ["monday", "tuesday", "wednesday"],
        "reminders": ["22:00"]
    }
    r = client.post("/habits/", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == payload["title"]

    # GET para asegurarnos
    r2 = client.get(f"/habits/{data['_id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["_id"] == data["_id"]
