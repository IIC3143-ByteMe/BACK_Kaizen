from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# MODELO TEMPLATE, NO USUARIO OFICIAL

class User(BaseModel):
    name: str
    email: str

class UserInDB(User):
    id: Optional[str] = Field(alias="_id")
