from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, ListGroup, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, List, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.buttons.order import admin as admin_btn
from bakery.presenters.bot.content.messages.order import admin as admin_msg
from bakery.presenters.bot.content.messages.order import user as user_msg
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.order.admin.getters import (
    get_admin_delete_confirm_data,
    get_admin_delete_order_confirm_data,
    get_admin_delete_order_reason_data,
    get_admin_delete_reason_data,
    get_admin_deleted_orders_data,
    get_admin_order_date_data,
    get_admin_orders_dates_data,
    get_admin_user_order_data,
    get_admin_user_orders_data,
)
from bakery.presenters.bot.dialogs.order.admin.handlers import (
    back_to_categories,
    back_to_date_view,
    back_to_dates,
    on_add_products_to_order,
    on_admin_date_selected,
    on_admin_delete_confirm,
    on_admin_delete_order_confirm,
    on_admin_delete_order_reason_input,
    on_admin_delete_order_start,
    on_admin_delete_reason_input,
    on_admin_product_delete_button,
    on_download_delivery_pdf,
    on_download_order_pdf,
    on_finish_delivery,
    on_start_delivery,
    on_take_in_work,
    on_user_order_selected,
    on_view_deleted_orders,
    on_view_products,
    on_view_user_orders,
    select_admin_orders_scope,
)
from bakery.presenters.bot.dialogs.states import AdminOrders


def admin_orders_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const(admin_msg.ADMIN_ORDERS_TITLE),
                Const(admin_msg.SELECT_CATEGORY),
            ),
            Row(
                Button(
                    Const(admin_btn.CURRENT_ORDERS),
                    id="orders_current",
                    on_click=lambda c, b, m: select_admin_orders_scope(
                        c, b, m, "current"
                    ),
                ),
                Button(
                    Const(admin_btn.ARCHIVE_ORDERS),
                    id="orders_archive",
                    on_click=lambda c, b, m: select_admin_orders_scope(
                        c, b, m, "archive"
                    ),
                ),
            ),
            Row(
                Button(
                    Const(common_btn.MAIN_MENU), id="to_main", on_click=to_main_menu
                ),
            ),
            state=AdminOrders.view_categories,
        ),
        Window(
            Multi(
                Const(admin_msg.SELECT_DATE),
                Const(admin_msg.NO_ORDERS, when=lambda d, *_: not d.get("has_dates")),
            ),
            ScrollingGroup(
                Select(
                    Format("{item[label]}"),
                    id="admin_order_dates",
                    item_id_getter=lambda item: item["id"],
                    items="dates",
                    on_click=on_admin_date_selected,
                ),
                id="admin_dates_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_dates"),
            ),
            Row(
                Button(
                    Const(admin_btn.BACK_TO_CATEGORY),
                    id="back_to_cat",
                    on_click=back_to_categories,
                ),
            ),
            state=AdminOrders.view_dates,
            getter=get_admin_orders_dates_data,
        ),
        Window(
            Multi(
                Format(admin_msg.DATE_TITLE, when=lambda d, *_: d.get("has_orders")),
                Format(
                    admin_msg.DATE_TOTAL_ORDERS,
                    when=lambda d, *_: d.get("has_orders"),
                ),
                Format(
                    admin_msg.DATE_TOTAL_SUM,
                    when=lambda d, *_: d.get("has_orders"),
                ),
                Const(
                    admin_msg.DATE_PRODUCTS_EMPTY,
                    when=lambda d, *_: d.get("has_orders")
                    and not d.get("has_products"),
                ),
                Const(admin_msg.NO_ORDERS, when=lambda d, *_: not d.get("has_orders")),
            ),
            Row(
                Button(
                    Const(admin_btn.TAKE_IN_WORK),
                    id="take_in_work",
                    on_click=on_take_in_work,
                    when="can_take_in_work",
                ),
                Button(
                    Const(admin_btn.START_DELIVERY),
                    id="start_delivery",
                    on_click=on_start_delivery,
                    when="can_start_delivery",
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.FINISH_DELIVERY),
                    id="finish_delivery",
                    on_click=on_finish_delivery,
                    when="can_finish_delivery",
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.EDIT_PRODUCTS),
                    id="edit_products",
                    on_click=on_view_products,
                    when="has_orders",
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.VIEW_USER_ORDERS),
                    id="view_user_orders",
                    on_click=on_view_user_orders,
                    when="has_orders",
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.VIEW_DELETED_ORDERS),
                    id="view_deleted_orders",
                    on_click=on_view_deleted_orders,
                    when="has_orders",
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.DOWNLOAD_ORDER_PDF),
                    id="download_order_pdf",
                    on_click=on_download_order_pdf,
                    when="has_orders",
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.DOWNLOAD_DELIVERY_PDF),
                    id="download_delivery_pdf",
                    on_click=on_download_delivery_pdf,
                    when="has_orders",
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.BACK_TO_DATES),
                    id="back_to_dates",
                    on_click=back_to_dates,
                ),
            ),
            state=AdminOrders.view_date,
            getter=get_admin_order_date_data,
        ),
        Window(
            Multi(
                Const(admin_msg.DATE_PRODUCTS_TITLE),
                Const(
                    admin_msg.DATE_PRODUCTS_EMPTY,
                    when=lambda d, *_: not d.get("has_products"),
                ),
            ),
            List(
                Format("{item[name]} ×{item[quantity]}"),
                items="products",
                when=lambda d, *_: d.get("has_products"),
            ),
            ScrollingGroup(
                ListGroup(
                    Row(
                        Button(
                            Format("{item[name]}"),
                            id="admin_product_name",
                            on_click=None,
                        ),
                        Button(
                            Const(common_btn.DELETE_REDUCED),
                            id="admin_product_delete",
                            on_click=on_admin_product_delete_button,
                        ),
                    ),
                    id="admin_products",
                    item_id_getter=lambda item: item["idx"],
                    items="products",
                ),
                id="admin_products_scroll",
                width=2,
                height=6,
                when=lambda d, *_: d.get("has_products") and d.get("can_edit_products"),
            ),
            Row(
                Button(
                    Const(admin_btn.BACK_TO_ORDER),
                    id="back_to_order",
                    on_click=back_to_date_view,
                ),
            ),
            state=AdminOrders.view_products,
            getter=get_admin_order_date_data,
        ),
        Window(
            Format(admin_msg.DELETE_REASON_TITLE),
            TextInput(
                id="admin_delete_reason",
                type_factory=str,
                on_success=on_admin_delete_reason_input,
            ),
            Row(
                Button(Const(common_btn.BACK), id="back", on_click=on_view_products),
            ),
            state=AdminOrders.delete_reason,
            getter=get_admin_delete_reason_data,
        ),
        Window(
            Format(admin_msg.DELETE_CONFIRM_TITLE),
            Row(
                Button(
                    Const(common_btn.YES),
                    id="confirm",
                    on_click=on_admin_delete_confirm,
                ),
                Button(Const(common_btn.NO), id="cancel", on_click=on_view_products),
            ),
            state=AdminOrders.delete_confirm,
            getter=get_admin_delete_confirm_data,
        ),
        Window(
            Format(admin_msg.DELETE_ORDER_REASON_TITLE),
            TextInput(
                id="admin_delete_order_reason",
                type_factory=str,
                on_success=on_admin_delete_order_reason_input,
            ),
            Row(
                Button(
                    Const(common_btn.BACK), id="back", on_click=on_view_deleted_orders
                ),
            ),
            state=AdminOrders.delete_order_reason,
            getter=get_admin_delete_order_reason_data,
        ),
        Window(
            Format(admin_msg.DELETE_ORDER_CONFIRM_TITLE),
            Row(
                Button(
                    Const(common_btn.YES),
                    id="confirm_delete_order",
                    on_click=on_admin_delete_order_confirm,
                ),
                Button(
                    Const(common_btn.NO),
                    id="cancel_delete_order",
                    on_click=on_view_deleted_orders,
                ),
            ),
            state=AdminOrders.delete_order_confirm,
            getter=get_admin_delete_order_confirm_data,
        ),
        Window(
            Multi(
                Format("{title}"),
                Const(admin_msg.NO_ORDERS, when=lambda d, *_: not d.get("has_orders")),
            ),
            ScrollingGroup(
                Select(
                    Format(admin_msg.USER_ORDER_ITEM),
                    id="admin_user_orders",
                    item_id_getter=lambda item: item["id"],
                    items="orders",
                    on_click=on_user_order_selected,
                ),
                id="admin_user_orders_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_orders"),
            ),
            Row(
                Button(
                    Const(admin_btn.BACK_TO_ORDER),
                    id="back_to_order",
                    on_click=back_to_date_view,
                ),
            ),
            state=AdminOrders.view_user_orders,
            getter=get_admin_user_orders_data,
        ),
        Window(
            Multi(
                Format("{title}"),
                Const(admin_msg.NO_ORDERS, when=lambda d, *_: not d.get("has_orders")),
            ),
            ScrollingGroup(
                Select(
                    Format(admin_msg.USER_ORDER_ITEM),
                    id="admin_deleted_orders",
                    item_id_getter=lambda item: item["id"],
                    items="orders",
                    on_click=on_user_order_selected,
                ),
                id="admin_deleted_orders_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_orders"),
            ),
            Row(
                Button(
                    Const(admin_btn.BACK_TO_ORDER),
                    id="back_to_order",
                    on_click=back_to_date_view,
                ),
            ),
            state=AdminOrders.view_deleted_orders,
            getter=get_admin_deleted_orders_data,
        ),
        Window(
            Multi(
                Format(
                    admin_msg.USER_ORDER_TITLE, when=lambda d, *_: d.get("has_order")
                ),
                Format(
                    user_msg.ORDER_DELIVERY_DATE,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    user_msg.ORDER_ADDRESS,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    admin_msg.USER_ORDER_CONTACTS,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    user_msg.ORDER_DELIVERY_PRICE,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Format(
                    user_msg.ORDER_TOTAL_PRICE,
                    when=lambda d, *_: d.get("has_order"),
                ),
                Const(admin_msg.NO_ORDERS, when=lambda d, *_: not d.get("has_order")),
            ),
            List(
                Format("{item[text]}"),
                items="products_text",
                when=lambda d, *_: d.get("has_order"),
            ),
            Format(
                admin_msg.USER_ORDER_PAYMENT,
                when=lambda d, *_: d.get("has_order"),
            ),
            Row(
                Button(
                    Const(admin_btn.ADD_PRODUCTS),
                    id="add_products",
                    on_click=on_add_products_to_order,
                    when=lambda d, *_: d.get("has_deleted_products")
                    and d.get("admin_deleted_flow"),
                ),
            ),
            Row(
                Button(
                    Const(admin_btn.DELETE_ORDER),
                    id="delete_order",
                    on_click=on_admin_delete_order_start,
                    when=lambda d, *_: d.get("admin_deleted_flow"),
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_user_orders",
                    on_click=on_view_deleted_orders,
                ),
            ),
            state=AdminOrders.view_user_order,
            getter=get_admin_user_order_data,
        ),
    ]
