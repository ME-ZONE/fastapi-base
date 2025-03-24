from fastapi.params import Query
from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo

from app.common.constants import PAGINATE_KEY_MAP_TRANSLATE, AppStatus
from app.common.definitions import CommonRequestDefinition
from app.schemas.base_schema import BaseSchema

MIN_VALUE = 0


class PaginateRequest(BaseSchema):
    offset: int | None = Query(
        None,
        description=CommonRequestDefinition.OFFSET,
    )
    limit: int | None = Query(
        None,
        description=CommonRequestDefinition.LIMIT,
    )

    @field_validator("offset", "limit", mode="before")
    def validate_username(cls, value: int | None, info: ValidationInfo) -> int | None:
        if value and value < MIN_VALUE:
            raise ValueError(
                AppStatus.COMMON_400_MIN_VALUE_BAD_REQUEST.message.format(
                    field_name=PAGINATE_KEY_MAP_TRANSLATE[info.field_name],
                    min=MIN_VALUE,
                )
            )
        return value
