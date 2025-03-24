
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.core import settings

Base = declarative_base()


class DatabaseSessionManager:
    _async_engine: AsyncEngine | None
    _async_session_maker: async_sessionmaker | None

    def __init__(self, database_uri: str) -> None:
        self.database_uri = database_uri
        self._async_engine = None
        self._async_session_maker = None

    def create_pg_async_engine(self) -> AsyncEngine:
        return create_async_engine(
            self.database_uri,
            pool_size=settings.POOL_SIZE,
            max_overflow=settings.MAX_OVERFLOW,
            pool_timeout=settings.POOL_TIMEOUT
        )

    def get_async_engine(self) -> AsyncEngine:
        if self._async_engine is None:
            self._async_engine = self.create_pg_async_engine()
        return self._async_engine

    def create_async_session_maker(self) -> async_sessionmaker:
        return async_sessionmaker(
            self.get_async_engine(),
            class_=AsyncSession,
            expire_on_commit=False
        )

    def get_async_session_maker(self) -> async_sessionmaker:
        if self._async_session_maker is None:
            self._async_session_maker = self.create_async_session_maker()
        return self._async_session_maker
