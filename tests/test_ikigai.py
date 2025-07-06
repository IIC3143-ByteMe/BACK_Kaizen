import pytest


@pytest.mark.skip(reason="admin/ikigai not implemented yet")
def test_ikigai_education_crud(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}

    before = client.get("/ikigai/", headers=headers).json()
    r1 = client.post(
        "/ikigai/",
        json={"title": "Edu1", "content": "Content1"},
        headers=headers,
    )
    assert r1.status_code == 201

    after = client.get("/ikigai/", headers=headers).json()
    assert len(after) == len(before) + 1
