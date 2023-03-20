from aiogram.fsm.state import StatesGroup, State


class NoteState(StatesGroup):
    note_date = State()
    note_procedures = State()
    note_recommendations = State()
    note_open = State()
    note_add_or_delete = State()

