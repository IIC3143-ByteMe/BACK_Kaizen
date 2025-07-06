from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum

from models.models import ArquetiposIkigai


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


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
