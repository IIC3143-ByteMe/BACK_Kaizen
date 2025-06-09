import pytest
import asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from main import app
from models.models import User, Habit, DailyHabitLog, IkigaiEducation
from schemas.schemas import UserCreate, TokenData
from utils.auth_utils import create_access_token, get_password_hash, SECRET_KEY, ALGORITHM
from jose import jwt

# Test data
TEST_USER = {"email": "pytest_user@example.com", "password": "TestPass123"}
TEST_HABIT = {
    "title": "PyTest Habit",
    "description": "Testing habit creation",
    "icon": "test-icon",
    "color": "red",
    "grupo": "Testing",
    "type": "personal",
    "goal_period": "daily",
    "goal_value": 1,
    "goal_value_unit": "times",
    "task_days": "Mon,Wed,Fri",
    "reminders": "08:00",
    "ikigai_category": "Health",
}
TEST_ADMIN = {"email": "admin_user@example.com", "password": "AdminPass123"}

@pytest.fixture(scope="session", autouse=True)
def init_db():
    """
    Initialize a fresh test database and Beanie before any tests run.
    Drops the database after tests complete.
    """
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    test_db = client["kaizen_test_db"]
    asyncio.get_event_loop().run_until_complete(
        init_beanie(
            database=test_db,
            document_models=[User, Habit, DailyHabitLog, IkigaiEducation],
        )
    )
    yield
    client.drop_database("kaizen_test_db")

@pytest.fixture(scope="module")
def client():
    """
    Provides a FastAPI TestClient for sending requests to the app.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def token(client):
    """
    Registers and logs in a test user, returning a valid JWT.
    """
    # Register (ignore if already exists)
    client.post("/auth/register", json=TEST_USER)
    # Login
    resp = client.post("/auth/login", json=TEST_USER)
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]

# --- Basic Habit Tests ---
def test_create_habit_missing_fields_returns_422(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post("/habits/", json={}, headers=headers)
    assert resp.status_code == 422

# --- Auth and Token Utils ---
def test_register_duplicate(client):
    r1 = client.post("/auth/register", json=TEST_USER)
    r2 = client.post("/auth/register", json=TEST_USER)
    assert r2.status_code == 400

@pytest.mark.parametrize("pwd", ["WrongPass", ""])
def test_login_wrong_password(client, pwd):
    resp = client.post(
        "/auth/login", json={"email": TEST_USER["email"], "password": pwd}
    )
    assert resp.status_code in (400, 401)


def test_token_creation_and_validation():
    token_ = create_access_token(data={"sub": "123", "role": "user"})
    payload = jwt.decode(token_, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "123"
    assert payload.get("role") == "user"

# --- Protected Endpoint ---
def test_protected_requires_auth(client):
    r = client.get("/habits/")
    assert r.status_code == 401

# --- Daily Habit Logs CRUD ---

def test_daily_logs_crud(client, token):
    """
    Insert a Habit directly, then test daily-log create, list, patch, delete.
    """
    # Decode user_id from token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    # Insert parent habit
    parent = asyncio.get_event_loop().run_until_complete(
        Habit(
            owner_id=user_id,
            title="Log Habit",
            description="desc",
            icon="i",
            color="c",
            grupo="g",
            type="t",
            goal_period="daily",
            goal_value=1,
            goal_value_unit="times",
            task_days="Mon",
            reminders="08:00",
            ikigai_category="Life",
        ).insert()
    )
    hid = str(parent.id)
    headers = {"Authorization": f"Bearer {token}"}
    # Create a daily log via API
    r1 = client.post(
        "/daily-logs/", 
        json={"habit_id": hid, "date": "2025-06-01T00:00:00Z", "completed": True},
        headers=headers
    )
    assert r1.status_code == 201
    lid = r1.json()["id"]
    # List logs
    r2 = client.get("/daily-logs/", headers=headers)
    assert any(l["id"] == lid for l in r2.json())
    # Update log
    r3 = client.patch(f"/daily-logs/{lid}", json={"notes": "note"}, headers=headers)
    assert r3.status_code == 200
    assert r3.json()["notes"] == "note"
    # Delete log
    r4 = client.delete(f"/daily-logs/{lid}" , headers=headers)
    assert r4.status_code == 204
@pytest.mark.skip(reason="create_habit endpoint not implemented yet")
def test_daily_logs_crud(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    # create parent habit
    r_h = client.post(
        "/habits/", json={
            "title": "Log Habit", "description": "desc",
            "icon": "i", "color": "c", "grupo": "g",
            "type": "t", "goal_period": "daily", "goal_value": 1,
            "goal_value_unit": "times", "task_days": "Mon",
            "reminders": "08:00", "ikigai_category": "Life"
        }, headers=headers
    )
    hid = r_h.json()["id"]
    # create log
    r1 = client.post(
        "/daily-logs/", json={"habit_id": hid, "date": "2025-06-01T00:00:00Z", "completed": True}, headers=headers
    )
    assert r1.status_code == 201
    lid = r1.json()["id"]
    # list logs
    r2 = client.get("/daily-logs/", headers=headers)
    assert any(l["id"] == lid for l in r2.json())
    # update log
    r3 = client.patch(f"/daily-logs/{lid}", json={"notes": "note"}, headers=headers)
    assert r3.status_code == 200 and r3.json()["notes"] == "note"
    # delete log
    r4 = client.delete(f"/daily-logs/{lid}", headers=headers)
    assert r4.status_code == 204

# --- Ikigai Education CRUD ---
@pytest.fixture(scope="module")
def admin_token(client):
    hashed = get_password_hash(TEST_ADMIN["password"])
    asyncio.get_event_loop().run_until_complete(
        User(email=TEST_ADMIN["email"], hashed_password=hashed, full_name="Admin", role="admin").insert()
    )
    resp = client.post("/auth/login", json=TEST_ADMIN)
    assert resp.status_code == 200
    return resp.json()["access_token"]

@pytest.mark.skip(reason="admin/ikigai not implemented yet")
def test_ikigai_education_crud(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    before = client.get("/ikigai/", headers=headers).json()
    r1 = client.post("/ikigai/", json={"title": "Edu1", "content": "Content1"}, headers=headers)
    assert r1.status_code == 201
    after = client.get("/ikigai/", headers=headers).json()
    assert len(after) == len(before) + 1
