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
