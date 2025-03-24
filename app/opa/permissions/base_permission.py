from abc import ABCMeta, abstractmethod
from collections.abc import Sequence

import httpx
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.constants import AppStatus
from app.common.enums import ClassEnum
from app.core import AppException, logger, settings
from app.models import User


class PermissionResult:
    def __init__(self, allow: bool, reasons: list[str] = None, filter_rpn: list[str | dict] = None) -> None:
        self.allow = allow
        self.reasons = reasons if reasons is not None else []
        self.filter_rpn = filter_rpn if filter_rpn is not None else []


class OpenPolicyAgentPermission(metaclass=ABCMeta):
    tag: str = None
    opa_url: str = None
    scope: str = None
    metadata: {} = {}
    resource: dict | list[dict] = None

    user_id: str = None
    is_superuser: bool = False

    class Scopes:
        CREATE = "create"
        LIST = "list"
        READ = "read"
        UPDATE = "update"
        DELETE = "delete"

    def __init__(self, **kwargs) -> None:
        # kwargs include scope, user_id
        for name, val in kwargs.items():
            setattr(self, name, val)

        self.opa_url = f"http://{settings.OPA_HOST}:{settings.OPA_PORT}/v1/data"

        self.payload = {
            "input": {
                "scope": self.scope,
                "auth": {"user": {"id": self.user_id, "is_superuser": self.is_superuser}},
                "metadata": self.metadata,
                "resource": self.resource,
            },
        }

    @classmethod
    @abstractmethod
    async def create(cls, request: Request, session: AsyncSession, user: User | None) -> Sequence[any]: ...

    @classmethod
    def create_base_perm(cls, **kwargs) -> "OpenPolicyAgentPermission":
        return cls(**kwargs)

    @abstractmethod
    async def get_resource(self, **kwargs) -> None:
        return None

    async def check_access(self) -> PermissionResult:
        reasons = []

        async with httpx.AsyncClient() as session:
            response = await session.post(self._opa_url, json=self.payload)
            response.raise_for_status()
            output = response.json().get("result", {})
            logger.info(f"[{ClassEnum.PERMISSION}] {self._tag} - payload :: {self.payload}")
            logger.info(f"[{ClassEnum.PERMISSION}] {self._tag} - output :: {output}")

        if isinstance(output, dict):
            allow = output.get("allow", False)
            reasons = output.get("reasons", [])
        elif isinstance(output, bool):
            allow = output
        else:
            raise AppException(app_status=AppStatus.INIT_500_INTERNAL_SERVER_ERROR)
        return PermissionResult(allow=allow, reasons=reasons)

    async def filter(self) -> PermissionResult:
        async with httpx.AsyncClient() as session:
            response = await session.post(self.opa_url.replace("/result", "/filter"), json=self.payload)
            filter_rpn = response.json().get("result", {})
        logger.info(f"[{ClassEnum.PERMISSION}] {self.tag} - payload :: {self.payload}")
        logger.info(f"[{ClassEnum.PERMISSION}] {self.tag} - filter_rpn :: {filter_rpn}")
        return PermissionResult(allow=True, filter_rpn=filter_rpn)
