import logging

from aiogram import Bot, F, Router
from aiogram.filters.command import Command
from aiogram.types import Message, PhotoSize
from dishka.integrations.aiogram import FromDishka, inject

from bakery_bot.common.entities.photo import UploadPhoto
from bakery_bot.domains.file_service import FileService

log = logging.getLogger(__name__)


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer("Привет! Загрузи фотографии для отправки в альбом VK, Курлык!")


@router.message(F.photo[-1].as_("photo"))
@inject
async def handle_photo_message(
    message: Message,
    photo: PhotoSize,
    bot: Bot,
    *,
    file_service: FromDishka[FileService],
) -> None:
    photo_path = (await bot.get_file(photo.file_id)).file_path  # type: ignore
    is_saved = await file_service.upload_photo_to_album(
        upload_photo=UploadPhoto(
            tg_chat_id=message.chat.id,
            tg_photo_path=photo_path,
        )
    )
    if not is_saved:
        log.info("VK photo upload failed")
        await message.answer("Не получилось загрузить фотографию в VK, Курлык!")
