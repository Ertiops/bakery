from uuid import UUID

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order import OrderStatus, UpdateOrder
from bakery.domains.services.order import OrderService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import UserOrderPayment


async def back_to_previous_dialog(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.done()


async def on_payment_file_received(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    file_id: str | None = None
    file_name: str | None = None

    if message.photo:
        file_id = message.photo[-1].file_id
        file_name = "Фото"
        manager.dialog_data["payment_file_type"] = ContentType.PHOTO
    elif message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name or "Документ"
        manager.dialog_data["payment_file_type"] = ContentType.DOCUMENT
    else:
        return

    manager.dialog_data["payment_file_id"] = file_id
    manager.dialog_data["payment_file_name"] = file_name

    await manager.switch_to(UserOrderPayment.confirm)


async def to_payment_finish(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    order_id_raw = manager.dialog_data.get("order_id")
    payment_file_id = manager.dialog_data.get("payment_file_id")
    if not order_id_raw:
        return
    try:
        order_uuid = UUID(order_id_raw)
    except ValueError:
        return
    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    order_service: OrderService = await container.get(OrderService)

    async with uow:
        try:
            order = await order_service.get_by_id(input_id=order_uuid)
        except EntityNotFoundException:
            return

        await order_service.update_by_id(
            input_dto=UpdateOrder(
                id=order.id,
                status=OrderStatus.PAID,
                payment_file_id=payment_file_id,  # type: ignore[arg-type]
            )
        )

    await manager.switch_to(UserOrderPayment.finish)
