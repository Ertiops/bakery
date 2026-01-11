from datetime import date
from typing import Any
from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.constants.common import PAGINATION_LIMIT_BREAKER
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.cart import CartListParams
from bakery.domains.entities.pickup_address import PickupAddressListParams
from bakery.domains.entities.user import User
from bakery.domains.services.cart import CartService
from bakery.domains.services.delivery_cost import DeliveryCostService
from bakery.domains.services.order_schedule import OrderScheduleService
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.uow import AbstractUow


async def get_pickup_address_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    pickup_address_service: PickupAddressService = await container.get(
        PickupAddressService
    )
    delivery_cost_service: DeliveryCostService = await container.get(
        DeliveryCostService
    )
    uow = await container.get(AbstractUow)
    async with uow:
        pickup_addresses = await pickup_address_service.get_list(
            input_dto=PickupAddressListParams(
                limit=PAGINATION_LIMIT_BREAKER,
                offset=0,
            )
        )
        try:
            cost = await delivery_cost_service.get_last()
            delivery_cost = cost.price
        except EntityNotFoundException:
            delivery_cost = 0

    return dict(
        addresses=[
            dict(id=str(pickup_address.id), name=pickup_address.name)
            for pickup_address in pickup_addresses.items
        ],
        has_addresses=bool(pickup_addresses.items),
        delivery_cost=delivery_cost,
    )


async def get_order_confirm_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    cart_service: CartService = await container.get(CartService)
    pickup_address_service: PickupAddressService = await container.get(
        PickupAddressService
    )
    delivery_cost_service: DeliveryCostService = await container.get(
        DeliveryCostService
    )

    user: User = dialog_manager.middleware_data["current_user"]
    pickup_address_id: str | None = dialog_manager.dialog_data.get("pickup_address_id")

    cart_items: list[dict[str, Any]] = []
    total = 0
    pickup_address_name: str | None = dialog_manager.dialog_data.get(
        "pickup_address_name"
    )

    async with uow:
        carts = await cart_service.get_list(
            input_dto=CartListParams(
                user_id=user.id,
                has_non_zero_quantity=True,
            )
        )

        for cart in carts:
            price = cart.product.price
            qty = cart.quantity
            subtotal = price * qty
            total += subtotal

            cart_items.append(
                dict(
                    id=str(cart.product.id),
                    name=cart.product.name,
                    price=price,
                    qty=qty,
                    subtotal=subtotal,
                )
            )
        try:
            cost = await delivery_cost_service.get_last()
            delivery_cost = cost.price
        except EntityNotFoundException:
            delivery_cost = 0

    is_city_delivery = dialog_manager.dialog_data.get(
        "pickup_address_id"
    ) is None and bool(pickup_address_name)

    total = total + (delivery_cost if is_city_delivery else 0)

    if pickup_address_id:
        async with uow:
            result = await pickup_address_service.get_by_id(
                input_id=UUID(pickup_address_id)
            )
        pickup_address_name = result.name
    order_date_iso = dialog_manager.dialog_data.get("order_date")

    order_date_label = None
    if order_date_iso:
        order_date_label = date.fromisoformat(order_date_iso).strftime("%d.%m.%Y")
    return dict(
        pickup_address_id=pickup_address_id,
        pickup_address_name=pickup_address_name,
        has_pickup_address=bool(pickup_address_name),
        cart_items=cart_items,
        has_cart_items=bool(cart_items),
        order_date=order_date_iso,
        order_date_label=order_date_label,
        has_order_date=bool(order_date_label),
        total=total,
        delivery_cost=delivery_cost,
        is_city_delivery=is_city_delivery,
    )


async def get_available_order_dates(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    order_schedule_service: OrderScheduleService = await container.get(
        OrderScheduleService
    )
    async with uow:
        try:
            dates = await order_schedule_service.get_available_order_dates()
        except EntityNotFoundException:
            dates = []

    items = [{"id": d.isoformat(), "label": d.strftime("%d.%m.%Y")} for d in dates]

    return dict(
        order_dates=items,
        has_order_dates=bool(items),
    )
