from collections.abc import Awaitable, Callable
from datetime import timedelta
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.storages.delivery_cost import DeliveryCostStorage
from bakery.adapters.database.tables import DeliveryCostTable
from bakery.application.exceptions import (
    EntityNotFoundException,
)
from bakery.domains.entities.delivery_cost import (
    CreateDeliveryCost,
    DeliveryCost,
    UpdateDeliveryCost,
)
from tests.utils import now_utc


async def test__create(
    delivery_cost_storage: DeliveryCostStorage,
) -> None:
    create_data = CreateDeliveryCost(price=100, free_delivery_amount=1000)
    delivery_cost = await delivery_cost_storage.create(input_dto=create_data)
    assert delivery_cost == DeliveryCost(
        id=IsUUID,
        price=create_data.price,
        free_delivery_amount=create_data.free_delivery_amount,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_last(
    delivery_cost_storage: DeliveryCostStorage,
    create_delivery_cost: Callable,
) -> None:
    db_delivery_cost: DeliveryCostTable = await create_delivery_cost()
    await create_delivery_cost(
        created_at=now_utc() - timedelta(days=1),
    )
    delivery_cost = await delivery_cost_storage.get_last()
    assert delivery_cost == DeliveryCost(
        id=db_delivery_cost.id,
        price=db_delivery_cost.price,
        free_delivery_amount=db_delivery_cost.free_delivery_amount,
        created_at=db_delivery_cost.created_at,
        updated_at=db_delivery_cost.updated_at,
    )


async def test__get_last__none(
    delivery_cost_storage: DeliveryCostStorage,
) -> None:
    assert await delivery_cost_storage.get_last() is None


async def test__update_by_id(
    delivery_cost_storage: DeliveryCostStorage,
    create_delivery_cost: Callable[..., Awaitable[DeliveryCostTable]],
) -> None:
    db_delivery_cost = await create_delivery_cost()
    update_data = UpdateDeliveryCost(
        id=db_delivery_cost.id,
        price=200,
        free_delivery_amount=1500,
    )
    delivery_cost = await delivery_cost_storage.update_by_id(input_dto=update_data)
    assert delivery_cost == DeliveryCost(
        id=db_delivery_cost.id,
        price=update_data.price,
        free_delivery_amount=update_data.free_delivery_amount,
        created_at=db_delivery_cost.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    delivery_cost_storage: DeliveryCostStorage,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await delivery_cost_storage.update_by_id(
            input_dto=UpdateDeliveryCost(
                id=uuid4(),
            )
        )
