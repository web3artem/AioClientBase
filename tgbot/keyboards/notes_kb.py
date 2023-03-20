from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

notes_ikb = InlineKeyboardBuilder()
notes_ikb.row(
    types.InlineKeyboardButton(text="➕ Добавить", callback_data="note_add"),
    types.InlineKeyboardButton(text="👀 Посмотреть", callback_data="note_read")
)

add_or_delete_note_ikb = InlineKeyboardBuilder()
add_or_delete_note_ikb.row(
    types.InlineKeyboardButton(text='Удалить существующую запись и добавить новую ❌', callback_data='delete_note')
)
add_or_delete_note_ikb.row(
    types.InlineKeyboardButton(text='Добавить к уже существующей ✳️', callback_data='add_to_note')
)

note_what_to_change_ikb = InlineKeyboardBuilder()
note_what_to_change_ikb.row(
    types.InlineKeyboardButton(text='Процедуры 💉', callback_data='procedures'),
    types.InlineKeyboardButton(text='Рекомендации', callback_data='recommendations')
)