from aiogram import F, Router
from aiogram.filters import Command

from bakery.presenters.bot.commands.utils import (
    Commands,
    enter_catalog,
    help_command,
    start_command,
)
from bakery.presenters.bot.content.buttons import admin_main_menu as admin_menu_btn
from bakery.presenters.bot.dialogs import (
    registration,
)
from bakery.presenters.bot.dialogs.catalogue import admin as admin_catalogue


def register_dialogs(router: Router) -> None:
    dialog_router = Router()
    dialog_router.message(Command(Commands.START))(start_command)
    dialog_router.message(Command(Commands.HELP))(help_command)
    dialog_router.message(F.text == admin_menu_btn.CATALOGUE)(enter_catalog)
    dialog_router.include_routers(
        registration.user_registration_dialog,
        admin_catalogue.admin_catalogue_dialog,
    )
    router.include_router(dialog_router)
