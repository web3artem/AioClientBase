from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

read_ikb = InlineKeyboardBuilder()
read_ikb.row(
    types.InlineKeyboardButton(text='Еще ➕', callback_data='more_note'),
    types.InlineKeyboardButton(text='Закончить 🛑', callback_data='cancel_note')
)