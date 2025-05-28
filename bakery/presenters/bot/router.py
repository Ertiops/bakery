from aiogram import Router

from bakery.presenters.bot.handlers import router as bot_router


def register_routers(router: Router) -> None:
    my_router = Router()
    my_router.include_routers(bot_router)
    router.include_router(my_router)
