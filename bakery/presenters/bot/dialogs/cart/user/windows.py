from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, ListGroup, Row
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.dialogs.cart.user.getters import get_cart_data
from bakery.presenters.bot.dialogs.cart.user.handlers import (
    on_decrement_quantity,
    on_increment_quantity,
)
from bakery.presenters.bot.dialogs.main_menu.user.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import UserCart


def cart_window() -> Window:
    return Window(
        Format("{cart_text}"),
        ListGroup(
            Row(
                Button(Format("{item.product.name}"), id="title"),
            ),
            Row(
                Button(Const("➖"), id="dec_cart", on_click=on_decrement_quantity),
                Button(
                    Format("{item.quantity}"),
                    id="quantity",
                ),
                Button(Const("➕"), id="inc_cart", on_click=on_increment_quantity),
            ),
            id="carts",
            item_id_getter=lambda item: str(item.product.id),
            items="carts",
        ),
        Button(Const(common_btn.BACK), id="back", on_click=to_main_menu),
        state=UserCart.view,
        getter=get_cart_data,
    )
