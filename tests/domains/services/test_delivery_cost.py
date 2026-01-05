from collections.abc import Awaitable, Callable
from datetime import timedelta
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.tables import DeliveryCostTable
from bakery.application.exceptions import (
    EntityNotFoundException,
)
from bakery.domains.entities.delivery_cost import (
    CreateDeliveryCost,
    DeliveryCost,
    UpdateDeliveryCost,
)
from bakery.domains.services.delivery_cost import DeliveryCostService
from tests.utils import now_utc


async def test__create(
    delivery_cost_service: DeliveryCostService,
) -> None:
    create_data = CreateDeliveryCost(price=200)
    delivery_cost = await delivery_cost_service.create(input_dto=create_data)
    assert delivery_cost == DeliveryCost(
        id=IsUUID,
        price=create_data.price,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_last(
    delivery_cost_service: DeliveryCostService,
    create_delivery_cost: Callable,
) -> None:
    db_delivery_cost: DeliveryCostTable = await create_delivery_cost()
    await create_delivery_cost(
        created_at=now_utc() - timedelta(days=1),
    )
    delivery_cost = await delivery_cost_service.get_last()
    assert delivery_cost == DeliveryCost(
        id=db_delivery_cost.id,
        price=db_delivery_cost.price,
        created_at=db_delivery_cost.created_at,
        updated_at=db_delivery_cost.updated_at,
    )


async def test__get_last__entity_not_found_exception(
    delivery_cost_service: DeliveryCostService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await delivery_cost_service.get_last()


async def test__update_by_id(
    delivery_cost_service: DeliveryCostService,
    create_delivery_cost: Callable[..., Awaitable[DeliveryCostTable]],
) -> None:
    db_delivery_cost = await create_delivery_cost()
    update_data = UpdateDeliveryCost(
        id=db_delivery_cost.id,
        price=200,
    )
    delivery_cost = await delivery_cost_service.update_by_id(input_dto=update_data)
    assert delivery_cost == DeliveryCost(
        id=db_delivery_cost.id,
        price=update_data.price,
        created_at=db_delivery_cost.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    delivery_cost_service: DeliveryCostService,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await delivery_cost_service.update_by_id(
            input_dto=UpdateDeliveryCost(
                id=uuid4(),
            )
        )
