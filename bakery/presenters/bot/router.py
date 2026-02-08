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
from bakery.presenters.bot.dialogs.blacklist import admin as admin_blacklist
from bakery.presenters.bot.dialogs.cart import user as user_cart
from bakery.presenters.bot.dialogs.catalogue import admin as admin_catalogue
from bakery.presenters.bot.dialogs.catalogue import user as user_catalogue
from bakery.presenters.bot.dialogs.delivery_cost import admin as admin_delivery_cost
from bakery.presenters.bot.dialogs.feedback_group import admin as admin_feedback_group
from bakery.presenters.bot.dialogs.main_menu import admin as admin_main_menu
from bakery.presenters.bot.dialogs.main_menu import user as user_main_menu
from bakery.presenters.bot.dialogs.order import admin as admin_order
from bakery.presenters.bot.dialogs.order import user as user_order
from bakery.presenters.bot.dialogs.order_payment import admin as admin_order_payment
from bakery.presenters.bot.dialogs.order_payment import user as user_order_payment
from bakery.presenters.bot.dialogs.order_schedule import admin as admin_order_schedule
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
        admin_order_payment.admin_order_payment_dialog,
        admin_order_schedule.admin_order_schedule_dialog,
        admin_feedback_group.admin_feedback_group_dialog,
        admin_order.admin_order_dialog,
        admin_blacklist.admin_blacklist_dialog,
    )
    dialog_router.include_routers(
        user_main_menu.user_main_menu_dialog,
        user_cart.user_cart_dialog,
        user_order.user_order_dialog,
        user_catalogue.user_catalogue_dialog,
        user_admin_contact.user_admin_contact_dialog,
        user_order_payment.user_order_payment_dialog,
    )
    router.include_router(dialog_router)
