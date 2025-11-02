from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.admin_contact import (
    admin as admin_contact_msg,
)
from bakery.presenters.bot.dialogs.admin_contact.user.getters import (
    get_admin_contact_data,
)
from bakery.presenters.bot.dialogs.main_menu.user.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import UserAdminContact


def admin_contact_window() -> Window:
    return Window(
        Format(admin_contact_msg.CONTACT),
        Button(
            Const(common_btn.BACK),
            id="back",
            on_click=to_main_menu,
        ),
        state=UserAdminContact.view_one,
        getter=get_admin_contact_data,
    )
