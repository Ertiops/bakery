from aiogram.fsm.state import State, StatesGroup


class RegistrationMenu(StatesGroup):
    start = State()
    personal_data_accept = State()
    name_input = State()
    phone_share = State()


class AdminMain(StatesGroup):
    menu = State()


class AdminCatalogue(StatesGroup):
    select_category = State()
    view_products = State()
    view_single_product = State()
    delete_product = State()
    edit_product = State()
    add_name = State()
    add_description = State()
    add_price = State()
    add_confirm = State()
