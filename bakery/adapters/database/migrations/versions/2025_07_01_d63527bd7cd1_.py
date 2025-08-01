"""empty message

Revision ID: d63527bd7cd1
Revises:
Create Date: 2025-07-01 12:43:33.668440

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d63527bd7cd1"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orders",
        sa.Column("tg_user_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "on_accept", "in_progress", "delivered", "paid", name="order_status"
            ),
            nullable=False,
        ),
        sa.Column("products", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__orders")),
    )
    op.create_table(
        "pickup_addresses",
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__pickup_addresses")),
    )
    op.create_index(
        op.f("ix__pickup_addresses__name"),
        "pickup_addresses",
        ["name"],
        unique=True,
        postgresql_where="deleted_at IS NULL",
    )
    op.create_table(
        "products",
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=False),
        sa.Column(
            "category",
            postgresql.ENUM(
                "bread",
                "oil",
                "flour",
                "dessert",
                "noodle",
                "other",
                name="product_category",
            ),
            nullable=False,
        ),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__products")),
    )
    op.create_index(
        op.f("ix__products__name"),
        "products",
        ["name"],
        unique=True,
        postgresql_where="deleted_at IS NULL",
    )
    op.create_table(
        "users",
        sa.Column("name", sa.String(length=63), nullable=False),
        sa.Column("tg_id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=16), nullable=False),
        sa.Column(
            "role", postgresql.ENUM("admin", "user", name="user_role"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
    )
    op.create_index(
        op.f("ix__users__phone"),
        "users",
        ["phone"],
        unique=True,
        postgresql_where="deleted_at IS NULL",
    )
    op.create_index(
        op.f("ix__users__tg_id"),
        "users",
        ["tg_id"],
        unique=True,
        postgresql_where="deleted_at IS NULL",
    )
    op.create_table(
        "user_addresses",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk__user_addresses__user_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user_addresses")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_addresses")
    op.drop_index(
        op.f("ix__users__tg_id"),
        table_name="users",
        postgresql_where="deleted_at IS NULL",
    )
    op.drop_index(
        op.f("ix__users__phone"),
        table_name="users",
        postgresql_where="deleted_at IS NULL",
    )
    op.drop_table("users")
    op.drop_index(
        op.f("ix__products__name"),
        table_name="products",
        postgresql_where="deleted_at IS NULL",
    )
    op.drop_table("products")
    op.drop_index(
        op.f("ix__pickup_addresses__name"),
        table_name="pickup_addresses",
        postgresql_where="deleted_at IS NULL",
    )
    op.drop_table("pickup_addresses")
    op.drop_table("orders")
    # ### end Alembic commands ###
