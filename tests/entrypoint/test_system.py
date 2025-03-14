import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.anyio


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/system/health")
    assert response.status_code == 200


async def test_ping(client: AsyncClient) -> None:
    response = await client.get("/system/ping")
    assert response.status_code == 200
    assert response.text == "pong"
