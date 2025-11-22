from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    menu = State()
    region = State()
    to_order = State()
    order_history = State()
    settings = State()
    sales = State()
    join_us = State()
    contact_us = State()

