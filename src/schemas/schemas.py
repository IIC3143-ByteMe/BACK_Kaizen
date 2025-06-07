from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum
from beanie import PydanticObjectId


# ----- ENUM PARA ROLES -----
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


# ----- CREACIÓN DE USUARIO -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


# ----- SALIDA DE USUARIO -----
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId
    email: EmailStr
    full_name: Optional[str]
    role: UserRole
    created_at: datetime


# ----- TOKEN JWT -----
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None


# ----- CREACIÓN DE HÁBITO -----
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


# ----- ACTUALIZACIÓN DE HÁBITO -----
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


# ----- SALIDA DE HÁBITO -----
class HabitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId
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

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# ----- REGISTRO DIARIO DE HÁBITO -----
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

    id: PydanticObjectId
    user_id: str
    habit_id: str
    date: datetime
    completed: bool
    notes: Optional[str]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# ----- EDUCACIÓN IKIGAI -----
class IkigaiEducationCreate(BaseModel):
    title: str
    content: str


class IkigaiEducationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId
    title: str
    content: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# ----- PROGRESO DE HÁBITOS (para reporte) -----
class HabitProgress(BaseModel):
    habit_id: str
    total_days: int
    completed_days: int
    completion_rate: float  # porcentaje completado (0.0–100.0)
