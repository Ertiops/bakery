from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bakery_bot.adapters.database.base import (
    BaseTable,
    IdentifableMixin,
    TimestampedMixin,
)
from bakery_bot.adapters.database.utils import make_pg_enum
from bakery_bot.domains.entities.user import UserRole


class UserTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(63), nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    role: Mapped[UserRole] = mapped_column(make_pg_enum(UserRole, name="user_role"))
