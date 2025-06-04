from aiogram.types import ContentType
from aiogram_dialog import StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Group,
    Row,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const

from bakery.presenters.bot.content.buttons import (
    common as common_btn,
)
from bakery.presenters.bot.content.messages.registration import (
    main_menu as main_menu_msg,
)
from bakery.presenters.bot.content.messages.registration import user as user_msg
from bakery.presenters.bot.dialogs.registration.user.handlers import (
    name_input_handler,
    on_phone_input,
)
from bakery.presenters.bot.dialogs.states import (
    RegistrationMenu,
)


def accept_policy_window() -> Window:
    return Window(
        Const(main_menu_msg.USER_FAQ_ACCEPTANCE),
        Group(
            Row(
                SwitchTo(
                    Const(common_btn.NEXT),
                    id="accept_policy",
                    state=RegistrationMenu.start,
                ),
            ),
        ),
        state=RegistrationMenu.personal_data_accept,
    )


def start_registration_window() -> Window:
    return Window(
        Const(main_menu_msg.REGISTRATION_START),
        Group(
            Row(
                Start(
                    Const(common_btn.NEXT),
                    id="start_registration",
                    state=RegistrationMenu.name_input,
                    mode=StartMode.RESET_STACK,
                ),
            ),
        ),
        state=RegistrationMenu.start,
    )


def name_input_window() -> Window:
    return Window(
        Const(user_msg.NAME_INPUT),
        MessageInput(name_input_handler, content_types=ContentType.TEXT),
        Group(
            Row(
                Start(
                    Const(common_btn.BACK),
                    id="name_input",
                    state=RegistrationMenu.name_input,
                    mode=StartMode.RESET_STACK,
                ),
            ),
        ),
        state=RegistrationMenu.name_input,
    )


def phone_share_window() -> Window:
    return Window(
        Const(user_msg.PHONE_SHARE_WAITING),
        MessageInput(
            on_phone_input,
            content_types=(ContentType.CONTACT, ContentType.TEXT),
        ),
        state=RegistrationMenu.phone_share,
    )
