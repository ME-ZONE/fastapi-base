from collections.abc import Awaitable, Callable

from fastapi import HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.common.constants import AppStatus
from app.common.enums import ClassEnum
from app.core import AppException, logger


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            response = await call_next(request)
            return response
        except AppException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except StarletteHTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            logger.error(f"[{ClassEnum.SERVER}] {str(e)}")
            return JSONResponse(status_code=AppStatus.INIT_500_INTERNAL_SERVER_ERROR.status_code,
                                content={"detail": {"name": AppStatus.INIT_500_INTERNAL_SERVER_ERROR.name,
                                                    "message": str(e)}})


def validation_exception_handler(request: Request, validation_error: RequestValidationError) -> JSONResponse:
    detail = validation_error.errors()[0]
    err_msg = f"{detail.get('msg')}".replace("Value error, ", "")
    return JSONResponse(
        status_code=AppStatus.INIT_400_BAD_REQUEST.status_code,
        content={"detail": {"name": AppStatus.INIT_400_BAD_REQUEST.name, "message": err_msg}},
    )


def rate_limit_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=AppStatus.INIT_429_TOO_MANY_REQUESTS.status_code,
                        content={
                            "detail": {"name": AppStatus.INIT_429_TOO_MANY_REQUESTS.name,
                                       "message": AppStatus.INIT_429_TOO_MANY_REQUESTS.message}})
