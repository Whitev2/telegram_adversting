from aiogram.dispatcher.fsm.state import State, StatesGroup

class Question(StatesGroup):
    question_start = State()
    ask_support = State()
    question_send = State()
    question_1 = State()
    answer_for_user = State()