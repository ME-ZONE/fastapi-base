import uuid
from datetime import datetime

import pytz
from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import RoleEnum
from app.utils import convert_enum_to_list

from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "pcs_users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(*convert_enum_to_list(enum=RoleEnum), name="role_enum"),
        nullable=False,
        default=RoleEnum.USER,
    )
    token_version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
        onupdate=datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
    )

    details: Mapped["UserDetails"] = relationship("UserDetails", back_populates="user", uselist=False, lazy="select")  # noqa: F821
