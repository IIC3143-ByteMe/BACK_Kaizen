from typing import List, Optional
from models.models import User, Habit, DailyHabitLog

class AdminDBRepository:
    async def get_user(self, user_id: str) -> Optional[User]:
        return await User.get(user_id)

    async def list_habits_for_user(self, user_id: str) -> List[Habit]:
        return await Habit.find(Habit.owner_id == user_id).to_list()

    async def list_logs_for_habit(self, user_id: str, habit_id: str) -> List[DailyHabitLog]:
        return await DailyHabitLog.find(
            (DailyHabitLog.user_id == user_id) &
            (DailyHabitLog.habit_id == habit_id)
        ).to_list()

    async def delete_habit(self, habit: Habit) -> None:
        await habit.delete()