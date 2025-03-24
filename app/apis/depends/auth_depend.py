import uuid
from datetime import datetime, timedelta
from typing import Any

import jwt
import pytz
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.constants import (
    ACCESS_TOKEN_EXPIRES_IN_SECONDS,
    JWT_ALGORITHM,
    REFRESH_TOKEN_EXPIRES_IN_SECONDS,
    AppStatus,
)
from app.common.enums import TokenTypeEnum
from app.core import AppException, settings
from app.models import User
from app.opa.permissions import OpenPolicyAgentPermission
from app.repositories import RegistryRepository
from app.utils import create_bullet_list

from .database_depend import get_async_db_session


## External Function ##
def create_access_token(data: dict) -> str:
    return _create_token(data=data, token_type=TokenTypeEnum.ACCESS_TOKEN)


def create_refresh_token(data: dict, expired_at: float | None = None) -> str:
    return _create_token(data=data, token_type=TokenTypeEnum.REFRESH_TOKEN, expired_at=expired_at)


async def verify_access_token(token: str, session: AsyncSession) -> User:
    (decoded_token, user) = await _verify_token(token=token, session=session)
    if decoded_token["token_type"] != TokenTypeEnum.ACCESS_TOKEN:
        raise AppException(app_status=AppStatus.AUTH_400_TOKEN_INVALID_BAD_REQUEST)
    return user


async def verify_refresh_token(token: str, session: AsyncSession) -> User:
    (decoded_token, user) = await _verify_token(token=token, session=session)
    if decoded_token["token_type"] != TokenTypeEnum.REFRESH_TOKEN:
        raise AppException(app_status=AppStatus.AUTH_400_TOKEN_INVALID_BAD_REQUEST)
    return user


async def get_current_active_user(
    request: Request,
    session: AsyncSession = Depends(get_async_db_session),
) -> User:
    token = request.cookies.get(TokenTypeEnum.ACCESS_TOKEN, None)
    user = await verify_access_token(token=token, session=session)
    return user


async def check_user_permissions(
    request: Request,
    session: AsyncSession = Depends(get_async_db_session),
    user: User = Depends(get_current_active_user),
) -> User:
    user_permissions = await _gather_permissions(request=request, session=session, user=user)
    await _check_permissions(user_permissions)
    return user


async def filter_by_user_permissions(
    request: Request,
    user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_db_session),
) -> list[dict | str]:
    user_permissions = await _gather_permissions(request=request, user=user, session=session)

    filter_rpn = []

    for perm in user_permissions:
        if perm.payload["input"]["scope"].startswith("list"):
            result = await perm.filter()
            if filter_rpn:
                filter_rpn.extend(result.filter_rpn.extend(["&"]))
            else:
                filter_rpn.extend(result.filter_rpn)

    return filter_rpn


## Internal Function ##
async def _verify_token(token: str, session: AsyncSession) -> tuple[Any, User]:
    if not token:
        raise AppException(app_status=AppStatus.AUTH_400_TOKEN_INVALID_BAD_REQUEST)

    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=JWT_ALGORITHM)
    except jwt.exceptions.ExpiredSignatureError as e:
        raise AppException(app_status=AppStatus.AUTH_400_TOKEN_INVALID_BAD_REQUEST) from e
    except jwt.exceptions.InvalidSignatureError as e:
        raise AppException(app_status=AppStatus.AUTH_400_TOKEN_INVALID_BAD_REQUEST) from e
    except jwt.exceptions.DecodeError as e:
        raise AppException(app_status=AppStatus.AUTH_400_TOKEN_INVALID_BAD_REQUEST) from e

    user_id = decoded_token["user_id"]
    token_version = int(decoded_token["token_version"])

    user_repo = RegistryRepository().get_user_repo()
    user = await user_repo.get_or_404(session, User.id == user_id)
    if token_version != user.token_version:
        raise AppException(app_status=AppStatus.AUTH_400_TOKEN_EXPIRED_BAD_REQUEST)
    if not user.is_active:
        raise AppException(app_status=AppStatus.AUTH_400_USER_INACTIVE_BAD_REQUEST)

    return decoded_token, user


def _serialize_data(data: dict) -> dict:
    serialized_data = {}
    for key, value in data.items():
        if isinstance(value, uuid.UUID):
            serialized_data[key] = str(value)
        else:
            serialized_data[key] = value

    return serialized_data


def _create_token(data: dict, token_type: TokenTypeEnum, expired_at: float | None = None) -> str:
    data = _serialize_data(data)
    created_at = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).timestamp()
    expires_delta = timedelta(
        seconds=ACCESS_TOKEN_EXPIRES_IN_SECONDS
        if token_type == TokenTypeEnum.ACCESS_TOKEN
        else REFRESH_TOKEN_EXPIRES_IN_SECONDS
    )
    expired_at = (
        datetime.fromtimestamp(expired_at)
        if expired_at
        else datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")) + expires_delta
    )
    to_encode = {**data, "token_type": token_type, "exp": expired_at, "created_at": created_at}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=JWT_ALGORITHM)


async def _gather_permissions(request: Request, user: User, session: AsyncSession) -> list[OpenPolicyAgentPermission]:
    permissions = []
    for perm_class in OpenPolicyAgentPermission.__subclasses__():
        permissions.extend(await perm_class.create(request=request, user=user, session=session))
    return permissions


async def _check_permissions(permissions: list[OpenPolicyAgentPermission]) -> bool:
    allow = True
    reasons = []

    for perm in permissions:
        result = await perm.check_access()
        reasons.extend(result.reasons)
        allow &= result.allow
    if not allow:
        if reasons:
            raise AppException(app_status=AppStatus.OPA_405_METHOD_NOT_ALLOWED, description=create_bullet_list(reasons))
        else:
            raise AppException(app_status=AppStatus.INIT_405_METHOD_NOT_ALLOWED)

    return allow
