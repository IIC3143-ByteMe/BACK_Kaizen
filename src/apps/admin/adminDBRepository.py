from typing import List, Optional
from models.models import User, Habit


class AdminDBRepository:
    async def get_user(self, user_id: str) -> Optional[User]:
        return await User.get(user_id)

    async def list_habits_for_user(self, user_id: str) -> List[Habit]:
        return await Habit.find(Habit.owner_id == user_id).to_list()

    async def delete_habit(self, habit: Habit) -> None:
        await habit.delete()
