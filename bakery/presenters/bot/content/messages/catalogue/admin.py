from typing import Final

NAME_INPUT: Final = "Введите название товара:"
DESCRIPTION_INPUT: Final = "Введите описание товара:"
PRICE_INPUT: Final = "Введите цену товара (в рублях):"
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
