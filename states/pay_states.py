from aiogram.dispatcher.fsm.state import State, StatesGroup


class Pay(StatesGroup):
    deposit_sum = State()