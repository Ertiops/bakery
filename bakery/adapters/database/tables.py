from __future__ import annotations

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class AdminContactTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "admin_contacts"

    name: Mapped[str] = mapped_column(String(63), nullable=False)
    tg_username: Mapped[str] = mapped_column(String(63), nullable=False)


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

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    category: Mapped[ProductCategory] = mapped_column(
        make_pg_enum(ProductCategory, name="product_category"),
        nullable=False,
    )
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class PickupAddressTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "pickup_addresses"

    __table_args__ = (
        Index(
            None,
            "name",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
    )

    name: Mapped[str] = mapped_column(String(256), nullable=False)


class CartTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "carts"

    __table_args__ = (
        Index(
            None,
            "user_id",
            "product_id",
            unique=True,
            postgresql_where="deleted_at IS NULL",
        ),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)


class OrderTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "orders"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    pickup_address_id: Mapped[UUID] = mapped_column(
        ForeignKey("pickup_addresses.id"), nullable=True
    )
    status: Mapped[OrderStatus] = mapped_column(
        make_pg_enum(OrderStatus, name="order_status"),
        nullable=False,
    )
    products: Mapped[Sequence[OrderProduct]] = mapped_column(
        JSONB,
        nullable=False,
    )
    address: Mapped[str] = mapped_column(String(256), nullable=True)
    delivered_at: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    pickup_address: Mapped[PickupAddressTable] = relationship(
        "PickupAddressTable",
        lazy="joined",
        innerjoin=False,
        backref="orders",
        foreign_keys=[pickup_address_id],
    )


class OrderScheduleTable(BaseTable, TimestampedMixin, IdentifableMixin):
    __tablename__ = "order_schedules"

    weekdays: Mapped[Sequence[int]] = mapped_column(JSONB, nullable=False)
    min_days_before: Mapped[int] = mapped_column(Integer, nullable=False)
    max_days_in_advance: Mapped[int] = mapped_column(Integer, nullable=False)
