from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
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
    admin_order_payment_start_create,
    admin_order_payment_start_update,
)
from bakery.presenters.bot.dialogs.states import AdminOrderPayment


def create_admin_order_payment_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const("💳 Реквизиты для оплаты\n\n"),
                Const(
                    "Реквизиты не настроены.\n",
                    when=lambda d, *_: not d["has_order_payment"],
                ),
                Multi(
                    Format("📞 Номер: <b>{phone}</b>\n"),
                    Format("🏦 Банк: <b>{bank}</b>\n"),
                    Format("👤 Получатель: <b>{addressee}</b>\n"),
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
                Const("Введите номер телефона для оплаты\n\n"),
                Format("Текущее: <b>{phone}</b>\n\n", when="has_phone"),
                Const("Отправьте сообщением 👇"),
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
            ),
            state=AdminOrderPayment.phone,
            getter=get_admin_order_payment_edit_data,
        ),
        Window(
            Multi(
                Const("Введите банк\n\n"),
                Format("Текущее: <b>{bank}</b>\n\n", when="has_bank"),
                Const("Отправьте сообщением 👇"),
            ),
            MessageInput(admin_order_payment_on_bank, content_types=[ContentType.TEXT]),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminOrderPayment.phone),
                ),
            ),
            state=AdminOrderPayment.bank,
            getter=get_admin_order_payment_edit_data,
        ),
        Window(
            Multi(
                Const("Введите получателя\n\n"),
                Format("Текущее: <b>{addressee}</b>\n\n", when="has_addressee"),
                Const("Отправьте сообщением 👇"),
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
            ),
            state=AdminOrderPayment.addressee,
            getter=get_admin_order_payment_edit_data,
        ),
        Window(
            Multi(
                Const("✅ Подтверждение\n\n"),
                Format("📞 Номер: <b>{phone}</b>\n"),
                Format("🏦 Банк: <b>{bank}</b>\n"),
                Format("👤 Получатель: <b>{addressee}</b>\n\n"),
                Format("Режим: <b>{mode}</b>\n"),
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
