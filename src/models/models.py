from typing import Optional, List
from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field, BaseModel, field_validator, ConfigDict
from enum import Enum
from bson import ObjectId


class ArquetiposIkigai(str, Enum):
    CONSTANTE = "constante"
    EXPLORADOR = "explorador"
    SOCIAL = "social"
    REFLECIVO = "reflexivo"


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Goal(BaseModel):
    period: str
    type: str
    target: int
    unit: str


class IkigaiEducation(BaseModel):
    arquetype: Optional[ArquetiposIkigai] = None
    you_love: Optional[str] = None
    good_at: Optional[str] = None
    world_needs: Optional[str] = None
    is_profitable: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    streak: int = 0
    ikigai_quiz_bool: bool = False
    ikigai: Optional[IkigaiEducation] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

    @field_validator("ikigai", mode="before")
    def _convert_goal(cls, v):
        if isinstance(v, dict):
            return IkigaiEducation(**v)
        if isinstance(v, IkigaiEducation):
            return v
        raise ValueError("IkigaiEducation must be a dict or IkigaiEducation instance")


class Habit(Document):
    owner_id: ObjectId
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

    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        arbitrary_types_allowed=True, json_encoders={ObjectId: str}
    )

    @field_validator("owner_id", mode="before")
    def _convert_owner_id(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return v

    @field_validator("goal", mode="before")
    def _convert_goal(cls, v):
        if isinstance(v, dict):
            return Goal(**v)
        if isinstance(v, Goal):
            return v
        raise ValueError("goal must be a dict or Goal instance")

    class Settings:
        name = "habits"


class DailyHabitLog(Document):
    user_id: str  # ID del User que registra
    habit_id: str  # ID del Habit que está registrando
    date: datetime
    completed: bool = False
    notes: Optional[str] = None

    class Settings:
        name = "daily_habit_logs"


class HabitTemplate(Document):
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
    published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "habit_templates"
