import logging
from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bakery.application.exceptions import EntityAlreadyExistsException
from bakery.domains.entities.product import (
    CreateProduct,
    ProductCategory,
    UpdateProduct,
)
from bakery.domains.services.product import ProductService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminCatalogue

log = logging.getLogger(__name__)


async def on_update_clicked(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    product_id = manager.start_data.get("product_id") or manager.dialog_data.get(  # type: ignore[union-attr]
        "product_id"
    )
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    await manager.start(
        state=AdminCatalogue.update_name,
        data=dict(product_id=product_id, category=category),
        mode=StartMode.RESET_STACK,
    )


async def on_update_name_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    manager.dialog_data["name"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminCatalogue.update_description)


async def on_skip_name(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    manager.dialog_data["name"] = manager.dialog_data["original_name"]
    await manager.switch_to(AdminCatalogue.update_description)


async def on_update_description_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    manager.dialog_data["description"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminCatalogue.update_price)


async def on_skip_description(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    manager.dialog_data["description"] = manager.dialog_data["original_description"]
    await manager.switch_to(AdminCatalogue.update_price)


async def on_update_price_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    try:
        price = int(message.text.strip())  # type: ignore[union-attr]
        if price <= 0:
            raise ValueError()
        manager.dialog_data["price"] = price
        await manager.switch_to(AdminCatalogue.update_confirm)
    except ValueError:
        await message.answer("Введите корректную цену (целое положительное число)")


async def on_skip_price(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    manager.dialog_data["price"] = manager.dialog_data["original_price"]
    await manager.switch_to(AdminCatalogue.update_confirm)


async def on_update_product(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    product_id = UUID(manager.start_data["product_id"])  # type: ignore
    service: ProductService = await manager.middleware_data["dishka_container"].get(
        ProductService
    )
    uow: AbstractUow = await manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    log.info("Updating product with ID: %s", product_id)
    try:
        async with uow:
            product = await service.update_by_id(
                input_dto=UpdateProduct(
                    id=product_id,
                    name=manager.dialog_data["name"],
                    description=manager.dialog_data["description"],
                    price=manager.dialog_data["price"],
                )
            )
        await manager.start(
            AdminCatalogue.view_single_product,
            data=dict(product_id=str(product_id), category=product.category),
            mode=StartMode.RESET_STACK,
        )
    except EntityAlreadyExistsException:
        await callback.answer(
            text="Товар с таким названием уже есть! Выберите другое название.",
        )
        await manager.switch_to(AdminCatalogue.update_name)


async def on_cancel_update(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if callback.message and hasattr(callback.message, "delete"):
        await callback.message.delete()
    await manager.start(
        AdminCatalogue.view_single_product,
        data=dict(
            product_id=manager.start_data["product_id"],  # type: ignore
            category=manager.start_data["category"],  # type: ignore
        ),
        mode=StartMode.RESET_STACK,
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
            raise ValueError
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
    log.info("Creating product in category: %s", category)
    try:
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
    except EntityAlreadyExistsException:
        await callback.answer(
            text="Товар с таким названием уже есть! Выберите другое название.",
        )
        await manager.switch_to(AdminCatalogue.add_name)


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
        data=dict(product_id=item_id, category=category),
    )


async def on_confirm_delete(
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
    log.info("Deleting product with ID: %s", product_id)
    async with uow:
        await service.delete_by_id(input_id=UUID(product_id))
    await manager.switch_to(AdminCatalogue.view_products)


async def go_to_confirm_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.start(
        state=AdminCatalogue.confirm_delete,
        data=dict(
            product_id=manager.dialog_data.get("product_id")
            or manager.start_data.get("product_id"),  # type: ignore[union-attr]
            category=manager.dialog_data.get("category")
            or manager.start_data.get("category"),  # type: ignore[union-attr]
        ),
    )


async def on_cancel_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    product_id = manager.dialog_data.get("product_id") or manager.start_data.get(  # type: ignore[union-attr]
        "product_id"
    )
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore[union-attr]
    await manager.start(
        state=AdminCatalogue.view_single_product,
        data=dict(product_id=product_id, category=category),
        mode=StartMode.RESET_STACK,
    )
