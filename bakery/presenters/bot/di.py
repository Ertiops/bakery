from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from dishka import BaseScope, Provider, Scope, provide

from bakery.config import MainConfig


class TelegramProvider(Provider):
    def __init__(
        self,
        config: MainConfig,
        scope: BaseScope | None = None,
        component: str | None = None,
    ):
        super().__init__(scope, component)
        self.__config = config

    @provide(scope=Scope.APP)
    async def config(self) -> MainConfig:
        return self.__config

    @provide(scope=Scope.APP)
    async def session(self) -> AiohttpSession:
        return AiohttpSession()

    @provide(scope=Scope.APP)
    async def bot(self, session: AiohttpSession) -> Bot:
        return Bot(
            token=self.__config.bot.token,
            session=session,
            default=DefaultBotProperties(
                parse_mode="HTML", link_preview_is_disabled=False
            ),
        )
