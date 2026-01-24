from __future__ import annotations

from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.domains.entities.order_schedule import CreateOrderSchedule
from bakery.domains.services.order_schedule import OrderScheduleService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminOrderSchedule

_SELECTED_KEY = "admin_order_schedule_weekdays"


def _get_selected(manager: DialogManager) -> set[int]:
    raw = manager.dialog_data.get(_SELECTED_KEY, [])
    return {int(x) for x in raw if 1 <= int(x) <= 7}


def _set_selected(manager: DialogManager, selected: set[int]) -> None:
    manager.dialog_data[_SELECTED_KEY] = sorted(selected)


def _set_error(manager: DialogManager, text: str | None) -> None:
    if text:
        manager.dialog_data["admin_order_schedule_error"] = text
    else:
        manager.dialog_data.pop("admin_order_schedule_error", None)


def _clear_error(manager: DialogManager) -> None:
    manager.dialog_data.pop("admin_order_schedule_error", None)


async def to_pick_weekdays(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _set_error(manager, None)
    manager.dialog_data.pop("current_min_days_before", None)
    manager.dialog_data.pop("current_max_days_in_advance", None)
    await manager.switch_to(AdminOrderSchedule.pick_weekdays)


async def pick_weekday(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _set_error(manager, None)
    day = int(button.widget_id.split("_")[1])  # type: ignore[union-attr]
    selected = _get_selected(manager)
    selected.add(day)
    _set_selected(manager, selected)
    await callback.answer()


async def reset_weekdays(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _set_error(manager, None)
    manager.dialog_data[_SELECTED_KEY] = []
    await callback.answer("Выбор сброшен")


async def go_next_from_weekdays(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if not _get_selected(manager):
        await callback.answer("Выберите хотя бы один день")
        return
    _set_error(manager, None)
    await manager.switch_to(AdminOrderSchedule.min_days_before)


async def on_min_days_before_input(
    message: Message, _w: object, manager: DialogManager
) -> None:
    try:
        value = int((message.text or "").strip())
    except ValueError:
        _set_error(manager, "Введите целое число (например 7).")
        return

    if value < 0:
        _set_error(manager, "Значение не может быть отрицательным.")
        return

    manager.dialog_data["current_min_days_before"] = value
    _set_error(manager, None)
    await manager.switch_to(AdminOrderSchedule.max_days_in_advance)


async def on_max_days_in_advance_input(
    message: Message, _w: object, manager: DialogManager
) -> None:
    try:
        value = int((message.text or "").strip())
    except ValueError:
        _set_error(manager, "Введите целое число (например 1).")
        return

    if value < 0:
        _set_error(manager, "Значение не может быть отрицательным.")
        return

    manager.dialog_data["current_max_days_in_advance"] = value
    _set_error(manager, None)
    await manager.switch_to(AdminOrderSchedule.confirm)


async def save_schedule(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    selected = _get_selected(manager)
    min_days_before = manager.dialog_data.get("current_min_days_before")
    max_days_in_advance = manager.dialog_data.get("current_max_days_in_advance")

    if not selected:
        _set_error(manager, "Выберите хотя бы один день недели.")
        return
    if min_days_before is None or max_days_in_advance is None:
        _set_error(manager, "Не заполнены min/max.")
        return

    if int(max_days_in_advance) >= int(min_days_before):
        _set_error(
            manager,
            (
                "Диапазон некорректен:"
                " Количество дней до конца заказа должно быть"
                " ≤ Количество дней до начала заказа."
            ),
        )
        return

    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: OrderScheduleService = await container.get(OrderScheduleService)

    async with uow:
        await service.create(
            input_dto=CreateOrderSchedule(
                weekdays=sorted(selected),
                min_days_before=int(min_days_before),
                max_days_in_advance=int(max_days_in_advance),
            )
        )

    _set_error(manager, None)
    await manager.switch_to(AdminOrderSchedule.finish)


async def back_to_max_days(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _clear_error(manager)
    await manager.switch_to(AdminOrderSchedule.max_days_in_advance)


async def back_to_min_days(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _clear_error(manager)
    await manager.switch_to(AdminOrderSchedule.min_days_before)


async def back_to_weekdays(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _clear_error(manager)
    await manager.switch_to(AdminOrderSchedule.pick_weekdays)
