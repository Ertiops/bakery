from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.buttons.fake_users import admin as fake_btn
from bakery.presenters.bot.content.messages.fake_users import admin as msg
from bakery.presenters.bot.dialogs.fake_users.admin.getters import (
    get_fake_user_confirm_data,
    get_fake_user_data,
    get_fake_users_data,
    get_fake_users_search_data,
)
from bakery.presenters.bot.dialogs.fake_users.admin.handlers import (
    on_create_order_for_fake_user,
    on_fake_user_confirm,
    on_fake_user_name_input,
    on_fake_user_phone_input,
    on_fake_user_selected,
    on_fake_users_next_page,
    on_fake_users_prev_page,
    on_fake_users_search_input,
    on_fake_users_search_next_page,
    on_fake_users_search_prev_page,
    to_fake_users_menu,
    to_fake_users_search,
)
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import AdminFakeUsers


def admin_fake_users_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const(msg.TITLE),
                Const(msg.LIST_TITLE),
                Const(msg.EMPTY_LIST, when=lambda d, *_: not d.get("has_users")),
            ),
            ScrollingGroup(
                Select(
                    Format(msg.USER_ITEM),
                    id="fake_users",
                    item_id_getter=lambda item: item["id"],
                    items="users",
                    on_click=on_fake_user_selected,
                ),
                id="fake_users_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_users"),
            ),
            Row(
                Button(
                    Const(common_btn.PREV),
                    id="fake_users_prev",
                    on_click=on_fake_users_prev_page,
                    when="has_prev",
                ),
                Button(
                    Const(common_btn.NEXT),
                    id="fake_users_next",
                    on_click=on_fake_users_next_page,
                    when="has_next",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.ADD),
                    id="fake_user_add",
                    on_click=lambda c, b, m: m.switch_to(AdminFakeUsers.input_name),
                ),
                Button(
                    Const(common_btn.SEARCH),
                    id="fake_user_search",
                    on_click=to_fake_users_search,
                ),
                Button(
                    Const(common_btn.BACK),
                    id="fake_users_back",
                    on_click=to_main_menu,
                ),
            ),
            state=AdminFakeUsers.view_list,
            getter=get_fake_users_data,
        ),
        Window(
            Const(msg.SEARCH_TITLE),
            TextInput(
                id="fake_users_search_phone",
                type_factory=str,
                on_success=on_fake_users_search_input,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_list",
                    on_click=to_fake_users_menu,
                ),
            ),
            state=AdminFakeUsers.search_phone,
        ),
        Window(
            Multi(
                Const(msg.SEARCH_RESULTS_TITLE),
                Const(msg.EMPTY_LIST, when=lambda d, *_: not d.get("has_users")),
            ),
            ScrollingGroup(
                Select(
                    Format(msg.USER_ITEM),
                    id="fake_users_search",
                    item_id_getter=lambda item: item["id"],
                    items="users",
                    on_click=on_fake_user_selected,
                ),
                id="fake_users_search_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_users"),
            ),
            Row(
                Button(
                    Const(common_btn.PREV),
                    id="fake_users_search_prev",
                    on_click=on_fake_users_search_prev_page,
                    when="has_prev",
                ),
                Button(
                    Const(common_btn.NEXT),
                    id="fake_users_search_next",
                    on_click=on_fake_users_search_next_page,
                    when="has_next",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="fake_users_search_back",
                    on_click=to_fake_users_menu,
                ),
            ),
            state=AdminFakeUsers.view_search,
            getter=get_fake_users_search_data,
        ),
        Window(
            Const(msg.NAME_TITLE),
            TextInput(
                id="fake_user_name",
                type_factory=str,
                on_success=on_fake_user_name_input,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_list",
                    on_click=to_fake_users_menu,
                ),
            ),
            state=AdminFakeUsers.input_name,
        ),
        Window(
            Const(msg.PHONE_TITLE),
            TextInput(
                id="fake_user_phone",
                type_factory=str,
                on_success=on_fake_user_phone_input,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_name",
                    on_click=lambda c, b, m: m.switch_to(AdminFakeUsers.input_name),
                ),
            ),
            state=AdminFakeUsers.input_phone,
        ),
        Window(
            Multi(
                Const(msg.CONFIRM_TITLE),
                Format(msg.CONFIRM_USER, when=lambda d, *_: d.get("has_data")),
            ),
            Row(
                Button(
                    Const(common_btn.YES),
                    id="fake_user_confirm",
                    on_click=on_fake_user_confirm,
                ),
                Button(
                    Const(common_btn.NO),
                    id="fake_user_cancel",
                    on_click=to_fake_users_menu,
                ),
            ),
            state=AdminFakeUsers.confirm_create,
            getter=get_fake_user_confirm_data,
        ),
        Window(
            Multi(
                Const(msg.TITLE),
                Format(msg.USER_CARD, when=lambda d, *_: d.get("has_user")),
                Const(msg.EMPTY_LIST, when=lambda d, *_: not d.get("has_user")),
            ),
            Row(
                Button(
                    Const(fake_btn.CREATE_ORDER),
                    id="fake_user_order",
                    on_click=on_create_order_for_fake_user,
                    when=lambda d, *_: d.get("has_user"),
                ),
                Button(
                    Const(common_btn.BACK),
                    id="back_to_list",
                    on_click=to_fake_users_menu,
                ),
            ),
            state=AdminFakeUsers.view_user,
            getter=get_fake_user_data,
        ),
    ]
