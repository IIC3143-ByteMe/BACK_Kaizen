from typing import Optional, Annotated
from datetime import datetime
from bson import ObjectId
from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
    field_validator,
    Field,
)


class DailyHabitLogCreate(BaseModel):
    habit_id: str
    date: datetime
    completed: bool = False
    notes: Optional[str] = None


class DailyHabitLogUpdate(BaseModel):
    completed: Optional[bool] = None
    notes: Optional[str] = None


class DailyHabitLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[str, Field(alias="_id")]
    user_id: str
    habit_id: str
    date: datetime
    completed: bool
    notes: Optional[str]

    @field_validator("id", mode="before")
    def _coerce_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)
