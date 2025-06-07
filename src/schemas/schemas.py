# src/schemas/schemas.py

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer
from enum import Enum
from beanie import PydanticObjectId

# ----- ENUM PARA ROLES -----
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

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
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId = Field(..., alias="_id")
    email: EmailStr
    full_name: Optional[str]
    role: UserRole
    created_at: datetime

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None

# ----- HABITS SCHEMAS -----
class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
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

class HabitUpdate(BaseModel):
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

class HabitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId = Field(..., alias="_id")
    owner_id: str
    title: str
    description: Optional[str]
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
    created_at: datetime

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)

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

    id: PydanticObjectId = Field(..., alias="_id")
    user_id: str
    habit_id: str
    date: datetime
    completed: bool
    notes: Optional[str]

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)

# ----- IKIGAI EDUCATION SCHEMAS -----
class IkigaiEducationCreate(BaseModel):
    title: str
    content: str

class IkigaiEducationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId = Field(..., alias="_id")
    title: str
    content: str
    created_at: datetime

    @field_serializer("id")
    def serialize_id(self, v):
        return str(v)

# ----- PROGRESO DE HÁBITOS -----
class HabitProgress(BaseModel):
    habit_id: str
    total_days: int
    completed_days: int
    completion_rate: float  # porcentaje completado (0.0–100.0)
