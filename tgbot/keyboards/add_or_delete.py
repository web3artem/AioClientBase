from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

add_or_delete_ikb = InlineKeyboardBuilder()
add_or_delete_ikb.row(
    types.InlineKeyboardButton(text='Удалить существующую запись и добавить новую ❌', callback_data='delete')
)
add_or_delete_ikb.row(
    types.InlineKeyboardButton(text='Добавить к уже существующей ✳️', callback_data='add')
)