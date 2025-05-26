import logging
from http import HTTPStatus
from io import BytesIO
from types import MappingProxyType

from aiohttp import ClientResponse
from asyncly import ResponseHandlersType

log = logging.getLogger(__name__)


async def photo_response(response: ClientResponse) -> BytesIO:
    return BytesIO(await response.read())


FETCH_PHOTO_HANDLERS: ResponseHandlersType = MappingProxyType(
    {HTTPStatus.OK: photo_response}
)
