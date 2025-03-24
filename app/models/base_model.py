from datetime import date, datetime
from uuid import UUID

from app.core.databases import Base
from app.utils import format_date, format_datetime


class BaseModel(Base):
    __abstract__ = True

    def to_dict(self) -> dict:
        result = {}
        for column in self.__table__.columns:
            column_name = column.name
            value = getattr(self, column_name)

            if isinstance(value, UUID):
                value = str(value)
            elif isinstance(value, datetime):
                value = format_datetime(value)
            elif isinstance(value, date):
                value = format_date(value)

            result[column_name] = value

        return result
