from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import ClassEnum
from app.models import User, UserDetails
from app.repositories import RegistryRepository, UserRepository
from app.repositories.user_details_repo import UserDetailsRepository
from app.schemas.requests import PaginateRequest, UserCreate, UserCreateRequest, UserDetailsCreate
from app.schemas.responses import UserDetailsReadResponse, UserListResponse, UserReadResponse
from app.utils import hash_data, logger_class_methods


@logger_class_methods(class_name=ClassEnum.SERVICE)
class UserService:
    ## Variable ##
    _repo: RegistryRepository
    _user_repo: UserRepository
    _user_details_repo: UserDetailsRepository

    ## Init ##
    def __init__(self) -> None:
        self._repo = RegistryRepository()
        self._user_repo = self._repo.get_user_repo()
        self._user_details_repo = self._repo.get_user_details_repo()

    ## External Function ##
    async def get_users(
        self, paginate: PaginateRequest, session: AsyncSession, filter_rpn: list[dict | str]
    ) -> list[UserListResponse]:
        users = await self._user_repo.get_multi(
            session=session, filter_rpn=filter_rpn, offset=paginate.offset, limit=paginate.limit
        )
        data = [UserListResponse(**user.to_dict()) for user in users]
        return data

    async def create_user(self, request: UserCreateRequest, session: AsyncSession) -> UserReadResponse:
        user_data = UserCreate(**request.model_dump())
        user_data.hashed_password = hash_data(request.password)
        del user_data.password
        user = await self._user_repo.get_or_create(session, User.username == user_data.username, obj_in=user_data)

        user_details_data = UserDetailsCreate(**request.model_dump())
        user_details_data.user_id = user.id
        user_details = await self._user_details_repo.get_or_create(
            session, UserDetails.user_id == user.id, obj_in=user_details_data
        )
        user_details_response = UserDetailsReadResponse(**user_details.to_dict())
        data = UserReadResponse(**user.to_dict(), details=user_details_response)
        return data

    ## Internal Function ##
