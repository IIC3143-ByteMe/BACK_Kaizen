import pytest
from datetime import date
from schemas.daily_completions import (
    DailyCompletionsResponse,
    CompletionEntryResponse,
)


@pytest.mark.asyncio
async def test_create_and_update_daily_completion(client, user_token, clean_db):
    headers = {"Authorization": f"Bearer {user_token}"}
    today = date.today()
    weekday = today.strftime("%a")

    habit_payload = {
        "title": "Drink water",
        "description": "Drink at least 1L of water",
        "icon": "glass",
        "color": "#00BFFF",
        "group": "Health",
        "type": "daily",
        "ikigai_category": "body",
        "goal": {"period": "daily", "type": "quantity", "target": 1, "unit": "L"},
        "task_days": [weekday],
        "reminders": ["09:00"],
    }

    resp = client.post("/habits/", json=habit_payload, headers=headers)
    assert resp.status_code == 201, resp.json()
    habit = resp.json()
    habit_id = habit["_id"]

    resp = client.post("/daily-completions/", json=str(today), headers=headers)
    assert resp.status_code in (200, 201), resp.json()
    daily = resp.json()
    parsed_daily = DailyCompletionsResponse.model_validate(daily)
    assert any(c.habit_id == habit_id for c in parsed_daily.completions)

    progress_payload = {"habit_id": habit_id, "date": str(today), "progress": 1}
    resp = client.patch(
        "/daily-completions/update-progress", json=progress_payload, headers=headers
    )
    assert resp.status_code == 200, resp.json()
    daily_update = resp.json()
    parsed_update = DailyCompletionsResponse.model_validate(daily_update)
    completion = next(c for c in parsed_update.completions if c.habit_id == habit_id)
    assert completion.completed is True
    assert completion.percentage >= 1.0

    resp = client.get(f"/daily-completions/{today}", headers=headers)
    assert resp.status_code == 200, resp.json()
    daily_get = resp.json()
    parsed_get = DailyCompletionsResponse.model_validate(daily_get)
    assert parsed_get.date == today
    assert any(c.habit_id == habit_id for c in parsed_get.completions)

    daily_id = daily_get["_id"] if "_id" in daily_get else daily_get["id"]
    resp = client.delete(f"/daily-completions/{daily_id}", headers=headers)
    assert resp.status_code == 204

    resp = client.get(f"/daily-completions/{today}", headers=headers)
    assert resp.status_code == 404
