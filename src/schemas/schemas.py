# src/schemas/schemas.py

from typing import Optional, Annotated, List
from datetime import datetime
from bson import ObjectId
from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    field_serializer,
    field_validator,
    Field,
)
from enum import Enum

from models.models import ArquetiposIkigai


# ----- ENUM PARA ROLES -----
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class IkigaiCategoryEnum(str, Enum):
    PASSION = "passion"
    VOCATION = "vocation"
    MISSION = "mission"
    PROFESSION = "profession"


class IkigaiEducationCreate(BaseModel):
    arquetype: ArquetiposIkigai
    you_love: str
    good_at: str
    world_needs: str
    is_profitable: str


class IkigaiEducation(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    arquetype: Optional[ArquetiposIkigai]
    you_love: Optional[str]
    good_at: Optional[str]
    world_needs: Optional[str]
    is_profitable: Optional[str]


# ----- MODELOS DE REQUEST -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


# ----- MODEL CONFIG -----
class UserOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: str = Field(
        alias="_id",
        title="User ID",
        description="MongoDB ObjectId, serialized as a string",
    )
    email: EmailStr
    full_name: Optional[str]
    role: UserRole
    streak: int
    ikigai_quiz_bool: bool
    ikigai: Optional[IkigaiEducation]
    created_at: datetime

    @field_validator("id", mode="before")
    def _coerce_objectid(cls, v):
        # before validation: if it's an ObjectId, make it a string
        if isinstance(v, ObjectId):
            return str(v)
        return v  # leave strings (or other) alone

    @field_serializer("id")
    def _serialize_id(self, v: str) -> str:
        # this only runs at dump-time
        return v

    @field_validator("ikigai", mode="before")
    def _unpack_ikigai(cls, v):
        if hasattr(v, "model_dump"):
            return v.model_dump()
        if isinstance(v, dict):
            return v
        return getattr(v, "__dict__", v)

    @field_serializer("ikigai", mode="plain")
    def _serialize_ikigai(v: IkigaiEducation, info):
        # v is the validated ikigai instance
        return v.model_dump()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None


# ----- GOAL SCHEMA -----
class Goal(BaseModel):
    period: str
    type: str
    target: int
    unit: str


# ----- HABITS SCHEMAS -----
class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    icon: str
    color: str
    group: Optional[str] = None
    type: str
    ikigai_category: Optional[IkigaiCategoryEnum] = None

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
    ikigai_category: Optional[IkigaiCategoryEnum] = None

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
    ikigai_category: Optional[IkigaiCategoryEnum]
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
        # v is the validated Goal instance
        return v.model_dump()


# ----- DAILY LOG SCHEMAS -----
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
        # before validation: if it's an ObjectId, make it a string
        if isinstance(v, ObjectId):
            return str(v)
        return v  # leave strings (or other) alone

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)


# ----- PROGRESO DE HÁBITOS -----
class HabitProgress(BaseModel):
    habit_id: str
    total_days: int
    completed_days: int
    completion_rate: float  # porcentaje completado (0.0–100.0)


# --- TEMPLATE SCHEMAS ---
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
        populate_by_name=True,  # ← add this
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
        # before validation: if it's an ObjectId, make it a string
        if isinstance(v, ObjectId):
            return str(v)
        return v  # leave strings (or other) alone

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)
