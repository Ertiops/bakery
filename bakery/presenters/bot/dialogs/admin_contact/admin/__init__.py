from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.admin_contact.admin.windows import (
    add_admin_contact_choice_window,
    add_admin_contact_windows,
    admin_contact_window,
    update_admin_contact_windows,
)

admin_admin_contact_dialog = Dialog(
    admin_contact_window(),
    add_admin_contact_choice_window(),
    *add_admin_contact_windows(),
    *update_admin_contact_windows(),
)
