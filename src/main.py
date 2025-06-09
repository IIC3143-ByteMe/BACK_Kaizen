# src/main.py

from typing import Union
from fastapi import FastAPI
import uvicorn
from beanie import init_beanie
from dotenv import load_dotenv
from google import genai
import os
from fastapi.middleware.cors import CORSMiddleware

# Conexión a MongoDB
from db.mongodb import db

# Modelos para Beanie
from models.models import User, Habit, DailyHabitLog, IkigaiEducation, HabitTemplate

# Routers
from routers.auth import router as auth_router
from routers.habits import router as habits_router
from routers.daily_logs import router as daily_logs_router
from routers.ikigai import router as ikigai_router
from routers.admin import router as admin_router
from routers.user import router as user_router

load_dotenv()
gemini_api = os.getenv("GEMINI_API")
gemini_client = genai.Client(api_key=gemini_api)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Explain how AI works in a few words",
    )
    return {"Hello": response.text}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.on_event("startup")
async def on_startup():
    # Inicializar Beanie con la DB ya conectada
    await init_beanie(
        database=db,
        document_models=[User, Habit, DailyHabitLog, IkigaiEducation, HabitTemplate],
    )


app.include_router(auth_router)
app.include_router(habits_router)
app.include_router(daily_logs_router)
app.include_router(ikigai_router)
app.include_router(admin_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
