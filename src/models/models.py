# app/models/models.py

from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field
from enum import Enum

# ----- ENUM PARA ROLES -----
class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

# ----- DOCUMENTO DE USUARIO -----
class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # nombre de la colección

# ----- DOCUMENTO DE HÁBITO -----
class Habit(Document):
    owner_id: str            # ID del User que creó el hábito
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "habits"

# ----- DOCUMENTO DE REGISTRO DIARIO DE HÁBITO -----
class DailyHabitLog(Document):
    user_id: str              # ID del User que registra
    habit_id: str             # ID del Habit que está registrando
    date: datetime
    completed: bool = False
    notes: Optional[str] = None

    class Settings:
        name = "daily_habit_logs"

# ----- DOCUMENTO DE EDUCACIÓN SOBRE IKIGAI -----
class IkigaiEducation(Document):
    title: str
    content: str              # Texto completo
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "ikigai_education"
