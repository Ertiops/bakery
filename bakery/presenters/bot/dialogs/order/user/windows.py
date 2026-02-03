from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select, Url
from aiogram_dialog.widgets.text import Const, Format, List, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.buttons.order import user as user_order_btn
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
    on_delete_order,
    on_edit_order,
    on_manual_address_entered,
    on_order_date_selected,
    on_top_product_add,
    on_user_order_selected,
)
from bakery.presenters.bot.dialogs.order.user.redirections import (
    to_cart,
    to_created_order,
    to_main_menu_from_order,
    to_manual_address,
    to_order_categories,
    to_order_payment,
)
from bakery.presenters.bot.dialogs.order.user.selections import (
    select_orders_cat_created,
    select_orders_cat_delivered,
    select_orders_cat_in_progress,
    select_orders_cat_paid,
)
from bakery.presenters.bot.dialogs.states import UserOrder


def create_order_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Format(user_msg.CREATE_ORDER),
                Format(
                    user_msg.FREE_DELIVERY_HINT,
                    when=lambda d, *_: d.get("has_free_delivery_amount"),
                ),
            ),
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
            Const(user_msg.MANUAL_ADDRESS_TITLE),
            Const(user_msg.MANUAL_ADDRESS_EXAMPLE),
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
                Const(user_msg.ORDER_DATE_TITLE),
                Const(
                    user_msg.ORDER_DATE_AVAILABLE_SUFFIX,
                    when=lambda d, *_: d.get("has_order_dates"),
                ),
                Const(
                    user_msg.ORDER_DATE_EMPTY,
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
                Const(user_msg.CONFIRM_TITLE),
                Const(user_msg.CONFIRM_ADDRESS_LABEL),
                Format(
                    "{pickup_address_name}",
                    when=lambda d, *_: d.get("has_pickup_address"),
                ),
                Const(
                    user_msg.CONFIRM_ADDRESS_EMPTY,
                    when=lambda d, *_: not d.get("has_pickup_address"),
                ),
                Const(user_msg.CONFIRM_DATE_LABEL),
                Format(
                    "{order_date_label}", when=lambda d, *_: d.get("has_order_date")
                ),
                Const(
                    user_msg.CONFIRM_DATE_EMPTY,
                    when=lambda d, *_: not d.get("has_order_date"),
                ),
                Const(user_msg.CONFIRM_CART_LABEL),
            ),
            List(
                Format(user_msg.CART_ITEM_LINE),
                items="cart_items",
                when=lambda d, *_: d.get("has_cart_items"),
            ),
            Format(
                user_msg.CONFIRM_DELIVERY_COST,
                when=lambda d, *_: d.get("is_city_delivery"),
            ),
            Format(user_msg.CONFIRM_TOTAL, when=lambda d, *_: d.get("has_cart_items")),
            Const(
                user_msg.CONFIRM_SUGGESTED_TITLE,
                when=lambda d, *_: d.get("has_top_products"),
            ),
            ScrollingGroup(
                Select(
                    Format(user_msg.CONFIRM_SUGGESTED_ITEM),
                    id="top_products",
                    item_id_getter=lambda item: item["id"],
                    items="top_products",
                    on_click=on_top_product_add,
                ),
                id="top_products_scroll",
                width=1,
                height=3,
                when=lambda d, *_: d.get("has_top_products"),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_addr",
                    on_click=lambda c, b, m: m.switch_to(UserOrder.add_date),
                ),
                Button(
                    Const(user_order_btn.CONFIRM_ORDER),
                    id="confirm_order",
                    on_click=on_confirm_order,
                ),
            ),
            state=UserOrder.confirm,
            getter=get_order_confirm_data,
        ),
        Window(
            Const(user_msg.ORDER_CREATED),
            Row(
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
                Button(
                    Const(user_order_btn.TO_ORDER),
                    id="my_orders",
                    on_click=to_created_order,
                ),
            ),
            state=UserOrder.finish,
        ),
        Window(
            Multi(
                Const(user_msg.MY_ORDERS_TITLE),
                Const(user_msg.SELECT_CATEGORY),
            ),
            Row(
                Button(
                    Const(user_order_btn.CATEGORY_CREATED),
                    id="cat_created",
                    on_click=select_orders_cat_created,
                ),
            ),
            Row(
                Button(
                    Const(user_order_btn.CATEGORY_IN_PROGRESS),
                    id="cat_in_progress",
                    on_click=select_orders_cat_in_progress,
                ),
            ),
            Row(
                Button(
                    Const(user_order_btn.CATEGORY_DELIVERED),
                    id="cat_delivered",
                    on_click=select_orders_cat_delivered,
                ),
            ),
            Row(
                Button(
                    Const(user_order_btn.CATEGORY_PAID),
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
                Format(user_msg.ORDERS_CATEGORY_TITLE),
                Const(user_msg.SELECT_ORDER),
                Const(
                    user_msg.NO_ORDERS,
                    when=lambda d, *_: not d.get("has_orders"),
                ),
            ),
            ScrollingGroup(
                Select(
                    Format(user_msg.ORDER_LIST_ITEM),
                    id="user_orders",
                    item_id_getter=lambda item: item["id"],
                    items="orders",
                    on_click=on_user_order_selected,
                ),
                id="user_orders_scroll",
                width=1,
                height=5,
                when=lambda d, *_: d.get("has_orders"),
            ),
            Row(
                Button(
                    Const(user_order_btn.BACK_TO_CATEGORIES),
                    id="to_categories",
                    on_click=to_order_categories,
                ),
            ),
            Row(
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
                Format(user_msg.ORDER_TITLE, when=lambda d, *_: d.get("has_order")),
                Format(
                    user_msg.ORDER_DELIVERY_DATE,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    user_msg.ORDER_ADDRESS,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Const(
                    user_msg.ORDER_CONTENT_LABEL, when=lambda d, *_: d.get("has_order")
                ),
                Format(
                    user_msg.ORDER_PRODUCTS_TEXT, when=lambda d, *_: d.get("has_order")
                ),
                Format(
                    user_msg.ORDER_DELIVERY_PRICE,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    user_msg.ORDER_TOTAL_PRICE,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Const(
                    user_msg.ORDER_NOT_FOUND, when=lambda d, *_: not d.get("has_order")
                ),
            ),
            Row(
                Button(
                    Const(user_order_btn.BACK_TO_ORDERS),
                    id="back_to_orders",
                    on_click=back_to_orders_list,
                ),
            ),
            Url(
                Const(user_order_btn.FEEDBACK_GROUP),
                url=Format("{feedback_group_url}"),
                when=lambda d, *_: d.get("is_paid") and d.get("has_feedback_group"),
            ),
            Row(
                Button(
                    Const(user_order_btn.DELETE),
                    id="delete_order",
                    on_click=on_delete_order,
                    when="can_delete",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.EDIT),
                    id="edit_order",
                    on_click=on_edit_order,
                    when="can_edit",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.MAIN_MENU),
                    id="to_main_menu",
                    on_click=to_main_menu_from_order,
                ),
            ),
            Button(
                Const(user_order_btn.PAY),
                id="pay",
                on_click=to_order_payment,
                when="is_delivered",
            ),
            state=UserOrder.view_one,
            getter=get_user_order_data,
        ),
    ]
