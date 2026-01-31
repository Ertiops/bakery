from collections.abc import Sequence
from typing import Any

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.entities import Unset
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.services.order_payment import OrderPaymentService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.utils.text import UNSET_MARK, display_list, display_text


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
                banks="",
                addressee="",
            )

    return dict(
        has_order_payment=True,
        order_payment_id=str(op.id),
        phone=op.phone,
        banks=display_list(op.banks),
        addressee=op.addressee,
    )


async def get_admin_order_payment_edit_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    return dict(
        mode=dialog_manager.dialog_data.get("order_payment_mode", "create"),
        is_update=dialog_manager.dialog_data.get("order_payment_mode") == "update",
        order_payment_id=dialog_manager.dialog_data.get("order_payment_id"),
        phone=_resolve_value(
            dialog_manager.dialog_data.get("order_payment_phone_value"),
            dialog_manager.dialog_data.get("order_payment_original_phone_value"),
        ),
        banks=_resolve_list(
            dialog_manager.dialog_data.get("order_payment_banks_value"),
            dialog_manager.dialog_data.get("order_payment_original_banks_value"),
        ),
        addressee=_resolve_value(
            dialog_manager.dialog_data.get("order_payment_addressee_value"),
            dialog_manager.dialog_data.get("order_payment_original_addressee_value"),
        ),
        has_phone=_has_value(
            dialog_manager.dialog_data.get("order_payment_phone_value"),
            dialog_manager.dialog_data.get("order_payment_original_phone_value"),
        ),
        has_banks=_has_value(
            dialog_manager.dialog_data.get("order_payment_banks_value"),
            dialog_manager.dialog_data.get("order_payment_original_banks_value"),
        ),
        has_addressee=_has_value(
            dialog_manager.dialog_data.get("order_payment_addressee_value"),
            dialog_manager.dialog_data.get("order_payment_original_addressee_value"),
        ),
    )


def _resolve_value(value: str | Unset | None, original: str | None) -> str:
    if value == UNSET_MARK:
        return display_text(original)
    return display_text(value)


def _resolve_list(
    value: Sequence[str] | Unset | None,
    original: Sequence[str] | None,
) -> str:
    if value == UNSET_MARK:
        return display_list(original)
    return display_list(value)


def _has_value(value: object, original: object) -> bool:
    if value == UNSET_MARK:
        return bool(original)
    return bool(value) and not isinstance(value, Unset) and value != UNSET_MARK
