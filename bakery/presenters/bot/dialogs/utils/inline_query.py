from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
)
from aiogram.types.inline_query_result_article import (
    InlineQueryResultArticle,
)
from dishka import AsyncContainer

from bakery.domains.entities.user import User
from bakery.presenters.bot.filters.via_bot import ViaBotMessageFilter

router = Router()


@router.inline_query(ViaBotMessageFilter())
async def fio_handler(
    query: InlineQuery,
    dishka_container: AsyncContainer,
    current_user: User,
) -> None:
    inline_query_results = [
        InlineQueryResultArticle(
            id="ssss",
            title=("sss"),
            input_message_content=InputTextMessageContent(
                message_text=("sss"),
            ),
        )
    ]
    await query.answer(results=inline_query_results, cache_time=1, is_personal=True)  # type: ignore[arg-type]
