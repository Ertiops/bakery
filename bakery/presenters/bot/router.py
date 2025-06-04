from aiogram import Router
from aiogram.filters import Command

from bakery.presenters.bot.commands.utils import (
    Commands,
    start_command,
)
from bakery.presenters.bot.dialogs import (
    registration,
)


def register_dialogs(router: Router) -> None:
    dialog_router = Router()
    dialog_router.message(Command(Commands.START))(start_command)
    dialog_router.include_router(
        registration.user_registration_dialog,
    )
    router.include_router(dialog_router)
