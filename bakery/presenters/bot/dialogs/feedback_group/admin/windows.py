from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.feedback_group import (
    admin as feedback_group_msg,
)
from bakery.presenters.bot.dialogs.feedback_group.admin.getters import (
    get_admin_feedback_group_edit_data,
    get_admin_feedback_group_view_data,
)
from bakery.presenters.bot.dialogs.feedback_group.admin.handlers import (
    admin_feedback_group_back_to_view,
    admin_feedback_group_on_url_input,
    admin_feedback_group_save,
    admin_feedback_group_skip_url_input,
    admin_feedback_group_start_create,
    admin_feedback_group_start_update,
)
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import AdminFeedbackGroup


def create_admin_feedback_group_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const(feedback_group_msg.TITLE),
                Const(
                    feedback_group_msg.NOT_CONFIGURED,
                    when=lambda d, *_: not d["has_feedback_group"],
                ),
                Multi(
                    Format(feedback_group_msg.VIEW_URL),
                    when="has_feedback_group",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.CREATE),
                    id="create",
                    on_click=admin_feedback_group_start_create,
                    when=lambda d, *_: not d["has_feedback_group"],
                ),
                Button(
                    Const(common_btn.UPDATE),
                    id="update",
                    on_click=admin_feedback_group_start_update,
                    when="has_feedback_group",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=to_main_menu,
                ),
            ),
            state=AdminFeedbackGroup.view,
            getter=get_admin_feedback_group_view_data,
        ),
        Window(
            Multi(
                Const(feedback_group_msg.URL_INPUT),
                Format(feedback_group_msg.URL_CURRENT, when="has_url"),
                Const(feedback_group_msg.INPUT_HINT),
            ),
            MessageInput(
                admin_feedback_group_on_url_input, content_types=[ContentType.TEXT]
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=admin_feedback_group_back_to_view,
                ),
                Button(
                    Const(common_btn.SKIP),
                    id="skip",
                    on_click=admin_feedback_group_skip_url_input,
                    when="is_update",
                ),
            ),
            state=AdminFeedbackGroup.url,
            getter=get_admin_feedback_group_edit_data,
        ),
        Window(
            Multi(
                Const(feedback_group_msg.CONFIRM_TITLE),
                Format(feedback_group_msg.CONFIRM_URL),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminFeedbackGroup.url),
                ),
                Button(
                    Const(common_btn.SAVE),
                    id="save",
                    on_click=admin_feedback_group_save,
                ),
            ),
            state=AdminFeedbackGroup.confirm,
            getter=get_admin_feedback_group_edit_data,
        ),
    ]
