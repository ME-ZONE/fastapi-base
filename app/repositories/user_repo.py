from app.common.enums import ClassEnum
from app.models import User
from app.utils import logger_class_methods

from .base_repo import BaseRepository


@logger_class_methods(class_name=ClassEnum.REPOSITORY)
class UserRepository(BaseRepository[User]):
    ## Variable ##
    ## Init ##
    def __init__(self) -> None:
        super().__init__(model=User)

    ## External Function ##
    ## Internal Function ##
