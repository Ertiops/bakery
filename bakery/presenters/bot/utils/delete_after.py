import asyncio

from aiogram.types import Message


async def delete_after(*, message: Message, ttl: float) -> None:
    await asyncio.sleep(ttl)
    await message.delete()
