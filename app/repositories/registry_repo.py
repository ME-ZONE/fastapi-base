from .user_details_repo import UserDetailsRepository
from .user_repo import UserRepository


class RegistryRepository:
    # Variable
    _user_repo: UserRepository
    _user_details_repo: UserDetailsRepository

    # Init
    def __init__(self) -> None:
        self._user_repo = UserRepository()
        self._user_details_repo = UserDetailsRepository()

    # External Function
    def get_user_repo(self) -> UserRepository:
        return self._user_repo

    def get_user_details_repo(self) -> UserDetailsRepository:
        return self._user_details_repo

    # Internal Function
