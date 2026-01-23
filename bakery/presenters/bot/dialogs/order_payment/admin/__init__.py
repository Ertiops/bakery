from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.order_payment.admin.windows import (
    create_admin_order_payment_windows,
)

admin_order_payment_dialog = Dialog(*create_admin_order_payment_windows())
