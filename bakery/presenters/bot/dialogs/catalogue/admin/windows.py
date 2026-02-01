from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Group,
    Row,
    Select,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.catalogue import (
    admin as admin_catalogue_msg,
)
from bakery.presenters.bot.content.messages.catalogue import (
    common as common_catalogue_msg,
)
from bakery.presenters.bot.dialogs.catalogue.admin.getters import (
    get_product_preview_data,
    get_products_data,
    get_selected_product,
)
from bakery.presenters.bot.dialogs.catalogue.admin.handlers import (
    go_to_confirm_delete,
    on_add_clicked,
    on_cancel_delete,
    on_cancel_product_creation,
    on_cancel_update,
    on_confirm_delete,
    on_create_product,
    on_description_input,
    on_name_input,
    on_photo_input,
    on_price_input,
    on_skip_description,
    on_skip_name,
    on_skip_price,
    on_skip_update_photo,
    on_update_clicked,
    on_update_description_input,
    on_update_name_input,
    on_update_photo_input,
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
        state=AdminCatalogue.select_category,
    )


def list_products_window() -> Window:
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
            Const(admin_catalogue_msg.PHOTO_INPUT),
            Const(admin_catalogue_msg.PHOTO_INPUT_HINT),
            MessageInput(on_photo_input, content_types=[ContentType.PHOTO]),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminCatalogue.add_price),
                ),
            ),
            state=AdminCatalogue.add_photo,
        ),
        Window(
            Format(admin_catalogue_msg.ADD_PRODUCT_PREVIEW),
            DynamicMedia(
                "product_preview_attachment",
                when=lambda d, *_: d.get("product_preview_attachment"),
            ),
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
        DynamicMedia(
            "product_photo_attachment",
            when=lambda d, *_: d.get("product_photo_attachment"),
        ),
        Format(common_catalogue_msg.PRODUCT_CARD),
        Row(
            Button(Const(common_btn.EDIT), id="update", on_click=on_update_clicked),
            Button(
                Const(common_btn.DELETE), id="delete", on_click=go_to_confirm_delete
            ),
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
            Const(admin_catalogue_msg.PHOTO_INPUT),
            Const(admin_catalogue_msg.UPDATE_PHOTO_INPUT_HINT),
            MessageInput(on_update_photo_input, content_types=[ContentType.PHOTO]),
            Row(
                Button(
                    Const(common_btn.SKIP),
                    id="skip_photo",
                    on_click=on_skip_update_photo,
                ),
            ),
            state=AdminCatalogue.update_photo,
            getter=get_selected_product,
        ),
        Window(
            Format(admin_catalogue_msg.UPDATE_PRODUCT_PREVIEW),
            DynamicMedia(
                "product_preview_attachment",
                when=lambda d, *_: d.get("product_preview_attachment"),
            ),
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


def confirm_delete_product_window() -> Window:
    return Window(
        Const(admin_catalogue_msg.CONFIRM_DELETE),
        Row(
            Button(Const(common_btn.YES), id="confirm", on_click=on_confirm_delete),
            Button(Const(common_btn.CANCEL), id="cancel", on_click=on_cancel_delete),
        ),
        state=AdminCatalogue.confirm_delete,
    )
