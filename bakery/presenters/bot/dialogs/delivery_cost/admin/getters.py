from typing import Any

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.services.delivery_cost import DeliveryCostService
from bakery.domains.uow import AbstractUow


async def get_delivery_cost_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    service: DeliveryCostService = await container.get(DeliveryCostService)
    uow: AbstractUow = await container.get(AbstractUow)

    try:
        async with uow:
            cost = await service.get_last()
    except EntityNotFoundException:
        return dict(
            has_cost=False,
            price=None,
            free_delivery_amount=None,
            has_free_delivery_amount=False,
            cost_id=None,
        )

    dialog_manager.dialog_data["delivery_cost_id"] = str(cost.id)
    if "delivery_cost_price" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["delivery_cost_price"] = cost.price
    if "delivery_cost_free_amount" not in dialog_manager.dialog_data:
        dialog_manager.dialog_data["delivery_cost_free_amount"] = (
            cost.free_delivery_amount
        )

    return dict(
        has_cost=True,
        price=cost.price,
        free_delivery_amount=cost.free_delivery_amount,
        has_free_delivery_amount=cost.free_delivery_amount is not None,
        cost_id=str(cost.id),
    )


async def get_delivery_cost_preview_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    return dict(
        price=dialog_manager.dialog_data.get("delivery_cost_price"),
        free_delivery_amount=dialog_manager.dialog_data.get(
            "delivery_cost_free_amount"
        ),
    )
