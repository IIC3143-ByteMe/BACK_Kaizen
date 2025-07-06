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


class TemplateCreate(BaseModel):
    title: str
    description: str
    icon: str
    color: str
    grupo: Optional[str] = None
    type: str
    goal_period: str
    goal_value: int
    goal_value_unit: str
    task_days: str
    reminders: str
    ikigai_category: str
    published: bool


class TemplateUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    grupo: Optional[str] = None
    type: Optional[str] = None
    goal_period: Optional[str] = None
    goal_value: Optional[int] = None
    goal_value_unit: Optional[str] = None
    task_days: Optional[str] = None
    reminders: Optional[str] = None
    ikigai_category: Optional[str] = None
    published: Optional[bool] = None


class TemplateOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: Annotated[str, Field(alias="_id")]
    title: str
    description: str
    icon: str
    color: str
    grupo: Optional[str]
    type: str
    goal_period: str
    goal_value: int
    goal_value_unit: str
    task_days: str
    reminders: str
    ikigai_category: str
    published: bool
    created_at: datetime

    @field_validator("id", mode="before")
    def _coerce_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)
