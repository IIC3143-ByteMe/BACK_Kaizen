from typing import Optional, List
from datetime import datetime, date
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
    last_timestamp: Optional[date] = None
    ikigai_quiz_bool: bool = False
    ikigai: Optional[IkigaiEducation] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def update_streak(self):
        today = date.today()
        if self.last_timestamp is None:
            self.streak = 1
        else:
            days_diff = (today - self.last_timestamp).days
            if days_diff == 0:
                return False
            elif days_diff == 1:
                self.streak += 1
            else:
                self.streak = 1
        self.last_timestamp = today
        return True

    class Settings:
        name = "users"

    @field_validator("ikigai", mode="before")
    def _convert_goal(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, dict):
            return IkigaiEducation(**v)
        if isinstance(v, IkigaiEducation):
            return v
        if isinstance(v, str) and v.lower() == "null":
            return None
        if isinstance(v, str):
            try:
                import json

                d = json.loads(v)
                if isinstance(d, dict):
                    return IkigaiEducation(**d)
            except Exception:
                pass
        raise ValueError(
            "IkigaiEducation must be a dict, None, "
            "IkigaiEducation instance, or valid dict as string"
        )


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


class HabitTemplate(Document):
    title: str
    description: str
    icon: str
    color: str
    group: Optional[str] = None
    type: str

    goal: Goal
    task_days: List[str]
    reminders: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        arbitrary_types_allowed=True, json_encoders={ObjectId: str}
    )

    @field_validator("goal", mode="before")
    def _convert_goal(cls, v):
        if isinstance(v, dict):
            return Goal(**v)
        if isinstance(v, Goal):
            return v
        raise ValueError("goal must be a dict or Goal instance")

    class Settings:
        name = "habit_templates"


class CompletionEntry(BaseModel):
    habit_id: ObjectId
    title: str
    goal: Goal
    progress: float
    percentage: float
    completed: bool

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class DailyCompletions(Document):
    user_id: ObjectId
    date: date
    completions: List[CompletionEntry]
    overall_percentage: float
    day_completed: bool = False

    class Settings:
        name = "daily_completions"

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateProgressInput(BaseModel):
    habit_id: str
    date: date
    progress: float


class CalendarDayStats(BaseModel):
    day: date
    completed_count: int
    total_habits: int
    completion_rate: float


class JournalQuestion(Document):
    date: date
    question: str

    class Settings:
        name = "journal_question"

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class JournalEntry(BaseModel):
    date: date
    entry: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Journal(Document):
    user_id: ObjectId
    entries: List[JournalEntry] = []

    class Settings:
        name = "journal"

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
