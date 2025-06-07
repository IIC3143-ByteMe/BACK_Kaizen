# app/schemas/schemas.py

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


# ----- ENUM (misma definición que en models, pero para validación) -----
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


# ----- USUARIO -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    email: EmailStr
    full_name: Optional[str]
    role: UserRole
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


# ----- LOGIN (token JWT) -----
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None


# ----- HÁBITO -----
class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None


class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class HabitOut(BaseModel):
    id: str = Field(..., alias="_id")
    owner_id: str
    title: str
    description: Optional[str]
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
    id: str = Field(..., alias="_id")
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
    id: str = Field(..., alias="_id")
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
