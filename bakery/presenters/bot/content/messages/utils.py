from typing import Final

from bakery.presenters.bot.content.buttons.main_menu import admin as admin_menu_btn
from bakery.presenters.bot.content.buttons.main_menu import user as user_menu_btn

USER_HELP: Final = "\n".join(
    [
        f"<b>{user_menu_btn.MAKE_ORDER}</b> — оформите заказ",
        f"<b>{user_menu_btn.CATALOGUE}</b> — ознакомьтесь с ассортиментом",
        f"<b>{user_menu_btn.MY_ORDERS}</b> — просмотр текущих заказов",
        f"<b>{user_menu_btn.HELP}</b> — контакт администратора",
    ]
)

ADMIN_HELP: Final = "\n".join(
    [
        f"<b>{admin_menu_btn.CATALOGUE}</b> — редактирование ассортимента",
        f"<b>{admin_menu_btn.ORDERS}</b> — управление заказами",
        f"<b>{admin_menu_btn.ADDRESSES}</b> — ведение адресами доставки",
        f"<b>{admin_menu_btn.CONTACTS}</b> — контакты администратора",
    ]
)
