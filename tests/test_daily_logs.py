import pytest
import asyncio
from jose import jwt
from models.models import Habit


@pytest.fixture(scope="module")
def habit_id(client, user_token):
    # Inserta un hábito directamente para usar en logs
    payload = jwt.decode(user_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload["sub"]
    habit = asyncio.get_event_loop().run_until_complete(
        Habit(
            owner_id=user_id,
            title="Log Habit",
            description="desc",
            icon="i",
            color="c",
            grupo="g",
            type="t",
            goal_period="daily",
            goal_value=1,
            goal_value_unit="times",
            task_days="Mon",
            reminders="08:00",
            ikigai_category="Life",
        ).insert()
    )
    return str(habit.id)


def test_daily_logs_crud(client, user_token, habit_id):
    headers = {"Authorization": f"Bearer {user_token}"}

    # Create
    r1 = client.post(
        "/daily-logs/",
        json={"habit_id": habit_id, "date": "2025-06-01T00:00:00Z", "completed": True},
        headers=headers,
    )
    assert r1.status_code == 201
    log_id = r1.json()["id"]

    # List
    r2 = client.get("/daily-logs/", headers=headers)
    assert any(l["id"] == log_id for l in r2.json())

    # Update
    r3 = client.patch(f"/daily-logs/{log_id}", json={"notes": "note"}, headers=headers)
    assert r3.status_code == 200
    assert r3.json()["notes"] == "note"

    # Delete
    r4 = client.delete(f"/daily-logs/{log_id}", headers=headers)
    assert r4.status_code == 204
