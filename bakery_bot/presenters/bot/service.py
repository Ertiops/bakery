import logging

from aiogram import Bot, Dispatcher
from aiomisc import Service
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka

from bakery_bot.adapters.http.di import HttpProvider
from bakery_bot.common.config import Config
from bakery_bot.domains.di import DomainProvider
from bakery_bot.presenters.bot.router import register_routers

log = logging.getLogger(__name__)


class TelegramBotService(Service):
    config: Config

    async def start(self) -> None:
        self.__bot = Bot(
            token=self.config.tg_bot_token,
        )
        self.__dispatcher = self.dispatcher()
        log.info("Initializing bot")
        await self._setup_dispatcher()
        self.__add_dependency_overrides()
        await self.__dispatcher.start_polling(self.__bot)

    def dispatcher(self) -> Dispatcher:
        return Dispatcher()

    async def _setup_dispatcher(self) -> None:
        await self._setup_routers()

    async def _setup_routers(self) -> None:
        register_routers(self.__dispatcher)

    def __add_dependency_overrides(self) -> None:
        container = make_async_container(
            HttpProvider(config=self.config),
            DomainProvider(config=self.config),
            skip_validation=True,
        )
        setup_dishka(container=container, router=self.__dispatcher)
