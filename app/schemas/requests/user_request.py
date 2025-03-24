from typing import Any
from uuid import UUID

from pydantic import ConfigDict, Field

from app.common.definitions import UserExampleDefinition, UserRequestDefinition
from app.common.enums import RoleEnum
from app.schemas.base_schema import BaseSchema


class UserDetailsCreate(BaseSchema):
    fullname: str = Field(
        ...,
        description=UserRequestDefinition.FULL_NAME,
        examples=UserExampleDefinition.FULL_NAME,
    )
    gender: str = Field(
        ...,
        description=UserRequestDefinition.GENDER,
        examples=UserExampleDefinition.GENDER,
    )
    user_id: UUID | None = Field(None)

class UserCreate(BaseSchema):
    username: str = Field(
        ...,
        description=UserRequestDefinition.USERNAME,
        examples=UserExampleDefinition.USERNAME,
    )
    password: str = Field(
        ...,
        description=UserRequestDefinition.PASSWORD,
        examples=UserExampleDefinition.PASSWORD,
    )
    role: RoleEnum = Field(..., description=UserRequestDefinition.ROLE, examples=UserExampleDefinition.ROLE)
    hashed_password: str | None = Field(None)


class UserCreateRequest(UserCreate, UserDetailsCreate):
    model_config = ConfigDict(
        from_attributes=True, json_schema_extra=lambda schema: UserCreateRequest.custom_schema(schema)
    )

    @staticmethod
    def custom_schema(schema: dict[str, Any]) -> None:
        for field in ["user_id", "hashed_password"]:
            schema.get("properties", {}).pop(field, None)
