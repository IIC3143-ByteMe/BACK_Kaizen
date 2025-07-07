from datetime import date, datetime
from typing import List
from beanie import Document
from fastapi import APIRouter, Body, Depends
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from schemas.roles import TokenData
from utils.dependencies import get_current_user

router = APIRouter()


class UpdateDayInput(BaseModel):
    day: date
    completed_count: int
    total_habits: int


class CalendarDayStats(BaseModel):
    day: date
    completed_count: int
    total_habits: int
    completion_rate: float = 0.0

    model_config = ConfigDict(arbitrary_types_allowed=True)


class HabitsCalendarSchema(Document):
    user_id: ObjectId = Field(..., json_schema_extra={"type": "string"})
    year: int
    month: int
    days: List[CalendarDayStats]

    class Settings:
        name = "habits_calendar"

    model_config = ConfigDict(
        arbitrary_types_allowed=True, json_encoders={ObjectId: str}
    )


@router.patch("/update-day")
async def update_day_stats(
    data: UpdateDayInput = Body(...),
    user: TokenData = Depends(get_current_user),
):
    day = (
        data.day
        if isinstance(data.day, date)
        else datetime.strptime(data.day, "%Y-%m-%d").date()
    )
    year, month = day.year, day.month

    calendar = await HabitsCalendarSchema.find_one(
        {"user_id": ObjectId(user.user_id), "year": year, "month": month}
    )
    if not calendar:
        calendar = HabitsCalendarSchema(
            user_id=ObjectId(user.user_id), year=year, month=month, days=[]
        )

    found = False
    for day_stat in calendar.days:
        if day_stat.day == day:
            day_stat.completed_count = data.completed_count
            day_stat.total_habits = data.total_habits
            day_stat.completion_rate = (
                data.completed_count / data.total_habits if data.total_habits else 0.0
            )
            found = True
            break
    if not found:
        calendar.days.append(
            CalendarDayStats(
                day=day,
                completed_count=data.completed_count,
                total_habits=data.total_habits,
                completion_rate=(
                    (data.completed_count / data.total_habits)
                    if data.total_habits
                    else 0.0
                ),
            )
        )

    await calendar.save()
    return {"detail": "Calendar updated", "calendar_id": str(calendar.id)}


@router.get("/calendar")
async def get_habits_calendar(
    year: int,
    month: int,
    user: TokenData = Depends(get_current_user),
):
    calendar = await HabitsCalendarSchema.find_one(
        {"user_id": ObjectId(user.user_id), "year": year, "month": month}
    )
    if not calendar:
        return {"user_id": user.user_id, "year": year, "month": month, "days": []}
    return calendar
