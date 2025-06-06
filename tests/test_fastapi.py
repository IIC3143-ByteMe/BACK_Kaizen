import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Datos de prueba
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


@pytest.fixture(scope="module")
def token():
    # Registrar usuario
    resp = client.post("/auth/register", json=TEST_USER)
    assert resp.status_code == 201
    # Login y obtener token
    resp = client.post("/auth/login", json=TEST_USER)
    assert resp.status_code == 200
    data = resp.json()
    return data["access_token"]


def test_create_habit(token):
    headers = {"Authorization": f"Bearer {token}"}
    # Crear hábito
    resp = client.post("/habits/", json=TEST_HABIT, headers=headers)
    assert resp.status_code == 201, resp.text
    habit = resp.json()
    # Verificar campos retornados
    for key, value in TEST_HABIT.items():
        assert habit[key] == value
    assert "id" in habit


def test_list_habits(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/habits/", headers=headers)
    assert resp.status_code == 200
    habits = resp.json()
    # Debe haber al menos un hábito con el título de TEST_HABIT
    titles = [h["title"] for h in habits]
    assert TEST_HABIT["title"] in titles


def test_progress_initial(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/habits/progress", headers=headers)
    assert resp.status_code == 200
    progress = resp.json()
    # Todos los hábitos deben tener total_days inicial = 0
    for p in progress:
        assert p["total_days"] >= 0
