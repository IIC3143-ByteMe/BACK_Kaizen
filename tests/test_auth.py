import pytest
from jose import jwt
from utils.auth_utils import create_access_token, SECRET_KEY, ALGORITHM

# Aplica el fixture clean_db a todos los tests de este módulo
pytestmark = pytest.mark.usefixtures("clean_db")




@pytest.mark.order(1)
def test_register_success(client, user_factory):
    new_user = user_factory("newuser")
    r = client.post("/auth/register", json=new_user)
    assert r.status_code == 201
    body = r.json()
    assert "_id" in body
    assert body["email"] == new_user["email"]




@pytest.mark.order(2)
def test_register_missing_fields_returns_422(client):
    bad_user = {"email": "", "password": ""}  # datos inválidos
    r = client.post("/auth/register", json=bad_user)
    assert r.status_code == 422


@pytest.mark.order(3)
def test_register_duplicate_returns_400(client, user_factory):
    dup_user = user_factory("duplicate")
    # Primer registro
    r1 = client.post("/auth/register", json=dup_user)
    assert r1.status_code == 201
    # Segundo registro con misma info → 400
    r2 = client.post("/auth/register", json=dup_user)
    assert r2.status_code == 400


@pytest.mark.order(4)
def test_login_success(client, user_factory):
    new_user = user_factory("loginuser")
    client.post("/auth/register", json=new_user)
    resp = client.post("/auth/login", json=new_user)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


@pytest.mark.order(5)
def test_login_invalid_password(client, user_factory):
    new_user = user_factory("wrongpass")
    client.post("/auth/register", json=new_user)
    
    # Intentar login con password incorrecta
    wrong_creds = {
        "email": new_user["email"],
        "password": "WrongPassword123"
    }
    resp = client.post("/auth/login", json=wrong_creds)
    assert resp.status_code in (400, 401)


@pytest.mark.order(6)
def test_login_missing_fields_returns_422(client):
    resp = client.post("/auth/login", json={})
    assert resp.status_code in (400, 422)


def test_token_creation_and_validation():
    token = create_access_token(data={"sub": "abc", "role": "user"})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "abc"
    assert payload["role"] == "user"


def test_protected_requires_auth(client):
    r = client.get("/habits/")
    assert r.status_code == 401
