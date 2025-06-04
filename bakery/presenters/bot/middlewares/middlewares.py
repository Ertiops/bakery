import logging
from collections.abc import Sequence

from aiogram import BaseMiddleware

from bakery.presenters.bot.middlewares.user import UserMiddleware

log = logging.getLogger(__name__)

bot_middlewares: Sequence[BaseMiddleware] = [UserMiddleware()]
