from typing import List, Optional
from bson import ObjectId
from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    Field,
)

from schemas.schemas import Goal


class TemplateHabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    icon: str
    color: str
    group: Optional[str] = None
    type: str

    goal: Goal
    task_days: List[str]
    reminders: List[str]


class TemplateHabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    group: Optional[str] = None
    type: Optional[str] = None

    goal: Optional[Goal] = None
    task_days: Optional[List[str]] = None
    reminders: Optional[List[str]] = None


class TemplateHabitOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str = Field(alias="_id")
    title: str
    description: Optional[str]
    icon: str
    color: str
    group: Optional[str]
    type: str
    goal: Goal
    task_days: List[str]
    reminders: List[str]

    @field_validator("id", mode="before")
    def _coerce_id(cls, v):
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
