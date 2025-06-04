# from aiogram import F, Router
# from aiogram.types import Message
# from aiogram_dialog import DialogManager, StartMode

# from bakery.application.exceptions import EntityNotFoundError
# from bakery.domains.entities.users import User
# from bakery.domains.services.users import UserService
# from bakery.presenters.bot.content.messages.super_admin import (
#     manage_users as manage_users_msg,
# )
# from bakery.presenters.bot.dialogs.states import SuperAdminMenu


# router = Router()


# @router.message(F.user_shared)
# async def handle_user_selectionasync(
#     message: Message,
#     dialog_manager: DialogManager,
# ) -> None:
#     if message.user_shared is None:
#         return
#     user_tg_id = message.user_shared.user_id
#     status = dialog_manager.dialog_data.get("status")
#     user_service: UserService = await dialog_manager.middleware_data[
#         "dishka_container"
#     ].get(UserService)
#     try:
#         user: User = await user_service.fetch_by_user_tg_id(user_tg_id=user_tg_id)
#     except EntityNotFoundError:
#         await message.answer(manage_users_msg.USER_NOT_FOUND)
#         return
#     await dialog_manager.done()
#     await dialog_manager.start(SuperAdminMenu.main, mode=StartMode.RESET_STACK)
