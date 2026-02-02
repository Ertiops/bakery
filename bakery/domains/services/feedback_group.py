from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.feedback_group import (
    CreateFeedbackGroup,
    FeedbackGroup,
    UpdateFeedbackGroup,
)
from bakery.domains.interfaces.storages.feedback_group import IFeedbackGroupStorage


class FeedbackGroupService:
    __feedback_group_storage: IFeedbackGroupStorage

    def __init__(self, feedback_group_storage: IFeedbackGroupStorage) -> None:
        self.__feedback_group_storage = feedback_group_storage

    async def create(self, *, input_dto: CreateFeedbackGroup) -> FeedbackGroup:
        return await self.__feedback_group_storage.create(input_dto=input_dto)

    async def get_last(self) -> FeedbackGroup:
        feedback_group = await self.__feedback_group_storage.get_last()
        if feedback_group is None:
            raise EntityNotFoundException(entity=FeedbackGroup, entity_id=None)
        return feedback_group

    async def update_by_id(self, *, input_dto: UpdateFeedbackGroup) -> FeedbackGroup:
        return await self.__feedback_group_storage.update_by_id(input_dto=input_dto)
