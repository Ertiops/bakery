from aiogram.fsm.state import State, StatesGroup


class RegistrationMenu(StatesGroup):
    start = State()
    personal_data_accept = State()
    name_input = State()
    phone_share = State()


class AdminMain(StatesGroup):
    menu = State()


class UserMain(StatesGroup):
    menu = State()


class AdminCatalogue(StatesGroup):
    select_category = State()
    view_products = State()
    view_single_product = State()
    delete_product = State()
    confirm_delete = State()
    update_product = State()
    add_name = State()
    add_description = State()
    add_price = State()
    add_confirm = State()
    update_name = State()
    update_description = State()
    update_price = State()
    update_confirm = State()


class UserCatalogue(StatesGroup):
    select_category = State()
    view_products = State()
    view_single_product = State()


class UserCart(StatesGroup):
    view = State()
    create_or_update = State()


class AdminPickupAddress(StatesGroup):
    view_all = State()
    view_one = State()
    add_name = State()
    add_confirm = State()
    update_name = State()
    update_confirm = State()
    confirm_delete = State()
    delete = State()
    update = State()
