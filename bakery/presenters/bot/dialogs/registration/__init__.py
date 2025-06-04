from aiogram_dialog import Dialog

from bakery.presenters.bot.dialogs.registration.user import (
    windows as user_register_windows,
)

user_registration_dialog = Dialog(
    user_register_windows.accept_policy_window(),
    user_register_windows.start_registration_window(),
    user_register_windows.name_input_window(),
    user_register_windows.phone_share_window(),
)
