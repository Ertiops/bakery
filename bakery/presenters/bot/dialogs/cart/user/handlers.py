from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.application.constants.cart import CART_PRODUCT_MAX
from bakery.domains.entities.cart import CreateCart, GetCartByUserProductIds
from bakery.domains.services.cart import CartService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import UserCatalogue
from bakery.presenters.bot.dialogs.utils.order_for_user import (
    get_order_for_user_data,
    get_order_for_user_id,
)


async def on_view_product_clicked(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    start_data = manager.start_data
    if isinstance(start_data, dict):
        category = manager.dialog_data.get("category") or start_data.get("category")
    else:
        category = manager.dialog_data.get("category")
    manager.dialog_data["product_id"] = item_id
    if category:
        manager.dialog_data["category"] = category

    await manager.start(
        state=UserCatalogue.view_single_product,
        data=dict(
            product_id=item_id, category=category, **get_order_for_user_data(manager)
        ),
    )


async def update_quantity(manager: DialogManager, delta: int) -> None:
    container = manager.middleware_data["dishka_container"]
    service: CartService = await container.get(CartService)
    uow: AbstractUow = await container.get(AbstractUow)
    raw_data = manager.event.data  # type: ignore[union-attr]
    parts = raw_data.split(":")  # type: ignore[union-attr]
    product_id = UUID(parts[1])
    user_id = get_order_for_user_id(manager)
    async with uow:
        cart = await service.get_w_product_by_user_product_ids(
            input_dto=GetCartByUserProductIds(
                user_id=user_id,
                product_id=product_id,
            )
        )
        if cart.quantity - delta < 0 or cart.quantity + delta > CART_PRODUCT_MAX:
            return
        await service.create_or_update(
            input_dto=CreateCart(
                user_id=user_id,
                product_id=product_id,
                quantity=cart.quantity + delta,
            )
        )
    await manager.show()


async def on_increment_quantity(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await update_quantity(manager, delta=1)


async def on_decrement_quantity(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await update_quantity(manager, delta=-1)


async def on_cart_item_delete(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    item_id = getattr(manager, "item_id", None)
    if not item_id:
        return
    cart_item_index = manager.dialog_data.get("cart_item_index") or {}
    product_id_raw = cart_item_index.get(str(item_id))
    if not product_id_raw:
        return
    try:
        product_id = UUID(product_id_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    service: CartService = await container.get(CartService)
    uow: AbstractUow = await container.get(AbstractUow)
    user_id = get_order_for_user_id(manager)

    async with uow:
        await service.create_or_update(
            input_dto=CreateCart(
                user_id=user_id,
                product_id=product_id,
                quantity=0,
            )
        )
    await manager.show()
