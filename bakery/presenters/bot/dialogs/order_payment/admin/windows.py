from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.order_payment import (
    admin as order_payment_admin_msg,
)
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.order_payment.admin.getters import (
    get_admin_order_payment_edit_data,
    get_admin_order_payment_view_data,
)
from bakery.presenters.bot.dialogs.order_payment.admin.handlers import (
    admin_order_payment_back_to_view,
    admin_order_payment_on_addressee,
    admin_order_payment_on_bank,
    admin_order_payment_on_phone,
    admin_order_payment_save,
    admin_order_payment_skip_addressee,
    admin_order_payment_skip_bank,
    admin_order_payment_skip_phone,
    admin_order_payment_start_create,
    admin_order_payment_start_update,
)
from bakery.presenters.bot.dialogs.states import AdminOrderPayment


def create_admin_order_payment_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const(order_payment_admin_msg.TITLE),
                Const(
                    order_payment_admin_msg.NOT_CONFIGURED,
                    when=lambda d, *_: not d["has_order_payment"],
                ),
                Multi(
                    Format(order_payment_admin_msg.VIEW_PHONE),
                    Format(order_payment_admin_msg.VIEW_BANK),
                    Format(order_payment_admin_msg.VIEW_ADDRESSEE),
                    when="has_order_payment",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.CREATE),
                    id="create",
                    on_click=admin_order_payment_start_create,
                    when=lambda d, *_: not d["has_order_payment"],
                ),
                Button(
                    Const(common_btn.UPDATE),
                    id="update",
                    on_click=admin_order_payment_start_update,
                    when="has_order_payment",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=to_main_menu,
                ),
            ),
            state=AdminOrderPayment.view,
            getter=get_admin_order_payment_view_data,
        ),
        Window(
            Multi(
                Const(order_payment_admin_msg.PHONE_INPUT),
                Format(order_payment_admin_msg.PHONE_CURRENT, when="has_phone"),
                Const(order_payment_admin_msg.INPUT_HINT),
            ),
            MessageInput(
                admin_order_payment_on_phone, content_types=[ContentType.TEXT]
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=admin_order_payment_back_to_view,
                ),
                Button(
                    Const(common_btn.SKIP),
                    id="skip",
                    on_click=admin_order_payment_skip_phone,
                    when="is_update",
                ),
            ),
            state=AdminOrderPayment.phone,
            getter=get_admin_order_payment_edit_data,
        ),
        Window(
            Multi(
                Const(order_payment_admin_msg.BANK_INPUT),
                Format(order_payment_admin_msg.BANK_CURRENT, when="has_bank"),
                Const(order_payment_admin_msg.INPUT_HINT),
            ),
            MessageInput(admin_order_payment_on_bank, content_types=[ContentType.TEXT]),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminOrderPayment.phone),
                ),
                Button(
                    Const(common_btn.SKIP),
                    id="skip",
                    on_click=admin_order_payment_skip_bank,
                    when="is_update",
                ),
            ),
            state=AdminOrderPayment.bank,
            getter=get_admin_order_payment_edit_data,
        ),
        Window(
            Multi(
                Const(order_payment_admin_msg.ADDRESSEE_INPUT),
                Format(order_payment_admin_msg.ADDRESSEE_CURRENT, when="has_addressee"),
                Const(order_payment_admin_msg.INPUT_HINT),
            ),
            MessageInput(
                admin_order_payment_on_addressee, content_types=[ContentType.TEXT]
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminOrderPayment.bank),
                ),
                Button(
                    Const(common_btn.SKIP),
                    id="skip",
                    on_click=admin_order_payment_skip_addressee,
                    when="is_update",
                ),
            ),
            state=AdminOrderPayment.addressee,
            getter=get_admin_order_payment_edit_data,
        ),
        Window(
            Multi(
                Const(order_payment_admin_msg.CONFIRM_TITLE),
                Format(order_payment_admin_msg.CONFIRM_PHONE),
                Format(order_payment_admin_msg.CONFIRM_BANK),
                Format(order_payment_admin_msg.CONFIRM_ADDRESSEE),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminOrderPayment.addressee),
                ),
                Button(
                    Const(common_btn.SAVE), id="save", on_click=admin_order_payment_save
                ),
            ),
            state=AdminOrderPayment.confirm,
            getter=get_admin_order_payment_edit_data,
        ),
    ]
