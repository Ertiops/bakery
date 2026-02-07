from collections.abc import Sequence
from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.constants.common import PAGINATION_LIMIT_BREAKER
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order import Order, OrderProduct, OrderStatus, UpdateOrder
from bakery.domains.entities.pickup_address import PickupAddressListParams
from bakery.domains.entities.user import UserRole
from bakery.domains.services.delivery_cost import DeliveryCostService
from bakery.domains.services.order import OrderService
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.uow import AbstractUow


def get_order_edit_id(manager: DialogManager) -> str | None:
    data = manager.start_data
    if isinstance(data, dict):
        order_edit_id = data.get("order_edit_id")
        if order_edit_id:
            return order_edit_id
    return manager.dialog_data.get("order_edit_id")


async def update_order_products(
    manager: DialogManager,
    *,
    order_id: UUID,
    products: Sequence[OrderProduct],
) -> Order | None:
    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    order_service: OrderService = await container.get(OrderService)
    pickup_address_service: PickupAddressService = await container.get(
        PickupAddressService
    )
    delivery_cost_service: DeliveryCostService = await container.get(
        DeliveryCostService
    )
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return None

    async with uow:
        try:
            order = await order_service.get_by_id(input_id=order_id)
        except EntityNotFoundException:
            return None

        if current_user.role != UserRole.ADMIN:
            if order.status not in (OrderStatus.CREATED, OrderStatus.CHANGED):
                return None
        if current_user.role == UserRole.ADMIN:
            if not any(item.get("is_deleted", False) for item in order.products):
                return None

        cart_total = sum(
            item["price"] * item["quantity"]
            for item in products
            if not item.get("is_deleted", False)
        )
        delivery_price = await _calculate_delivery_price(
            pickup_address_service=pickup_address_service,
            delivery_cost_service=delivery_cost_service,
            pickup_address_name=order.pickup_address_name,
            pickup_address_id=order.pickup_address_id,
            cart_total=cart_total,
        )
        total_price = cart_total + delivery_price

        status = order.status
        if current_user.role != UserRole.ADMIN:
            status = OrderStatus.CHANGED

        order = await order_service.update_by_id(
            input_dto=UpdateOrder(
                id=order.id,
                products=products,
                total_price=total_price,
                delivery_price=delivery_price,
                status=status,
            ),
            user=current_user,
        )

    return order


async def update_order_products_admin(
    manager: DialogManager,
    *,
    order_id: UUID,
    products: Sequence[OrderProduct],
) -> Order | None:
    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    order_service: OrderService = await container.get(OrderService)
    pickup_address_service: PickupAddressService = await container.get(
        PickupAddressService
    )
    delivery_cost_service: DeliveryCostService = await container.get(
        DeliveryCostService
    )
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return None

    async with uow:
        try:
            order = await order_service.get_by_id(input_id=order_id)
        except EntityNotFoundException:
            return None

        if order.status in (
            OrderStatus.DELIVERED,
            OrderStatus.PAID,
            OrderStatus.CANCELLED,
        ):
            return None

        cart_total = sum(item["price"] * item["quantity"] for item in products)
        delivery_price = await _calculate_delivery_price(
            pickup_address_service=pickup_address_service,
            delivery_cost_service=delivery_cost_service,
            pickup_address_name=order.pickup_address_name,
            pickup_address_id=order.pickup_address_id,
            cart_total=cart_total,
        )
        total_price = cart_total + delivery_price

        status = order.status
        if status in (OrderStatus.CREATED, OrderStatus.CHANGED):
            status = OrderStatus.CHANGED

        order = await order_service.update_by_id(
            input_dto=UpdateOrder(
                id=order.id,
                products=products,
                total_price=total_price,
                delivery_price=delivery_price,
                status=status,
            ),
            user=current_user,
        )

    return order


async def _calculate_delivery_price(
    *,
    pickup_address_service: PickupAddressService,
    delivery_cost_service: DeliveryCostService,
    pickup_address_name: str,
    pickup_address_id: UUID | None,
    cart_total: int,
) -> int:
    if cart_total <= 0:
        return 0

    is_pickup = bool(pickup_address_id)
    if not is_pickup:
        is_pickup = await _is_pickup_address(
            pickup_address_service=pickup_address_service,
            pickup_address_name=pickup_address_name,
        )
    if is_pickup:
        return 0

    try:
        cost = await delivery_cost_service.get_last()
    except EntityNotFoundException:
        return 0

    delivery_price = cost.price
    if (
        cost.free_delivery_amount is not None
        and cart_total >= cost.free_delivery_amount
    ):
        delivery_price = 0
    return delivery_price


async def _is_pickup_address(
    *,
    pickup_address_service: PickupAddressService,
    pickup_address_name: str,
) -> bool:
    if not pickup_address_name:
        return False

    pickup_addresses = await pickup_address_service.get_list(
        input_dto=PickupAddressListParams(
            limit=PAGINATION_LIMIT_BREAKER,
            offset=0,
        )
    )
    return any(item.name == pickup_address_name for item in pickup_addresses.items)
