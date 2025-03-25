import secrets

from sqlalchemy.orm import Session

from app.common.enums import RoleEnum
from app.models import User
from app.utils import hash_data

from .seed_base import BaseSeed


class SeedUser(BaseSeed):
    def __init__(self) -> None:
        super().__init__(file_name="users.json")

    def generate_data(self, num_records: int = 10) -> None:
        users = self.load_data(file_path=self.data_file_path)
        if users:
            print("Dữ liệu user đã được khởi tạo.")  # noqa: T201
            return

        existing_usernames = set()
        for _ in range(num_records):
            password = self.faker.password()

            while True:
                username = self.faker.user_name()
                if username not in existing_usernames:
                    existing_usernames.add(username)
                    break

            users.append(
                {
                    "id": self.faker.uuid4(),
                    "username": username,
                    "password": password,
                    "hashed_password": hash_data(password),
                    "is_superuser": self.faker.boolean(),
                    "is_active": self.faker.boolean(),
                    "role": secrets.choice(list(RoleEnum)),
                    "token_version": 0,
                }
            )

        self.save_data(file_path=self.data_file_path, data=users)

    def create_data(self, session: Session) -> None:
        users = self.load_data(file_path=self.data_file_path)
        if not users:
            print("Không có dữ liệu user để khởi tạo.")  # noqa: T201
            return

        user_objs = [User(**{k: v for k, v in user.items() if k != "password"}) for user in users]
        session.add_all(instances=user_objs)
        session.commit()

seed_user = SeedUser()
