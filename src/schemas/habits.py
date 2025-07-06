from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    Field,
)
from models.models import Goal


class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    icon: str
    color: str
    group: Optional[str] = None
    type: str
    ikigai_category: Optional[str] = None

    goal: Goal
    task_days: List[str]
    reminders: List[str]


class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    group: Optional[str] = None
    type: Optional[str] = None
    ikigai_category: Optional[str] = None

    goal: Optional[Goal] = None
    task_days: Optional[List[str]] = None
    reminders: Optional[List[str]] = None


class HabitOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    id: str = Field(alias="_id")
    owner_id: str
    title: str
    description: Optional[str]
    icon: str
    color: str
    group: Optional[str]
    type: str
    ikigai_category: Optional[str]
    goal: Goal
    task_days: List[str]
    reminders: List[str]
    created_at: datetime

    @field_validator("id", mode="before")
    def _coerce_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @field_validator("owner_id", mode="before")
    def _coerce_owner_id(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @field_validator("goal", mode="before")
    def _unpack_goal(cls, v):
        if hasattr(v, "model_dump"):
            return v.model_dump()
        if isinstance(v, dict):
            return v
        return getattr(v, "__dict__", v)

    @field_serializer("goal", mode="plain")
    def _serialize_goal(v: Goal, info):
        return v.model_dump()


class HabitProgress(BaseModel):
    habit_id: str
    total_days: int
    completed_days: int
    completion_rate: float
