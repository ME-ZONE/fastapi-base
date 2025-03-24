from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.constants import BasePath
from app.models import User
from app.opa.permissions.base_permission import OpenPolicyAgentPermission


class UserPermission(OpenPolicyAgentPermission):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tag = "users"
        self.opa_url = f"{self.opa_url}/{self.tag}/result"

    class UserScopes(OpenPolicyAgentPermission.Scopes):
        pass

    def get_scope(self, request: Request) -> UserScopes | None:
        if request.url.path.startswith(f"{BasePath}/{self.tag}/") and request.method == "GET":
            return self.UserScopes.LIST
        if request.url.path.startswith(f"{BasePath}/{self.tag}/") and request.method == "POST":
            return self.UserScopes.CREATE
        return None

    @classmethod
    async def create(
        cls, request: Request, session: AsyncSession, user: User | None
    ) -> list[OpenPolicyAgentPermission]:
        permissions = []
        instance = cls()
        scope = instance.get_scope(request=request)

        if scope in [instance.UserScopes.LIST, instance.UserScopes.CREATE]:
            perm = instance.create_base_perm(
                scope=scope,
                user_id=str(user.id),
                is_superuser=user.is_superuser,
            )
            await perm.get_resource(session, request=request)
            permissions.append(perm)
        return permissions

    async def get_resource(self, session: AsyncSession, **kwargs) -> None:
        switch_scope = {
            self.UserScopes.LIST: self.handle_list_scope,
            self.UserScopes.READ: self.handle_read_scope,
            self.UserScopes.CREATE: self.handle_create_scope,
            self.UserScopes.UPDATE: self.handle_update_scope,
            self.UserScopes.DELETE: self.handle_delete_scope,
        }

        handler = switch_scope.get(self.scope)
        await handler(session=session, **kwargs)

    async def handle_list_scope(self, session: AsyncSession, **kwargs) -> None:
        pass

    async def handle_read_scope(self, session: AsyncSession, **kwargs) -> None:
        pass

    async def handle_create_scope(self, session: AsyncSession, **kwargs) -> None:
        pass

    async def handle_update_scope(self, session: AsyncSession, **kwargs) -> None:
        pass

    async def handle_delete_scope(self, session: AsyncSession, **kwargs) -> None:
        pass
