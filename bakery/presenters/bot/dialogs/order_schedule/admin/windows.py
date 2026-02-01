from __future__ import annotations

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.order_schedule import (
    admin as order_schedule_admin_msg,
)
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.order_schedule.admin.getters import (
    get_admin_order_schedule_data,
)
from bakery.presenters.bot.dialogs.order_schedule.admin.handlers import (
    back_to_max_days,
    back_to_min_days,
    go_next_from_weekdays,
    on_close_time_input,
    on_max_days_in_advance_input,
    on_min_days_before_input,
    on_open_time_input,
    pick_weekday,
    reset_weekdays,
    save_schedule,
    to_pick_weekdays,
)
from bakery.presenters.bot.dialogs.states import AdminOrderSchedule


def admin_order_schedule_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const("🗓 Расписание доставки (админ)\n\n"),
                Const("Текущее:\n"),
                Format("Дни: <b>{current_weekdays}</b>\n"),
                Format(order_schedule_admin_msg.CURRENT_MIN_DAYS_BEFORE),
                Format(order_schedule_admin_msg.CURRENT_MAX_DAYS_IN_ADVANCE),
                Format(order_schedule_admin_msg.CURRENT_OPEN_TIME),
                Format(order_schedule_admin_msg.CURRENT_CLOSE_TIME),
                Format("\n❗ {error}\n", when=lambda d, *_: bool(d.get("error"))),
            ),
            Row(
                Button(Const("✏️ Настроить"), id="edit", on_click=to_pick_weekdays),
                Button(Const(common_btn.BACK), id="back", on_click=to_main_menu),
            ),
            state=AdminOrderSchedule.view,
            getter=get_admin_order_schedule_data,
        ),
        Window(
            Multi(
                Const("Выберите дни недели доставки\n\n"),
                Format("Выбрано: <b>{selected_weekdays}</b>\n\n"),
                Const("Нажимайте на дни — выбранные кнопки исчезнут.\n"),
                Format("\n❗ {error}\n", when=lambda d, *_: bool(d.get("error"))),
            ),
            Group(
                Row(
                    Button(
                        Const("Пн"), id="wd_1", on_click=pick_weekday, when="wd1_free"
                    ),
                    Button(
                        Const("Вт"), id="wd_2", on_click=pick_weekday, when="wd2_free"
                    ),
                    Button(
                        Const("Ср"), id="wd_3", on_click=pick_weekday, when="wd3_free"
                    ),
                    Button(
                        Const("Чт"), id="wd_4", on_click=pick_weekday, when="wd4_free"
                    ),
                ),
                Row(
                    Button(
                        Const("Пт"), id="wd_5", on_click=pick_weekday, when="wd5_free"
                    ),
                    Button(
                        Const("Сб"), id="wd_6", on_click=pick_weekday, when="wd6_free"
                    ),
                    Button(
                        Const("Вс"), id="wd_7", on_click=pick_weekday, when="wd7_free"
                    ),
                ),
            ),
            Row(
                Button(Const(common_btn.RESET), id="reset", on_click=reset_weekdays),
                Button(
                    Const(common_btn.NEXT),
                    id="next",
                    on_click=go_next_from_weekdays,
                    when="has_selected",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminOrderSchedule.view),
                ),
            ),
            state=AdminOrderSchedule.pick_weekdays,
            getter=get_admin_order_schedule_data,
        ),
        Window(
            Multi(
                Const("Введите <b>Количество дней до начала заказа</b>\n"),
                Const("Нижняя граница для Стартовой даты.\n\n"),
                Const("Пример: <b>2</b>\n"),
                Format("\n❗ {error}\n", when=lambda d, *_: bool(d.get("error"))),
            ),
            MessageInput(on_min_days_before_input),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(
                        AdminOrderSchedule.pick_weekdays
                    ),
                ),
            ),
            state=AdminOrderSchedule.min_days_before,
            getter=get_admin_order_schedule_data,
        ),
        Window(
            Multi(
                Const("Введите <b>Количество дней до конца заказа</b>\n"),
                Const("Верхняя граница для Стартовой даты.\n\n"),
                Const("Пример: <b>1</b>\n"),
                Format("\n❗ {error}\n", when=lambda d, *_: bool(d.get("error"))),
            ),
            MessageInput(on_max_days_in_advance_input),
            Row(
                Button(Const(common_btn.BACK), id="back", on_click=back_to_min_days),
            ),
            state=AdminOrderSchedule.max_days_in_advance,
            getter=get_admin_order_schedule_data,
        ),
        Window(
            Multi(
                Const("Введите время открытия заказов (МСК)\n"),
                Const("Формат: <b>HH:MM</b>\n\n"),
                Const("Пример: <b>00:00</b>\n"),
                Format("\n❗ {error}\n", when=lambda d, *_: bool(d.get("error"))),
            ),
            MessageInput(on_open_time_input),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(
                        AdminOrderSchedule.max_days_in_advance
                    ),
                ),
            ),
            state=AdminOrderSchedule.open_time,
            getter=get_admin_order_schedule_data,
        ),
        Window(
            Multi(
                Const("Введите время закрытия заказов (МСК)\n"),
                Const("Формат: <b>HH:MM</b>\n\n"),
                Const("Пример: <b>12:00</b>\n"),
                Format("\n❗ {error}\n", when=lambda d, *_: bool(d.get("error"))),
            ),
            MessageInput(on_close_time_input),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminOrderSchedule.open_time),
                ),
            ),
            state=AdminOrderSchedule.close_time,
            getter=get_admin_order_schedule_data,
        ),
        Window(
            Multi(
                Const("Подтвердите расписание\n\n"),
                Format("Дни: <b>{selected_weekdays}</b>\n"),
                Format(order_schedule_admin_msg.MIN_DAYS_BEFORE),
                Format(order_schedule_admin_msg.MAX_DAYS_IN_ADVANCE),
                Format(order_schedule_admin_msg.OPEN_TIME),
                Format(order_schedule_admin_msg.CLOSE_TIME),
                Format("\n❗ {error}\n", when=lambda d, *_: bool(d.get("error"))),
            ),
            Row(
                Button(Const(common_btn.SAVE), id="save", on_click=save_schedule),
                Button(Const(common_btn.BACK), id="back", on_click=back_to_max_days),
            ),
            state=AdminOrderSchedule.confirm,
            getter=get_admin_order_schedule_data,
        ),
        Window(
            Multi(
                Const("✅ Расписание сохранено.\n"),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminOrderSchedule.view),
                ),
                Button(Const(common_btn.MAIN_MENU), id="menu", on_click=to_main_menu),
            ),
            state=AdminOrderSchedule.finish,
        ),
    ]
