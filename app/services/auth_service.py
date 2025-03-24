import json

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import create_access_token, create_refresh_token
from app.common.constants import (
    ACCESS_TOKEN_EXPIRES_IN_SECONDS,
    REFRESH_TOKEN_EXPIRES_IN_SECONDS,
    AppStatus,
)
from app.common.enums import ClassEnum, ProjectBuildTypes, TokenTypeEnum
from app.core import AppException, settings
from app.models import User
from app.repositories import RegistryRepository, UserRepository
from app.schemas.requests import AuthLoginRequest, EncryptedAuthLoginRequest
from app.utils import (
    decrypt_data,
    logger_class_methods,
    verify_data,
)


@logger_class_methods(class_name=ClassEnum.SERVICE)
class AuthService:
    ## Variable ##
    _repo: RegistryRepository
    _user_repo: UserRepository

    ## Init ##
    def __init__(self) -> None:
        self._repo = RegistryRepository()
        self._user_repo = self._repo.get_user_repo()

    ## External Function ##
    async def login(self, request: AuthLoginRequest, response: Response, session: AsyncSession) -> Response:
        user = await self._user_repo.get(session, User.username == request.username)
        if not user or not verify_data(data=request.password, hashed_data=str(user.hashed_password)):
            raise AppException(app_status=AppStatus.AUTH_400_LOGIN_BAD_REQUEST)
        response = self._set_cookie_response(response=response, user=user)
        return response

    @staticmethod
    def decrypt_auth_data(request: EncryptedAuthLoginRequest) -> AuthLoginRequest:
        try:
            decrypted_data = decrypt_data(encrypted_data=request.encrypted_data)
            data = json.loads(decrypted_data)
            return AuthLoginRequest(**data)
        except Exception as e:
            raise AppException(app_status=AppStatus.AUTH_400_DECRYPT_DATA_BAD_REQUEST) from e

    ## Internal Function ##
    @staticmethod
    def _set_cookie_response(response: Response, user: User) -> Response:
        data = {"user_id": user.id, "username": user.username, "token_version": user.token_version}
        access_token = create_access_token(data=data)
        refresh_token = create_refresh_token(data=data)
        response.set_cookie(
            key=TokenTypeEnum.ACCESS_TOKEN.value,
            value=access_token,
            max_age=ACCESS_TOKEN_EXPIRES_IN_SECONDS,
            httponly=True,
            path="/",
            secure=settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.DEVELOPMENT,
            samesite="lax" if settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.PRODUCTION else "none",
        )
        response.set_cookie(
            key=TokenTypeEnum.REFRESH_TOKEN.value,
            value=refresh_token,
            max_age=REFRESH_TOKEN_EXPIRES_IN_SECONDS,
            httponly=True,
            path="/",
            secure=settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.DEVELOPMENT,
            samesite="lax" if settings.PROJECT_BUILD_TYPE == ProjectBuildTypes.DEVELOPMENT else "none",
        )
        return response
