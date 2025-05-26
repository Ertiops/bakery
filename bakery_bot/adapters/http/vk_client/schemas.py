from collections.abc import Sequence

from msgspec import Struct


class VkAlbumStruct(Struct, frozen=True, kw_only=True):
    id: int
    thumb_id: int
    owner_id: int
    title: str
    description: str | None
    created: int
    updated: int
    size: int
    can_upload: int


class VKAlbumListStruct(Struct, frozen=True, kw_only=True):
    count: int
    items: Sequence[VkAlbumStruct]


class VKAlbumListResponseStruct(Struct, frozen=True, kw_only=True):
    response: VKAlbumListStruct


class VKAlbumResponseStruct(Struct, frozen=True, kw_only=True):
    response: VkAlbumStruct


class VKPhotoUrlStruct(Struct, frozen=True, kw_only=True):
    upload_url: str


class VKPhotoUrlResponseStruct(Struct, frozen=True, kw_only=True):
    response: VKPhotoUrlStruct


class VKUploadPhotoResponseStruct(Struct, frozen=True, kw_only=True):
    server: int
    photos_list: str
    aid: int
    hash: str
    gid: int


class VKPhotoSizeStruct(Struct, frozen=True, kw_only=True):
    height: int
    type: str
    width: int
    url: str


class VKOrigPhotoStruct(Struct, frozen=True, kw_only=True):
    height: int
    type: str
    url: str
    width: int


class VKPhotoSavedStruct(Struct, frozen=True, kw_only=True):
    album_id: int
    date: int
    id: int
    owner_id: int
    sizes: Sequence[VKPhotoSizeStruct]
    text: str
    user_id: int
    web_view_token: str
    orig_photo: VKOrigPhotoStruct


class VKPhotoSavedResponseStruct(Struct, frozen=True, kw_only=True):
    response: Sequence[VKPhotoSavedStruct]
