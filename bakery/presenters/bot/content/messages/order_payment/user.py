from typing import Final

TITLE: Final[str] = "💳 Оплата заказа\n\n"
ORDER_NUMBER: Final[str] = "🧾 Заказ {number}\n\n"
PAYMENT_DETAILS: Final[str] = (
    "Отправьте сумму <b>{total_price}₽</b>\n\n"
    "📞 Номер: <b>{phone}</b>\n"
    "🏦 Банки: <b>{banks}</b>\n"
    "👤 Получатель: <b>{addressee}</b>\n\n"
)
REQUISITES_NOT_SET: Final[str] = (
    "❗ Реквизиты оплаты пока не настроены.\nНапишите администратору."
)
ORDER_NOT_FOUND: Final[str] = "Заказ не найден 😔"

ATTACH_FILE_TITLE: Final[str] = "📎 Прикрепите чек/скрин оплаты\n\n"
ATTACH_FILE_HINT: Final[str] = "Подойдёт фото или PDF.\n"
ATTACH_FILE_ACTION: Final[str] = "\nОтправьте файл одним сообщением 👇"

CONFIRM_ORDER_NUMBER: Final[str] = "🧾 Заказ {number}\n"
CONFIRM_TOTAL: Final[str] = "💰 Сумма: {total_price}₽\n\n"
CONFIRM_NO_FILE: Final[str] = "Файл не прикреплён 😔"

FINISH_TITLE: Final[str] = "✅ Спасибо!\n\n"
FINISH_BODY: Final[str] = "Мы получили ваше подтверждение оплаты.\n"

BTN_ATTACH_CHECK: Final[str] = "📎 Прикрепить чек"
BTN_CONFIRM: Final[str] = "✅ Подтвердить"
BTN_TO_ORDERS: Final[str] = "📦 К заказам"
BTN_FEEDBACK_GROUP: Final[str] = "💬 Оставить отзыв"
