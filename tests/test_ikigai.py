import pytest

def test_ikigai_endpoint(client, user_factory):
    user = user_factory()
    client.post("/auth/register", json=user)
    login_resp = client.post("/auth/login", json=user)
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Simple GET
    resp = client.get("/ikigai/", headers=headers)
    assert resp.status_code == 200 or resp.status_code == 404  # depende si hay datos o no

    # Create ikigai data
    data = {
        "arquetype": "constante",
        "you_love": "coding",
        "good_at": "solving problems",
        "world_needs": "innovation",
        "is_profitable": "software"
    }
    resp = client.post("/ikigai/", json=data, headers=headers)
    assert resp.status_code in (200, 201)

    # Get again
    resp = client.get("/ikigai/", headers=headers)
    assert resp.status_code == 200
    res = resp.json()
    for k in data:
        assert k in res and res[k] == data[k]
