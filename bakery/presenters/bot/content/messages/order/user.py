from typing import Final

CREATE_ORDER: Final[str] = (
    "🧾 Выберите адрес доставки.\n"
    "Вы можете пропустить этот шаг, если вы хотите оформить доставку до дома*.\n"
    "*Доставка до дома - {delivery_cost} руб.\n"
)
FREE_DELIVERY_HINT: Final[str] = "*Бесплатная доставка от {free_delivery_amount} руб.\n"
MANUAL_ADDRESS_TITLE: Final[str] = "✍️ Введите адрес доставки одним сообщением:"
MANUAL_ADDRESS_EXAMPLE: Final[str] = (
    "\n\nНапример: ул. Шамиля Усманова 10, 1 подъезд, кв. 3"
)
ORDER_DATE_TITLE: Final[str] = "📅 Выберите дату доставки"
ORDER_DATE_AVAILABLE_SUFFIX: Final[str] = "\n\nДоступные даты:"
ORDER_DATE_EMPTY: Final[str] = "\n\nСейчас нет доступных дат 😔"
CONFIRM_TITLE: Final[str] = "✅ Подтверждение заказа\n\n"
CONFIRM_ADDRESS_LABEL: Final[str] = "📍 Адрес доставки:"
CONFIRM_ADDRESS_EMPTY: Final[str] = "Не выбран"
CONFIRM_DATE_LABEL: Final[str] = "\n\n📅 Дата доставки:"
CONFIRM_DATE_EMPTY: Final[str] = "Не выбрана"
CONFIRM_CART_LABEL: Final[str] = "\n\n🧺 Корзина:"
CONFIRM_DELIVERY_COST: Final[str] = "\n\n🚚 Доставка до дома: {delivery_cost} руб."
CONFIRM_TOTAL: Final[str] = "\n\n💰 Итого: {total}"
CONFIRM_SUGGESTED_TITLE: Final[str] = "\n\n🧁 Популярное к заказу:"
CONFIRM_SUGGESTED_ITEM: Final[str] = "{item[name]} — {item[price]}₽"
ORDER_CREATED: Final[str] = "✅ Заказ успешно создан!\n\n"
MY_ORDERS_TITLE: Final[str] = "📦 Мои заказы\n\n"
SELECT_CATEGORY: Final[str] = "Выберите категорию:"
SELECT_ORDER: Final[str] = "Выберите заказ:"
NO_ORDERS: Final[str] = "\n\nПока заказов нет 😔"
ORDERS_CATEGORY_TITLE: Final[str] = "{category_title}\n\n"
ORDER_LIST_ITEM: Final[str] = (
    "🧾 {item[number]} • {item[delivered_at]} • {item[total]}₽"
)
ORDER_TITLE: Final[str] = "📦 Заказ {number}\n\n"
ORDER_DELIVERY_DATE: Final[str] = "📅 Доставка: {delivered_at}\n"
ORDER_ADDRESS: Final[str] = "📍 Адрес: {pickup_address_name}\n"
ORDER_CONTENT_LABEL: Final[str] = "🧺 Состав заказа:\n"
ORDER_PRODUCTS_TEXT: Final[str] = "{products_text}\n\n"
ORDER_DELIVERY_PRICE: Final[str] = "🚚 Доставка: {delivery_price}₽\n"
ORDER_TOTAL_PRICE: Final[str] = "💰 Итого: {total_price}₽"
ORDER_NOT_FOUND: Final[str] = "Заказ не найден 😔"
ORDER_PRODUCT_REMOVED: Final[str] = (
    "📨 Из вашего заказа {order_number} удален товар: {product_name}.\n"
    "Причина: {reason}"
)
DELIVERY_STARTED: Final[str] = (
    "🚚 Начат развоз вашего заказа {order_number}.\nДоставим в течение {hours} часов."
)
ORDER_DELIVERED: Final[str] = "✅ Ваш заказ {order_number} доставлен."
PRODUCT_NAME_FALLBACK: Final[str] = "товар"
ORDER_DELETED: Final[str] = "🛑 Ваш заказ {order_number} удален.\nПричина: {reason}"
CART_ITEM_LINE: Final[str] = (
    "• {item[name]} — {item[qty]} × {item[price]} = {item[subtotal]}"
)
CATEGORY_TITLE_FALLBACK: Final[str] = "📦 Мои заказы"
