from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.admin_contact.user.windows import (
    admin_contact_window,
)

user_admin_contact_dialog = Dialog(
    admin_contact_window(),
)
