from aiogram.dispatcher.fsm.state import State, StatesGroup


class Customer(StatesGroup):
    customer_menu = State()
