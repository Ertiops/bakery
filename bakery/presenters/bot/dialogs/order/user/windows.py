from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, List, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.order import user as user_msg
from bakery.presenters.bot.dialogs.order.user.getters import (
    get_available_order_dates,
    get_order_confirm_data,
    get_pickup_address_data,
    get_user_order_data,
    get_user_orders_data,
)
from bakery.presenters.bot.dialogs.order.user.handlers import (
    back_to_orders_list,
    on_address_selected,
    on_confirm_order,
    on_manual_address_entered,
    on_order_date_selected,
    on_user_order_selected,
)
from bakery.presenters.bot.dialogs.order.user.redirections import (
    to_cart,
    to_main_menu_from_order,
    to_manual_address,
    to_order_categories,
)
from bakery.presenters.bot.dialogs.order.user.selections import (
    select_orders_cat_created,
    select_orders_cat_delivered,
    select_orders_cat_paid,
)
from bakery.presenters.bot.dialogs.states import UserOrder


def create_order_windows() -> list[Window]:
    return [
        Window(
            Format(user_msg.CREATE_ORDER),
            ScrollingGroup(
                Select(
                    Format("{item[name]}"),
                    id="addr",
                    item_id_getter=lambda item: item["id"],
                    items="addresses",
                    on_click=on_address_selected,
                ),
                id="addr_scroll",
                width=1,
                height=5,
                when=lambda d, *_: d.get("has_addresses"),
            ),
            Row(
                Button(Const(common_btn.BACK), id="back", on_click=to_cart),
                Button(
                    Const(common_btn.SKIP), id="skip_addr", on_click=to_manual_address
                ),
            ),
            state=UserOrder.add_address,
            getter=get_pickup_address_data,
        ),
        Window(
            Const("✍️ Введите адрес доставки одним сообщением:"),
            Const("\n\nНапример: ул. Шамиля Усманова 10, 1 подъезд, кв. 3"),
            TextInput(
                id="manual_address_input",
                type_factory=str,
                on_success=on_manual_address_entered,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_list",
                    on_click=lambda c, b, m: m.switch_to(UserOrder.add_address),
                ),
            ),
            state=UserOrder.add_manual_address,
        ),
        Window(
            Multi(
                Const("📅 Выберите дату доставки"),
                Const(
                    "\n\nДоступные даты:", when=lambda d, *_: d.get("has_order_dates")
                ),
                Const(
                    "\n\nСейчас нет доступных дат 😔",
                    when=lambda d, *_: not d.get("has_order_dates"),
                ),
            ),
            ScrollingGroup(
                Select(
                    Format("{item[label]}"),
                    id="order_date",
                    item_id_getter=lambda item: item["id"],  # iso
                    items="order_dates",
                    on_click=on_order_date_selected,
                ),
                id="order_date_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_order_dates"),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_addr",
                    on_click=lambda c, b, m: m.switch_to(UserOrder.add_address),
                ),
            ),
            state=UserOrder.add_date,
            getter=get_available_order_dates,
        ),
        Window(
            Multi(
                Const("✅ Подтверждение заказа\n\n"),
                Const("📍 Адрес доставки:"),
                Format(
                    "{pickup_address_name}",
                    when=lambda d, *_: d.get("has_pickup_address"),
                ),
                Const("Не выбран", when=lambda d, *_: not d.get("has_pickup_address")),
                Const("\n\n📅 Дата доставки:"),
                Format(
                    "{order_date_label}", when=lambda d, *_: d.get("has_order_date")
                ),
                Const("Не выбрана", when=lambda d, *_: not d.get("has_order_date")),
                Const("\n\n🧺 Корзина:"),
            ),
            List(
                Format(
                    "• {item[name]} — {item[qty]} × {item[price]} = {item[subtotal]}"
                ),
                items="cart_items",
                when=lambda d, *_: d.get("has_cart_items"),
            ),
            Format(
                "\n\n🚚 Доставка по городу: {delivery_cost} руб.",
                when=lambda d, *_: d.get("is_city_delivery"),
            ),
            Format("\n\n💰 Итого: {total}", when=lambda d, *_: d.get("has_cart_items")),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_addr",
                    on_click=lambda c, b, m: m.switch_to(UserOrder.add_date),
                ),
                Button(
                    Const("✅ Подтвердить"),
                    id="confirm_order",
                    on_click=on_confirm_order,
                ),
            ),
            state=UserOrder.confirm,
            getter=get_order_confirm_data,
        ),
        Window(
            Const("✅ Заказ успешно создан!\n\n"),
            Row(
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
                # Button(Const("📦 К заказу"), id="my_orders", on_click=...),
            ),
            state=UserOrder.finish,
        ),
        Window(
            Multi(
                Const("📦 Мои заказы\n\n"),
                Const("Выберите категорию:"),
            ),
            Row(
                Button(
                    Const("🆕 Готовятся"),
                    id="cat_created",
                    on_click=select_orders_cat_created,
                ),
            ),
            Row(
                Button(
                    Const("📬 Доставлены"),
                    id="cat_delivered",
                    on_click=select_orders_cat_delivered,
                ),
            ),
            Row(
                Button(
                    Const("💳 Оплачены"),
                    id="cat_paid",
                    on_click=select_orders_cat_paid,
                ),
            ),
            Row(
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
            ),
            state=UserOrder.view_categories,
        ),
        Window(
            Multi(
                Format("📦 {category_title}\n\n"),
                Const("Выберите заказ:"),
                Const(
                    "\n\nПока заказов нет 😔",
                    when=lambda d, *_: not d.get("has_orders"),
                ),
            ),
            ScrollingGroup(
                Select(
                    Format("🧾 {item[number]} • {item[delivered_at]} • {item[total]}₽"),
                    id="user_orders",
                    item_id_getter=lambda item: item["id"],
                    items="orders",
                    on_click=on_user_order_selected,
                ),
                id="user_orders_scroll",
                width=1,
                height=2,
                when=lambda d, *_: d.get("has_orders"),
            ),
            Row(
                Button(
                    Const("⬅️ К категориям"),
                    id="to_categories",
                    on_click=to_order_categories,
                ),
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
            ),
            state=UserOrder.view_many,
            getter=get_user_orders_data,
        ),
        Window(
            Multi(
                Format("📦 Заказ {number}\n\n", when=lambda d, *_: d.get("has_order")),
                Format(
                    "📅 Доставка: {delivered_at}\n",
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    "📍 Адрес: {pickup_address_name}\n",
                    when=lambda d, *_: d.get("has_order"),
                ),
                Const("🧺 Состав заказа:\n", when=lambda d, *_: d.get("has_order")),
                Format("{products_text}\n\n", when=lambda d, *_: d.get("has_order")),
                Format(
                    "🚚 Доставка: {delivery_price}₽\n",
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    "💰 Итого: {total_price}₽", when=lambda d, *_: d.get("has_order")
                ),
                Const("Заказ не найден 😔", when=lambda d, *_: not d.get("has_order")),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_orders",
                    on_click=back_to_orders_list,
                ),
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
            ),
            state=UserOrder.view_one,
            getter=get_user_order_data,
        ),
    ]
