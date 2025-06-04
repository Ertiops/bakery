import re

from aiogram.types import (
    Message,
)
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from bakery.domains.entities.user import CreateUser, UserRole
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.registration import (
    main_menu as main_menu_msg,
)
from bakery.presenters.bot.content.messages.registration import (
    user as user_msg,
)
from bakery.presenters.bot.dialogs.registration.user.keyboards import get_share_phone_kb
from bakery.presenters.bot.dialogs.states import (
    RegistrationMenu,
)


async def name_input_handler(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    if not message.text:
        return
    if re.match(r"^[A-ZА-ЯЁ][^0-9]*$", message.text):
        dialog_manager.dialog_data["name"] = message.text
    else:
        await message.answer(user_msg.NAME_INPUT_INVALID)
        return
    await message.answer(user_msg.PHONE_SHARE, reply_markup=get_share_phone_kb())
    await dialog_manager.switch_to(RegistrationMenu.phone_share)


async def on_phone_input(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
) -> None:
    if not message.contact or not message.contact.phone_number:
        await message.answer(
            user_msg.PHONE_SHARE_INVALID, reply_markup=get_share_phone_kb()
        )
        return
    service: UserService = await dialog_manager.middleware_data["dishka_container"].get(
        UserService
    )
    uow: AbstractUow = await dialog_manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    async with uow:
        await service.create(
            input_dto=CreateUser(
                name=dialog_manager.dialog_data["name"],
                tg_id=message.from_user.id,  # type: ignore[union-attr]
                phone=message.contact.phone_number,
                role=UserRole.USER,
            )
        )
    await message.answer(main_menu_msg.REGISTRATION_FINISH, reply_markup=None)
    await dialog_manager.done()
