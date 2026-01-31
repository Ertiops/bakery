from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mashumaro.mixins.json import DataClassJSONMixin

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import ToDictMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateOrderPayment(ToDictMixin):
    phone: str
    banks: Sequence[str]
    addressee: str


@dataclass(frozen=True, kw_only=True, slots=True)
class OrderPayment(DataClassJSONMixin):
    id: UUID
    phone: str
    banks: Sequence[str]
    addressee: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateOrderPayment(ToDictMixin):
    id: UUID
    phone: str | Unset = UNSET
    banks: Sequence[str] | Unset = UNSET
    addressee: str | Unset = UNSET
