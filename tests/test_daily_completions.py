import pytest
from datetime import date

@pytest.mark.asyncio
def test_daily_completions_crud(client, user_factory):
    user = user_factory()
    client.post("/auth/register", json=user)
    login_resp = client.post("/auth/login", json=user)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    habit_data = {
        "title": "Drink Water",
        "description": "Drink 8 glasses per day",
        "icon": "💧",
        "color": "#00BFFF",
        "group": "health",
        "type": "daily",
        "ikigai_category": None,
        "goal": {
            "period": "day",
            "type": "quantity",
            "target": 8,
            "unit": "glasses"
        },
        "task_days": ["Mon"],   # Lunes, para que se cree el completion ese día
        "reminders": ["08:00"],
    }
    habit_resp = client.post("/habits/", json=habit_data, headers=headers)
    assert habit_resp.status_code == 201
    habit_id = habit_resp.json()["_id"]

    test_date = date(2024, 7, 8)
    resp = client.post(
    "/daily-completions/",
    data='"2024-07-08"',
    headers={**headers, "Content-Type": "application/json"},
    )
    assert resp.status_code in (200, 201)
    dc = resp.json()
    assert dc["date"].startswith(str(test_date))
    assert len(dc["completions"]) == 1
    assert dc["completions"][0]["habit_id"] == habit_id
    assert dc["completions"][0]["progress"] == 0.0
    assert dc["completions"][0]["completed"] is False

    patch_data = {
        "habit_id": habit_id,
        "date": str(test_date),
        "progress": 8,
    }
    resp = client.patch("/daily-completions/update-progress", json=patch_data, headers=headers)
    assert resp.status_code == 200
    dc = resp.json()
    completion = next(c for c in dc["completions"] if c["habit_id"] == habit_id)
    assert completion["progress"] == 8
    assert completion["percentage"] == 1.0
    assert completion["completed"] is True
    assert dc["day_completed"] is True

    resp = client.get(f"/daily-completions/{test_date}", headers=headers)
    assert resp.status_code == 200
    dc = resp.json()
    assert dc["date"].startswith(str(test_date))
    assert dc["completions"][0]["completed"] is True
