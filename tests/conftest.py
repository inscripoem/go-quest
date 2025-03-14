import pytest
from litestar import Litestar


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(name="app")
def fx_app() -> Litestar:
    from go_quest.asgi import create_app

    return create_app()
