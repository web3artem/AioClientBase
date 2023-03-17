from aiogram.fsm.state import StatesGroup, State


class ClientAdd(StatesGroup):
    FIO = State()
    gender = State()
    age = State()
    mobile = State()
    skin_type = State()
    chronic_diseases = State()
    medication = State()
    date_of_receipt = State()
    manipulations = State()
    recommendations = State()
    notes = State()
    summary = State()
    disagree = State()
    change = State()
    change_any = State()