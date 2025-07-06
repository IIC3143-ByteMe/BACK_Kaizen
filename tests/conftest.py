import os
import asyncio
import pytest
import uuid
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from main import app
from models.models import User, Habit, DailyHabitLog, HabitTemplate
from utils.auth_utils import get_password_hash
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
@pytest.fixture(scope="function")
def user_token(client, user_factory):
    test_user = user_factory("pytest_user")
    client.post("/auth/register", json=test_user)
    resp = client.post("/auth/login", json=test_user)
    assert resp.status_code == 200
    return resp.json()["access_token"]


# — Token de usuario admin —
@pytest.fixture(scope="function")
def admin_token(client, admin_factory):
    test_admin = admin_factory("admin_user")
    hashed = get_password_hash(test_admin["password"])
    asyncio.get_event_loop().run_until_complete(
        User(
            email=test_admin["email"],
            hashed_password=hashed,
            full_name=test_admin["full_name"],
            role="admin",
        ).insert()
    )
    resp = client.post("/auth/login", json=test_admin)
    assert resp.status_code == 200
    return resp.json()["access_token"]


@pytest.fixture()
async def clean_db():
    """Limpia todas las colecciones de la base de datos de test antes de cada test"""
    from dotenv import load_dotenv
    load_dotenv()
    
    mongo_uri = os.environ["MONGODB_URI"]
    db_name = os.environ["MONGO_DB_NAME_TEST"]
    
    client = AsyncIOMotorClient(mongo_uri)
    test_db = client[db_name]
    
    # Limpiar todas las colecciones
    await User.delete_all()
    await Habit.delete_all()
    await DailyHabitLog.delete_all()
    await HabitTemplate.delete_all()
    
    yield
    
    # Limpiar después del test también
    await User.delete_all()
    await Habit.delete_all()
    await DailyHabitLog.delete_all()
    await HabitTemplate.delete_all()
    
    client.close()


# — Factories para crear datos únicos en cada test —
@pytest.fixture
def user_factory():
    """Factory para crear usuarios únicos"""
    def _create_user(email_prefix="testuser", password="TestPass123"):
        unique_id = str(uuid.uuid4())[:8]
        return {
            "email": f"{email_prefix}_{unique_id}@example.com",
            "password": password,
            "full_name": f"Test User {unique_id}"
        }
    return _create_user


@pytest.fixture
def admin_factory():
    """Factory para crear usuarios admin únicos"""
    def _create_admin(email_prefix="testadmin", password="AdminPass123"):
        unique_id = str(uuid.uuid4())[:8]
        return {
            "email": f"{email_prefix}_{unique_id}@example.com",
            "password": password,
            "full_name": f"Admin User {unique_id}",
            "role": "admin"
        }
    return _create_admin
