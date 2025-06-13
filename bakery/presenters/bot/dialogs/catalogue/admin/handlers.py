from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bakery.domains.entities.product import CreateProduct, ProductCategory
from bakery.domains.services.product import ProductService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminCatalogue


async def on_delete_clicked(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    product_id = manager.start_data.get("product_id") or manager.dialog_data.get(  # type: ignore
        "product_id"
    )
    if not product_id:
        await callback.answer("Не удалось определить товар!", show_alert=True)
        return
    container = manager.middleware_data["dishka_container"]
    service: ProductService = await container.get(ProductService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        await service.delete_by_id(input_id=UUID(product_id))

    await manager.switch_to(AdminCatalogue.view_products)


async def on_edit_clicked(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    product_id = manager.start_data.get("product_id")  # type: ignore[union-attr]
    await manager.start(
        state=AdminCatalogue.edit_product,
        data={"product_id": product_id},
        mode=StartMode.NEW_STACK,
    )


async def on_add_clicked(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    manager.dialog_data["category"] = category
    await manager.switch_to(AdminCatalogue.add_name)


async def on_name_input(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data["name"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminCatalogue.add_description)


async def on_description_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    manager.dialog_data["description"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminCatalogue.add_price)


async def on_price_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    try:
        price = int(message.text.strip())  # type: ignore[union-attr]
        if price <= 0:
            raise ValueError()
    except ValueError:
        await message.answer("Введите корректную цену (целое положительное число)")
        return

    manager.dialog_data["price"] = price
    await manager.switch_to(AdminCatalogue.add_confirm)


async def on_create_product(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if callback.message is None:
        return

    category: str = manager.start_data.get("category") or manager.dialog_data.get(  # type: ignore
        "category"
    )
    container = manager.middleware_data["dishka_container"]
    service: ProductService = await container.get(ProductService)
    uow: AbstractUow = await container.get(AbstractUow)
    async with uow:
        product = await service.create(
            input_dto=CreateProduct(
                name=manager.dialog_data["name"],
                description=manager.dialog_data["description"],
                category=ProductCategory(category),
                price=manager.dialog_data["price"],
            )
        )
    await manager.start(
        AdminCatalogue.view_single_product,
        data=dict(product_id=str(product.id), category=category),
    )


async def on_cancel_product_creation(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if callback.message is None:
        return
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    manager.dialog_data["category"] = category
    await manager.switch_to(AdminCatalogue.view_products)


async def on_view_product_clicked(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    manager.dialog_data["product_id"] = item_id
    if category:
        manager.dialog_data["category"] = category

    await manager.start(
        state=AdminCatalogue.view_single_product,
        data={"product_id": item_id, "category": category},
    )
