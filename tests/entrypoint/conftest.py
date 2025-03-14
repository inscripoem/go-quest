from collections.abc import AsyncIterator

import pytest
from httpx import AsyncClient
from litestar import Litestar
from litestar.testing import AsyncTestClient


@pytest.fixture(name="client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncClient]:
    """Async client that calls requests on the ASGI app."""

    async with AsyncTestClient(app) as client:
        yield client
