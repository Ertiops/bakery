from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import TelegramObject
from aiogram.types import User as TGUser
from dishka import AsyncContainer

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.user import User, UserRole
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow


class UserMiddleware(BaseMiddleware):
    container: AsyncContainer

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: TGUser = data["event_from_user"]
        if not hasattr(self, "container"):
            self.container: AsyncContainer = data["dishka_container"]
        uow: AbstractUow = await self.container.get(AbstractUow)
        async with uow:
            try:
                user_service: UserService = await self.container.get(UserService)
                data["current_user"] = await user_service.get_by_tg_id(input_id=user.id)
            except EntityNotFoundException:
                data["current_user"] = None
        current_user: User | None = data.get("current_user")
        if current_user and current_user.exclusion_reason:
            bot = data.get("bot")
            if bot:
                message = getattr(event, "message", None)
                if message and getattr(message, "message_id", None):
                    try:
                        await bot.delete_message(
                            chat_id=message.chat.id,
                            message_id=message.message_id,
                        )
                    except TelegramBadRequest:
                        pass
                await bot.send_message(
                    chat_id=user.id,
                    text="⛔ Вы находитесь в черном списке.",
                )
            state = data.get("state")
            if state:
                await state.clear()
            return None
        return await handler(event, data)


class UserRoleMiddleware(BaseMiddleware):
    accessed_roles: Sequence[UserRole]

    def __init__(self, accessed_roles: Sequence[UserRole]) -> None:
        super().__init__()
        self.accessed_roles = accessed_roles

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        current_user: User | None = data.get("current_user")
        if current_user and current_user.role in self.accessed_roles:
            return await handler(event, data)
