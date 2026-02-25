import pytest


@pytest.mark.anyio
async def test_provider_cannot_accept_more_than_two_bookings_per_week(client):
    company_auth = await client.post(
        "/auth/register",
        json={"email": "empresa@appcaldas.com", "password": "strongpass123", "role": "company"},
    )
    provider_auth = await client.post(
        "/auth/register",
        json={"email": "prestador@appcaldas.com", "password": "strongpass123", "role": "provider"},
    )

    company_token = company_auth.json()["access_token"]
    provider_token = provider_auth.json()["access_token"]

    company_res = await client.post(
        "/companies",
        headers={"Authorization": f"Bearer {company_token}"},
        json={"name": "Hotel Caldas", "description": "Hotel", "city": "Caldas Novas"},
    )
    provider_res = await client.post(
        "/providers",
        headers={"Authorization": f"Bearer {provider_token}"},
        json={
            "full_name": "Maria Silva",
            "primary_function": "copeira",
            "bio": "Disponivel",
            "is_available": True,
        },
    )

    company_id = company_res.json()["id"]
    provider_id = provider_res.json()["id"]

    booking_ids = []
    for day in ["2026-03-02", "2026-03-03", "2026-03-04"]:
        res = await client.post(
            "/bookings",
            headers={"Authorization": f"Bearer {company_token}"},
            json={
                "company_id": company_id,
                "provider_id": provider_id,
                "function_name": "copeira",
                "start_date": day,
                "season": True,
            },
        )
        assert res.status_code == 200
        booking_ids.append(res.json()["id"])

    first_accept = await client.post(
        f"/bookings/{booking_ids[0]}/accept",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    second_accept = await client.post(
        f"/bookings/{booking_ids[1]}/accept",
        headers={"Authorization": f"Bearer {provider_token}"},
    )
    third_accept = await client.post(
        f"/bookings/{booking_ids[2]}/accept",
        headers={"Authorization": f"Bearer {provider_token}"},
    )

    assert first_accept.status_code == 200
    assert second_accept.status_code == 200
    assert third_accept.status_code == 400
    assert "weekly limit" in third_accept.json()["detail"].lower()
