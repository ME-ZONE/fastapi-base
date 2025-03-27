from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import settings
from app.core.databases import DatabaseSessionManager


@lru_cache
def get_database_session_maker() -> DatabaseSessionManager:
    return DatabaseSessionManager(settings.POSTGRES_ASYNC_URL)


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_local = get_database_session_maker().get_async_session_maker()
    session: AsyncSession = session_local()

    try:
        yield session
        if session.in_transaction():
            await session.commit()
    except Exception as exc:
        if session.in_transaction():
            await session.rollback()
        raise exc
    finally:
        await session.close()
