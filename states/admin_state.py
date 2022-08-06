from aiogram.dispatcher.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    Admin_menu = State()
    edit_balance = State()
    up_balance = State()