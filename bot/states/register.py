from aiogram.fsm.state import StatesGroup, State


class RegisterForm(StatesGroup):
    full_name = State()
    phone = State()
    age = State()
    selected_course = State()