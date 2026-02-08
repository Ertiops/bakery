from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Multi

from bakery.presenters.bot.content.buttons import common as common_btn
from bakery.presenters.bot.content.messages.blacklist import admin as msg
from bakery.presenters.bot.dialogs.blacklist.admin.getters import (
    get_blacklist_confirm_data,
    get_blacklist_data,
    get_blacklist_user_data,
    get_search_data,
)
from bakery.presenters.bot.dialogs.blacklist.admin.handlers import (
    on_blacklist_add_start,
    on_blacklist_confirm,
    on_blacklist_next_page,
    on_blacklist_prev_page,
    on_blacklist_reason_input,
    on_blacklist_remove,
    on_blacklist_user_selected,
    on_search_next_page,
    on_search_phone_input,
    on_search_prev_page,
    to_blacklist_menu,
    to_search_phone,
)
from bakery.presenters.bot.dialogs.main_menu.admin.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import AdminBlacklist


def admin_blacklist_windows() -> list[Window]:
    return [
        Window(
            Multi(
                Const(msg.TITLE),
                Const(msg.LIST_TITLE),
            ),
            ScrollingGroup(
                Select(
                    Format(msg.USER_ITEM),
                    id="blacklist_users",
                    item_id_getter=lambda item: item["id"],
                    items="users",
                    on_click=on_blacklist_user_selected,
                ),
                id="blacklist_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_users"),
            ),
            Row(
                Button(
                    Const(common_btn.PREV),
                    id="blacklist_prev",
                    on_click=on_blacklist_prev_page,
                    when="has_prev",
                ),
                Button(
                    Const(common_btn.NEXT),
                    id="blacklist_next",
                    on_click=on_blacklist_next_page,
                    when="has_next",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.SEARCH),
                    id="blacklist_search",
                    on_click=to_search_phone,
                ),
                Button(
                    Const(common_btn.BACK),
                    id="blacklist_back",
                    on_click=to_main_menu,
                ),
            ),
            state=AdminBlacklist.view_list,
            getter=get_blacklist_data,
        ),
        Window(
            Const(msg.SEARCH_TITLE),
            TextInput(
                id="blacklist_search_phone",
                type_factory=str,
                on_success=on_search_phone_input,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_list",
                    on_click=to_blacklist_menu,
                ),
            ),
            state=AdminBlacklist.search_phone,
        ),
        Window(
            Multi(
                Const(msg.SEARCH_RESULTS_TITLE),
            ),
            ScrollingGroup(
                Select(
                    Format(msg.USER_ITEM),
                    id="search_users",
                    item_id_getter=lambda item: item["id"],
                    items="users",
                    on_click=on_blacklist_user_selected,
                ),
                id="search_scroll",
                width=1,
                height=6,
                when=lambda d, *_: d.get("has_users"),
            ),
            Row(
                Button(
                    Const(common_btn.PREV),
                    id="search_prev",
                    on_click=on_search_prev_page,
                    when="has_prev",
                ),
                Button(
                    Const(common_btn.NEXT),
                    id="search_next",
                    on_click=on_search_next_page,
                    when="has_next",
                ),
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="search_back",
                    on_click=to_blacklist_menu,
                ),
            ),
            state=AdminBlacklist.view_search,
            getter=get_search_data,
        ),
        Window(
            Format(msg.USER_CARD, when=lambda d, *_: d.get("has_user")),
            Row(
                Button(
                    Const(common_btn.ADD),
                    id="blacklist_add",
                    on_click=on_blacklist_add_start,
                    when=lambda d, *_: not d.get("has_exclusion"),
                ),
                Button(
                    Const(common_btn.REMOVE),
                    id="blacklist_remove",
                    on_click=on_blacklist_remove,
                    when=lambda d, *_: d.get("has_exclusion"),
                ),
                Button(
                    Const(common_btn.BACK),
                    id="back_to_list",
                    on_click=to_blacklist_menu,
                ),
            ),
            state=AdminBlacklist.view_user,
            getter=get_blacklist_user_data,
        ),
        Window(
            Const(msg.ADD_REASON_TITLE),
            TextInput(
                id="blacklist_reason",
                type_factory=str,
                on_success=on_blacklist_reason_input,
            ),
            Row(
                Button(
                    Const(common_btn.BACK),
                    id="back_to_user",
                    on_click=lambda c, b, m: m.switch_to(AdminBlacklist.view_user),
                ),
            ),
            state=AdminBlacklist.input_reason,
        ),
        Window(
            Const(msg.CONFIRM_TITLE),
            Row(
                Button(
                    Const(common_btn.YES),
                    id="confirm_blacklist",
                    on_click=on_blacklist_confirm,
                ),
                Button(
                    Const(common_btn.NO),
                    id="cancel_blacklist",
                    on_click=to_blacklist_menu,
                ),
            ),
            state=AdminBlacklist.confirm_add,
            getter=get_blacklist_confirm_data,
        ),
    ]
