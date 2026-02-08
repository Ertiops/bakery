from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.blacklist.admin.windows import (
    admin_blacklist_windows,
)

admin_blacklist_dialog = Dialog(*admin_blacklist_windows())

__all__ = ["admin_blacklist_dialog"]
