from __future__ import annotations

import logging
import zoneinfo
from datetime import datetime

from bakery_bot.adapters.http.tg_client.base import ITGClient
from bakery_bot.adapters.http.vk_client.base import IVKClient
from bakery_bot.common.config import Config
from bakery_bot.common.entities.building import BuildingTitle
from bakery_bot.common.entities.photo import UploadPhoto
from bakery_bot.common.entities.vk import (
    CreateVKAlbum,
    FetchVKUploadUrl,
    SaveVKPhoto,
    UploadVKPhoto,
)
from bakery_bot.common.exceptions import ConflictException, ForbiddenException
from bakery_bot.domains.utils.last_day_of_month_validator import (
    is_yesterday_last_month,
)
from bakery_bot.domains.utils.month_transformer import RUSSIAN_MONTHS

log = logging.getLogger(__name__)


class FileService:
    __config: Config
    __vk_client: IVKClient
    __tg_client: ITGClient

    def __init__(
        self,
        config: Config,
        vk_client: IVKClient,
        tg_client: ITGClient,
    ) -> None:
        self.__config = config
        self.__vk_client = vk_client
        self.__tg_client = tg_client

    async def upload_photo_to_album(
        self,
        *,
        upload_photo: UploadPhoto,
    ) -> bool:
        if upload_photo.tg_chat_id not in (
            -self.__config.tg_fontan_id,
            -self.__config.tg_fort_dialog_id,
            -self.__config.tg_test_id,
        ):
            log.info("Forbidden chat id: %s", upload_photo.tg_chat_id)
            raise ForbiddenException("В этот чат нельзя отправлять фотографии, Курлык!")
        if not upload_photo.tg_photo_path:
            log.info("There is no photo path")
            raise ConflictException("URL фотографии на TG сервере не найден, Курлык!")
        photo_bytes = await self.__tg_client.fetch_photo(
            path=upload_photo.tg_photo_path
        )
        photo_bytes.name = "photo.jpg"
        album_title = self.__combine_album_title(tg_chat_id=upload_photo.tg_chat_id)
        albums = await self.__vk_client.fetch_album_list()
        album = next(filter(lambda album: album.title == album_title, albums), None)
        if not album:
            album = await self.__vk_client.create_album(
                create_album=CreateVKAlbum(
                    group_id=self.__config.vk_group_id,
                    title=album_title,
                )
            )
        upload_url = await self.__vk_client.fetch_photo_upload_url(
            fetch_upload_url=FetchVKUploadUrl(
                album_id=album.id,
                group_id=self.__config.vk_group_id,
            )
        )
        upload_photo_server = await self.__vk_client.upload_photo(
            upload_photo=UploadVKPhoto(
                album_id=album.id,
                group_id=self.__config.vk_group_id,
                photo=photo_bytes,
                upload_url=upload_url,
            )
        )
        is_saved = await self.__vk_client.save_photo(
            save_photo=SaveVKPhoto(
                album_id=album.id,
                group_id=self.__config.vk_group_id,
                photos_list=upload_photo_server.photos_list,
                server=upload_photo_server.server,
                hash=upload_photo_server.hash,
            )
        )
        return is_saved

    def __combine_album_title(self, *, tg_chat_id: int) -> str:
        current_date = datetime.now(tz=zoneinfo.ZoneInfo("Europe/Moscow"))
        if current_date.hour in (0, 1, 2, 3, 4) and is_yesterday_last_month(
            current_date
        ):
            month = current_date.month - 1
        else:
            month = current_date.month
        if tg_chat_id == -self.__config.tg_fort_dialog_id:
            building = BuildingTitle.FORT_DIALOG
        elif tg_chat_id == -self.__config.tg_fontan_id:
            building = BuildingTitle.TZ_FONTAN
        else:
            building = BuildingTitle.TEST
        return f"{building} {RUSSIAN_MONTHS[month]} {current_date.year}"
