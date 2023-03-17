from aiogram.fsm.state import StatesGroup, State


class ChangeState(StatesGroup):
    info = State()
    what_to_change = State()
    change_fio = State()
    change_birthdate = State()
    change_phone = State()
    change_delete = State()
    change_add = State()