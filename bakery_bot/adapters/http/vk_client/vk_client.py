import logging
from collections.abc import Sequence
from typing import ClassVar

from aiohttp import ClientSession, FormData
from aiomisc import asyncretry
from asyncly import BaseHttpClient
from asyncly.client.timeout import TimeoutType
from msgspec.structs import asdict
from yarl import URL

from bakery_bot.adapters.http.vk_client.base import IVKClient
from bakery_bot.adapters.http.vk_client.handlers import (
    CREATE_ALBUM_HANDLERS,
    FETCH_ALBUM_LIST_HANDLERS,
    FETCH_PHOTO_UPLOAD_URL_HANDLERS,
    SAVE_PHOTO_HANDLERS,
    UPLOAD_PHOTO_HANDLERS,
)
from bakery_bot.adapters.http.vk_client.schemas import (
    VKAlbumListResponseStruct,
    VKAlbumResponseStruct,
    VKPhotoSavedResponseStruct,
    VKPhotoUrlResponseStruct,
    VKUploadPhotoResponseStruct,
)
from bakery_bot.adapters.http.vk_client.urls import (
    CREATE_ALBUM,
    FETCH_ALBUM_LIST,
    FETCH_PHOTO_UPLOAD_URL,
    SAVE_PHOTO,
)
from bakery_bot.common.config import Config
from bakery_bot.common.entities.vk import (
    CreateVKAlbum,
    FetchVKUploadUrl,
    SaveVKPhoto,
    UploadVKPhoto,
    UploadVKPhotoServer,
    VKAlbum,
)
from bakery_bot.common.exceptions import ChallengeBotException

log = logging.getLogger(__name__)

config = Config()

API_VERSION = "5.92"


class VKClient(BaseHttpClient, IVKClient):
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
    async def fetch_album_list(
        self,
        *,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> Sequence[VKAlbum]:
        params = dict(
            access_token=self.__config.vk_token,
            v=API_VERSION,
            owner_id=-self.__config.vk_group_id,
        )
        albums: VKAlbumListResponseStruct = await self._make_req(
            method="GET",
            url=self._url / FETCH_ALBUM_LIST,
            handlers=FETCH_ALBUM_LIST_HANDLERS,
            timeout=timeout,
            params=params,
        )
        if not albums:
            raise ChallengeBotException("Error at VK side fetching album list")
        return [VKAlbum(**asdict(album)) for album in albums.response.items]

    @asyncretry(max_tries=3)
    async def create_album(
        self,
        *,
        create_album: CreateVKAlbum,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> VKAlbum:
        params = dict(
            access_token=self.__config.vk_token,
            v=API_VERSION,
            title=create_album.title,
            group_id=create_album.group_id,
        )
        album: VKAlbumResponseStruct = await self._make_req(
            method="GET",
            url=self._url / CREATE_ALBUM,
            handlers=CREATE_ALBUM_HANDLERS,
            timeout=timeout,
            params=params,
        )
        if not album:
            raise ChallengeBotException("Error at VK side creating album")
        return VKAlbum(**asdict(album.response))

    @asyncretry(max_tries=3)
    async def fetch_photo_upload_url(
        self,
        *,
        fetch_upload_url: FetchVKUploadUrl,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> URL:
        params = dict(
            access_token=self.__config.vk_token,
            v=API_VERSION,
            album_id=fetch_upload_url.album_id,
            group_id=fetch_upload_url.group_id,
        )
        response: VKPhotoUrlResponseStruct = await self._make_req(
            method="GET",
            url=self._url / FETCH_PHOTO_UPLOAD_URL,
            handlers=FETCH_PHOTO_UPLOAD_URL_HANDLERS,
            timeout=timeout,
            params=params,
        )
        if not response:
            raise ChallengeBotException("Error at VK side fetching upload url")
        return URL(response.response.upload_url)

    async def upload_photo(
        self,
        *,
        upload_photo: UploadVKPhoto,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> UploadVKPhotoServer:
        data = FormData()
        data.add_field(
            "file1", upload_photo.photo, filename="photo.jpg", content_type="image/jpeg"
        )
        response: VKUploadPhotoResponseStruct = await self._make_req(
            method="POST",
            url=upload_photo.upload_url,
            handlers=UPLOAD_PHOTO_HANDLERS,
            timeout=timeout,
            data=data,
        )
        if not response:
            raise ChallengeBotException("Error at VK side uploading photo")
        return UploadVKPhotoServer(**asdict(response))

    async def save_photo(
        self,
        *,
        save_photo: SaveVKPhoto,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> bool:
        params = dict(
            access_token=self.__config.vk_token,
            v=API_VERSION,
            album_id=save_photo.album_id,
            group_id=save_photo.group_id,
            photos_list=save_photo.photos_list,
            server=save_photo.server,
            hash=save_photo.hash,
        )
        response: VKPhotoSavedResponseStruct = await self._make_req(
            method="GET",
            url=self._url / SAVE_PHOTO,
            handlers=SAVE_PHOTO_HANDLERS,
            timeout=timeout,
            params=params,
        )
        if not response:
            raise ChallengeBotException("Error at VK side saving photo")
        return True
