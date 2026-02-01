from datetime import UTC, date, datetime, time
from uuid import uuid4

from bakery.domains.entities.order_schedule import OrderSchedule
from bakery.domains.utils.get_available_delivery_dates import (
    get_available_delivery_dates,
)
from tests.utils import now_utc


async def test__get_available_delivery_days() -> None:
    order_schedule = OrderSchedule(
        id=uuid4(),
        weekdays=(3, 6),
        min_days_before=2,
        max_days_in_advance=1,
        order_open_time=time(21, 0),
        order_close_time=time(9, 0),
        created_at=now_utc(),
        updated_at=now_utc(),
    )
    result = get_available_delivery_dates(
        order_schedule=order_schedule,
        now=datetime(2025, 12, 29, 6, 0, tzinfo=UTC),
    )
    assert result == [
        date(2025, 12, 31),
        date(2026, 1, 3),
        date(2026, 1, 7),
        date(2026, 1, 10),
    ]


async def test__get_available_delivery_days__next_week_window() -> None:
    order_schedule = OrderSchedule(
        id=uuid4(),
        weekdays=(3,),
        min_days_before=3,
        max_days_in_advance=2,
        order_open_time=time(21, 0),
        order_close_time=time(9, 0),
        created_at=now_utc(),
        updated_at=now_utc(),
    )
    result = get_available_delivery_dates(
        order_schedule=order_schedule,
        now=datetime(2026, 2, 1, 9, 0, tzinfo=UTC),
    )
    assert result == [date(2026, 2, 4), date(2026, 2, 11)]


async def test__get_available_delivery_days__skip_today_after_close() -> None:
    order_schedule = OrderSchedule(
        id=uuid4(),
        weekdays=(3, 7),
        min_days_before=3,
        max_days_in_advance=2,
        order_open_time=time(21, 0),
        order_close_time=time(9, 0),
        created_at=now_utc(),
        updated_at=now_utc(),
    )
    result = get_available_delivery_dates(
        order_schedule=order_schedule,
        now=datetime(2026, 2, 1, 8, 0, tzinfo=UTC),
    )
    assert result == [
        date(2026, 2, 4),
        date(2026, 2, 8),
        date(2026, 2, 11),
    ]
