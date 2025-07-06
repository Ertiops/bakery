from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.pickup_address.admin.windows import (
    add_pickup_address_windows,
    confirm_delete_pickup_address_window,
    pickup_address_list_window,
    pickup_address_window,
    update_pickup_address_windows,
)

admin_pickup_address_dialog = Dialog(
    pickup_address_list_window(),
    *add_pickup_address_windows(),
    pickup_address_window(),
    *update_pickup_address_windows(),
    confirm_delete_pickup_address_window(),
)
