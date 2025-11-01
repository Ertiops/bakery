from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import ToDictMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateAdminContact(ToDictMixin):
    name: str
    phone: str
    tg_username: str


@dataclass(frozen=True, kw_only=True, slots=True)
class AdminContact:
    id: UUID
    name: str
    phone: str
    tg_username: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateAdminContact(ToDictMixin):
    id: UUID
    name: str | Unset = UNSET
    phone: str | Unset = UNSET
    tg_username: str | Unset = UNSET
