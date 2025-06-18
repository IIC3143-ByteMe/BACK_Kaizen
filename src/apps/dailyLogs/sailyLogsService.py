from typing import List
from fastapi import HTTPException, status
from schemas.schemas import (
    DailyHabitLogCreate,
    DailyHabitLogUpdate,
    DailyHabitLogOut,
    TokenData,
)
from apps.dailyLogs.dailyLogsDBRepository import DailyLogsDBRepository
from models.models import Habit


class DailyLogsService:
    def __init__(self):
        self.repo = DailyLogsDBRepository()

    async def create_daily_log(
        self, payload: DailyHabitLogCreate, user: TokenData
    ) -> DailyHabitLogOut:
        habit = await Habit.get(payload.habit_id)
        if not habit or habit.owner_id != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hábito no encontrado o no perteneciente al usuario",
            )
        data = payload.dict()
        data["user_id"] = user.user_id
        log = await self.repo.create_log(data)
        return DailyHabitLogOut.from_orm(log)

    async def list_daily_logs(self, user: TokenData) -> List[DailyHabitLogOut]:
        logs = await self.repo.list_user_logs(user.user_id)
        return [DailyHabitLogOut.from_orm(log) for log in logs]

    async def update_daily_log(
        self, log_id: str, payload: DailyHabitLogUpdate, user: TokenData
    ) -> DailyHabitLogOut:
        log = await self.repo.get_log(log_id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro diario no encontrado",
            )
        if log.user_id != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permisos insuficientes"
            )
        if payload.completed is not None:
            log.completed = payload.completed
        if payload.notes is not None:
            log.notes = payload.notes
        updated = await self.repo.save_log(log)
        return DailyHabitLogOut.from_orm(updated)

    async def delete_daily_log(self, log_id: str, user: TokenData) -> None:
        log = await self.repo.get_log(log_id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro diario no encontrado",
            )
        if log.user_id != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permisos insuficientes"
            )
        await self.repo.delete_log(log)
