from typing import List
from fastapi import HTTPException, status
from schemas.schemas import HabitProgress, TokenData
from apps.admin.adminDBRepository import AdminDBRepository

class AdminService:
    def __init__(self):
        self.repo = AdminDBRepository()

    async def get_user_progress(self, user_id: str, admin: TokenData) -> List[HabitProgress]:
        # require_admin dependency ensures admin
        user = await self.repo.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        habits = await self.repo.list_habits_for_user(user_id)
        result: List[HabitProgress] = []
        for habit in habits:
            logs = await self.repo.list_logs_for_habit(user_id, str(habit.id))
            total = len(logs)
            done = sum(1 for log in logs if log.completed)
            rate = (done / total * 100) if total else 0.0
            result.append(HabitProgress(
                habit_id=str(habit.id),
                total_days=total,
                completed_days=done,
                completion_rate=rate
            ))
        return result

    async def delete_habit(self, habit_id: str, admin: TokenData) -> None:
        # require_admin ensures admin role
        from models.models import Habit
        habit = await Habit.get(habit_id)
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hábito no encontrado"
            )
        await self.repo.delete_habit(habit)