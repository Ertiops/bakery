from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Select
from aiogram_dialog.widgets.text import Const, Format

from bakery.domains.entities.product import ProductCategory
from bakery.presenters.bot.content.buttons.catalogue import common as category_btn
from bakery.presenters.bot.content.messages.catalogue import (
    common as catalogue_common_msg,
)
from bakery.presenters.bot.dialogs.catalogue.admin.selections import (
    on_category_selected,
)
from bakery.presenters.bot.dialogs.states import AdminCatalogue


def select_category_window() -> Window:
    return Window(
        Const(catalogue_common_msg.CATALOGUE_CATEGORY_SELECTION),
        Group(
            Select(
                id="category_select",
                items=[
                    dict(id=ProductCategory.BREAD, text=category_btn.BREAD),
                    dict(id=ProductCategory.OIL, text=category_btn.OIL),
                    dict(id=ProductCategory.FLOUR, text=category_btn.FLOUR),
                    dict(id=ProductCategory.SNACK, text=category_btn.SNACK),
                    dict(id=ProductCategory.OTHER, text=category_btn.OTHER),
                ],
                item_id_getter=lambda item: item["id"],
                text=Format("{item[text]}"),
                on_click=on_category_selected,
                type_factory=str,
            ),
            width=1,
        ),
        state=AdminCatalogue.select_category,
    )
