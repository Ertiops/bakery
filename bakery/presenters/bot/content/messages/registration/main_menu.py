from typing import Final

from bakery.presenters.bot.content import links

USER_FAQ_ACCEPTANCE: Final = (
    "Добро Пожаловать! \n\n"
    'Нажимая кнопку "Продолжить" вы даёте '
    f'<a href="{links.FAQ_ACCEPTANCE}">'
    "согласие на обработку персональных данных</a>"
)

REGISTRATION_START: Final = 'Пройдите регистрацию, нажав кнопку "Продолжить"!'
REGISTRATION_FINISH: Final = "Регистрация завершена"
