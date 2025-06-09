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


# ----- ENUM PARA ARQUETIPOS -----
class ArquetiposIkigai(str, Enum):
    CONSTANTE = "constante"
    EXPLORADOR = "explorador"
    SOCIAL = "social"
    REFLECIVO = "reflexivo"


# ----- DOCUMENTO DE USUARIO -----
class User(Document):
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    streak: int = 0
    ikigai_quiz_bool: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # nombre de la colección


# ----- DOCUMENTO DE HÁBITO -----
class Habit(Document):
    owner_id: str  # ID del User que creó el hábito
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
    ikigai_category: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "habits"


# ----- DOCUMENTO DE REGISTRO DIARIO DE HÁBITO -----
class DailyHabitLog(Document):
    user_id: str  # ID del User que registra
    habit_id: str  # ID del Habit que está registrando
    date: datetime
    completed: bool = False
    notes: Optional[str] = None

    class Settings:
        name = "daily_habit_logs"


# ----- DOCUMENTO DE EDUCACIÓN SOBRE IKIGAI -----
class IkigaiEducation(Document):
    owner_id: str  # ID del User que creó el hábito
    arquetipo: Optional[ArquetiposIkigai] = None
    amas: Optional[str] = None
    bueno: Optional[str] = None
    necesita: Optional[str] = None
    pagar: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "ikigai_education"

# ----- TEMPLATE HÁBITO -----
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
