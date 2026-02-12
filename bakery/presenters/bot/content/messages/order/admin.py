from typing import Final

ADMIN_ORDERS_TITLE: Final[str] = "📦 Заказы\n\n"
SELECT_CATEGORY: Final[str] = "Выберите раздел:"
SELECT_DATE: Final[str] = "Выберите дату:"
NO_ORDERS: Final[str] = "Заказов нет 😔"
DATE_TITLE: Final[str] = "📅 Заказ на {date}\n\n"
DATE_TOTAL_ORDERS: Final[str] = "Всего заказов: {count}\n"
DATE_TOTAL_SUM: Final[str] = "Сумма: {total}₽\n\n"
DATE_PRODUCTS_TITLE: Final[str] = "🧺 Состав общего заказа:\n"
DATE_PRODUCTS_EMPTY: Final[str] = "Состав пуст\n"
TAKE_IN_WORK_CONFIRM_TITLE: Final[str] = "Взять заказы в работу?"
TAKE_IN_WORK_SENT: Final[str] = "Заказы взяты в работу."
START_DELIVERY_HOURS_TITLE: Final[str] = "Введите количество часов доставки:"
START_DELIVERY_CONFIRM_TITLE: Final[str] = (
    "Отправить пользователю сообщение о доставке?\n"
    "Сообщение:\n"
    "Доставим в течение {hours} часов."
)
START_DELIVERY_SENT: Final[str] = "Сообщение о развозе отправлено пользователям."
FINISH_DELIVERY_CONFIRM_TITLE: Final[str] = "Подтвердите завершение доставки."
FINISH_DELIVERY_SENT: Final[str] = "Все пользователи уведомлены о завершении доставки."
DELETE_REASON_TITLE: Final[str] = "Введите причину удаления товара:\n\n{product_name}"
DELETE_CONFIRM_TITLE: Final[str] = (
    "Подтвердите удаление товара:\n\n{product_name}\n\nПричина:\n{reason}"
)
USER_ORDERS_TITLE: Final[str] = "👥 Заказы пользователей на {date}\n\n"
DELETED_ORDERS_TITLE: Final[str] = "🧾 Измененные заказы на {date}\n\n"
UNPAID_ORDERS_TITLE: Final[str] = "💸 Неоплаченные заказы\n\n"
USER_ORDER_ITEM: Final[str] = "🧾 {item[number]} • {item[user_name]} • {item[total]}₽"
USER_ORDER_TITLE: Final[str] = "🧾 Заказ {number}\n\n"
USER_ORDER_CONTACTS: Final[str] = "👤 {user_name}\n📞 {user_phone}\n\n"
USER_ORDER_PAYMENT: Final[str] = "🧾 Чек: {has_payment}\n"
DELETE_ORDER_REASON_TITLE: Final[str] = (
    "Введите причину удаления заказа:\n\n{order_number}"
)
DELETE_ORDER_CONFIRM_TITLE: Final[str] = (
    "Подтвердите удаление заказа:\n\n{order_number}\n\nПричина:\n{reason}"
)
