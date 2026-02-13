from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.fake_users.admin.windows import (
    admin_fake_users_windows,
)

admin_fake_users_dialog = Dialog(*admin_fake_users_windows())
