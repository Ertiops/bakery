from collections.abc import Sequence
from typing import Any
from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.domains.entities.pickup_address import (
    PickupAddress,
    PickupAddressListParams,
)
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.uow import AbstractUow


async def get_pickup_address_list_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Sequence[PickupAddress]]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await dialog_manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    service: PickupAddressService = await container.get(PickupAddressService)
    async with uow:
        pickup_address_list = await service.get_list(
            input_dto=PickupAddressListParams(limit=100, offset=0)
        )
    return dict(pickup_addresses=pickup_address_list.items)


async def get_pickup_address_preview_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, str]:
    return dict(
        name=dialog_manager.dialog_data.get("name", "<нет>"),
    )


async def get_selected_pickup_address(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, PickupAddress]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await dialog_manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    service: PickupAddressService = await container.get(PickupAddressService)
    pickup_address_id = dialog_manager.start_data.get(  # type: ignore[union-attr]
        "pickup_address_id"
    ) or dialog_manager.dialog_data.get("pickup_address_id")  # type: ignore[union-attr]
    async with uow:
        pickup_address = await service.get_by_id(input_id=UUID(pickup_address_id))
    dialog_manager.dialog_data.update(
        dict(
            pickup_address_id=str(pickup_address.id),
            original_name=pickup_address.name,
        )
    )
    return dict(pickup_address=pickup_address)
