from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.catalogue.admin.windows import (
    add_product_windows,
    confirm_delete_product_window,
    list_products_window,
    product_card_window,
    select_category_window,
    update_product_windows,
)

admin_catalogue_dialog = Dialog(
    select_category_window(),
    list_products_window(),
    *add_product_windows(),
    product_card_window(),
    *update_product_windows(),
    confirm_delete_product_window(),
)
