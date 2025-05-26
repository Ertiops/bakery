from collections.abc import Sequence
from dataclasses import dataclass
from io import BytesIO

from yarl import URL


@dataclass(frozen=True, slots=True, kw_only=True)
class VKAlbum:
    id: int
    thumb_id: int
    owner_id: int
    title: str
    description: str | None
    created: int
    updated: int
    size: int
    can_upload: int


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateVKAlbum:
    group_id: int
    title: str


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchVKUploadUrl:
    album_id: int
    group_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class UploadVKPhoto:
    album_id: int
    group_id: int
    photo: BytesIO
    upload_url: URL


@dataclass(frozen=True, slots=True, kw_only=True)
class UploadVKPhotoServer:
    server: int
    photos_list: str
    aid: int
    hash: str
    gid: int


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveVKPhoto:
    album_id: int
    group_id: int
    photos_list: str
    server: int
    hash: str


@dataclass(frozen=True, slots=True, kw_only=True)
class VKPhotoSize:
    height: int
    type: str
    width: int
    url: str


@dataclass(frozen=True, slots=True, kw_only=True)
class VKOrigPhoto:
    height: int
    type: str
    url: str
    width: int


@dataclass(frozen=True, slots=True, kw_only=True)
class VKPhotoSaved:
    album_id: int
    date: int
    id: int
    owner_id: int
    sizes: Sequence[VKPhotoSize]
    text: str
    user_id: int
    web_view_token: str
    orig_photo: VKOrigPhoto


@dataclass(frozen=True, slots=True, kw_only=True)
class VKPhotoSavedList:
    items: Sequence[VKPhotoSaved]
