from datetime import date
from uuid import uuid4

from bakery.domains.entities.order_schedule import OrderSchedule
from bakery.domains.utils.get_available_delivery_dates import (
    get_available_delivery_dates,
)
from tests.utils import now_utc


async def test__get_available_delivery_days() -> None:
    today = date(2025, 12, 29)
    order_schedule = OrderSchedule(
        id=uuid4(),
        weekdays=(3, 6),
        min_days_before=2,
        max_days_in_advance=1,
        created_at=now_utc(),
        updated_at=now_utc(),
    )
    result = get_available_delivery_dates(
        order_schedule=order_schedule,
        today=today,
    )
    assert result == [date(2025, 12, 31)]
