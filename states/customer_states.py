from aiogram.dispatcher.fsm.state import State, StatesGroup


class Customer(StatesGroup):
    customer_menu = State()
    start_answers = State()
    answer_2 = State()
    answer_3 = State()
    confirm_or_not = State()

    start_other_task = State()
    name_other_task = State()
    description_other_task = State()
    link_other_task = State()
    count_of_executions_other_task = State()
    price_other_task = State()
    confirm_or_not_other_task = State()
    confirm_other_task = State()


