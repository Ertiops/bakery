import logging
from http import HTTPStatus
from types import MappingProxyType

from aiohttp import ClientResponse
from asyncly import ResponseHandlersType
from asyncly.client.handlers.msgspec import parse_struct

from bakery_bot.adapters.http.vk_client.schemas import (
    VKAlbumListResponseStruct,
    VKAlbumResponseStruct,
    VKPhotoSavedResponseStruct,
    VKPhotoUrlResponseStruct,
    VKUploadPhotoResponseStruct,
)

log = logging.getLogger(__name__)


async def log_response_status(response: ClientResponse) -> None:
    log.info(
        "STATUS_CODE: %s, JSON: %s",
        response.status,
        await response.json(),
    )
    return None


FETCH_ALBUM_LIST_HANDLERS: ResponseHandlersType = MappingProxyType(
    {HTTPStatus.OK: parse_struct(struct=VKAlbumListResponseStruct)}
)

CREATE_ALBUM_HANDLERS: ResponseHandlersType = MappingProxyType(
    {HTTPStatus.OK: parse_struct(struct=VKAlbumResponseStruct)}
)

FETCH_PHOTO_UPLOAD_URL_HANDLERS: ResponseHandlersType = MappingProxyType(
    {HTTPStatus.OK: parse_struct(struct=VKPhotoUrlResponseStruct)}
)

UPLOAD_PHOTO_HANDLERS: ResponseHandlersType = MappingProxyType(
    {HTTPStatus.OK: parse_struct(struct=VKUploadPhotoResponseStruct)}
)

SAVE_PHOTO_HANDLERS: ResponseHandlersType = MappingProxyType(
    {HTTPStatus.OK: parse_struct(VKPhotoSavedResponseStruct)}
)
