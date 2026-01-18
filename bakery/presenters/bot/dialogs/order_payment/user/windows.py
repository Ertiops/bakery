from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.dialogs.order.user.redirections import (
    to_main_menu_from_order,
)
from bakery.presenters.bot.dialogs.order_payment.user.getters import (
    get_order_payment_data,
)
from bakery.presenters.bot.dialogs.order_payment.user.handlers import (
    back_to_previous_dialog,
    on_payment_file_received,
    to_payment_finish,
)
from bakery.presenters.bot.dialogs.order_payment.user.redirections import (
    to_order_categories,
)
from bakery.presenters.bot.dialogs.states import UserOrderPayment


def create_order_payment_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const("💳 Оплата заказа\n\n"),
                Format("🧾 Заказ {number}\n\n", when="has_order"),
                Format(
                    "Отправьте сумму <b>{total_price}₽</b>\n"
                    "по номеру <b>{phone}</b>\n"
                    "в банк <b>{bank}</b>\n"
                    "получателю <b>{addressee}</b>\n\n",
                    when="has_requisites",
                ),
                Const(
                    "❗ Реквизиты оплаты пока не настроены.\nНапишите администратору.",
                    when=lambda d, *_: d.get("has_order")
                    and not d.get("has_requisites"),
                ),
                Const("Заказ не найден 😔", when=lambda d, *_: not d.get("has_order")),
            ),
            Row(
                Button(
                    Const(common_btn.BACK), id="back", on_click=back_to_previous_dialog
                ),
                Button(
                    Const("📎 Прикрепить чек"),
                    id="to_file",
                    on_click=lambda c, b, m: m.switch_to(UserOrderPayment.add_file),
                    when=lambda d, *_: d.get("has_order") and d.get("has_requisites"),
                ),
            ),
            state=UserOrderPayment.show_order_payment,
            getter=get_order_payment_data,
        ),
        Window(
            Multi(
                Const("📎 Прикрепите чек/скрин оплаты\n\n"),
                Const("Подойдёт фото или PDF.\n"),
                Const("\nОтправьте файл одним сообщением 👇"),
            ),
            MessageInput(
                on_payment_file_received,
                content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_pay",
                    on_click=lambda c, b, m: m.switch_to(
                        UserOrderPayment.show_order_payment
                    ),
                ),
            ),
            state=UserOrderPayment.add_file,
            getter=get_order_payment_data,
        ),
        Window(
            DynamicMedia(
                "payment_file_attachment",
                when=lambda d, *_: d.get("payment_file_attachment"),
            ),
            Multi(
                Format("🧾 Заказ {number}\n"),
                Format("💰 Сумма: {total_price}₽\n\n"),
                Const(
                    "Файл не прикреплён 😔",
                    when=lambda d, *_: not d.get("has_payment_file"),
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_file",
                    on_click=lambda c, b, m: m.switch_to(UserOrderPayment.add_file),
                ),
                Button(
                    Const("✅ Подтвердить"),
                    id="confirm",
                    on_click=to_payment_finish,
                    when="has_payment_file",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
            ),
            state=UserOrderPayment.confirm,
            getter=get_order_payment_data,
        ),
        Window(
            Multi(
                Const("✅ Спасибо!\n\n"),
                Const("Мы получили ваше подтверждение оплаты.\n"),
            ),
            Row(
                Button(
                    Const("📦 К заказам"), id="to_orders", on_click=to_order_categories
                ),
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
            ),
            state=UserOrderPayment.finish,
        ),
    ]
