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
    FAKE_USER = "fake_user"


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    id: UUID
    name: str
    tg_id: int | None
    phone: str
    role: UserRole
    exclusion_reason: str | None = None
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
    tg_id: int | None
    phone: str
    role: UserRole
    exclusion_reason: str | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateFakeUser:
    name: str
    phone: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateUser(ToDictMixin):
    id: UUID
    name: str | Unset = UNSET
    tg_id: int | None | Unset = UNSET
    phone: str | Unset = UNSET
    role: UserRole | Unset = UNSET
    exclusion_reason: str | None | Unset = UNSET


@dataclass(frozen=True, kw_only=True, slots=True)
class UserBlacklistListParams(Pagination): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class UserPhoneSearchParams(Pagination):
    phone: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UserFakeListParams(Pagination): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class UserFakeSearchParams(Pagination):
    phone: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UserExclusionParams:
    id: UUID
    reason: str


@dataclass(frozen=True, kw_only=True, slots=True)
class UserClearExclusionParams:
    id: UUID
