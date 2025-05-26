from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class UploadPhoto:
    tg_chat_id: int
    tg_photo_path: str | None
