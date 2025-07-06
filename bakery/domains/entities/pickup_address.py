from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import Pagination, ToDictMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class CreatePickupAddress(ToDictMixin):
    name: str


@dataclass(frozen=True, kw_only=True, slots=True)
class PickupAddress(ToDictMixin):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdatePickupAddress(ToDictMixin):
    id: UUID
    name: str | Unset = UNSET


@dataclass(frozen=True, kw_only=True, slots=True)
class PickupAddressListParams(Pagination): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class PickupAddressList:
    total: int
    items: Sequence[PickupAddress]
