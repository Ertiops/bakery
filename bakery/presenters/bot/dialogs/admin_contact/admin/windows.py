from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.admin_contact import (
    admin as admin_contact_msg,
)
from bakery.presenters.bot.dialogs.admin_contact.admin.getters import (
    get_admin_contact_data,
    get_admin_contact_preview_data,
)
from bakery.presenters.bot.dialogs.admin_contact.admin.handlers import (
    on_cancel_creation,
    on_cancel_update,
    on_create,
    on_create_name_input,
    on_create_tg_username_input,
    on_update,
    on_update_name_input,
    on_update_tg_username_input,
)
from bakery.presenters.bot.dialogs.admin_contact.admin.redirections import (
    to_creation,
    to_update,
)
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import AdminContact


def admin_contact_window() -> Window:
    return Window(
        Format(admin_contact_msg.CONTACT),
        Row(
            Button(
                Const(common_btn.EDIT),
                id="edit",
                on_click=to_update,
            ),
        ),
        Row(
            Button(
                Const(common_btn.BACK),
                id="back",
                on_click=to_main_menu,
            ),
        ),
        state=AdminContact.view_one,
        getter=get_admin_contact_data,
    )


def add_admin_contact_choice_window() -> Window:
    return Window(
        Format(admin_contact_msg.CHOICE_MESSAGE),
        Row(
            Button(
                Const(common_btn.CREATE),
                id="create",
                on_click=to_creation,
            ),
            Button(
                Const(common_btn.BACK),
                id="back",
                on_click=to_main_menu,
            ),
        ),
        state=AdminContact.add_choice,
    )


def add_admin_contact_windows() -> list[Window]:
    return [
        Window(
            Const(admin_contact_msg.NAME_INPUT),
            MessageInput(on_create_name_input, content_types=[ContentType.TEXT]),
            state=AdminContact.add_name,
        ),
        Window(
            Const(admin_contact_msg.TG_USERNAME_INPUT),
            MessageInput(
                on_create_tg_username_input,
                content_types=[ContentType.TEXT],
            ),
            state=AdminContact.add_tg_username,
        ),
        Window(
            Format(admin_contact_msg.ADD_PREVIEW),
            Row(
                Button(Const(common_btn.CREATE), id="create", on_click=on_create),
                Button(
                    Const(common_btn.CANCEL),
                    id="cancel",
                    on_click=on_cancel_creation,
                ),
            ),
            state=AdminContact.add_confirm,
            getter=get_admin_contact_preview_data,
        ),
    ]


def update_admin_contact_windows() -> list[Window]:
    return [
        Window(
            Const(admin_contact_msg.NAME_INPUT),
            MessageInput(on_update_name_input, content_types=[ContentType.TEXT]),
            state=AdminContact.update_name,
        ),
        Window(
            Const(admin_contact_msg.TG_USERNAME_INPUT),
            MessageInput(
                on_update_tg_username_input,
                content_types=[ContentType.TEXT],
            ),
            state=AdminContact.update_tg_username,
        ),
        Window(
            Format(admin_contact_msg.UPDATE_PREVIEW),
            Row(
                Button(Const(common_btn.UPDATE), id="create", on_click=on_update),
                Button(
                    Const(common_btn.CANCEL),
                    id="cancel",
                    on_click=on_cancel_update,
                ),
            ),
            state=AdminContact.update_confirm,
            getter=get_admin_contact_preview_data,
        ),
    ]
