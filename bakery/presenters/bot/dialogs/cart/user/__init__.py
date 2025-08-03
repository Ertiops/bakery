from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.cart.user.windows import (
    cart_window,
)

user_cart_dialog = Dialog(
    cart_window(),
)
