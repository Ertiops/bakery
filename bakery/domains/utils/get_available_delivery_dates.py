from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta

from bakery.application.constants.common import WEEKDAYS_BASE
from bakery.application.constants.order_schedule import ORDER_PERIOD_DAYS
from bakery.domains.entities.order_schedule import OrderSchedule
from bakery.domains.utils.timezone import MOSCOW_TZ, time_utc_to_msk_time


def is_order_date_available(
    *,
    order_schedule: OrderSchedule,
    delivered_at: date,
    now: datetime | None = None,
) -> bool:
    return delivered_at in get_available_delivery_dates(
        order_schedule=order_schedule,
        now=now,
    )


def get_available_delivery_dates(
    order_schedule: OrderSchedule,
    *,
    now: datetime | None = None,
) -> Sequence[date]:
    now_utc = now or datetime.now(tz=UTC)
    now_msk = now_utc.astimezone(MOSCOW_TZ)
    today = now_msk.date()

    if order_schedule.min_days_before < 0 or order_schedule.max_days_in_advance < 0:
        return []

    allowed_weekdays: set[int] = set()
    for wd in order_schedule.weekdays:
        wd0 = wd - 1 if WEEKDAYS_BASE == 1 else wd
        if not 0 <= wd0 <= 6:
            return []
        allowed_weekdays.add(wd0)

    order_open_time_msk = time_utc_to_msk_time(order_schedule.order_open_time)
    order_close_time_msk = time_utc_to_msk_time(order_schedule.order_close_time)
    anchor_dt_msk = datetime.combine(today, order_open_time_msk, tzinfo=MOSCOW_TZ)
    if now_msk < anchor_dt_msk:
        anchor_dt_msk -= timedelta(days=1)

    start_date = anchor_dt_msk.date()
    end_date = (anchor_dt_msk + timedelta(days=ORDER_PERIOD_DAYS - 1)).date()
    total_days = (end_date - start_date).days + 1

    result: list[date] = []
    for i in range(total_days):
        d = start_date + timedelta(days=i)
        if d < today:
            continue
        if d.weekday() not in allowed_weekdays:
            continue
        close_date = d - timedelta(days=order_schedule.max_days_in_advance)
        close_dt_msk = datetime.combine(
            close_date, order_close_time_msk, tzinfo=MOSCOW_TZ
        )
        if now_msk > close_dt_msk:
            continue
        result.append(d)

    return result
