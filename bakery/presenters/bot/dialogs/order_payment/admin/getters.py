from typing import Any

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.services.order_payment import OrderPaymentService
from bakery.domains.uow import AbstractUow


async def get_admin_order_payment_view_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: OrderPaymentService = await container.get(OrderPaymentService)

    async with uow:
        try:
            op = await service.get_last()
        except EntityNotFoundException:
            return dict(
                has_order_payment=False,
                order_payment_id=None,
                phone="",
                bank="",
                addressee="",
            )

    return dict(
        has_order_payment=True,
        order_payment_id=str(op.id),
        phone=op.phone,
        bank=op.bank,
        addressee=op.addressee,
    )


async def get_admin_order_payment_edit_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    return dict(
        mode=dialog_manager.dialog_data.get("order_payment_mode", "create"),
        order_payment_id=dialog_manager.dialog_data.get("order_payment_id"),
        phone=dialog_manager.dialog_data.get("order_payment_phone", ""),
        bank=dialog_manager.dialog_data.get("order_payment_bank", ""),
        addressee=dialog_manager.dialog_data.get("order_payment_addressee", ""),
        has_phone=bool(dialog_manager.dialog_data.get("order_payment_phone")),
        has_bank=bool(dialog_manager.dialog_data.get("order_payment_bank")),
        has_addressee=bool(dialog_manager.dialog_data.get("order_payment_addressee")),
    )
