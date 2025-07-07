import pytest

def test_register_missing_fields_returns_422(client):
    response = client.post("/auth/register", json={})
    assert response.status_code == 422

def test_register_duplicate_returns_400(client, user_factory):
    user = user_factory()
    client.post("/auth/register", json=user)
    response = client.post("/auth/register", json=user)
    assert response.status_code == 400

def test_login_success(client, user_factory):
    user = user_factory()
    client.post("/auth/register", json=user)
    response = client.post("/auth/login", json=user)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(client, user_factory):
    user = user_factory()
    client.post("/auth/register", json=user)
    wrong = dict(user)
    wrong["password"] = "other"
    response = client.post("/auth/login", json=wrong)
    assert response.status_code == 401

def test_login_missing_fields_returns_400(client):
    response = client.post("/auth/login", json={})
    assert response.status_code == 400

def test_protected_requires_auth(client):
    response = client.get("/habits/")
    assert response.status_code == 401
