from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from bakery.presenters.bot.content.buttons.main_menu import user as user_main_menu_msg
from bakery.presenters.bot.dialogs.main_menu.user.handlers import (
    enter_cart,
    enter_catalog,
    enter_order_categories,
)
from bakery.presenters.bot.dialogs.states import UserMain


def user_main_menu_window() -> Window:
    return Window(
        Const(user_main_menu_msg.MAIN_MENU),
        Group(
            Button(
                Const(user_main_menu_msg.CATALOGUE),
                id="catalog",
                on_click=enter_catalog,
            ),
            Button(
                Const(user_main_menu_msg.CART),
                id="cart",
                on_click=enter_cart,
            ),
            Button(
                Const(user_main_menu_msg.MY_ORDERS),
                id="my_orders",
                on_click=enter_order_categories,
            ),
            width=1,
        ),
        state=UserMain.menu,
    )
