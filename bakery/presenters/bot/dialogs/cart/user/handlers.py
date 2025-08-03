from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.domains.entities.cart import CreateCart, GetCartByUserProductIds
from bakery.domains.entities.user import User
from bakery.domains.services.cart import CartService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import UserCatalogue


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
        state=UserCatalogue.view_single_product,
        data=dict(product_id=item_id, category=category),
    )


async def update_quantity(manager: DialogManager, delta: int) -> None:
    container = manager.middleware_data["dishka_container"]
    service: CartService = await container.get(CartService)
    user: User = manager.middleware_data["current_user"]
    uow: AbstractUow = await container.get(AbstractUow)

    raw_data = manager.event.data  # type: ignore[union-attr]
    parts = raw_data.split(":")  # type: ignore[union-attr]
    product_id = UUID(parts[1])
    async with uow:
        cart = await service.get_w_product_by_user_product_ids(
            input_dto=GetCartByUserProductIds(
                user_id=user.id,
                product_id=product_id,
            )
        )
        await service.create_or_update(
            input_dto=CreateCart(
                user_id=user.id, product_id=product_id, quantity=cart.quantity + delta
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
