import pytest
from jose import jwt
from utils.auth_utils import create_access_token, SECRET_KEY, ALGORITHM

# Datos de prueba
NEW_USER = {"email": "new_user@example.com", "password": "StrongPass1!"}
BAD_USER = {"email": "", "password": ""}  # datos inválidos
DUP_USER = {"email": "dup@example.com", "password": "DupPass123"}


@pytest.mark.order(1)
def test_register_success(client):
    # Registro debe devolver 201 y un campo "id"
    r = client.post("/auth/register", json=NEW_USER)
    assert r.status_code == 201
    body = r.json()
    assert "id" in body
    assert body["email"] == NEW_USER["email"]


@pytest.mark.order(2)
def test_register_missing_fields_returns_422(client):
    # Campos vacíos / faltantes → 422 Unprocessable Entity
    r = client.post("/auth/register", json=BAD_USER)
    assert r.status_code == 422


@pytest.mark.order(3)
def test_register_duplicate_returns_400(client):
    # Primer registro
    r1 = client.post("/auth/register", json=DUP_USER)
    assert r1.status_code == 201
    # Segundo registro con misma info → 400 Bad Request
    r2 = client.post("/auth/register", json=DUP_USER)
    assert r2.status_code == 400


@pytest.mark.order(4)
def test_login_success(client):
    # Asegurémonos de que el usuario NEW_USER esté registrado
    client.post("/auth/register", json=NEW_USER)
    # Login correcto → 200 + token
    resp = client.post("/auth/login", json=NEW_USER)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


@pytest.mark.order(5)
@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"email": NEW_USER["email"], "password": "WrongPass"}, (400, 401)),
        ({}, (422,)),
    ],
)
def test_login_invalid(client, payload, expected):
    # Login con contraseña errónea o payload vacío
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code in expected


def test_token_creation_and_validation():
    # Verificamos utilitario de creación de JWT
    token = create_access_token(data={"sub": "abc", "role": "user"})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "abc"
    assert payload["role"] == "user"


def test_protected_requires_auth(client):
    # Sin token no debería permitir acceso
    r = client.get("/habits/")
    assert r.status_code == 401
