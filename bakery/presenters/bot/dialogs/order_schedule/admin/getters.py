from __future__ import annotations

from typing import Any

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.services.order_schedule import OrderScheduleService
from bakery.domains.uow import AbstractUow
from bakery.domains.utils.timezone import format_hhmm, time_utc_to_msk_time

_SELECTED_KEY = "admin_order_schedule_weekdays"

WD_NAMES: dict[int, str] = {
    1: "Пн",
    2: "Вт",
    3: "Ср",
    4: "Чт",
    5: "Пт",
    6: "Сб",
    7: "Вс",
}


def _get_selected_weekdays(manager: DialogManager) -> set[int]:
    raw = manager.dialog_data.get(_SELECTED_KEY, [])
    return {int(x) for x in raw if 1 <= int(x) <= 7}


def _format_selected(selected: set[int]) -> str:
    if not selected:
        return "—"
    return ", ".join(WD_NAMES[d] for d in sorted(selected))


async def get_admin_order_schedule_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: OrderScheduleService = await container.get(OrderScheduleService)

    async with uow:
        try:
            schedule = await service.get_last()
            has_schedule = True
        except EntityNotFoundException:
            schedule = None
            has_schedule = False

    selected = _get_selected_weekdays(dialog_manager)

    min_days_before = dialog_manager.dialog_data.get("current_min_days_before")
    max_days_in_advance = dialog_manager.dialog_data.get("current_max_days_in_advance")
    open_time = dialog_manager.dialog_data.get("current_order_open_time")
    close_time = dialog_manager.dialog_data.get("current_order_close_time")

    return {
        "has_schedule": has_schedule,
        "current_weekdays": _format_selected(set(schedule.weekdays))
        if schedule
        else "—",
        "current_min_days_before": schedule.min_days_before if schedule else "—",
        "current_max_days_in_advance": schedule.max_days_in_advance
        if schedule
        else "—",
        "current_open_time": format_hhmm(time_utc_to_msk_time(schedule.order_open_time))
        if schedule
        else "—",
        "current_close_time": format_hhmm(
            time_utc_to_msk_time(schedule.order_close_time)
        )
        if schedule
        else "—",
        "selected_weekdays": _format_selected(selected),
        "has_selected": bool(selected),
        "min_days_before": min_days_before if min_days_before is not None else "—",
        "max_days_in_advance": max_days_in_advance
        if max_days_in_advance is not None
        else "—",
        "open_time": open_time if open_time else "—",
        "close_time": close_time if close_time else "—",
        "wd1_free": 1 not in selected,
        "wd2_free": 2 not in selected,
        "wd3_free": 3 not in selected,
        "wd4_free": 4 not in selected,
        "wd5_free": 5 not in selected,
        "wd6_free": 6 not in selected,
        "wd7_free": 7 not in selected,
        "error": dialog_manager.dialog_data.get("admin_order_schedule_error", ""),
    }
