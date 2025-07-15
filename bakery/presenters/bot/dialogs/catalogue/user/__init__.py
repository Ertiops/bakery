from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.catalogue.user.windows import (
    product_card_window,
    product_list_window,
    select_category_window,
)

user_catalogue_dialog = Dialog(
    select_category_window(),
    product_list_window(),
    product_card_window(),
)
