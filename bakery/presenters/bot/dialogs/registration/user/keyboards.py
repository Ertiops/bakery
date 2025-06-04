from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bakery.presenters.bot.content.buttons.registration import user as user_btn


def get_share_phone_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=user_btn.PHONE_SHARE, request_contact=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
