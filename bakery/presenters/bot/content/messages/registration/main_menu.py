from typing import Final

from bakery.presenters.bot.content import links

USER_FAQ_ACCEPTANCE: Final = (
    "Добро Пожаловать! \n\n"
    'Нажимая кнопку "Продолжить" вы даёте '
    f'<a href="{links.FAQ_ACCEPTANCE}">'
    "согласие на обработку персональных данных</a>"
)

ROLE_CHOICE: Final = (
    'Добро пожаловать в чат-бот "Алабуга Политех".\n\n'
    'Для регистрации участника дуальной программы "Алабуга Политех" '
    'выберите кнопку "Колледжист".\n\n'
    'Воспользуйтесь ролью "Родитель" для входа в учетную запись родителя.\n\n'
    'Всех сотрудников компании просим зарегистрироваться через роль "Сотрудник"'
)
ROLE_WORKER: Final = "Сотрудник"
ROLE_PARENT: Final = "Родитель"
ROLE_STUDENT: Final = "Колледжист"
BACK: Final = "Назад"

REGISTRATION_START: Final = 'Пройдите регистрацию, нажав кнопку "Продолжить"!'
REGISTRATION_FINISH: Final = "Регистрация завершена"
