from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Url
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.order_payment import (
    user as order_payment_user_msg,
)
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
                Const(order_payment_user_msg.TITLE),
                Format(order_payment_user_msg.ORDER_NUMBER, when="has_order"),
                Format(
                    order_payment_user_msg.PAYMENT_DETAILS,
                    when="has_requisites",
                ),
                Const(
                    order_payment_user_msg.REQUISITES_NOT_SET,
                    when=lambda d, *_: d.get("has_order")
                    and not d.get("has_requisites"),
                ),
                Const(
                    order_payment_user_msg.ORDER_NOT_FOUND,
                    when=lambda d, *_: not d.get("has_order"),
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK), id="back", on_click=back_to_previous_dialog
                ),
                Button(
                    Const(order_payment_user_msg.BTN_ATTACH_CHECK),
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
                Const(order_payment_user_msg.ATTACH_FILE_TITLE),
                Const(order_payment_user_msg.ATTACH_FILE_HINT),
                Const(order_payment_user_msg.ATTACH_FILE_ACTION),
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
                Format(order_payment_user_msg.CONFIRM_ORDER_NUMBER),
                Format(order_payment_user_msg.CONFIRM_TOTAL),
                Const(
                    order_payment_user_msg.CONFIRM_NO_FILE,
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
                    Const(order_payment_user_msg.BTN_CONFIRM),
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
                Const(order_payment_user_msg.FINISH_TITLE),
                Const(order_payment_user_msg.FINISH_BODY),
            ),
            Url(
                Const(order_payment_user_msg.BTN_FEEDBACK_GROUP),
                url=Format("{feedback_group_url}"),
                when="has_feedback_group",
            ),
            Row(
                Button(
                    Const(order_payment_user_msg.BTN_TO_ORDERS),
                    id="to_orders",
                    on_click=to_order_categories,
                ),
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
            ),
            state=UserOrderPayment.finish,
            getter=get_order_payment_data,
        ),
    ]
