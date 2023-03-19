from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

notes_ikb = InlineKeyboardBuilder()
notes_ikb.row(
    types.InlineKeyboardButton(text="➕ Добавить", callback_data="note_add"),
    types.InlineKeyboardButton(text="👀 Посмотреть", callback_data="note_read")
)