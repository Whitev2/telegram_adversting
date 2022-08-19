from aiogram.dispatcher.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    member = State()