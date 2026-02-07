from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.order.admin.windows import admin_orders_windows

admin_order_dialog = Dialog(*admin_orders_windows())
