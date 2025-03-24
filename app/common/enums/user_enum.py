from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
