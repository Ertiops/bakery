from typing import Final

CHOICE_MESSAGE: Final = "Контактов пока нет, добавим?"
ADD_NUMBER: Final = "Введите номер"
NAME_INPUT: Final = "Введите имя"
TG_USERNAME_INPUT: Final = "Введите имя пользователя тг: @username"
ADD_PREVIEW: Final = (
    "<b>Подтвердите создание контакта:</b>\n\n"
    "<b>Имя:</b> {name}\n"
    "<b>Телеграм:</b> {tg_username}\n"
)
CONTACT: Final = "<b>Контакт:</b>\n<b>Имя:</b> {name}\n<b>Телеграм:</b> {tg_username}\n"
UPDATE_PREVIEW: Final = (
    "<b>Подтвердите изменение контакта:</b>\n\n"
    "<b>Имя:</b> {name}\n"
    "<b>Телеграм:</b> {tg_username}\n"
)
