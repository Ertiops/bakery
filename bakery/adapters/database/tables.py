from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from bakery.adapters.database.base import BaseTable, IdentifableMixin, TimestampedMixin
from bakery.adapters.database.utils import make_pg_enum
from bakery.domains.entities.user import UserRole


class UserTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "users"

    __table_args__ = (
        Index(
            None,
            "tg_id",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
        Index(
            None,
            "phone",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
    )

    name: Mapped[str] = mapped_column(String(63), nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    role: Mapped[UserRole] = mapped_column(make_pg_enum(UserRole, name="user_role"))
