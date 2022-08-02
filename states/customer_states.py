from aiogram.dispatcher.fsm.state import State, StatesGroup


class Customer(StatesGroup):
    customer_menu = State()
    start_answers = State()
    answer_2 = State()
    answer_3 = State()
