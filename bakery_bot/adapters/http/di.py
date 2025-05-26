from collections.abc import AsyncIterator

import aiohttp
from dishka import AnyOf, Provider, Scope, provide
from yarl import URL

from bakery_bot.adapters.http.tg_client.base import ITGClient
from bakery_bot.adapters.http.tg_client.tg_client import TGClient
from bakery_bot.adapters.http.vk_client.base import IVKClient
from bakery_bot.adapters.http.vk_client.vk_client import VKClient
from bakery_bot.common.config import Config


class HttpProvider(Provider):
    __config: Config

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.__config = config

    @provide(scope=Scope.APP)
    async def vk_client(self) -> AsyncIterator[AnyOf[IVKClient, VKClient]]:
        async with aiohttp.ClientSession() as session:
            yield VKClient(
                url=URL(self.__config.vk_base_url),
                session=session,
                client_name="vk_client",
                config=self.__config,
            )

    @provide(scope=Scope.APP)
    async def tg_client(self) -> AsyncIterator[AnyOf[ITGClient, TGClient]]:
        async with aiohttp.ClientSession() as session:
            yield TGClient(
                url=URL(self.__config.tg_api_base_url),
                session=session,
                client_name="tg_client",
                config=self.__config,
            )
