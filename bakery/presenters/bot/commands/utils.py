import logging
from enum import StrEnum

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, Message
from aiogram_dialog import DialogManager, StartMode

from bakery.application.constants.admin_contact import ABSENCE_MESSAGE_TTL
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.user import User, UserRole
from bakery.domains.services.admin_contact import AdminContactService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.utils import ADMIN_HELP, USER_HELP
from bakery.presenters.bot.dialogs.states import (
    AdminAdminContact,
    AdminMain,
    UserAdminContact,
    UserMain,
)
from bakery.presenters.bot.utils.delete_after import delete_after

log = logging.getLogger(__name__)


class Commands(StrEnum):
    START = "start"
    HELP = "help"
    CONTACT = "contact"


async def set_ui_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command=Commands.START, description="Начать работу с ботом"),
        BotCommand(command=Commands.CONTACT, description="Контaкты"),
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
    if not user:
        return
    match user.role:
        case UserRole.USER:
            await dialog_manager.start(UserMain.menu)
        case UserRole.ADMIN:
            await dialog_manager.start(AdminMain.menu)
    await message.delete()


async def help_command(message: Message, dialog_manager: DialogManager) -> None:
    if not message.from_user:
        return
    user: User | None = dialog_manager.middleware_data["current_user"]
    if not user:
        return
    match user.role:
        case UserRole.USER:
            await message.answer(USER_HELP)
        case UserRole.ADMIN:
            await message.answer(ADMIN_HELP)
    await message.delete()


async def contact_command(message: Message, dialog_manager: DialogManager) -> None:
    if not message.from_user:
        return
    user: User | None = dialog_manager.middleware_data["current_user"]
    if not user:
        return
    container = dialog_manager.middleware_data["dishka_container"]
    service: AdminContactService = await container.get(AdminContactService)
    uow: AbstractUow = await container.get(AbstractUow)
    try:
        async with uow:
            admin_contact = await service.get_last()
    except EntityNotFoundException:
        message = await message.answer("Пока нет контактов администратора")
        await delete_after(message=message, ttl=ABSENCE_MESSAGE_TTL)
        return
    match user.role:
        case UserRole.USER:
            await dialog_manager.start(
                state=UserAdminContact.view_one,
                mode=StartMode.RESET_STACK,
                data=dict(
                    contact_id=str(admin_contact.id),
                    name=admin_contact.name,
                    tg_username=admin_contact.tg_username,
                ),
            )
        case UserRole.ADMIN:
            await dialog_manager.start(
                state=AdminAdminContact.view_one,
                mode=StartMode.RESET_STACK,
                data=dict(
                    contact_id=str(admin_contact.id),
                    name=admin_contact.name,
                    tg_username=admin_contact.tg_username,
                ),
            )
