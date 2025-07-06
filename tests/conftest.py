import os
import asyncio
import pytest
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from main import app
from models.models import User, Habit, DailyHabitLog, HabitTemplate
from utils.auth_utils import get_password_hash
from schemas.roles import TokenData
from jose import jwt
from utils.auth_utils import SECRET_KEY, ALGORITHM

# — Exception handler para debug en todos los tests —
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback
    print("Exception:", traceback.format_exc())
    return JSONResponse(500, {"detail": "Internal server error", "error": str(exc)})


# — Base de datos de test (se ejecuta una vez por sesión) —
@pytest.fixture(scope="session", autouse=True)
def init_db():
    from dotenv import load_dotenv
    load_dotenv()

    mongo_uri = os.environ["MONGODB_URI"]
    db_name = os.environ["MONGO_DB_NAME_TEST"]

    client = AsyncIOMotorClient(mongo_uri)
    test_db = client[db_name]
    asyncio.get_event_loop().run_until_complete(
        init_beanie(
            database=test_db,
            document_models=[User, Habit, DailyHabitLog, HabitTemplate],
        )
    )
    yield
    client.drop_database(db_name)


# — Cliente HTTP para FastAPI —
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# — Token de usuario normal —
@pytest.fixture(scope="module")
def user_token(client):
    TEST_USER = {"email": "pytest_user@example.com", "password": "TestPass123"}
    client.post("/auth/register", json=TEST_USER)
    resp = client.post("/auth/login", json=TEST_USER)
    assert resp.status_code == 200
    return resp.json()["access_token"]


# — Token de usuario admin —
@pytest.fixture(scope="module")
def admin_token(client):
    TEST_ADMIN = {"email": "admin_user@example.com", "password": "AdminPass123"}
    hashed = get_password_hash(TEST_ADMIN["password"])
    asyncio.get_event_loop().run_until_complete(
        User(
            email=TEST_ADMIN["email"],
            hashed_password=hashed,
            full_name="Admin",
            role="admin",
        ).insert()
    )
    resp = client.post("/auth/login", json=TEST_ADMIN)
    assert resp.status_code == 200
    return resp.json()["access_token"]
