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


class AdminDeliveryPrice(StatesGroup):
    view = State()
    create = State()
    update = State()


class UserCatalogue(StatesGroup):
    select_category = State()
    view_products = State()
    view_single_product = State()


class UserCart(StatesGroup):
    view = State()
    create_or_update = State()


class UserOrder(StatesGroup):
    add_address = State()
    add_manual_address = State()
    add_date = State()
    confirm = State()
    finish = State()
    view_categories = State()
    view_many = State()
    view_one = State()


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


class AdminAdminContact(StatesGroup):
    view_one = State()
    add_choice = State()
    add_name = State()
    add_tg_username = State()
    add_confirm = State()
    update_name = State()
    update_tg_username = State()
    update_confirm = State()


class UserAdminContact(StatesGroup):
    view_one = State()


class UserOrderPayment(StatesGroup):
    show_order_payment = State()
    add_file = State()
    confirm = State()
    finish = State()


class AdminOrderPayment(StatesGroup):
    view = State()
    phone = State()
    bank = State()
    addressee = State()
    confirm = State()


class AdminOrderSchedule(StatesGroup):
    view = State()
    pick_weekdays = State()
    min_days_before = State()
    max_days_in_advance = State()
    confirm = State()
    finish = State()
