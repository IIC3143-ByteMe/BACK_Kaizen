from datetime import date
from typing import List
from pydantic import BaseModel, Field

class CalendarDayStatsSchema(BaseModel):
    day: date
    completed_count: int
    total_habits: int
    completion_rate: float

class HabitsCalendarSchema(BaseModel):
    user_id: str
    year: int
    month: int
    days: List[CalendarDayStatsSchema] = Field(default_factory=list)