from aiogram import Router
from aiogram.filters import Command

from bakery.presenters.bot.commands.utils import (
    Commands,
    help_command,
    start_command,
)
from bakery.presenters.bot.dialogs import (
    registration,
)
from bakery.presenters.bot.dialogs.catalogue import admin as admin_catalogue
from bakery.presenters.bot.dialogs.catalogue import user as user_catalogue
from bakery.presenters.bot.dialogs.main_menu import admin as admin_main_menu
from bakery.presenters.bot.dialogs.main_menu import user as user_main_menu
from bakery.presenters.bot.dialogs.pickup_address import admin as admin_pickup_address


def register_dialogs(router: Router) -> None:
    dialog_router = Router()
    dialog_router.message(Command(Commands.START))(start_command)
    dialog_router.message(Command(Commands.HELP))(help_command)
    dialog_router.include_routers(
        registration.user_registration_dialog,
    )
    dialog_router.include_routers(
        admin_main_menu.admin_main_menu_dialog,
        admin_catalogue.admin_catalogue_dialog,
        user_catalogue.user_catalogue_dialog,
        admin_pickup_address.admin_pickup_address_dialog,
    )
    dialog_router.include_routers(
        user_main_menu.user_main_menu_dialog,
        # admin_catalogue.admin_catalogue_dialog,
        # user_catalogue.user_catalogue_dialog,
        # admin_pickup_address.admin_pickup_address_dialog,
    )
    router.include_router(dialog_router)
