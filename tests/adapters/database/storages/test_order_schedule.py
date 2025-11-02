from collections.abc import Callable
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.storages.order_schedule import OrderScheduleStorage
from bakery.adapters.database.tables import OrderScheduleTable
from bakery.application.exceptions import (
    EntityNotFoundException,
)
from bakery.domains.entities.order_schedule import (
    CreateOrderSchedule,
    OrderSchedule,
    UpdateOrderSchedule,
)
from tests.utils import now_utc


async def test__create(
    order_schedule_storage: OrderScheduleStorage,
) -> None:
    create_data = CreateOrderSchedule(
        weekdays=[1, 3],
        min_days_before=1,
        max_days_in_advance=7,
    )
    order_schedule = await order_schedule_storage.create(input_dto=create_data)
    assert order_schedule == OrderSchedule(
        id=IsUUID,
        weekdays=create_data.weekdays,
        min_days_before=create_data.min_days_before,
        max_days_in_advance=create_data.max_days_in_advance,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_last(
    order_schedule_storage: OrderScheduleStorage,
    create_order_schedule: Callable,
) -> None:
    db_order_schedules: list[OrderScheduleTable] = [
        await create_order_schedule() for _ in range(2)
    ]
    order_schedule = await order_schedule_storage.get_last()
    assert order_schedule == OrderSchedule(
        id=db_order_schedules[1].id,
        weekdays=db_order_schedules[1].weekdays,
        min_days_before=db_order_schedules[1].min_days_before,
        max_days_in_advance=db_order_schedules[1].max_days_in_advance,
        created_at=db_order_schedules[1].created_at,
        updated_at=db_order_schedules[1].updated_at,
    )


async def test__get_last__last_deleted(
    order_schedule_storage: OrderScheduleStorage,
    create_order_schedule: Callable,
) -> None:
    db_order_schedule: OrderScheduleTable = await create_order_schedule()
    await create_order_schedule(deleted_at=now_utc())
    order_schedule = await order_schedule_storage.get_last()
    assert order_schedule == OrderSchedule(
        id=db_order_schedule.id,
        weekdays=db_order_schedule.weekdays,
        min_days_before=db_order_schedule.min_days_before,
        max_days_in_advance=db_order_schedule.max_days_in_advance,
        created_at=db_order_schedule.created_at,
        updated_at=db_order_schedule.updated_at,
    )


async def test__get_last__none(
    order_schedule_storage: OrderScheduleStorage,
) -> None:
    assert await order_schedule_storage.get_last() is None


async def test__get_last__deleted(
    order_schedule_storage: OrderScheduleStorage,
    create_order_schedule: Callable,
) -> None:
    await create_order_schedule(deleted_at=now_utc())
    assert await order_schedule_storage.get_last() is None


async def test__update_by_id(
    order_schedule_storage: OrderScheduleStorage,
    create_order_schedule: Callable,
) -> None:
    db_order_schedule: OrderScheduleTable = await create_order_schedule()
    update_data = UpdateOrderSchedule(
        id=db_order_schedule.id,
        weekdays=[1, 3],
        min_days_before=1,
        max_days_in_advance=7,
    )
    order_schedule = await order_schedule_storage.update_by_id(input_dto=update_data)
    assert order_schedule == OrderSchedule(
        id=db_order_schedule.id,
        weekdays=update_data.weekdays,
        min_days_before=update_data.min_days_before,
        max_days_in_advance=update_data.max_days_in_advance,
        created_at=db_order_schedule.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    order_schedule_storage: OrderScheduleStorage,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await order_schedule_storage.update_by_id(
            input_dto=UpdateOrderSchedule(id=uuid4())
        )


async def test__delete_by_id(
    order_schedule_storage: OrderScheduleStorage,
    create_order_schedule: Callable,
) -> None:
    db_order_schedule: OrderScheduleTable = await create_order_schedule()
    await order_schedule_storage.delete_by_id(input_id=db_order_schedule.id)
    assert db_order_schedule.deleted_at is not None


async def test__delete_by_id__none(
    order_schedule_storage: OrderScheduleStorage,
) -> None:
    assert await order_schedule_storage.delete_by_id(input_id=uuid4()) is None
