from typing import Optional
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
from models.models import UserRole, IkigaiEducation


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
    last_timestamp: Optional[datetime] = None
    ikigai_quiz_bool: bool
    ikigai: Optional[IkigaiEducation]
    created_at: datetime

    @field_validator("id", mode="before")
    def _coerce_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_serializer("id")
    def _serialize_id(self, v: str) -> str:
        return v

    @field_validator("ikigai", mode="before")
    def _unpack_ikigai(cls, v):
        if v is None:
            return None
        if hasattr(v, "model_dump"):
            return v.model_dump()
        if isinstance(v, dict):
            return v
        if isinstance(v, str) and v.lower() == "null":
            return None
        if isinstance(v, str):
            try:
                import json

                d = json.loads(v)
                if isinstance(d, dict):
                    return d
            except Exception:
                pass
        return getattr(v, "__dict__", v)

    @field_serializer("ikigai", mode="plain")
    def _serialize_ikigai(v: "IkigaiEducation", info):
        if v is None:
            return None
        if hasattr(v, "model_dump"):
            return v.model_dump()
        if isinstance(v, dict):
            return v
        return getattr(v, "__dict__", v)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None
