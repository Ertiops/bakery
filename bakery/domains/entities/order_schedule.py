from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import ToDictMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateOrderSchedule(ToDictMixin):
    weekdays: Sequence[int]
    min_days_before: int
    max_days_in_advance: int


@dataclass(frozen=True, kw_only=True, slots=True)
class OrderSchedule:
    id: UUID
    weekdays: Sequence[int]
    min_days_before: int
    max_days_in_advance: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateOrderSchedule(ToDictMixin):
    id: UUID
    weekdays: Sequence[int] | Unset = UNSET
    min_days_before: int | Unset = UNSET
    max_days_in_advance: int | Unset = UNSET
