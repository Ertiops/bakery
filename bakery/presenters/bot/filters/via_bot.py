from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery

CHAT_TYPE = "sender"


class ViaBotMessageFilter(BaseFilter):
    async def __call__(
        self,
        query: InlineQuery,
    ) -> bool:
        return query.chat_type == CHAT_TYPE
