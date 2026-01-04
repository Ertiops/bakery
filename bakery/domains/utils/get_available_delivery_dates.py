from __future__ import annotations

from collections.abc import Sequence
from datetime import date, timedelta

from bakery.application.constants.order_schedule import ORDER_PERIOD
from bakery.domains.entities.order_schedule import OrderSchedule


def get_available_delivery_dates(
    order_schedule: OrderSchedule,
    *,
    today: date | None = None,
) -> Sequence[date]:
    weekdays_base = 1
    today = today or date.today()

    if order_schedule.min_days_before < 0 or order_schedule.max_days_in_advance < 0:
        return []
    if order_schedule.max_days_in_advance > order_schedule.min_days_before:
        return []

    allowed_weekdays: set[int] = set()
    for wd in order_schedule.weekdays:
        wd0 = wd - 1 if weekdays_base == 1 else wd
        if not 0 <= wd0 <= 6:
            return []
        allowed_weekdays.add(wd0)

    start_of_week = today - timedelta(days=today.weekday())

    result: list[date] = []
    for i in range(ORDER_PERIOD):
        d = start_of_week + timedelta(days=i)

        if d.weekday() not in allowed_weekdays:
            continue

        days_before = (d - today).days
        if days_before < 0:
            continue

        if not (
            order_schedule.max_days_in_advance
            <= days_before
            <= order_schedule.min_days_before
        ):
            continue

        result.append(d)

    return result
