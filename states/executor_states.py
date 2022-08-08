from aiogram.dispatcher.fsm.state import State, StatesGroup


class Executor(StatesGroup):
    executor_menu = State()
    sending_result = State()
    confirm_task = State()