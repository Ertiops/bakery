from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.catalogue.admin.windows import (
    add_product_windows,
    list_products_window,
    product_card_window,
    select_category_window,
)

admin_catalogue_dialog = Dialog(
    select_category_window(),
    list_products_window(),
    *add_product_windows(),
    product_card_window(),
)
