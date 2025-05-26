from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from yarl import URL

from bakery_bot.common.entities.vk import (
    CreateVKAlbum,
    FetchVKUploadUrl,
    SaveVKPhoto,
    UploadVKPhoto,
    UploadVKPhotoServer,
    VKAlbum,
)


class IVKClient(Protocol):
    @abstractmethod
    async def fetch_album_list(self) -> Sequence[VKAlbum]:
        raise NotImplementedError

    @abstractmethod
    async def create_album(self, *, create_album: CreateVKAlbum) -> VKAlbum:
        raise NotImplementedError

    @abstractmethod
    async def fetch_photo_upload_url(
        self, *, fetch_upload_url: FetchVKUploadUrl
    ) -> URL:
        raise NotImplementedError

    @abstractmethod
    async def upload_photo(self, *, upload_photo: UploadVKPhoto) -> UploadVKPhotoServer:
        raise NotImplementedError

    @abstractmethod
    async def save_photo(self, *, save_photo: SaveVKPhoto) -> bool:
        raise NotImplementedError
