from uuid import UUID

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.application.entities import Unset
from bakery.domains.entities.order_payment import CreateOrderPayment, UpdateOrderPayment
from bakery.domains.services.order_payment import OrderPaymentService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminOrderPayment
from bakery.presenters.bot.utils.text import (
    UNSET_MARK,
    extract_list,
    extract_text,
    normalize_text,
    split_items,
)


async def admin_order_payment_start_create(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["order_payment_mode"] = "create"
    manager.dialog_data.pop("order_payment_id", None)

    manager.dialog_data.pop("order_payment_phone_value", None)
    manager.dialog_data.pop("order_payment_banks_value", None)
    manager.dialog_data.pop("order_payment_addressee_value", None)

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
    manager.dialog_data["order_payment_phone_value"] = op.phone
    manager.dialog_data["order_payment_banks_value"] = list(op.banks)
    manager.dialog_data["order_payment_addressee_value"] = op.addressee
    manager.dialog_data["order_payment_original_phone_value"] = op.phone
    manager.dialog_data["order_payment_original_banks_value"] = list(op.banks)
    manager.dialog_data["order_payment_original_addressee_value"] = op.addressee

    await manager.switch_to(AdminOrderPayment.phone)


async def admin_order_payment_back_to_view(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(AdminOrderPayment.view)


async def admin_order_payment_on_phone_input(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    if message.content_type != ContentType.TEXT:
        return
    value = normalize_text(message.text)
    if not value:
        return
    manager.dialog_data["order_payment_phone_value"] = value
    await manager.switch_to(AdminOrderPayment.banks)


async def admin_order_payment_skip_phone_input(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["order_payment_phone_value"] = UNSET_MARK
    await manager.switch_to(AdminOrderPayment.banks)


async def admin_order_payment_on_banks_input(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    if message.content_type != ContentType.TEXT:
        return
    items = split_items(message.text)
    if not items:
        return
    manager.dialog_data["order_payment_banks_value"] = items
    await manager.switch_to(AdminOrderPayment.addressee)


async def admin_order_payment_skip_banks_input(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["order_payment_banks_value"] = UNSET_MARK
    await manager.switch_to(AdminOrderPayment.addressee)


async def admin_order_payment_on_addressee_input(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    if message.content_type != ContentType.TEXT:
        return
    value = normalize_text(message.text)
    if not value:
        return
    manager.dialog_data["order_payment_addressee_value"] = value
    await manager.switch_to(AdminOrderPayment.confirm)


async def admin_order_payment_skip_addressee_input(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["order_payment_addressee_value"] = UNSET_MARK
    await manager.switch_to(AdminOrderPayment.confirm)


async def admin_order_payment_go_to_confirm(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    if (
        manager.dialog_data.get("order_payment_phone_value")
        and manager.dialog_data.get("order_payment_banks_value")
        and manager.dialog_data.get("order_payment_addressee_value")
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

    mode = manager.dialog_data.get("order_payment_mode", "create")

    async with uow:
        if mode == "update":
            phone = extract_text(manager.dialog_data.get("order_payment_phone_value"))
            banks = extract_list(manager.dialog_data.get("order_payment_banks_value"))
            addressee = extract_text(
                manager.dialog_data.get("order_payment_addressee_value")
            )
            if isinstance(phone, Unset):
                phone = normalize_text(
                    manager.dialog_data.get("order_payment_original_phone_value")
                )
            if isinstance(banks, Unset):
                banks = extract_list(
                    manager.dialog_data.get("order_payment_original_banks_value")
                )
            if isinstance(addressee, Unset):
                addressee = normalize_text(
                    manager.dialog_data.get("order_payment_original_addressee_value")
                )
            order_payment_id = manager.dialog_data.get("order_payment_id")
            if not order_payment_id:
                return
            await service.update_by_id(
                input_dto=UpdateOrderPayment(
                    id=UUID(order_payment_id),
                    phone=phone,
                    banks=banks,
                    addressee=addressee,
                )
            )
        else:
            phone = normalize_text(manager.dialog_data.get("order_payment_phone_value"))
            banks = extract_list(manager.dialog_data.get("order_payment_banks_value"))
            addressee = normalize_text(
                manager.dialog_data.get("order_payment_addressee_value")
            )

            if not phone or not addressee or not banks or isinstance(banks, Unset):
                return
            await service.create(
                input_dto=CreateOrderPayment(
                    phone=phone,
                    banks=banks,
                    addressee=addressee,
                )
            )

    await manager.switch_to(AdminOrderPayment.view)
