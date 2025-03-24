from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends import filter_by_user_permissions, get_async_db_session, get_current_active_user
from app.common.constants import COMMON_RESPONSES, AppStatus
from app.common.definitions import UserEndpointDefinition
from app.common.enums import ClassEnum
from app.core import AppResponse
from app.schemas.requests import PaginateRequest, UserCreateRequest
from app.schemas.responses import EmptyMetaResponse, StandardResponse, UserReadResponse
from app.services import UserService
from app.utils import logger_function_call

router: APIRouter = APIRouter()
_service: UserService = UserService()


@router.get(
    path="/",
    summary=UserEndpointDefinition.LIST_SUMMARY,
    description=UserEndpointDefinition.LIST_DESCRIPTION,
    response_model=StandardResponse[UserReadResponse, EmptyMetaResponse],
    responses=COMMON_RESPONSES,
)
@logger_function_call(class_name=ClassEnum.ENDPOINT)
async def get_users(
    paginate: PaginateRequest = Depends(),
    session: AsyncSession = Depends(get_async_db_session),
    filter_rpn: list[dict | str] = Depends(filter_by_user_permissions),
) -> AppResponse:
    data = await _service.get_users(paginate=paginate, session=session, filter_rpn=filter_rpn)
    return AppResponse(
        app_status=AppStatus.COMMON_200_LIST_OK, object_name="Tài khoản", data=[user.model_dump() for user in data]
    )


@router.post(
    path="/",
    summary=UserEndpointDefinition.CREATE_SUMMARY,
    description=UserEndpointDefinition.CREATE_DESCRIPTION,
    response_model=StandardResponse[UserReadResponse, EmptyMetaResponse],
    responses=COMMON_RESPONSES,
    dependencies=[Depends(get_current_active_user)],
)
@logger_function_call(class_name=ClassEnum.ENDPOINT)
async def create_user(request: UserCreateRequest, session: AsyncSession = Depends(get_async_db_session)) -> AppResponse:
    data = await _service.create_user(request=request, session=session)
    return AppResponse(app_status=AppStatus.COMMON_200_CREATE_OK, object_name="Tài khoản", data=data.model_dump())
