from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Row,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.catalogue import (
    common as common_catalogue_msg,
)
from bakery.presenters.bot.dialogs.catalogue.user.getters import (
    get_products_data,
    get_selected_product,
)
from bakery.presenters.bot.dialogs.catalogue.user.handlers import (
    on_view_product_clicked,
)
from bakery.presenters.bot.dialogs.catalogue.user.redirections import (
    to_product_categories,
    to_product_list,
)
from bakery.presenters.bot.dialogs.catalogue.user.selections import (
    on_category_selected,
)
from bakery.presenters.bot.dialogs.catalogue.windows import CATEGORY_ITEMS
from bakery.presenters.bot.dialogs.main_menu.user.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import UserCatalogue


def select_category_window() -> Window:
    return Window(
        Const(common_catalogue_msg.CATALOGUE_CATEGORY_SELECTION),
        Group(
            Select(
                id="category_select",
                items=CATEGORY_ITEMS,
                item_id_getter=lambda item: item["id"],
                text=Format("{item[text]}"),
                on_click=on_category_selected,
                type_factory=str,
            ),
            width=2,
        ),
        Button(Const(common_btn.BACK), id="back_to_main", on_click=to_main_menu),
        state=UserCatalogue.select_category,
    )


def product_list_window() -> Window:
    return Window(
        Const(common_catalogue_msg.CATALOGUE_CATEGORY),
        Group(
            Select(
                id="product_select",
                items="products",
                item_id_getter=lambda item: str(item.id),
                text=Format("{item.name} — {item.price}₽"),
                on_click=on_view_product_clicked,
            ),
            Row(
                Button(
                    Const(common_btn.BACK), id="back", on_click=to_product_categories
                ),
            ),
            width=1,
        ),
        state=UserCatalogue.view_products,
        getter=get_products_data,
    )


def product_card_window() -> Window:
    return Window(
        Format(common_catalogue_msg.PRODUCT_CARD),
        # Row(
        #     Button(Const(common_btn.EDIT), id="update", on_click=...),
        # ),
        Button(Const(common_btn.BACK), id="back", on_click=to_product_list),
        state=UserCatalogue.view_single_product,
        getter=get_selected_product,
    )
