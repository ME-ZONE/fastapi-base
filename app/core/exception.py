import json

from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.common.constants import AppStatus


class AppException(HTTPException):
    ## Init ##
    def __init__(self, app_status: AppStatus, **kwargs) -> None:
        super().__init__(
            status_code=app_status.status_code,
            detail={"name": app_status.name, "message": self._format_message(app_status.message, **kwargs)},
        )

    ## Internal Function ##
    @staticmethod
    def _format_message(message: str, **kwargs) -> str:
        return message.format(**kwargs) if kwargs else message


class AppResponse(JSONResponse):
    ## Init ##
    def __init__(
        self, app_status: AppStatus, data: dict | list[dict] = None, meta: dict | list[dict] = None, **kwargs
    ) -> None:
        self.content = {
            "status_code": app_status.status_code,
            "detail": {
                "name": app_status.name,
                "message": self._format_message(app_status.message, **kwargs),
                "data": data,
                "meta": meta,
            },
        }
        super().__init__(
            status_code=app_status.status_code,
            content={
                "detail": {
                    "name": app_status.name,
                    "message": self._format_message(app_status.message, **kwargs),
                    "data": data,
                    "meta": meta,
                }
            },
        )

    def __str__(self) -> str:
        return json.dumps(self.content, ensure_ascii=False, indent=2)

    ## Internal Function ##
    @staticmethod
    def _format_message(message: str, **kwargs) -> str:
        return message.format(**kwargs) if kwargs else message
