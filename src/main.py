import traceback
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from beanie import init_beanie
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

from motor.motor_asyncio import AsyncIOMotorClient  # <--- Import directo aquí

from models.models import User, Habit, HabitTemplate, DailyCompletions

from routers.auth import router as auth_router
from routers.habits import router as habits_router
from routers.ikigai import router as ikigai_router
from routers.admin import router as admin_router
from routers.user import router as user_router
from routers.daily_completions import router as daily_completion_router
from routers.monthly_bucket import router as monthly_bucket_router

import os

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        print(f"Unhandled error during {request.method} {request.url}: {exc}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.on_event("startup")
async def on_startup():
    mongo_uri = os.environ["MONGODB_URI"]
    db_name = os.environ["MONGO_DB_NAME_TEST"]  # O tu nombre de BD
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    await init_beanie(
        database=db,
        document_models=[User, Habit, HabitTemplate, DailyCompletions],
    )
    # Opcional: si quieres acceder a db en endpoints: app.state.db = db

app.include_router(auth_router)
app.include_router(habits_router)
app.include_router(ikigai_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(daily_completion_router)
app.include_router(monthly_bucket_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
