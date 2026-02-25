import pytest


@pytest.mark.anyio
async def test_auth_register_login_refresh_logout(client):
    register_payload = {
        "email": "company@appcaldas.com",
        "password": "strongpass123",
        "role": "company",
    }
    register_res = await client.post("/auth/register", json=register_payload)
    assert register_res.status_code == 200
    register_data = register_res.json()
    assert "access_token" in register_data
    assert "refresh_token" in register_data

    login_res = await client.post(
        "/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    assert login_res.status_code == 200
    login_data = login_res.json()

    refresh_res = await client.post(
        "/auth/refresh", json={"refresh_token": login_data["refresh_token"]}
    )
    assert refresh_res.status_code == 200

    logout_res = await client.post(
        "/auth/logout", json={"refresh_token": refresh_res.json()["refresh_token"]}
    )
    assert logout_res.status_code == 200
