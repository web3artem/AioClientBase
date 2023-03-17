from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

gender_kb = InlineKeyboardBuilder()
gender_kb.row(
    types.InlineKeyboardButton(text='Женщина 👱‍♀️', callback_data='Женщина'),
    types.InlineKeyboardButton(text='Мужчина 👨‍🦱', callback_data='Мужчина')
)

