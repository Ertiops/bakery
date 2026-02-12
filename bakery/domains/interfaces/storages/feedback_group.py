from typing import Protocol

from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.feedback_group import (
    CreateFeedbackGroup,
    FeedbackGroup,
    UpdateFeedbackGroup,
)


class IFeedbackGroupStorage(Protocol):
    async def create(self, *, input_dto: CreateFeedbackGroup) -> FeedbackGroup: ...

    async def get_last(self) -> FeedbackGroup | None: ...

    async def update_by_id(
        self, *, input_dto: UpdateFeedbackGroup
    ) -> FeedbackGroup: ...

    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None: ...
