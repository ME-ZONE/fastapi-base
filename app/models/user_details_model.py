import uuid
from datetime import datetime

import pytz
from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import GenderEnum
from app.utils import convert_enum_to_list

from .base_model import BaseModel


class UserDetails(BaseModel):
    __tablename__ = "pcs_user_details"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pcs_users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    fullname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(*convert_enum_to_list(enum=GenderEnum), name="gender_enum"),
        nullable=False,
        default=GenderEnum.MALE,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
        onupdate=datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
    )

    user: Mapped["User"] = relationship("User", back_populates="details", uselist=False, lazy="select")  # noqa: F821
