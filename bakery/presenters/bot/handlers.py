import logging

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

log = logging.getLogger(__name__)


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer("Бугага!")
