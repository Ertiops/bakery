from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.order_schedule.admin.windows import (
    admin_order_schedule_windows,
)

admin_order_schedule_dialog = Dialog(*admin_order_schedule_windows())
