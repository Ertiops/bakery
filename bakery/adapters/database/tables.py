from sqlalchemy import Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from bakery.adapters.database.base import BaseTable, IdentifableMixin, TimestampedMixin
from bakery.adapters.database.utils import make_pg_enum
from bakery.domains.entities.order import OrderProduct, OrderStatus
from bakery.domains.entities.product import ProductCategory
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


class ProductTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "products"

    __table_args__ = (
        Index(
            None,
            "name",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
    )

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    category: Mapped[ProductCategory] = mapped_column(
        make_pg_enum(ProductCategory, name="product_category"),
        nullable=False,
    )
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=False)
    protein: Mapped[int] = mapped_column(Integer, nullable=False)
    fat: Mapped[int] = mapped_column(Integer, nullable=False)
    carbohydrate: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class OrderTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "orders"

    tg_user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    status: Mapped[OrderStatus] = mapped_column(
        make_pg_enum(OrderStatus, name="order_status"),
        nullable=False,
    )
    products: Mapped[list[OrderProduct]] = mapped_column(
        JSONB,
        nullable=False,
    )
    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
