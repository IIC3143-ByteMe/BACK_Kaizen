from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.models import DailyHabitLog, Habit
from schemas.schemas import DailyHabitLogCreate, DailyHabitLogUpdate, DailyHabitLogOut
from utils.dependencies import get_current_user
from schemas.schemas import TokenData

router = APIRouter(prefix="/daily-logs", tags=["daily-logs"])


# ----- CREAR REGISTRO DIARIO DE HÁBITO -----
@router.post("/", response_model=DailyHabitLogOut, status_code=status.HTTP_201_CREATED)
async def create_daily_log(
    log_in: DailyHabitLogCreate, current_user: TokenData = Depends(get_current_user)
):
    habit = await Habit.get(log_in.habit_id)
    if not habit or habit.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=404, detail="Hábito no encontrado o no perteneciente al usuario"
        )
    log = DailyHabitLog(
        user_id=current_user.user_id,
        habit_id=log_in.habit_id,
        date=log_in.date,
        completed=log_in.completed,
        notes=log_in.notes,
    )
    await log.insert()
    return DailyHabitLogOut.from_orm(log)


# ----- LISTAR REGISTROS DIARIOS PROPIOS -----
@router.get("/", response_model=List[DailyHabitLogOut])
async def get_my_daily_logs(current_user: TokenData = Depends(get_current_user)):
    logs = await DailyHabitLog.find(
        DailyHabitLog.user_id == current_user.user_id
    ).to_list()
    return [DailyHabitLogOut.from_orm(l) for l in logs]


# ----- MODIFICAR REGISTRO DIARIO -----
@router.put("/{log_id}", response_model=DailyHabitLogOut)
async def update_daily_log(
    log_id: str,
    log_update: DailyHabitLogUpdate,
    current_user: TokenData = Depends(get_current_user),
):
    log = await DailyHabitLog.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Registro diario no encontrado")
    if log.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    if log_update.completed is not None:
        log.completed = log_update.completed
    if log_update.notes is not None:
        log.notes = log_update.notes
    await log.save()
    return DailyHabitLogOut.from_orm(log)


# ----- ELIMINAR REGISTRO DIARIO -----
@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_daily_log(
    log_id: str, current_user: TokenData = Depends(get_current_user)
):
    log = await DailyHabitLog.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Registro diario no encontrado")
    if log.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    await log.delete()
    return None
