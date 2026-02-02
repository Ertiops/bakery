from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mashumaro.mixins.json import DataClassJSONMixin

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import ToDictMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateDeliveryCost(ToDictMixin):
    price: int
    free_delivery_amount: int | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class DeliveryCost(DataClassJSONMixin):
    id: UUID
    price: int
    free_delivery_amount: int | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateDeliveryCost(ToDictMixin):
    id: UUID
    price: int | Unset = UNSET
    free_delivery_amount: int | None | Unset = UNSET
