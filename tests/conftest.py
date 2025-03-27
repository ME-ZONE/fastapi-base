import json
import uuid
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import Boolean, create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.common.enums import ProjectBuildTypes
from app.core import settings
from app.core.databases import Base
from app.main import app
from app.models import User, UserDetails


@pytest.fixture(scope="session")
def client(disable_rate_limiter: None) -> Generator[TestClient, Any, None]:
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


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer | None, Any, None]:
    if settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.DEVELOPMENT:
        with PostgresContainer("postgres:16") as postgres:
            postgres.start()
            yield postgres
    else:
        yield None


@pytest.fixture(scope="session", autouse=True)
def override_settings(postgres_container: PostgresContainer) -> None:
    if settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.DEVELOPMENT and postgres_container:
        settings.POSTGRES_HOST = postgres_container.get_container_host_ip()
        settings.POSTGRES_PORT = postgres_container.get_exposed_port(5432)
        settings.POSTGRES_USER = postgres_container.username
        settings.POSTGRES_PASSWORD = postgres_container.password
        settings.POSTGRES_DB = postgres_container.dbname
    else:
        settings.POSTGRES_HOST = settings.TEST_POSTGRES_HOST
        settings.POSTGRES_PORT = settings.TEST_POSTGRES_PORT

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def session(override_settings: None) -> Generator[Session | None, Any, None]:
    if settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.DEVELOPMENT:
        engine = create_engine(
            settings.POSTGRES_URL,
            connect_args={},
        )
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = session_local()
        yield session
        session.close()
    else:
        yield None


# Mapping between filenames and models
MODEL_MAP = {
    "users": User,
    "user_details": UserDetails,
}


def load_data_from_file(file_path: Path) -> list[dict]:
    """Loads data from a JSON file."""
    try:
        with open(file_path, encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading file {file_path.name}: {e}")  # noqa: T201
        return []


def transform_item_fields(item: dict, model: Base) -> dict:
    for field in list(item.keys()):
        value = item[field]
        # Lấy cột từ bảng của model
        column = model.__table__.columns.get(field)
        if column is not None and isinstance(column.type, Boolean):
            item[field] = value == "1"
        elif field != "id" and not field.endswith("_id"):
            try:
                uuid.UUID(str(value))
                fk_field = f"{field}_id"
                if fk_field in model.__table__.columns:
                    item[fk_field] = value
                    del item[field]
            except Exception:  # noqa: S110
                pass
    return item


def insert_data_into_session(session: Session, model: Base, data: list[dict]) -> None:
    """Filters out keys not in the table, then inserts processed data into the session."""
    for item in data:
        try:
            valid_item = {k: v for k, v in item.items() if k in model.__table__.columns}

            if "id" in valid_item and session.query(model).filter_by(id=valid_item["id"]).first():
                print(f"Record with ID {valid_item['id']} already exists, skipping insert.")  # noqa: T201
                continue

            instance = model(**valid_item)
            session.add(instance)
        except Exception as e:
            print(f"Error processing item {item}: {e}")  # noqa: T201

    try:
        session.commit()
    except Exception as e:
        print(f"Error committing session: {e}")  # noqa: T201
        session.rollback()


@pytest.fixture(scope="session", autouse=True)
def create_db_data(session: Session) -> None:
    """Load and insert data into the database."""
    if settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.DEVELOPMENT:
        data_dir = Path(__file__).parent / "data"
        for file_path in data_dir.glob("*.json"):
            table_name = file_path.stem
            model = MODEL_MAP.get(table_name)
            if not model:
                print(f"Model not found for {table_name}.json, skipping.")  # noqa: T201
                continue

            data = load_data_from_file(file_path)
            if data:
                # Process each item to handle boolean fields
                processed_data = [transform_item_fields(item, model) for item in data]
                insert_data_into_session(session, model, processed_data)
            else:
                print(f"No data found in {file_path.name}, skipping.")  # noqa: T201
