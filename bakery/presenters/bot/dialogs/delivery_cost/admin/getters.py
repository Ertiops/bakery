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
            cost_id=None,
        )

    dialog_manager.dialog_data["delivery_cost_id"] = str(cost.id)

    return dict(
        has_cost=True,
        price=cost.price,
        cost_id=str(cost.id),
    )
