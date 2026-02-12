from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from bakery.presenters.bot.content.buttons.main_menu import admin as admin_main_menu_msg
from bakery.presenters.bot.dialogs.admin_contact.admin.handlers import (
    open_admin_contact,
)
from bakery.presenters.bot.dialogs.main_menu.admin.handlers import (
    enter_blacklist,
    enter_catalog,
    enter_delivery_cost,
    enter_fake_users,
    enter_orders,
    enter_pickup_address_menu,
    enter_unpaid_orders,
    to_admin_feedback_group,
    to_admin_order_payment,
    to_admin_order_schedule,
)
from bakery.presenters.bot.dialogs.states import AdminMain


def admin_main_menu_window() -> Window:
    return Window(
        Const(admin_main_menu_msg.ADMIN_CONSOLE),
        Group(
            Button(
                Const(admin_main_menu_msg.CATALOGUE),
                id="catalog",
                on_click=enter_catalog,
            ),
            Button(
                Const(admin_main_menu_msg.ADDRESSES),
                id="pickup_address_menu",
                on_click=enter_pickup_address_menu,
            ),
            Button(
                Const(admin_main_menu_msg.CONTACTS),
                id="contacts",
                on_click=open_admin_contact,
            ),
            Button(
                Const(admin_main_menu_msg.DELIVERY_COST),
                id="delivery_cost",
                on_click=enter_delivery_cost,
            ),
            Button(
                Const(admin_main_menu_msg.ORDERS),
                id="orders",
                on_click=enter_orders,
            ),
            Button(
                Const(admin_main_menu_msg.UNPAID_ORDERS),
                id="unpaid_orders",
                on_click=enter_unpaid_orders,
            ),
            Button(
                Const(admin_main_menu_msg.BLACKLIST),
                id="blacklist",
                on_click=enter_blacklist,
            ),
            Button(
                Const(admin_main_menu_msg.FAKE_USERS),
                id="fake_users",
                on_click=enter_fake_users,
            ),
            Button(
                Const(admin_main_menu_msg.ORDER_PAYMENT),
                id="admin_order_payment",
                on_click=to_admin_order_payment,
            ),
            Button(
                Const(admin_main_menu_msg.ORDER_SCHEDULE),
                id="admin_order_schedule",
                on_click=to_admin_order_schedule,
            ),
            Button(
                Const(admin_main_menu_msg.FEEDBACK_GROUP),
                id="admin_feedback_group",
                on_click=to_admin_feedback_group,
            ),
            width=2,
        ),
        state=AdminMain.menu,
    )
