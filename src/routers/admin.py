from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.models import User, Habit, DailyHabitLog
from schemas.schemas import HabitProgress
from utils.dependencies import require_admin
from schemas.schemas import TokenData

router = APIRouter(prefix="/admin", tags=["admin"])


# ----- REVISAR PROGRESO DE UN USUARIO ESPECÍFICO (ADMIN) -----
@router.get("/user-progress/{user_id}", response_model=List[HabitProgress])
async def get_user_progress(
    user_id: str, current_admin: TokenData = Depends(require_admin)
):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    habits = await Habit.find(Habit.owner_id == user_id).to_list()
    progreso = []
    for habit in habits:
        logs = await DailyHabitLog.find(
            (DailyHabitLog.user_id == user_id)
            & (DailyHabitLog.habit_id == str(habit.id))
        ).to_list()
        total_days = len(logs)
        completed_days = sum(1 for log in logs if log.completed)
        rate = (completed_days / total_days) * 100 if total_days > 0 else 0.0
        progreso.append(
            HabitProgress(
                habit_id=str(habit.id),
                total_days=total_days,
                completed_days=completed_days,
                completion_rate=rate,
            )
        )
    return progreso


# ----- ELIMINAR HÁBITO (ADMIN) -----
@router.delete("/habit/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_habit(
    habit_id: str, current_admin: TokenData = Depends(require_admin)
):
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    await habit.delete()
    return None
