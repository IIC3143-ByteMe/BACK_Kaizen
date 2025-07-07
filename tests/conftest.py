import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app
import uuid
from utils.auth_utils import get_password_hash

# --- Event loop fix para Mac y Python >3.8 (obligatorio para Beanie + pytest)
@pytest.fixture(autouse=True)
def fresh_event_loop():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield
    try:
        loop.close()
    except Exception:
        pass

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def user_factory():
    def _create_user(email_prefix="testuser", password="TestPass123"):
        unique_id = str(uuid.uuid4())[:8]
        return {
            "email": f"{email_prefix}_{unique_id}@example.com",
            "password": password,
            "full_name": f"Test User {unique_id}",
        }
    return _create_user

@pytest.fixture
def admin_factory():
    def _create_admin(email_prefix="testadmin", password="AdminPass123"):
        unique_id = str(uuid.uuid4())[:8]
        return {
            "email": f"{email_prefix}_{unique_id}@example.com",
            "password": password,
            "full_name": f"Admin User {unique_id}",
            "role": "admin",
        }
    return _create_admin
