import logging
from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.application.constants.cart import CART_PRODUCT_MAX
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.cart import CreateCart
from bakery.domains.entities.order import OrderProduct, OrderStatus
from bakery.domains.entities.user import User, UserRole
from bakery.domains.services.cart import CartService
from bakery.domains.services.order import OrderService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import UserCatalogue
from bakery.presenters.bot.dialogs.utils.order_edit import (
    get_order_edit_id,
    update_order_products,
)
from bakery.presenters.bot.dialogs.utils.order_for_user import get_order_for_user_id

log = logging.getLogger(__name__)


async def on_view_product_clicked(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    start_data = manager.start_data if isinstance(manager.start_data, dict) else {}
    category = manager.dialog_data.get("category") or start_data.get("category")
    order_edit_id = get_order_edit_id(manager)
    admin_order_edit = bool(
        manager.dialog_data.get("admin_order_edit")
        or start_data.get("admin_order_edit")
    )
    admin_selected_date = manager.dialog_data.get(
        "admin_selected_date"
    ) or start_data.get("admin_selected_date")
    admin_deleted_flow = (
        manager.dialog_data.get("admin_deleted_flow")
        if manager.dialog_data.get("admin_deleted_flow") is not None
        else start_data.get("admin_deleted_flow")
    )
    order_for_user_id = manager.dialog_data.get("order_for_user_id") or start_data.get(
        "order_for_user_id"
    )
    admin_fake_user = bool(
        manager.dialog_data.get("admin_fake_user") or start_data.get("admin_fake_user")
    )
    manager.dialog_data["product_id"] = item_id
    if category:
        manager.dialog_data["category"] = category

    data = dict(product_id=item_id, category=category)
    if order_edit_id:
        data["order_edit_id"] = order_edit_id
    if admin_order_edit:
        data["admin_order_edit"] = True
    if admin_selected_date:
        data["admin_selected_date"] = admin_selected_date
    if admin_deleted_flow is not None:
        data["admin_deleted_flow"] = admin_deleted_flow
    if order_for_user_id:
        data["order_for_user_id"] = order_for_user_id
    if admin_fake_user:
        data["admin_fake_user"] = True

    await manager.start(
        state=UserCatalogue.view_single_product,
        data=data,
    )


async def update_quantity(
    callback: CallbackQuery,
    manager: DialogManager,
    delta: int,
) -> None:
    order_edit_id = get_order_edit_id(manager)
    if order_edit_id:
        updated = await _update_order_item_quantity(
            manager=manager,
            order_edit_id=order_edit_id,
            delta=delta,
        )
        if not updated:
            await callback.answer("Нельзя изменить заказ в работе.")
        return

    container = manager.middleware_data["dishka_container"]
    service: CartService = await container.get(CartService)
    uow: AbstractUow = await container.get(AbstractUow)

    product_id = UUID(manager.dialog_data["product_id"])
    quantity = max(0, manager.dialog_data.get("quantity", 0) + delta)
    manager.dialog_data["quantity"] = quantity
    if quantity < 0 or quantity > CART_PRODUCT_MAX:
        return
    user_id = get_order_for_user_id(manager)
    async with uow:
        await service.create_or_update(
            input_dto=CreateCart(
                user_id=user_id, product_id=product_id, quantity=quantity
            )
        )
    await manager.show()


async def on_increment_quantity(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await update_quantity(callback, manager, delta=1)


async def on_decrement_quantity(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await update_quantity(callback, manager, delta=-1)


async def _update_order_item_quantity(  # noqa: C901
    *,
    manager: DialogManager,
    order_edit_id: str,
    delta: int,
) -> bool:
    try:
        order_uuid = UUID(order_edit_id)
    except ValueError:
        return False

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    uow: AbstractUow = await container.get(AbstractUow)

    product_id = UUID(manager.dialog_data["product_id"])

    async with uow:
        try:
            order = await order_service.get_by_id(input_id=order_uuid)
        except EntityNotFoundException:
            return False

    current_user: User = manager.middleware_data["current_user"]
    if current_user.role != UserRole.ADMIN:
        if order.status not in (OrderStatus.CREATED, OrderStatus.CHANGED):
            return False

    if current_user.role == UserRole.ADMIN:
        if not any(item.get("is_deleted", False) for item in order.products):
            return False

    product_id_str = str(product_id)
    current_qty = 0
    current_item = None
    for item in order.products:
        if item.get("is_deleted", False):
            continue
        if item["id"] == product_id_str:
            current_qty = item["quantity"]
            current_item = item
            break

    quantity = max(0, current_qty + delta)
    quantity = min(quantity, CART_PRODUCT_MAX)

    name = manager.dialog_data.get("original_name")
    price = manager.dialog_data.get("original_price")
    if current_item:
        name = name or current_item["name"]
        if price is None:
            price = current_item["price"]

    if name is None or price is None:
        return False

    updated_products: list[OrderProduct] = []
    found = False
    for item in order.products:
        if item["id"] == product_id_str and not item.get("is_deleted", False):
            found = True
            if quantity > 0:
                updated_products.append(
                    _make_order_product(
                        product_id=product_id_str,
                        name=name,
                        price=price,
                        quantity=quantity,
                    )
                )
        else:
            updated_products.append(item)

    if not found and quantity > 0:
        updated_products.append(
            _make_order_product(
                product_id=product_id_str,
                name=name,
                price=price,
                quantity=quantity,
            )
        )

    updated = await update_order_products(
        manager,
        order_id=order_uuid,
        products=updated_products,
    )
    if not updated:
        return False

    manager.dialog_data["quantity"] = quantity
    await manager.show()
    return True


def _make_order_product(
    *,
    product_id: str,
    name: str,
    price: int,
    quantity: int,
) -> OrderProduct:
    return OrderProduct(
        id=product_id,
        name=name,
        price=price,
        quantity=quantity,
        is_deleted=False,
    )
