from aiogram.fsm.state import State, StatesGroup


class RegistrationMenu(StatesGroup):
    start = State()
    personal_data_accept = State()
    name_input = State()
    phone_share = State()


class UserMenu(StatesGroup):
    menu = State()
