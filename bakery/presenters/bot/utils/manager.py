from collections.abc import AsyncGenerator

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import InputFile
from aiogram.types import URLInputFile as AiogramURLInputFile
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.manager.message_manager import MessageManager


class S3MessageManager(MessageManager):
    def __init__(self, s3_host: str, session: AiohttpSession) -> None:
        self._s3_host = s3_host
        self.session = session

    async def get_media_source(
        self, media: MediaAttachment, bot: Bot
    ) -> InputFile | str:
        if media.url and media.url.startswith(self._s3_host):
            return URLInputFile(media.url, bot=bot, session=self.session)
        return await super().get_media_source(media, bot)


class URLInputFile(AiogramURLInputFile):
    def __init__(
        self,
        url: str,
        session: AiohttpSession,
        bot: Bot,
    ):
        super().__init__(url=url, bot=bot)
        self.session = session

    async def read(self, bot: Bot) -> AsyncGenerator[bytes, None]:
        bot = self.bot or bot
        stream = self.session.stream_content(
            url=self.url,
            headers=self.headers,
            timeout=self.timeout,
            chunk_size=self.chunk_size,
            raise_for_status=True,
        )

        async for chunk in stream:
            yield chunk
