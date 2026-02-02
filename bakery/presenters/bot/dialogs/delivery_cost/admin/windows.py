from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.delivery_cost import (
    admin as delivery_cost_msg,
)
from bakery.presenters.bot.dialogs.delivery_cost.admin.getters import (
    get_delivery_cost_data,
    get_delivery_cost_preview_data,
)
from bakery.presenters.bot.dialogs.delivery_cost.admin.handlers import (
    on_delivery_cost_cancel,
    on_delivery_cost_confirm_create,
    on_delivery_cost_confirm_update,
    on_delivery_cost_entered_create,
    on_delivery_cost_entered_update,
    on_free_delivery_amount_entered_create,
    on_free_delivery_amount_entered_update,
    to_create_delivery_cost,
    to_update_delivery_cost,
)
from bakery.presenters.bot.dialogs.delivery_cost.admin.redirections import (
    to_admin_main_menu,
)
from bakery.presenters.bot.dialogs.states import AdminDeliveryPrice


def admin_delivery_cost_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const(delivery_cost_msg.TITLE),
                Const(delivery_cost_msg.CURRENT_COST_LABEL),
                Format(
                    delivery_cost_msg.PRICE_FORMAT,
                    when=lambda d, *_: d.get("has_cost"),
                ),
                Const(delivery_cost_msg.CURRENT_FREE_DELIVERY_LABEL),
                Format(
                    delivery_cost_msg.FREE_DELIVERY_FORMAT,
                    when=lambda d, *_: d.get("has_free_delivery_amount"),
                ),
                Const(
                    delivery_cost_msg.NOT_SET,
                    when=lambda d, *_: not d.get("has_free_delivery_amount"),
                ),
            ),
            Row(
                Button(
                    Const(common_btn.CREATE),
                    id="create",
                    on_click=to_create_delivery_cost,
                    when=lambda d, *_: not d.get("has_cost"),
                ),
                Button(
                    Const(common_btn.UPDATE),
                    id="update",
                    on_click=to_update_delivery_cost,
                    when=lambda d, *_: d.get("has_cost"),
                ),
            ),
            Row(
                Button(Const(common_btn.BACK), id="back", on_click=to_admin_main_menu),
            ),
            state=AdminDeliveryPrice.view,
            getter=get_delivery_cost_data,
        ),
        Window(
            Const(delivery_cost_msg.CREATE_INPUT),
            TextInput(
                id="delivery_cost_create",
                type_factory=int,
                on_success=on_delivery_cost_entered_create,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminDeliveryPrice.view),
                ),
            ),
            state=AdminDeliveryPrice.create,
        ),
        Window(
            Const(delivery_cost_msg.CREATE_FREE_DELIVERY_INPUT),
            TextInput(
                id="delivery_cost_create_free_amount",
                type_factory=int,
                on_success=on_free_delivery_amount_entered_create,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminDeliveryPrice.create),
                ),
            ),
            state=AdminDeliveryPrice.create_free_amount,
        ),
        Window(
            Format(delivery_cost_msg.CREATE_CONFIRM),
            Row(
                Button(
                    Const(common_btn.CREATE),
                    id="create",
                    on_click=on_delivery_cost_confirm_create,
                ),
                Button(
                    Const(common_btn.CANCEL),
                    id="cancel",
                    on_click=on_delivery_cost_cancel,
                ),
            ),
            state=AdminDeliveryPrice.create_confirm,
            getter=get_delivery_cost_preview_data,
        ),
        Window(
            Const(delivery_cost_msg.UPDATE_INPUT),
            TextInput(
                id="delivery_cost_update",
                type_factory=int,
                on_success=on_delivery_cost_entered_update,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminDeliveryPrice.view),
                ),
                Button(
                    Const(common_btn.SKIP),
                    id="skip",
                    on_click=lambda c, b, m: m.switch_to(
                        AdminDeliveryPrice.update_free_amount
                    ),
                ),
            ),
            state=AdminDeliveryPrice.update,
            getter=get_delivery_cost_data,
        ),
        Window(
            Const(delivery_cost_msg.UPDATE_FREE_DELIVERY_INPUT),
            TextInput(
                id="delivery_cost_update_free_amount",
                type_factory=int,
                on_success=on_free_delivery_amount_entered_update,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminDeliveryPrice.update),
                ),
                Button(
                    Const(common_btn.SKIP),
                    id="skip",
                    on_click=lambda c, b, m: m.switch_to(AdminDeliveryPrice.view),
                ),
            ),
            state=AdminDeliveryPrice.update_free_amount,
            getter=get_delivery_cost_data,
        ),
        Window(
            Format(delivery_cost_msg.UPDATE_CONFIRM),
            Row(
                Button(
                    Const(common_btn.UPDATE),
                    id="update",
                    on_click=on_delivery_cost_confirm_update,
                ),
                Button(
                    Const(common_btn.CANCEL),
                    id="cancel",
                    on_click=on_delivery_cost_cancel,
                ),
            ),
            state=AdminDeliveryPrice.update_confirm,
            getter=get_delivery_cost_preview_data,
        ),
    ]
