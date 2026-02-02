from typing import Any
from uuid import UUID

from aiogram.types import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order import OrderStatus
from bakery.domains.services.feedback_group import FeedbackGroupService
from bakery.domains.services.order import OrderService
from bakery.domains.services.order_payment import OrderPaymentService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.utils.order import combine_order_number
from bakery.presenters.bot.utils.text import display_list


def _get_order_id_from_start_or_dialog(manager: DialogManager) -> str | None:
    start_data = getattr(manager, "start_data", None) or {}
    order_id = start_data.get("selected_order_id") or manager.dialog_data.get(
        "selected_order_id"
    )
    if order_id:
        manager.dialog_data["selected_order_id"] = order_id
    return order_id


async def get_order_payment_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    order_service: OrderService = await container.get(OrderService)
    order_payment_service: OrderPaymentService = await container.get(
        OrderPaymentService
    )
    feedback_group_service: FeedbackGroupService = await container.get(
        FeedbackGroupService
    )

    order_id_raw = _get_order_id_from_start_or_dialog(dialog_manager)
    dialog_manager.dialog_data["order_id"] = order_id_raw
    if not order_id_raw:
        return {"has_order": False, "has_requisites": False, "has_payment_file": False}

    try:
        order_uuid = UUID(order_id_raw)
    except ValueError:
        return {"has_order": False, "has_requisites": False, "has_payment_file": False}

    async with uow:
        try:
            order = await order_service.get_by_id(input_id=order_uuid)
        except EntityNotFoundException:
            return {
                "has_order": False,
                "has_requisites": False,
                "has_payment_file": False,
            }

        try:
            requisites = await order_payment_service.get_last()
            has_requisites = True
        except EntityNotFoundException:
            requisites = None
            has_requisites = False

        try:
            feedback_group = await feedback_group_service.get_last()
        except EntityNotFoundException:
            feedback_group = None

    delivered_at = order.delivered_at
    number = (
        combine_order_number(delivered_at, order.delivered_at_id)
        if delivered_at
        else ""
    )

    file_id = dialog_manager.dialog_data.get("payment_file_id")
    file_name = dialog_manager.dialog_data.get("payment_file_name")
    payment_file_attachment = (
        MediaAttachment(
            type=ContentType.PHOTO if file_name == "Фото" else ContentType.DOCUMENT,
            file_id=MediaId(file_id),
        )
        if file_id
        else None
    )
    if "order_rating" not in dialog_manager.dialog_data and order.rating is not None:
        dialog_manager.dialog_data["order_rating"] = order.rating
    rating_raw = dialog_manager.dialog_data.get("order_rating", 5)
    try:
        rating = int(rating_raw)
    except (TypeError, ValueError):
        rating = 5
    rating = max(1, min(5, rating))
    dialog_manager.dialog_data["order_rating"] = rating

    return dict(
        has_order=True,
        order_id=str(order.id),
        number=number,
        total_price=order.total_price,
        is_delivered=(order.status == OrderStatus.DELIVERED),
        has_requisites=has_requisites,
        phone=(requisites.phone if requisites else ""),
        banks=(display_list(requisites.banks) if requisites else ""),
        addressee=(requisites.addressee if requisites else ""),
        payment_file_id=file_id,
        payment_file_name=file_name or "Файл",
        has_payment_file=bool(file_id),
        payment_file_attachment=payment_file_attachment,
        rating=rating,
        feedback_group_url=(feedback_group.url if feedback_group else ""),
        has_feedback_group=bool(feedback_group),
    )
