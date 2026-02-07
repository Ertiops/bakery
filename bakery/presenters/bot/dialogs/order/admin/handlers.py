from datetime import date
from uuid import UUID

from aiogram.types import BufferedInputFile, CallbackQuery, Message
from aiogram_dialog import ShowMode
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bakery.application.constants.common import USER_ORDERS_LIMIT_BREAKER
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order import (
    DeleteOrderParams,
    OrderListByDateWithProductParams,
    OrderListParams,
    OrderStatus,
    UpdateOrder,
)
from bakery.domains.interfaces.adapters.order_report_pdf import IOrderReportPdfAdapter
from bakery.domains.services.order import OrderService
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.order import user as user_msg
from bakery.presenters.bot.dialogs.states import AdminOrders, UserCatalogue
from bakery.presenters.bot.dialogs.utils.order import combine_order_number


async def select_admin_orders_scope(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager,
    scope: str,
) -> None:
    manager.dialog_data["admin_order_scope"] = scope
    await manager.switch_to(AdminOrders.view_dates)


async def on_admin_date_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["admin_selected_date"] = item_id
    await manager.switch_to(AdminOrders.view_date)


async def back_to_categories(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminOrders.view_categories)


async def back_to_dates(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminOrders.view_dates)


async def back_to_date_view(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminOrders.view_date)


async def on_take_in_work(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    date_raw = manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        result = await order_service.get_list(
            input_dto=OrderListParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
                delivered_at=selected_date,
            )
        )
        update_items = [
            UpdateOrder(id=order.id, status=OrderStatus.IN_PROGRESS)
            for order in result.items
            if order.status in (OrderStatus.CREATED, OrderStatus.CHANGED)
        ]
        if update_items:
            await order_service.update_list(input_dto=update_items)
    await manager.show()


async def on_start_delivery(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    date_raw = manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    user_service: UserService = await container.get(UserService)
    uow: AbstractUow = await container.get(AbstractUow)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    async with uow:
        result = await order_service.get_list(
            input_dto=OrderListParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
                delivered_at=selected_date,
            )
        )
        for order in result.items:
            if order.status == OrderStatus.IN_PROGRESS:
                await order_service.update_by_id(
                    input_dto=UpdateOrder(id=order.id, status=OrderStatus.DELIVERING),
                    user=current_user,
                )
                try:
                    user = await user_service.get_by_id(input_id=order.user_id)
                except EntityNotFoundException:
                    continue
                bot = callback.bot
                if bot is None:
                    return
                await bot.send_message(
                    chat_id=user.tg_id,
                    text=user_msg.DELIVERY_STARTED.format(
                        order_number=combine_order_number(
                            order.delivered_at, order.delivered_at_id
                        )
                    ),
                )
    await manager.show()


async def on_finish_delivery(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    date_raw = manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    user_service: UserService = await container.get(UserService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        result = await order_service.get_list(
            input_dto=OrderListParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
                delivered_at=selected_date,
            )
        )
        update_items = [
            UpdateOrder(id=order.id, status=OrderStatus.DELIVERED)
            for order in result.items
            if order.status == OrderStatus.DELIVERING
        ]
        if update_items:
            updated_orders = await order_service.update_list(input_dto=update_items)
            for order in updated_orders:
                try:
                    user = await user_service.get_by_id(input_id=order.user_id)
                except EntityNotFoundException:
                    continue
                bot = callback.bot
                if bot is None:
                    return
                await bot.send_message(
                    chat_id=user.tg_id,
                    text=user_msg.ORDER_DELIVERED,
                )
    await manager.show()


async def on_admin_product_delete_select(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str | None = None,
) -> None:
    await _select_admin_product_delete(
        manager, item_id or getattr(manager, "item_id", None)
    )


async def on_admin_product_delete_button(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    _ = callback
    _ = button
    await _select_admin_product_delete(manager, getattr(manager, "item_id", None))


async def _select_admin_product_delete(
    manager: DialogManager,
    item_id: str | None,
) -> None:
    if not item_id:
        return
    product_index = manager.dialog_data.get("admin_product_index") or {}
    item = product_index.get(str(item_id))
    if not item:
        return
    manager.dialog_data["admin_selected_product_id"] = item["id"]
    manager.dialog_data["admin_selected_product_name"] = item["name"]
    manager.dialog_data["product_name"] = item["name"]
    await manager.switch_to(AdminOrders.delete_reason)


async def on_admin_delete_reason_input(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    reason = (text or "").strip()
    if not reason:
        return
    manager.dialog_data["admin_delete_reason"] = reason
    await manager.switch_to(AdminOrders.delete_confirm)


async def on_admin_delete_confirm(  # noqa: C901
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    reason = (manager.dialog_data.get("admin_delete_reason") or "").strip()
    if not reason:
        return

    date_raw = manager.dialog_data.get("admin_selected_date")
    product_id_raw = manager.dialog_data.get("admin_selected_product_id")
    product_name = (
        manager.dialog_data.get("admin_selected_product_name")
        or user_msg.PRODUCT_NAME_FALLBACK
    )
    if not date_raw or not product_id_raw:
        return
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return
    try:
        product_uuid = UUID(product_id_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    user_service: UserService = await container.get(UserService)
    uow: AbstractUow = await container.get(AbstractUow)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    async with uow:
        updated_orders = await order_service.remove_product_from_orders_by_date(
            input_dto=OrderListByDateWithProductParams(
                limit=USER_ORDERS_LIMIT_BREAKER,
                offset=0,
                delivered_at=selected_date,
                product_id=product_uuid,
            ),
            user=current_user,
        )
        user_tg_by_id: dict[str, int] = {}
        for order in updated_orders:
            try:
                user = await user_service.get_by_id(input_id=order.user_id)
            except EntityNotFoundException:
                continue
            user_tg_by_id[str(order.user_id)] = user.tg_id

    for order in updated_orders:
        user_tg_id = user_tg_by_id.get(str(order.user_id))
        if not user_tg_id:
            continue
        order_number = combine_order_number(order.delivered_at, order.delivered_at_id)
        bot = callback.bot
        if bot is None:
            return
        await bot.send_message(
            chat_id=user_tg_id,
            text=user_msg.ORDER_PRODUCT_REMOVED.format(
                order_number=order_number,
                product_name=product_name,
                reason=reason,
            ),
        )

    manager.dialog_data.pop("admin_selected_product_id", None)
    manager.dialog_data.pop("admin_selected_product_name", None)
    manager.dialog_data.pop("admin_delete_reason", None)
    manager.show_mode = ShowMode.EDIT
    await manager.switch_to(AdminOrders.view_date)
    await manager.show()


async def on_view_user_orders(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    manager.dialog_data["admin_deleted_flow"] = False
    await manager.switch_to(AdminOrders.view_user_orders)


async def on_view_deleted_orders(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    manager.dialog_data["admin_deleted_flow"] = True
    await manager.switch_to(AdminOrders.view_deleted_orders)


async def on_view_products(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminOrders.view_products)


async def on_add_products_to_order(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    order_id = manager.dialog_data.get("selected_order_id")
    if not order_id:
        return
    admin_selected_date = manager.dialog_data.get("admin_selected_date")
    manager.dialog_data["admin_order_edit"] = True
    await manager.start(
        state=UserCatalogue.select_category,
        data={
            "order_edit_id": order_id,
            "admin_order_edit": True,
            "admin_selected_date": admin_selected_date,
            "admin_deleted_flow": True,
        },
        mode=StartMode.RESET_STACK,
    )


async def on_admin_delete_order_start(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    await manager.switch_to(AdminOrders.delete_order_reason)


async def on_admin_delete_order_reason_input(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    reason = (text or "").strip()
    if not reason:
        return
    manager.dialog_data["admin_delete_order_reason"] = reason
    await manager.switch_to(AdminOrders.delete_order_confirm)


async def on_admin_delete_order_confirm(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = button
    reason = (manager.dialog_data.get("admin_delete_order_reason") or "").strip()
    if not reason:
        return
    order_id_raw = manager.dialog_data.get("selected_order_id")
    if not order_id_raw:
        return
    try:
        order_uuid = UUID(order_id_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    user_service: UserService = await container.get(UserService)
    uow: AbstractUow = await container.get(AbstractUow)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    async with uow:
        try:
            order = await order_service.get_by_id(input_id=order_uuid)
        except EntityNotFoundException:
            return
        try:
            user = await user_service.get_by_id(input_id=order.user_id)
        except EntityNotFoundException:
            return
        await order_service.delete_by_id(
            input_dto=DeleteOrderParams(id=order.id, reason=reason),
            user=current_user,
        )

    bot = callback.bot
    if bot is None:
        return
    await bot.send_message(
        chat_id=user.tg_id,
        text=user_msg.ORDER_DELETED.format(
            order_number=combine_order_number(
                order.delivered_at, order.delivered_at_id
            ),
            reason=reason,
        ),
    )

    manager.dialog_data.pop("admin_delete_order_reason", None)
    await manager.switch_to(AdminOrders.view_deleted_orders)


async def on_user_order_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["selected_order_id"] = item_id
    await manager.switch_to(AdminOrders.view_user_order)


async def on_download_order_pdf(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    date_raw = manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    pdf_adapter: IOrderReportPdfAdapter = await container.get(IOrderReportPdfAdapter)
    uow: AbstractUow = await container.get(AbstractUow)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    bot = callback.bot
    if bot is None:
        return

    async with uow:
        pdf_bytes = await order_service.build_order_report_pdf(
            delivered_at=selected_date,
            pdf_adapter=pdf_adapter,
            limit=USER_ORDERS_LIMIT_BREAKER,
            user=current_user,
        )
    await bot.send_document(
        chat_id=callback.from_user.id,
        document=BufferedInputFile(pdf_bytes, filename="order.pdf"),
    )


async def on_download_delivery_pdf(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    date_raw = manager.dialog_data.get("admin_selected_date")
    if not date_raw:
        return
    try:
        selected_date = date.fromisoformat(date_raw)
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    order_service: OrderService = await container.get(OrderService)
    pdf_adapter: IOrderReportPdfAdapter = await container.get(IOrderReportPdfAdapter)
    uow: AbstractUow = await container.get(AbstractUow)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    bot = callback.bot
    if bot is None:
        return

    async with uow:
        pdf_bytes = await order_service.build_delivery_report_pdf(
            delivered_at=selected_date,
            pdf_adapter=pdf_adapter,
            limit=USER_ORDERS_LIMIT_BREAKER,
            user=current_user,
        )
    await bot.send_document(
        chat_id=callback.from_user.id,
        document=BufferedInputFile(pdf_bytes, filename="delivery_report.pdf"),
    )
