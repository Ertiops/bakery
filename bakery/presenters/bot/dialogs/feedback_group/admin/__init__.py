from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.feedback_group.admin.windows import (
    create_admin_feedback_group_windows,
)

admin_feedback_group_dialog = Dialog(*create_admin_feedback_group_windows())
