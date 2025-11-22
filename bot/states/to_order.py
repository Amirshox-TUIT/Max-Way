from aiogram.fsm.state import StatesGroup, State


class OrderState(StatesGroup):
    delivery_type = State()
    location = State()
    branches = State()
    categories = State()
    products = State()