from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Row,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.catalogue import (
    admin as admin_catalogue_msg,
)
from bakery.presenters.bot.content.messages.catalogue import (
    common as catalogue_common_msg,
)
from bakery.presenters.bot.dialogs.catalogue.admin.getters import (
    get_product_preview_data,
    get_products_data,
    get_selected_product,
)
from bakery.presenters.bot.dialogs.catalogue.admin.handlers import (
    on_add_clicked,
    on_cancel_product_creation,
    on_cancel_update,
    on_create_product,
    on_delete_clicked,
    on_description_input,
    on_name_input,
    on_price_input,
    on_skip_description,
    on_skip_name,
    on_skip_price,
    on_update_clicked,
    on_update_description_input,
    on_update_name_input,
    on_update_price_input,
    on_update_product,
    on_view_product_clicked,
)
from bakery.presenters.bot.dialogs.catalogue.admin.redirections import (
    to_product_categories,
    to_product_list,
)
from bakery.presenters.bot.dialogs.catalogue.admin.selections import (
    on_category_selected,
)
from bakery.presenters.bot.dialogs.catalogue.windows import CATEGORY_ITEMS
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import AdminCatalogue


def select_category_window() -> Window:
    return Window(
        Const(catalogue_common_msg.CATALOGUE_CATEGORY_SELECTION),
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
        state=AdminCatalogue.select_category,
    )


def list_products_window() -> Window:
    return Window(
        Const(catalogue_common_msg.CATALOGUE_CATEGORY),
        Group(
            Select(
                id="product_select",
                items="products",
                item_id_getter=lambda item: str(item.id),
                text=Format("{item.name} — {item.price}₽"),
                on_click=on_view_product_clicked,
            ),
            Row(
                Button(Const(common_btn.ADD), id="add", on_click=on_add_clicked),
                Button(
                    Const(common_btn.BACK), id="back", on_click=to_product_categories
                ),
            ),
            width=1,
        ),
        state=AdminCatalogue.view_products,
        getter=get_products_data,
    )


def add_product_windows() -> list[Window]:
    return [
        Window(
            Const(admin_catalogue_msg.NAME_INPUT),
            MessageInput(on_name_input),
            state=AdminCatalogue.add_name,
        ),
        Window(
            Const(admin_catalogue_msg.DESCRIPTION_INPUT),
            MessageInput(on_description_input),
            state=AdminCatalogue.add_description,
        ),
        Window(
            Const(admin_catalogue_msg.PRICE_INPUT),
            MessageInput(on_price_input),
            state=AdminCatalogue.add_price,
        ),
        Window(
            Format(admin_catalogue_msg.ADD_PRODUCT_PREVIEW),
            Row(
                Button(
                    Const(common_btn.CREATE), id="create", on_click=on_create_product
                ),
                Button(
                    Const(common_btn.CANCEL),
                    id="cancel",
                    on_click=on_cancel_product_creation,
                ),
            ),
            state=AdminCatalogue.add_confirm,
            getter=get_product_preview_data,
        ),
    ]


def product_card_window() -> Window:
    return Window(
        Format(admin_catalogue_msg.PRODUCT_CARD),
        Row(
            Button(Const(common_btn.EDIT), id="update", on_click=on_update_clicked),
            Button(Const(common_btn.DELETE), id="delete", on_click=on_delete_clicked),
        ),
        Button(Const(common_btn.BACK), id="back", on_click=to_product_list),
        state=AdminCatalogue.view_single_product,
        getter=get_selected_product,
    )


def update_product_windows() -> list[Window]:
    return [
        Window(
            Const(admin_catalogue_msg.NAME_INPUT),
            MessageInput(on_update_name_input),
            Row(
                Button(Const(common_btn.SKIP), id="skip_name", on_click=on_skip_name),
            ),
            state=AdminCatalogue.update_name,
            getter=get_selected_product,
        ),
        Window(
            Const(admin_catalogue_msg.DESCRIPTION_INPUT),
            MessageInput(on_update_description_input),
            Row(
                Button(
                    Const(common_btn.SKIP),
                    id="skip_description",
                    on_click=on_skip_description,
                ),
            ),
            state=AdminCatalogue.update_description,
            getter=get_selected_product,
        ),
        Window(
            Const(admin_catalogue_msg.PRICE_INPUT),
            MessageInput(on_update_price_input),
            Row(
                Button(Const(common_btn.SKIP), id="skip_price", on_click=on_skip_price),
            ),
            state=AdminCatalogue.update_price,
            getter=get_selected_product,
        ),
        Window(
            Format(admin_catalogue_msg.UPDATE_PRODUCT_PREVIEW),
            Row(
                Button(Const(common_btn.SAVE), id="save", on_click=on_update_product),
                Button(
                    Const(common_btn.CANCEL), id="cancel", on_click=on_cancel_update
                ),
            ),
            state=AdminCatalogue.update_confirm,
            getter=get_product_preview_data,
        ),
    ]
