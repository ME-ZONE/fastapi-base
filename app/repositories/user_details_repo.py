from app.common.enums import ClassEnum
from app.models import UserDetails
from app.utils import logger_class_methods

from .base_repo import BaseRepository


@logger_class_methods(class_name=ClassEnum.REPOSITORY)
class UserDetailsRepository(BaseRepository[UserDetails]):
    ## Variable ##
    ## Init ##
    def __init__(self) -> None:
        super().__init__(model=UserDetails)

    ## External Function ##
    ## Internal Function ##
