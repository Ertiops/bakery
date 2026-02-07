from collections.abc import Mapping, Sequence
from typing import Any

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, ListGroup, Row, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.cart import user as user_msg
from bakery.presenters.bot.dialogs.cart.user.getters import get_cart_data
from bakery.presenters.bot.dialogs.cart.user.handlers import on_cart_item_delete
from bakery.presenters.bot.dialogs.cart.user.redirections import to_order_create
from bakery.presenters.bot.dialogs.main_menu.user.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import UserCart


def _carts_getter(data: dict, *_args: Any, **_kwargs: Any) -> Sequence[Mapping]:
    return data.get("carts") or []


def _has_items(data: dict, *_args: Any, **_kwargs: Any) -> bool:
    return bool(data.get("carts"))


def cart_window() -> Window:
    return Window(
        Const(user_msg.CART_EMPTY, when=lambda d, *_: not _has_items(d)),
        Format("{cart_text}", when=_has_items),
        ScrollingGroup(
            ListGroup(
                Row(
                    Button(
                        Format("{item[name]} ×{item[quantity]}"),
                        id="cart_item_name",
                        on_click=None,
                    ),
                    Button(
                        Const(common_btn.DELETE_REDUCED),
                        id="cart_item_delete",
                        on_click=on_cart_item_delete,
                    ),
                ),
                id="cart_items",
                item_id_getter=lambda item: item["idx"],
                items=_carts_getter,
            ),
            id="cart_scroll",
            width=2,
            height=3,
            when=_has_items,
        ),
        Button(
            Const(common_btn.CREATE),
            id="create_order",
            on_click=to_order_create,
            when=_has_items,
        ),
        Button(Const(common_btn.BACK), id="back", on_click=to_main_menu),
        state=UserCart.view,
        getter=get_cart_data,
    )
