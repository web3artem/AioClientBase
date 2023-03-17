from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main_kb_builder = ReplyKeyboardBuilder()
main_kb_builder.row(
    types.KeyboardButton(text='Добавить клиента'),
    types.KeyboardButton(text='Получить информацию о клиенте')
)

yes_kb_builder = InlineKeyboardBuilder()
yes_kb_builder.row(
    types.InlineKeyboardButton(text='Да ✅', callback_data='yes'),
)
