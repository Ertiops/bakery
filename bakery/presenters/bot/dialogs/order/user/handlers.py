from datetime import date
from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import ShowMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.cart import CartListParams
from bakery.domains.entities.order import (
    CreateOrderAsUser,
    OrderProduct,
)
from bakery.domains.entities.user import User
from bakery.domains.services.cart import CartService
from bakery.domains.services.delivery_cost import DeliveryCostService
from bakery.domains.services.order import OrderService
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import UserOrder


async def on_address_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["pickup_address_id"] = item_id
    await manager.switch_to(UserOrder.add_date)


async def on_manual_address_entered(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    text = (text or "").strip()
    if not text:
        return

    manager.dialog_data["pickup_address_name"] = text
    manager.dialog_data["has_pickup_address"] = True
    manager.dialog_data.pop("pickup_address_id", None)
    manager.show_mode = ShowMode.EDIT
    await manager.switch_to(UserOrder.add_date)
    await manager.show()


async def on_order_date_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["order_date"] = item_id
    await manager.switch_to(UserOrder.confirm)


async def on_confirm_order(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
    **_kwargs: Any,
) -> None:
    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    cart_service: CartService = await container.get(CartService)
    pickup_address_service: PickupAddressService = await container.get(
        PickupAddressService
    )
    delivery_cost_service: DeliveryCostService = await container.get(
        DeliveryCostService
    )
    uow: AbstractUow = await container.get(AbstractUow)
    user: User = manager.middleware_data["current_user"]

    order_date_iso = manager.dialog_data.get("order_date")
    if not order_date_iso:
        return
    delivered_at = date.fromisoformat(order_date_iso)

    pickup_address_id: str | None = manager.dialog_data.get("pickup_address_id")
    manual_address_name: str | None = manager.dialog_data.get("pickup_address_name")

    pickup_address_name: str | None = None
    delivery_price = 0
    products: list[OrderProduct] = []
    cart_total = 0

    async with uow:
        carts = await cart_service.get_list(
            input_dto=CartListParams(user_id=user.id, has_non_zero_quantity=True)
        )

        for cart in carts:
            name = cart.product.name
            price = cart.product.price
            qty = cart.quantity

            products.append(OrderProduct(name=name, price=price, quantity=qty))

            cart_total += price * qty

        if pickup_address_id:
            pickup_address = await pickup_address_service.get_by_id(
                input_id=UUID(pickup_address_id)
            )
            pickup_address_name = pickup_address.name
        else:
            pickup_address_name = manual_address_name

        is_city_delivery = (pickup_address_id is None) and bool(manual_address_name)
        if is_city_delivery:
            try:
                delivery_cost = await delivery_cost_service.get_last()
                delivery_price = delivery_cost.price
            except EntityNotFoundException:
                delivery_price = 0

    total_price = cart_total + delivery_price

    async with uow:
        await order_service.create(
            input_dto=CreateOrderAsUser(
                user_id=user.id,
                pickup_address_name=pickup_address_name or "",
                products=products,
                delivered_at=delivered_at,
                total_price=total_price,
                delivery_price=delivery_price,
            )
        )

    await manager.switch_to(UserOrder.finish)
