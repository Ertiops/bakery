from typing import Final

from bakery.presenters.bot.content.buttons.main_menu import user as user_menu_btn

USER_HELP: Final = "\n".join(
    [
        f"<b>{user_menu_btn.MAKE_ORDER}</b> — оформите заказ",
        f"<b>{user_menu_btn.CATALOGUE}</b> — ознакомьтесь с ассортиментом",
        f"<b>{user_menu_btn.MY_ORDERS}</b> — просмотр текущих заказов",
        f"<b>{user_menu_btn.HELP}</b> — контакт администратора",
    ]
)


ADMIN_GREETING: Final = "Здравствуйте, {name}!"
