from collections import defaultdict
from datetime import date, timedelta
from typing import Any, cast
from uuid import UUID

from aiogram.types import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.api.protocols import DialogManager

from bakery.application.constants.common import USER_ORDERS_LIMIT_BREAKER
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order import (
    OrderListParams,
    OrderListWithUsersParams,
    OrderStatus,
)
from bakery.domains.services.order import OrderService
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.order import admin as admin_msg
from bakery.presenters.bot.dialogs.utils.order import combine_order_number


async def get_admin_delete_reason_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    return dict(
        product_name=dialog_manager.dialog_data.get("admin_selected_product_name")
        or "товар"
    )


async def get_admin_delete_confirm_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    return dict(
        product_name=dialog_manager.dialog_data.get("admin_selected_product_name")
        or "товар",
        reason=dialog_manager.dialog_data.get("admin_delete_reason") or "",
    )


async def get_admin_orders_dates_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    uow: AbstractUow = await container.get(AbstractUow)

    scope = dialog_manager.dialog_data.get("admin_order_scope", "current")
    today = date.today()
    yesterday = today - timedelta(days=1)

    async with uow:
        result = await order_service.get_list(
            input_dto=OrderListParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
            )
        )

    grouped: dict[date, list] = defaultdict(list)
    for order in result.items:
        if scope == "current":
            if order.delivered_at >= today:
                grouped[order.delivered_at].append(order)
        else:
            if order.delivered_at <= yesterday:
                grouped[order.delivered_at].append(order)

    items: list[dict[str, Any]] = []
    for delivered_at, orders in grouped.items():
        total_sum = sum(item.total_price for item in orders)
        items.append(
            dict(
                id=delivered_at.isoformat(),
                label=(
                    f"{delivered_at.strftime('%d.%m.%Y')} • "
                    f"{len(orders)} • {total_sum}₽"
                ),
                delivered_at=delivered_at,
            )
        )

    items.sort(
        key=lambda item: cast(date, item["delivered_at"]),
        reverse=(scope == "archive"),
    )

    return dict(
        dates=items,
        has_dates=bool(items),
        empty_text=admin_msg.NO_ORDERS,
    )


async def get_admin_order_date_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    uow: AbstractUow = await container.get(AbstractUow)

    date_raw = dialog_manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return dict(has_orders=False)
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return dict(has_orders=False)

    async with uow:
        result = await order_service.get_list(
            input_dto=OrderListParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
                delivered_at=selected_date,
            )
        )

    orders = list(result.items)
    total_sum = sum(item.total_price for item in orders)
    total_count = len(orders)

    products: dict[str, dict[str, Any]] = {}
    for order in orders:
        for item in order.products:
            if item.get("is_deleted", False):
                continue
            product_id = item["id"]
            if product_id not in products:
                products[product_id] = dict(
                    id=product_id,
                    name=item["name"],
                    quantity=0,
                )
            products[product_id]["quantity"] += item["quantity"]

    product_items = []
    product_index: dict[str, dict[str, str]] = {}
    for idx, product_item in enumerate(products.values(), start=1):
        idx_str = str(idx)
        product_items.append(
            dict(
                idx=idx_str,
                id=product_item["id"],
                name=product_item["name"],
                quantity=product_item["quantity"],
            )
        )
        product_index[idx_str] = dict(
            id=product_item["id"],
            name=product_item["name"],
        )
    dialog_manager.dialog_data["admin_product_index"] = product_index

    statuses = [item.status for item in orders]
    can_take_in_work = any(
        s in (OrderStatus.CREATED, OrderStatus.CHANGED) for s in statuses
    )
    can_start_delivery = any(s == OrderStatus.IN_PROGRESS for s in statuses)
    can_finish_delivery = any(s == OrderStatus.DELIVERING for s in statuses)

    can_edit_products = selected_date > date.today()

    return dict(
        has_orders=bool(orders),
        date=selected_date.strftime("%d.%m.%Y"),
        count=total_count,
        total_sum=total_sum,
        total=total_sum,
        products=product_items,
        has_products=bool(product_items),
        can_take_in_work=can_take_in_work,
        can_start_delivery=can_start_delivery,
        can_finish_delivery=can_finish_delivery,
        can_edit_products=can_edit_products,
    )


async def get_admin_user_orders_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    uow: AbstractUow = await container.get(AbstractUow)
    current_user = dialog_manager.middleware_data.get("current_user")
    if current_user is None:
        return dict(has_orders=False)

    date_raw = dialog_manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return dict(
            title=admin_msg.USER_ORDERS_TITLE.format(date="—"),
            orders=[],
            has_orders=False,
        )
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return dict(
            title=admin_msg.USER_ORDERS_TITLE.format(date="—"),
            orders=[],
            has_orders=False,
        )

    async with uow:
        items_with_users = await order_service.get_list_with_users_by_date(
            input_dto=OrderListWithUsersParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
                delivered_at=selected_date,
            ),
            user=current_user,
        )

    items = []
    for item in items_with_users:
        items.append(
            dict(
                id=str(item.order.id),
                number=combine_order_number(
                    item.order.delivered_at, item.order.delivered_at_id
                ),
                user_name=item.user.name,
                total=item.order.total_price,
            )
        )

    return dict(
        title=admin_msg.USER_ORDERS_TITLE.format(
            date=selected_date.strftime("%d.%m.%Y")
        ),
        orders=items,
        has_orders=bool(items),
    )


async def get_admin_deleted_orders_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    uow: AbstractUow = await container.get(AbstractUow)
    current_user = dialog_manager.middleware_data.get("current_user")
    if current_user is None:
        return dict(
            title=admin_msg.DELETED_ORDERS_TITLE.format(date="—"),
            orders=[],
            has_orders=False,
        )

    date_raw = dialog_manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return dict(
            title=admin_msg.DELETED_ORDERS_TITLE.format(date="—"),
            orders=[],
            has_orders=False,
        )
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return dict(
            title=admin_msg.DELETED_ORDERS_TITLE.format(date="—"),
            orders=[],
            has_orders=False,
        )

    async with uow:
        items_with_users = await order_service.get_list_with_users_by_date(
            input_dto=OrderListWithUsersParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
                delivered_at=selected_date,
            ),
            user=current_user,
        )

    items = []
    for item in items_with_users:
        if not any(p.get("is_deleted", False) for p in item.order.products):
            continue
        items.append(
            dict(
                id=str(item.order.id),
                number=combine_order_number(
                    item.order.delivered_at, item.order.delivered_at_id
                ),
                user_name=item.user.name,
                total=item.order.total_price,
            )
        )

    return dict(
        title=admin_msg.DELETED_ORDERS_TITLE.format(
            date=selected_date.strftime("%d.%m.%Y")
        ),
        orders=items,
        has_orders=bool(items),
    )


async def get_admin_user_order_data(  # noqa: C901
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    user_service: UserService = await container.get(UserService)
    uow: AbstractUow = await container.get(AbstractUow)

    order_id_raw = dialog_manager.dialog_data.get("selected_order_id")
    if isinstance(dialog_manager.start_data, dict):
        start_order_id = dialog_manager.start_data.get("selected_order_id")
        if not order_id_raw:
            order_id_raw = start_order_id
        admin_selected_date = dialog_manager.start_data.get("admin_selected_date")
        if admin_selected_date:
            dialog_manager.dialog_data["admin_selected_date"] = admin_selected_date
        admin_deleted_flow = dialog_manager.start_data.get("admin_deleted_flow")
        if admin_deleted_flow is not None:
            dialog_manager.dialog_data["admin_deleted_flow"] = admin_deleted_flow
    if not order_id_raw:
        return dict(has_order=False)
    try:
        order_uuid = UUID(order_id_raw)
    except ValueError:
        return dict(has_order=False)
    dialog_manager.dialog_data["selected_order_id"] = order_id_raw

    async with uow:
        try:
            order = await order_service.get_by_id(input_id=order_uuid)
        except EntityNotFoundException:
            return dict(has_order=False)
        try:
            user = await user_service.get_by_id(input_id=order.user_id)
        except EntityNotFoundException:
            return dict(has_order=False)

    number = combine_order_number(order.delivered_at, order.delivered_at_id)
    dialog_manager.dialog_data["selected_order_number"] = number
    products_text = []
    has_deleted_products = False
    for item in order.products:
        name = item.get("name") or "—"
        qty = int(item.get("quantity") or 0)
        price = int(item.get("price") or 0)
        text = f"{name} — {qty} × {price}"
        if item.get("is_deleted", False):
            text = f"<s>{text}</s>"
            has_deleted_products = True
        products_text.append(dict(text=text))
    return dict(
        has_order=True,
        number=number,
        order_number=number,
        delivered_at=order.delivered_at.strftime("%d.%m.%Y"),
        pickup_address_name=order.pickup_address_name,
        products_text=products_text,
        delivery_price=order.delivery_price,
        total_price=order.total_price,
        user_name=user.name,
        user_phone=user.phone,
        has_payment="есть" if order.payment_file_id else "нет",
        has_deleted_products=has_deleted_products,
        admin_deleted_flow=bool(dialog_manager.dialog_data.get("admin_deleted_flow")),
        has_payment_file=bool(order.payment_file_id),
        title=admin_msg.DELETED_ORDERS_TITLE.format(
            date=order.delivered_at.strftime("%d.%m.%Y")
        ),
        has_orders=any(item.get("is_deleted", False) for item in order.products),
        payment_file_attachment=(
            MediaAttachment(
                type=ContentType.PHOTO,
                file_id=MediaId(order.payment_file_id),
            )
            if order.payment_file_id
            else None
        ),
    )


async def get_admin_delete_order_reason_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    order_number = dialog_manager.dialog_data.get("selected_order_number") or "—"
    return dict(order_number=order_number)


async def get_admin_delete_order_confirm_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    order_number = dialog_manager.dialog_data.get("selected_order_number") or "—"
    reason = dialog_manager.dialog_data.get("admin_delete_order_reason") or ""
    return dict(order_number=order_number, reason=reason)
