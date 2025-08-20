from bakery.adapters.database.tables import OrderScheduleTable
from bakery.domains.entities.order_schedule import OrderSchedule


def convert_order_schedule_to_dto(
    *,
    result: OrderScheduleTable,
) -> OrderSchedule:
    return OrderSchedule(
        id=result.id,
        weekdays=result.weekdays,
        min_days_before=result.min_days_before,
        max_days_in_advance=result.max_days_in_advance,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
