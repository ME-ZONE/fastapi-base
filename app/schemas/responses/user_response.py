from pydantic import Field

from app.common.definitions import CommonExampleDefinition, UserExampleDefinition
from app.common.enums import GenderEnum, RoleEnum
from app.schemas.base_schema import BaseSchema


class UserListResponse(BaseSchema):
    id: str = Field(..., examples=UserExampleDefinition.USERNAME)
    username: str = Field(..., examples=UserExampleDefinition.USERNAME)
    is_superuser: bool
    is_active: bool
    role: RoleEnum = Field(None, examples=UserExampleDefinition.ROLE)


class UserDetailsReadResponse(BaseSchema):
    id: str = Field(..., examples=CommonExampleDefinition.UUID)
    user_id: str = Field(..., examples=CommonExampleDefinition.UUID)
    fullname: str = Field(..., examples=UserExampleDefinition.FULL_NAME)
    gender: GenderEnum = Field(None, examples=UserExampleDefinition.GENDER)
    created_at: str = Field(None, examples=CommonExampleDefinition.CREATED_AT)
    updated_at: str = Field(None, examples=CommonExampleDefinition.UPDATED_AT)


class UserReadResponse(BaseSchema):
    id: str = Field(..., examples=UserExampleDefinition.USERNAME)
    username: str = Field(..., examples=UserExampleDefinition.USERNAME)
    is_superuser: bool
    is_active: bool
    role: RoleEnum = Field(None, examples=UserExampleDefinition.ROLE)
    created_at: str = Field(None, examples=CommonExampleDefinition.CREATED_AT)
    updated_at: str = Field(None, examples=CommonExampleDefinition.UPDATED_AT)
    details: UserDetailsReadResponse
