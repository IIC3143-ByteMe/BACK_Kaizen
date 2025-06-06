from fastapi import APIRouter, HTTPException
from models.user_model import User, UserInDB
from db.mongodb import db
from bson import ObjectId

# RUTA TEMPLATE NO OFICIAL

router = APIRouter()

@router.post("/users/", response_model=UserInDB)
async def create_user(user: User):
    result = await db.users.insert_one(user.dict())
    user_id = str(result.inserted_id)
    return {**user.dict(), "_id": user_id}

@router.get("/users/{user_id}", response_model=UserInDB)
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")
