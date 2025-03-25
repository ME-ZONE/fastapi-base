from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.common.constants import POSTGRES_DB
from app.core import settings
from app.main import app


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session", autouse=True)
def disable_rate_limiter() -> Generator[None, Any, None]:
    original_call = RateLimiter.__call__

    async def override_rate_limiter(*args, **kwargs) -> None:
        return None

    RateLimiter.__call__ = AsyncMock(side_effect=override_rate_limiter)
    yield
    RateLimiter.__call__ = original_call


@pytest.fixture(scope="session", autouse=True)
def override_settings() -> None:
    settings.POSTGRES_HOST = settings.TEST_POSTGRES_HOST
    settings.POSTGRES_PORT = settings.TEST_POSTGRES_PORT
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def session() -> Generator[Any, Any, None]:
    engine = create_engine(
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.TEST_POSTGRES_HOST}:{settings.TEST_POSTGRES_PORT}/{POSTGRES_DB}",
        connect_args={},
    )
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    yield session
    session.close()
