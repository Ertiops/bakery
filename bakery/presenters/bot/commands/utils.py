import logging
from enum import StrEnum

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, Message
from aiogram_dialog import DialogManager

from bakery.domains.entities.user import User, UserRole
from bakery.presenters.bot.dialogs.redirections import (
    start_menu_registration,
    start_menu_user,
)

log = logging.getLogger(__name__)


class Commands(StrEnum):
    START = "start"
    HELP = "help"


async def set_ui_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command=Commands.START, description="Начать работу с ботом"),
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
    if user is None:
        await start_menu_registration(dialog_manager=dialog_manager)
    elif user and user.role == UserRole.USER:
        await start_menu(user, dialog_manager)


async def start_menu(user: User, dialog_manager: DialogManager) -> None:
    if user.role == UserRole.USER:
        await start_menu_user(dialog_manager=dialog_manager)
