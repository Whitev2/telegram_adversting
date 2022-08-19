from aiogram.dispatcher.fsm.state import State, StatesGroup


class Customer(StatesGroup):
    customer_menu = State()
    amount = State()
    price = State()
    link = State()

    post_1 = State()
    post_2 = State()
    post_3 = State()


