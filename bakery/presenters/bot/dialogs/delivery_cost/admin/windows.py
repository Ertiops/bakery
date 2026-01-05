from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.dialogs.delivery_cost.admin.getters import (
    get_delivery_cost_data,
)
from bakery.presenters.bot.dialogs.delivery_cost.admin.handlers import (
    on_delivery_cost_entered_create,
    on_delivery_cost_entered_update,
    to_create_delivery_cost,
    to_update_delivery_cost,
)
from bakery.presenters.bot.dialogs.delivery_cost.admin.redirections import (
    to_admin_main_menu,
)
from bakery.presenters.bot.dialogs.states import AdminDeliveryPrice


def admin_delivery_cost_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const("🚚 Стоимость доставки"),
                Const("\n\nТекущая стоимость:"),
                Format("{price} ₸", when=lambda d, *_: d.get("has_cost")),
                Const("не задана", when=lambda d, *_: not d.get("has_cost")),
            ),
            Row(
                Button(
                    Const(common_btn.CREATE),
                    id="create",
                    on_click=to_create_delivery_cost,
                    when=lambda d, *_: not d.get("has_cost"),
                ),
                Button(
                    Const(common_btn.UPDATE),
                    id="update",
                    on_click=to_update_delivery_cost,
                    when=lambda d, *_: d.get("has_cost"),
                ),
            ),
            Row(
                Button(Const(common_btn.BACK), id="back", on_click=to_admin_main_menu),
            ),
            state=AdminDeliveryPrice.view,
            getter=get_delivery_cost_data,
        ),
        Window(
            Const("➕ Введите стоимость доставки (числом):"),
            TextInput(
                id="delivery_cost_create",
                type_factory=int,
                on_success=on_delivery_cost_entered_create,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminDeliveryPrice.view),
                ),
            ),
            state=AdminDeliveryPrice.create,
        ),
        Window(
            Const("✏️ Введите новую стоимость доставки (числом):"),
            TextInput(
                id="delivery_cost_update",
                type_factory=int,
                on_success=on_delivery_cost_entered_update,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back",
                    on_click=lambda c, b, m: m.switch_to(AdminDeliveryPrice.view),
                ),
            ),
            state=AdminDeliveryPrice.update,
            getter=get_delivery_cost_data,
        ),
    ]
