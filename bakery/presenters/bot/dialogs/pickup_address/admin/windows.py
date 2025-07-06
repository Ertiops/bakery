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
from bakery.presenters.bot.content.messages.pickup_address import (
    admin as pickup_address_msg,
)
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.pickup_address.admin.getters import (
    get_pickup_address_list_data,
    get_pickup_address_preview_data,
    get_selected_pickup_address,
)
from bakery.presenters.bot.dialogs.pickup_address.admin.handlers import (
    go_to_confirm_delete,
    on_add_clicked,
    on_cancel_delete,
    on_confirm_delete,
    on_create_pickup_address,
    on_name_input,
    on_update_clicked,
    on_update_name_input,
    on_update_pickup_address,
    on_view_pickup_address_clicked,
)
from bakery.presenters.bot.dialogs.pickup_address.admin.redirections import (
    to_pickup_address_list,
)
from bakery.presenters.bot.dialogs.states import (
    AdminPickupAddress,
)


def pickup_address_list_window() -> Window:
    return Window(
        Const(pickup_address_msg.PICKUP_ADDRESS_SELECTION),
        Group(
            Select(
                id="pickup_address",
                items="pickup_addresses",
                item_id_getter=lambda item: str(item.id),
                text=Format("{item.name}"),
                on_click=on_view_pickup_address_clicked,
            ),
            Row(
                Button(Const(common_btn.ADD), id="add", on_click=on_add_clicked),
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=to_main_menu,
                ),
            ),
            width=1,
        ),
        state=AdminPickupAddress.view_all,
        getter=get_pickup_address_list_data,
    )


def add_pickup_address_windows() -> list[Window]:
    return [
        Window(
            Const(pickup_address_msg.NAME_INPUT),
            MessageInput(on_name_input),
            state=AdminPickupAddress.add_name,
        ),
        Window(
            Format(pickup_address_msg.ADD_PICKUP_ADDRESS_PREVIEW),
            Row(
                Button(
                    Const(common_btn.CREATE),
                    id="create",
                    on_click=on_create_pickup_address,
                ),
                Button(
                    Const(common_btn.CANCEL),
                    id="cancel",
                    on_click=to_pickup_address_list,
                ),
            ),
            state=AdminPickupAddress.add_confirm,
            getter=get_pickup_address_preview_data,
        ),
    ]


def pickup_address_window() -> Window:
    return Window(
        Format(pickup_address_msg.PICKUP_ADDRESS_CARD),
        Row(
            Button(Const(common_btn.EDIT), id="update", on_click=on_update_clicked),
            Button(
                Const(common_btn.DELETE), id="delete", on_click=go_to_confirm_delete
            ),
        ),
        Button(Const(common_btn.BACK), id="back", on_click=to_pickup_address_list),
        state=AdminPickupAddress.view_one,
        getter=get_selected_pickup_address,
    )


def update_pickup_address_windows() -> list[Window]:
    return [
        Window(
            Const(pickup_address_msg.NAME_INPUT),
            MessageInput(on_update_name_input),
            state=AdminPickupAddress.update_name,
        ),
        Window(
            Format(pickup_address_msg.UPDATE_PICKUP_ADDRESS_PREVIEW),
            Row(
                Button(
                    Const(common_btn.SAVE), id="save", on_click=on_update_pickup_address
                ),
                Button(
                    Const(common_btn.CANCEL),
                    id="cancel",
                    on_click=to_pickup_address_list,
                ),
            ),
            state=AdminPickupAddress.update_confirm,
            getter=get_pickup_address_preview_data,
        ),
    ]


def confirm_delete_pickup_address_window() -> Window:
    return Window(
        Const(pickup_address_msg.CONFIRM_DELETE_PICKUP_ADDRESS),
        Row(
            Button(Const(common_btn.YES), id="confirm", on_click=on_confirm_delete),
            Button(Const(common_btn.CANCEL), id="cancel", on_click=on_cancel_delete),
        ),
        state=AdminPickupAddress.confirm_delete,
    )
