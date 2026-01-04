from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.order.user.windows import create_order_windows

user_order_dialog = Dialog(
    *create_order_windows(),
)
