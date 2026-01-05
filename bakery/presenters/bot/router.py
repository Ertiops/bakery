from aiogram import Router
from aiogram.filters import Command

from bakery.presenters.bot.commands.utils import (
    Commands,
    contact_command,
    help_command,
    start_command,
)
from bakery.presenters.bot.dialogs import (
    registration,
)
from bakery.presenters.bot.dialogs.admin_contact import admin as admin_contact
from bakery.presenters.bot.dialogs.admin_contact import user as user_admin_contact
from bakery.presenters.bot.dialogs.cart import user as user_cart
from bakery.presenters.bot.dialogs.catalogue import admin as admin_catalogue
from bakery.presenters.bot.dialogs.catalogue import user as user_catalogue
from bakery.presenters.bot.dialogs.delivery_cost import admin as admin_delivery_cost
from bakery.presenters.bot.dialogs.main_menu import admin as admin_main_menu
from bakery.presenters.bot.dialogs.main_menu import user as user_main_menu
from bakery.presenters.bot.dialogs.order import user as user_order
from bakery.presenters.bot.dialogs.pickup_address import admin as admin_pickup_address


def register_dialogs(router: Router) -> None:
    dialog_router = Router()
    dialog_router.message(Command(Commands.START))(start_command)
    dialog_router.message(Command(Commands.HELP))(help_command)
    dialog_router.message(Command(Commands.CONTACT))(contact_command)
    dialog_router.include_routers(
        registration.user_registration_dialog,
    )
    dialog_router.include_routers(
        admin_main_menu.admin_main_menu_dialog,
        admin_catalogue.admin_catalogue_dialog,
        admin_pickup_address.admin_pickup_address_dialog,
        admin_contact.admin_admin_contact_dialog,
        admin_delivery_cost.admin_delivery_cost_dialog,
    )
    dialog_router.include_routers(
        user_main_menu.user_main_menu_dialog,
        user_cart.user_cart_dialog,
        user_order.user_order_dialog,
        user_catalogue.user_catalogue_dialog,
        user_admin_contact.user_admin_contact_dialog,
    )
    router.include_router(dialog_router)
