from aiogram.fsm.state import State, StatesGroup


class RegistrationMenu(StatesGroup):
    start = State()
    personal_data_accept = State()
    name_input = State()
    phone_share = State()


class AdminMain(StatesGroup):
    menu = State()


class AdminBlacklist(StatesGroup):
    view_list = State()
    search_phone = State()
    view_search = State()
    view_user = State()
    input_reason = State()
    confirm_add = State()


class AdminFakeUsers(StatesGroup):
    view_list = State()
    input_name = State()
    input_phone = State()
    confirm_create = State()
    search_phone = State()
    view_search = State()
    view_user = State()


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
    add_photo = State()
    add_confirm = State()
    update_name = State()
    update_description = State()
    update_price = State()
    update_photo = State()
    update_confirm = State()


class AdminDeliveryPrice(StatesGroup):
    view = State()
    create = State()
    create_free_amount = State()
    create_confirm = State()
    update = State()
    update_free_amount = State()
    update_confirm = State()


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
    rate = State()
    finish = State()


class AdminOrderPayment(StatesGroup):
    view = State()
    phone = State()
    banks = State()
    addressee = State()
    confirm = State()


class AdminFeedbackGroup(StatesGroup):
    view = State()
    url = State()
    confirm = State()


class AdminOrderSchedule(StatesGroup):
    view = State()
    pick_weekdays = State()
    min_days_before = State()
    max_days_in_advance = State()
    open_time = State()
    close_time = State()
    confirm = State()
    finish = State()


class AdminOrders(StatesGroup):
    view_categories = State()
    view_dates = State()
    view_date = State()
    take_in_work_confirm = State()
    take_in_work_sent = State()
    start_delivery_hours = State()
    start_delivery_confirm = State()
    start_delivery_sent = State()
    view_products = State()
    delete_reason = State()
    delete_confirm = State()
    view_user_orders = State()
    view_user_order = State()
    view_deleted_orders = State()
    view_unpaid_orders = State()
    finish_delivery_confirm = State()
    finish_delivery_sent = State()
    delete_order_reason = State()
    delete_order_confirm = State()
