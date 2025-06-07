from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.models import Habit, DailyHabitLog
from schemas.schemas import HabitCreate, HabitUpdate, HabitOut, HabitProgress
from utils.dependencies import get_current_user
from schemas.schemas import TokenData

router = APIRouter(prefix="/habits", tags=["habits"])


# ----- CREAR HÁBITO (USER) -----
@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
    habit_in: HabitCreate, current_user: TokenData = Depends(get_current_user)
):
    new_habit = Habit(
        owner_id=current_user.user_id,
        title=habit_in.title,
        description=habit_in.description,
    )
    await new_habit.insert()
    return HabitOut.from_orm(new_habit)


# ----- LISTAR HÁBITOS PROPIOS (USER) -----
@router.get("/", response_model=List[HabitOut])
async def get_my_habits(current_user: TokenData = Depends(get_current_user)):
    habits = await Habit.find(Habit.owner_id == current_user.user_id).to_list()
    return [HabitOut.from_orm(h) for h in habits]


# ----- MODIFICAR HÁBITO (USER O ADMIN) -----
@router.put("/{habit_id}", response_model=HabitOut)
async def update_habit(
    habit_id: str,
    habit_update: HabitUpdate,
    current_user: TokenData = Depends(get_current_user),
):
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    # Solo el dueño o admin puede modificarlo
    if habit.owner_id != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    if habit_update.title is not None:
        habit.title = habit_update.title
    if habit_update.description is not None:
        habit.description = habit_update.description
    await habit.save()
    return HabitOut.from_orm(habit)


# ----- ELIMINAR HÁBITO (ADMIN) -----
@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: str, current_user: TokenData = Depends(get_current_user)
):
    # Requiere rol admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Permisos insuficientes: se requiere admin"
        )
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    await habit.delete()
    return None


# ----- OBTENER PROGRESO PERSONAL (USER) -----
@router.get("/progress", response_model=List[HabitProgress])
async def get_my_progress(current_user: TokenData = Depends(get_current_user)):
    habits = await Habit.find(Habit.owner_id == current_user.user_id).to_list()
    progreso = []
    for habit in habits:
        logs = await DailyHabitLog.find(
            (DailyHabitLog.user_id == current_user.user_id)
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
