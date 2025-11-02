from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from bakery.presenters.bot.content.buttons.main_menu import admin as admin_main_menu_msg
from bakery.presenters.bot.dialogs.admin_contact.admin.handlers import (
    open_admin_contact,
)
from bakery.presenters.bot.dialogs.main_menu.admin.handlers import (
    enter_catalog,
    enter_pickup_address_menu,
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
            width=1,
        ),
        state=AdminMain.menu,
    )
