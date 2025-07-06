from typing import Final

NAME_INPUT: Final = "Введите название товара:"
DESCRIPTION_INPUT: Final = "Введите описание товара:"
PRICE_INPUT: Final = "Введите цену товара (в рублях):"
INVALID_PRICE_INOUT: Final = "Цена должна быть положительным числом"
ADD_PRODUCT_PREVIEW: Final = (
    "<b>Подтвердите создание товара:</b>\n\n"
    "<b>Название:</b> {name}\n"
    "<b>Описание:</b> {description}\n"
    "<b>Цена:</b> {price} ₽"
)
PRODUCT_CARD: Final = (
    "<b>Название:</b> {product.name}\n"
    "<b>Описание:</b> {product.description}\n"
    "<b>Цена:</b> {product.price}₽"
)
UPDATE_PRODUCT_PREVIEW: Final = (
    "<b>Подтвердите обновление товара:</b>\n\n"
    "<b>Название:</b> {name}\n"
    "<b>Описание:</b> {description}\n"
    "<b>Цена:</b> {price} ₽"
)
CONFIRM_DELETE: Final = "❗ Вы уверены, что хотите удалить этот товар?"
