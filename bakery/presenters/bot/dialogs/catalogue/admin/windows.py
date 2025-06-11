from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Row,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from bakery.presenters.bot.dialogs.catalogue.admin.getters import (
    get_product_preview_data,
    get_products_data,
    get_selected_product,
)
from bakery.presenters.bot.dialogs.catalogue.admin.handlers import (
    go_back_to_list,
    on_add_clicked,
    on_cancel_product_creation,
    on_create_product,
    on_delete_clicked,
    on_description_input,
    on_edit_clicked,
    on_name_input,
    on_price_input,
    on_view_product_clicked,
)
from bakery.presenters.bot.dialogs.states import AdminCatalogue


def list_products_window() -> Window:
    return Window(
        Const("📦 Товары в категории:"),
        Select(
            id="product_select",
            items="products",
            item_id_getter=lambda item: str(item.id),
            text=Format("🧁 {item.name} — {item.price}₽"),
            on_click=on_view_product_clicked,
        ),
        Button(Const("➕ Добавить товар"), id="add", on_click=on_add_clicked),
        state=AdminCatalogue.view_products,
        getter=get_products_data,
    )


def add_product_windows() -> list[Window]:
    return [
        Window(
            Const("Введите название товара:"),
            MessageInput(on_name_input),
            state=AdminCatalogue.add_name,
        ),
        Window(
            Const("Введите описание товара:"),
            MessageInput(on_description_input),
            state=AdminCatalogue.add_description,
        ),
        Window(
            Const("Введите цену товара (в рублях):"),
            MessageInput(on_price_input),
            state=AdminCatalogue.add_price,
        ),
        Window(
            Format(
                "📄 Подтвердите создание товара:\n\n"
                "🌟 <b>{name}</b>\n"
                "📍 {description}\n"
                "💲 {price} ₽"
            ),
            Row(
                Button(Const("✅ Создать"), id="create", on_click=on_create_product),
                Button(
                    Const("❌ Отмена"), id="cancel", on_click=on_cancel_product_creation
                ),
            ),
            state=AdminCatalogue.add_confirm,
            getter=get_product_preview_data,
        ),
    ]


def product_card_window() -> Window:
    return Window(
        Format(
            "📦 <b>{product.name}</b>\n\n"
            "📍 {product.description}\n"
            "💰 Цена: {product.price}₽"
        ),
        Row(
            Button(Const("✏️ Редактировать"), id="edit", on_click=on_edit_clicked),
            Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_clicked),
        ),
        Button(Const("🔙 Назад"), id="back", on_click=go_back_to_list),
        state=AdminCatalogue.view_single_product,
        getter=get_selected_product,
    )
