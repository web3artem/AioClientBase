from aiogram.fsm.state import StatesGroup, State


class ClientAdd(StatesGroup):
    FIO = State()
    gender = State()
    age = State()
    mobile = State()
    skin_type = State()
    chronic_diseases = State()
    medication = State()
    notes = State()
    summary = State()
    disagree = State()
    change = State()
    change_any = State()