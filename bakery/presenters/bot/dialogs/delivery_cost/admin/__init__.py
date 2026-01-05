from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.delivery_cost.admin.windows import (
    admin_delivery_cost_windows,
)

admin_delivery_cost_dialog = Dialog(*admin_delivery_cost_windows())
