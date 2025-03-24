from enum import Enum


class TokenTypeEnum(str, Enum):
    ACCESS_TOKEN = "access_token"  # noqa: S105
    REFRESH_TOKEN = "refresh_token"  # noqa: S105
