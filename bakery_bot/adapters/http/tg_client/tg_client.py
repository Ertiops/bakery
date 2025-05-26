import logging
from io import BytesIO
from typing import ClassVar

from aiohttp import ClientSession
from aiomisc import asyncretry
from asyncly import BaseHttpClient, TimeoutType
from yarl import URL

from bakery_bot.adapters.http.tg_client.base import ITGClient
from bakery_bot.adapters.http.tg_client.handlers import FETCH_PHOTO_HANDLERS
from bakery_bot.adapters.http.tg_client.urls import FETCH_PHOTO
from bakery_bot.common.config import Config
from bakery_bot.common.exceptions import ChallengeBotException

log = logging.getLogger(__name__)


class TGClient(BaseHttpClient, ITGClient):
    __config: Config

    DEFAULT_TIMEOUT: ClassVar[TimeoutType] = 20

    def __init__(
        self,
        url: URL,
        session: ClientSession,
        client_name: str,
        config: Config,
    ) -> None:
        super().__init__(url=url, session=session, client_name=client_name)
        self.__config = config

    @asyncretry(max_tries=3)
    async def fetch_photo(
        self,
        *,
        path: str,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> BytesIO:
        response: BytesIO = await self._make_req(
            method="GET",
            url=self._url
            / FETCH_PHOTO.format(
                token=self.__config.tg_bot_token,
                path=path,
            ),
            handlers=FETCH_PHOTO_HANDLERS,
            timeout=timeout,
        )
        if not response:
            raise ChallengeBotException("Error at TG side fetchong photo")
        return response
