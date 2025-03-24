from pydantic import Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from app.common.constants import AUTH_KEY_MAP_TRANSLATE, AppStatus
from app.common.definitions import AuthExampleDefinition, AuthRequestDefinition
from app.schemas.base_schema import BaseSchema

MIN_USERNAME_LENGTH = 4
MIN_PASSWORD_LENGTH = 6


class AuthLoginRequest(BaseSchema):
    username: str = Field(
        ...,
        description=AuthRequestDefinition.USERNAME,
        min_length=4,
        max_length=50,
        examples=AuthExampleDefinition.USERNAME,
    )
    password: str = Field(
        ...,
        description=AuthRequestDefinition.PASSWORD,
        min_length=6,
        max_length=100,
        examples=AuthExampleDefinition.PASSWORD,
    )

    @field_validator("username", mode="before")
    def validate_username(cls, value: str, info: ValidationInfo) -> str:
        if len(value) < MIN_USERNAME_LENGTH:
            raise ValueError(
                AppStatus.COMMON_400_MIN_LENGTH_BAD_REQUEST.message.format(
                    field_name=AUTH_KEY_MAP_TRANSLATE[info.field_name], min=MIN_USERNAME_LENGTH
                )
            )
        return value

    @field_validator("password", mode="before")
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        if len(value) < MIN_PASSWORD_LENGTH:
            raise ValueError(
                AppStatus.COMMON_400_MIN_LENGTH_BAD_REQUEST.message.format(
                    field_name=AUTH_KEY_MAP_TRANSLATE[info.field_name], min=MIN_PASSWORD_LENGTH
                )
            )
        return value


class EncryptedAuthLoginRequest(BaseSchema):
    encrypted_data: str = Field(
        ..., description=AuthRequestDefinition.ENCRYPTED, examples=AuthExampleDefinition.ENCRYPTED
    )
