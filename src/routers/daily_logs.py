from typing import List
from fastapi import APIRouter, Depends, status
from schemas.schemas import (
    DailyHabitLogCreate,
    DailyHabitLogUpdate,
    DailyHabitLogOut,
    TokenData,
)
from apps.dailyLogs.sailyLogsService import DailyLogsService
from utils.dependencies import get_current_user


router = APIRouter(prefix="/daily-logs", tags=["daily-logs"])
service = DailyLogsService()

@router.post(
    "/",
    response_model=DailyHabitLogOut,
    status_code=status.HTTP_201_CREATED
)
async def create_daily_log(
    payload: DailyHabitLogCreate,
    user: TokenData = Depends(get_current_user)
) -> DailyHabitLogOut:
    return await service.create_daily_log(payload, user)

@router.get(
    "/",
    response_model=List[DailyHabitLogOut]
)
async def list_daily_logs(
    user: TokenData = Depends(get_current_user)
) -> List[DailyHabitLogOut]:
    return await service.list_daily_logs(user)

@router.put(
    "/{log_id}",
    response_model=DailyHabitLogOut
)
async def update_daily_log(
    log_id: str,
    payload: DailyHabitLogUpdate,
    user: TokenData = Depends(get_current_user)
) -> DailyHabitLogOut:
    return await service.update_daily_log(log_id, payload, user)

@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_daily_log(
    log_id: str,
    user: TokenData = Depends(get_current_user)
):
    await service.delete_daily_log(log_id, user)
    return None