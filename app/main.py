from collections.abc import Callable
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
from starlette.middleware.cors import CORSMiddleware

from app.apis.endpoints import router
from app.common.constants import BasePath
from app.common.enums import ProjectBuildTypes, SwaggerPaths
from app.core import logger, settings
from app.core.middlewares import (
    ExceptionMiddleware,
    rate_limit_exception_handler,
    validation_exception_handler,
)


class App:
    application: FastAPI
    _redis_client: Redis

    def __init__(self) -> None:
        self.application = FastAPI(
            title=settings.PROJECT_NAME,
            description=settings.PROJECT_DESCRIPTION,
            debug=settings.DEBUG,
            version=settings.VERSION,
            docs_url=None if settings.PROJECT_BUILD_TYPE == ProjectBuildTypes.PRODUCTION else SwaggerPaths.DOCS,
            redoc_url=None if settings.PROJECT_BUILD_TYPE == ProjectBuildTypes.PRODUCTION else SwaggerPaths.RE_DOC,
        )
        self._redis_client = Redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0", decode_responses=True
        )

        self.application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.application.include_router(router, prefix=BasePath)
        self.application.add_event_handler("startup", self.on_init_app())
        self.application.add_event_handler("shutdown", self.on_terminate_app())
        self.application.add_exception_handler(RequestValidationError, validation_exception_handler)
        self.application.add_exception_handler(429, rate_limit_exception_handler)
        self.application.add_middleware(ExceptionMiddleware)
        self.application.openapi = self.custom_openapi

    def custom_openapi(self) -> dict[str, Any]:
        if self.application.openapi_schema:
            return self.application.openapi_schema
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            description=settings.PROJECT_DESCRIPTION,
            routes=self.application.routes,
        )

        for path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["responses"].pop("422", None)

        self.application.openapi_schema = openapi_schema
        return self.application.openapi_schema

    def on_init_app(self) -> Callable:
        async def start_app() -> None:
            await FastAPILimiter.init(self._redis_client)

        return start_app

    def on_terminate_app(self) -> Callable:
        @logger.catch
        async def stop_app() -> None:
            await self._redis_client.close()

        return stop_app


app = App().application

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", reload=True)  # noqa: S104
