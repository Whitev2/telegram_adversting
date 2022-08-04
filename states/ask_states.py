from aiogram.dispatcher.fsm.state import State, StatesGroup

class Ask(StatesGroup):
    start_ask = State()
    ask_support = State()
    send_ask = State()
    question_1 = State()
    answer_for_user = State()