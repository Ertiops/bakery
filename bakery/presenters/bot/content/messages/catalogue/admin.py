from typing import Final

NAME_INPUT: Final = "Введите название товара:"
DESCRIPTION_INPUT: Final = "Введите описание товара:"
PRICE_INPUT: Final = "Введите цену товара (в рублях):"
PHOTO_INPUT: Final = "Пришлите фото товара (одно изображение):"
PHOTO_INPUT_HINT: Final = "Фото обязательно."
UPDATE_PHOTO_INPUT_HINT: Final = "Можно оставить текущее фото."
INVALID_PRICE_INOUT: Final = "Цена должна быть положительным числом"
ADD_PRODUCT_PREVIEW: Final = (
    "<b>Подтвердите создание товара:</b>\n\n"
    "<b>Название:</b> {name}\n"
    "<b>Описание:</b> {description}\n"
    "<b>Цена:</b> {price} ₽"
)
UPDATE_PRODUCT_PREVIEW: Final = (
    "<b>Подтвердите обновление товара:</b>\n\n"
    "<b>Название:</b> {name}\n"
    "<b>Описание:</b> {description}\n"
    "<b>Цена:</b> {price} ₽"
)
CONFIRM_DELETE: Final = "❗ Вы уверены, что хотите удалить этот товар?"
