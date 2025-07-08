def test_create_habit_missing_fields_returns_422(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = client.post("/habits/", json={}, headers=headers)
    assert resp.status_code == 422


def test_create_and_get_habit_success(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    payload = {
    "owner_id": "668cbee4dcdab82ae503f7cd",
    "title": "Read every day",
    "description": "Read at least 10 pages of a book every day",
    "icon": "book",
    "color": "#FFD700",
    "group": "Personal Development",
    "type": "daily",
    "ikigai_category": "Mind",
    "goal": {
        "target": 10,
        "unit": "pages",
        "period": "daily",
        "type": "quantity"
    },
    "task_days": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "reminders": ["08:00", "20:00"]
}

    r = client.post("/habits/", json=payload, headers=headers)
    print("RESPONSE JSON:", r.json())
    assert r.status_code == 201

    data = r.json()
    assert data["title"] == payload["title"]

    # GET para asegurarnos
    r2 = client.get(f"/habits/{data['_id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["_id"] == data["_id"]
