import json
from abc import ABC, abstractmethod
from pathlib import Path

from faker import Faker
from sqlalchemy.orm import Session


class BaseSeed(ABC):
    faker: Faker
    data_folder_path: Path
    data_file_path: Path

    def __init__(self, file_name: str) -> None:
        self.faker = Faker()
        self.data_folder_path = Path(__file__).parent / "data"
        self.data_folder_path.mkdir(exist_ok=True)
        self.data_file_path = self.data_folder_path / file_name

    @abstractmethod
    def generate_data(self, num_records: int = 20) -> list:
        pass


    @abstractmethod
    def create_data(self, session: Session) -> None:
        pass

    @staticmethod
    def load_data(file_path: Path) -> list:
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_data(file_path: Path, data: list) -> None:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except OSError as e:
            print(f"Lỗi khi ghi file {file_path}: {e}")  # noqa: T201
