from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bakery.presenters.bot.content.buttons.main_menu import admin as admin_menu_btn
from bakery.presenters.bot.content.buttons.main_menu import user as user_menu_btn


def get_user_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=user_menu_btn.MAKE_ORDER),
                KeyboardButton(text=user_menu_btn.CATALOGUE),
                KeyboardButton(text=user_menu_btn.MY_ORDERS),
                KeyboardButton(text=user_menu_btn.HELP),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_admin_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=admin_menu_btn.ORDERS),
                KeyboardButton(text=admin_menu_btn.CATALOGUE),
                KeyboardButton(text=admin_menu_btn.ADDRESSES),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
