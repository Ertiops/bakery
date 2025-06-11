from aiogram_dialog import DialogManager, StartMode

from bakery.presenters.bot.dialogs.states import RegistrationMenu


async def start_new_dialog(
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(
        RegistrationMenu.personal_data_accept,
        mode=StartMode.RESET_STACK,
    )


async def start_menu_registration(dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=RegistrationMenu.personal_data_accept,
        mode=StartMode.RESET_STACK,
    )
