import logging
from enum import StrEnum

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, Message
from aiogram_dialog import DialogManager

from bakery.domains.entities.user import User, UserRole
from bakery.presenters.bot.content.messages.utils import ADMIN_GREETING, USER_HELP
from bakery.presenters.bot.dialogs.states import AdminMain
from bakery.presenters.bot.keyboards.main_menu import (
    get_user_main_menu_kb,
)

log = logging.getLogger(__name__)


class Commands(StrEnum):
    START = "start"
    HELP = "help"
    CONTACTS = "contacts"


async def set_ui_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command=Commands.START, description="Начать работу с ботом"),
        BotCommand(command=Commands.CONTACTS, description="Контaкты"),
        BotCommand(command=Commands.HELP, description="Помощь"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault(),
    )


async def start_command(message: Message, dialog_manager: DialogManager) -> None:
    if not message.from_user:
        return
    user: User | None = dialog_manager.middleware_data["current_user"]
    if user is None or user.role == UserRole.USER:
        await message.answer(USER_HELP, reply_markup=get_user_main_menu_kb())
    elif user and user.role == UserRole.ADMIN:
        await message.answer(ADMIN_GREETING.format(name=user.name))
        await dialog_manager.start(AdminMain.menu)


async def help_command(message: Message, dialog_manager: DialogManager) -> None:
    if not message.from_user:
        return
    user: User | None = dialog_manager.middleware_data["current_user"]
    if user is None or user.role == UserRole.USER:
        pass


# async def start_menu(user: User | None, dialog_manager: DialogManager) -> None:
#     if user.role == UserRole.ADMIN:
#         await start_menu_admin(dialog_manager=dialog_manager)
