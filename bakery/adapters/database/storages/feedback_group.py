from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.feedback_group import convert_feedback_group
from bakery.adapters.database.tables import FeedbackGroupTable
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.feedback_group import (
    CreateFeedbackGroup,
    FeedbackGroup,
    UpdateFeedbackGroup,
)
from bakery.domains.interfaces.storages.feedback_group import IFeedbackGroupStorage


class FeedbackGroupStorage(IFeedbackGroupStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateFeedbackGroup) -> FeedbackGroup:
        result = (
            await self.__session.scalars(
                insert(FeedbackGroupTable)
                .values(**input_dto.to_dict())
                .returning(FeedbackGroupTable)
            )
        ).one()
        return convert_feedback_group(result=result)

    async def get_last(self) -> FeedbackGroup | None:
        result = await self.__session.scalar(
            select(FeedbackGroupTable)
            .order_by(FeedbackGroupTable.created_at.desc())
            .limit(1)
        )
        return convert_feedback_group(result=result) if result else None

    async def update_by_id(self, *, input_dto: UpdateFeedbackGroup) -> FeedbackGroup:
        result = await self.__session.scalar(
            update(FeedbackGroupTable)
            .where(FeedbackGroupTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(FeedbackGroupTable)
        )
        if not result:
            raise EntityNotFoundException(entity=FeedbackGroup, entity_id=input_dto.id)
        return convert_feedback_group(result=result)
