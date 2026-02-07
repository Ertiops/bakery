import logging
from collections.abc import Sequence

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from aiomisc import Service
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from bakery.adapters.database.di import DatabaseProvider
from bakery.adapters.pdf.di import PdfProvider
from bakery.config import MainConfig
from bakery.domains.di import DomainProvider
from bakery.presenters.bot.commands.utils import set_ui_commands
from bakery.presenters.bot.di import TelegramProvider
from bakery.presenters.bot.exception_handlers import (
    on_unknown_intent,
    on_unknown_state,
)
from bakery.presenters.bot.middlewares.middlewares import bot_middlewares
from bakery.presenters.bot.router import register_dialogs

log = logging.getLogger(__name__)


class TelegramBotService(Service):
    __required__ = ("config",)

    MIDDLEWARES: Sequence[BaseMiddleware] = bot_middlewares
    config: MainConfig

    async def start(self) -> None:
        log.info("Start bot service")

        self.__dispatcher = await self.dispatcher()
        self.__add_dependency_overrides()
        self.__bot = await self.__container.get(Bot)
        log.info("Initialize bot")
        await self._setup_bot()
        await self._setup_bot_dispatcher()
        self.start_event.set()

        log.info("Start pooling")
        await self.__dispatcher.start_polling(self.__bot, skip_updates=True)

    async def stop(self, exception: Exception | None = None) -> None:
        await self.__bot.session.close()

    async def dispatcher(self) -> Dispatcher:
        return Dispatcher(
            storage=await self.fsm_storage(),
            events_isolation=SimpleEventIsolation(),
        )

    async def fsm_storage(self) -> BaseStorage:
        return RedisStorage.from_url(
            url=self.config.redis.dsn,
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )

    async def _setup_bot(self) -> None:
        await set_ui_commands(self.__bot)
        await self.__bot.delete_webhook(drop_pending_updates=True)

    async def _setup_bot_dispatcher(self) -> None:
        await self._setup_middlewares()
        await self._setup_dialogs()
        await self._setup_error_handlers()

    async def _setup_middlewares(self) -> None:
        for middleware in self.MIDDLEWARES:
            self.__dispatcher.update.middleware(middleware)

    async def _setup_dialogs(self) -> None:
        register_dialogs(self.__dispatcher)
        setup_dialogs(self.__dispatcher)
        return None

    async def _setup_error_handlers(self) -> None:
        self.__dispatcher.errors.register(
            on_unknown_intent, ExceptionTypeFilter(UnknownIntent)
        )
        self.__dispatcher.errors.register(
            on_unknown_state, ExceptionTypeFilter(UnknownState)
        )

    def __add_dependency_overrides(self) -> None:
        self.__container = make_async_container(
            DatabaseProvider(self.config.db),
            PdfProvider(),
            DomainProvider(),
            TelegramProvider(self.config),
            skip_validation=True,
        )
        setup_dishka(self.__container, self.__dispatcher)
