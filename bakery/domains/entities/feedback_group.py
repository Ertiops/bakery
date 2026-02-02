from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from mashumaro.mixins.json import DataClassJSONMixin

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import ToDictMixin


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateFeedbackGroup(ToDictMixin):
    url: str


@dataclass(frozen=True, kw_only=True, slots=True)
class FeedbackGroup(DataClassJSONMixin):
    id: UUID
    url: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateFeedbackGroup(ToDictMixin):
    id: UUID
    url: str | Unset = UNSET
