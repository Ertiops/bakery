from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, unique
from uuid import UUID

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import Pagination, ToDictMixin


@unique
class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    id: UUID
    name: str
    tg_id: int
    phone: str
    role: UserRole
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UserListParams(Pagination): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class UserList:
    total: int
    items: Sequence[User]


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUser(ToDictMixin):
    name: str
    tg_id: int
    phone: str
    role: UserRole


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateUser(ToDictMixin):
    id: UUID
    name: str | Unset = UNSET
    tg_id: int | Unset = UNSET
    phone: str | Unset = UNSET
    role: UserRole | Unset = UNSET
