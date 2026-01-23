from uuid import UUID

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.domains.entities.order_payment import CreateOrderPayment, UpdateOrderPayment
from bakery.domains.services.order_payment import OrderPaymentService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminOrderPayment


def _normalize_text(text: str | None) -> str:
    return (text or "").strip()


async def admin_order_payment_start_create(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["order_payment_mode"] = "create"
    manager.dialog_data.pop("order_payment_id", None)

    manager.dialog_data.pop("order_payment_phone", None)
    manager.dialog_data.pop("order_payment_bank", None)
    manager.dialog_data.pop("order_payment_addressee", None)

    await manager.switch_to(AdminOrderPayment.phone)


async def admin_order_payment_start_update(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: OrderPaymentService = await container.get(OrderPaymentService)

    async with uow:
        op = await service.get_last()

    manager.dialog_data["order_payment_mode"] = "update"
    manager.dialog_data["order_payment_id"] = str(op.id)
    manager.dialog_data["order_payment_phone"] = op.phone
    manager.dialog_data["order_payment_bank"] = op.bank
    manager.dialog_data["order_payment_addressee"] = op.addressee

    await manager.switch_to(AdminOrderPayment.phone)


async def admin_order_payment_back_to_view(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(AdminOrderPayment.view)


async def admin_order_payment_on_phone(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    if message.content_type != ContentType.TEXT:
        return
    value = _normalize_text(message.text)
    if not value:
        return
    manager.dialog_data["order_payment_phone"] = value
    await manager.switch_to(AdminOrderPayment.bank)


async def admin_order_payment_on_bank(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    if message.content_type != ContentType.TEXT:
        return
    value = _normalize_text(message.text)
    if not value:
        return
    manager.dialog_data["order_payment_bank"] = value
    await manager.switch_to(AdminOrderPayment.addressee)


async def admin_order_payment_on_addressee(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    if message.content_type != ContentType.TEXT:
        return
    value = _normalize_text(message.text)
    if not value:
        return
    manager.dialog_data["order_payment_addressee"] = value
    await manager.switch_to(AdminOrderPayment.confirm)


async def admin_order_payment_to_confirm(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if (
        manager.dialog_data.get("order_payment_phone")
        and manager.dialog_data.get("order_payment_bank")
        and manager.dialog_data.get("order_payment_addressee")
    ):
        await manager.switch_to(AdminOrderPayment.confirm)


async def admin_order_payment_save(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: OrderPaymentService = await container.get(OrderPaymentService)

    phone = _normalize_text(manager.dialog_data.get("order_payment_phone"))
    bank = _normalize_text(manager.dialog_data.get("order_payment_bank"))
    addressee = _normalize_text(manager.dialog_data.get("order_payment_addressee"))

    if not (phone and bank and addressee):
        return

    mode = manager.dialog_data.get("order_payment_mode", "create")

    async with uow:
        if mode == "update":
            order_payment_id = manager.dialog_data.get("order_payment_id")
            if not order_payment_id:
                return
            await service.update_by_id(
                input_dto=UpdateOrderPayment(
                    id=UUID(order_payment_id),
                    phone=phone,
                    bank=bank,
                    addressee=addressee,
                )
            )
        else:
            await service.create(
                input_dto=CreateOrderPayment(
                    phone=phone,
                    bank=bank,
                    addressee=addressee,
                )
            )

    await manager.switch_to(AdminOrderPayment.view)
