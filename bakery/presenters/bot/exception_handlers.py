import logging
from typing import Any

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager

from bakery.presenters.bot.dialogs.redirections import start_new_dialog

log = logging.getLogger(__name__)

REGISTER_TEXT = "Пожалуйста, зарегистрируйся сначала"


log = logging.getLogger(__name__)


async def on_unknown_intent(event: ErrorEvent, *args: Any, **kwargs: Any) -> None:
    log.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Бот был перезапущен для тех. обслуживания.\n"
            "Вы будете перенаправлены в главное меню.",
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()  # type: ignore[union-attr]
            except TelegramBadRequest:
                pass


async def on_unknown_user(event: ErrorEvent, *args: Any, **kwargs: Any) -> None:
    log.error("Unknown user")
    if event.update.callback_query:
        await event.update.callback_query.answer(f"{REGISTER_TEXT}")
    if event.update.message:
        await event.update.message.answer(f"{REGISTER_TEXT}")


async def on_unknown_state(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    log.error("Restarting dialog: %s", event.exception)
    await start_new_dialog(dialog_manager)
