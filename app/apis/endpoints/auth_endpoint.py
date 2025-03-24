
from fastapi import APIRouter, Depends, Response
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import get_async_db_session
from app.common.constants import COMMON_RESPONSES, AppStatus
from app.common.definitions import AuthEndpointDefinition
from app.common.enums import ClassEnum, ProjectBuildTypes
from app.core import AppResponse, settings
from app.schemas.requests import AuthLoginRequest, EncryptedAuthLoginRequest
from app.schemas.responses import EmptyDataResponse, EmptyMetaResponse, StandardResponse
from app.services import AuthService
from app.utils import logger_function_call

router: APIRouter = APIRouter()
_service: AuthService = AuthService()

if settings.PROJECT_BUILD_TYPE != ProjectBuildTypes.PRODUCTION:

    @router.post(
        path="/login/",
        summary=AuthEndpointDefinition.LOGIN_SUMMARY,
        description=AuthEndpointDefinition.LOGIN_DESCRIPTION,
        response_model=StandardResponse[EmptyDataResponse, EmptyMetaResponse],
        responses=COMMON_RESPONSES,
        dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    )
    @logger_function_call(class_name=ClassEnum.ENDPOINT)
    async def login(
        request: AuthLoginRequest,
        session: AsyncSession = Depends(get_async_db_session),
    ) -> Response:
        response = AppResponse(app_status=AppStatus.AUTH_200_LOGIN_OK)
        response = await _service.login(request=request, response=response, session=session)
        return response
else:

    @router.post(
        path="/login/",
        summary=AuthEndpointDefinition.LOGIN_SUMMARY,
        description=AuthEndpointDefinition.LOGIN_DESCRIPTION,
        response_model=StandardResponse[EmptyDataResponse, EmptyMetaResponse],
        responses=COMMON_RESPONSES,
        dependencies=[Depends(RateLimiter(times=5, seconds=60))],
    )
    @logger_function_call(class_name=ClassEnum.ENDPOINT)
    async def login_encrypted(
        request: EncryptedAuthLoginRequest,
        session: AsyncSession = Depends(get_async_db_session),
    ) -> Response:
        response = AppResponse(app_status=AppStatus.AUTH_200_LOGIN_OK)
        new_request = _service.decrypt_auth_data(request=request)
        response = await _service.login(request=new_request, response=response, session=session)
        return response
