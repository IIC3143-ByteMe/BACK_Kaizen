from typing import List
from pydantic import BaseModel, Field
from models.models import Goal
from datetime import date


class CompletionEntryCreate(BaseModel):
    habit_id: str
    title: str
    goal: Goal
    progress: float
    percentage: float
    completed: bool


class CompletionEntryResponse(BaseModel):
    habit_id: str
    title: str
    goal: Goal
    progress: float
    percentage: float
    completed: bool


class DailyCompletionsCreate(BaseModel):
    user_id: str
    date: date
    completions: List[CompletionEntryCreate]
    overall_percentage: float
    day_completed: bool = False


class DailyCompletionsResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    date: date
    completions: List[CompletionEntryResponse]
    overall_percentage: float
    day_completed: bool
