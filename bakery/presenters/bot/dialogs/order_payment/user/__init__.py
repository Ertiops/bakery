from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.order_payment.user.windows import (
    create_order_payment_windows,
)

user_order_payment_dialog = Dialog(*create_order_payment_windows())
