from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

skin_type_kb = InlineKeyboardBuilder()
skin_type_kb.row(
    types.InlineKeyboardButton(text='Сухая', callback_data='Сухая'),
    types.InlineKeyboardButton(text='Жирная', callback_data='Жирная'))
skin_type_kb.row(
    types.InlineKeyboardButton(text='Комбинированная', callback_data='Комбинированная'))
skin_type_kb.row(
    types.InlineKeyboardButton(text='Нормальная', callback_data='Нормальная'),
    types.InlineKeyboardButton(text='Тонкая', callback_data='Тонкая'),
    types.InlineKeyboardButton(text='Толстая', callback_data='Толстая')
)
skin_type_kb.row(
    types.InlineKeyboardButton(text='Эластоз', callback_data='Эластоз'),
    types.InlineKeyboardButton(text='Пигментация', callback_data='Пигментация')
)
skin_type_kb.row(
    types.InlineKeyboardButton(text='Расширенные_поры', callback_data='Расширенные_поры')
)


# Функция генерации новой инлайн клавиатуры
async def generate_new_kb(kb: InlineKeyboardBuilder, used_button: list) -> InlineKeyboardBuilder:
    new_inline_kb = InlineKeyboardBuilder()
    new_buttons = [i.text for i in kb.buttons if i.text not in used_button]
    for i in new_buttons:
        new_inline_kb.button(text=i, callback_data=i)
    if len(new_buttons) % 2 == 0:
        new_inline_kb.adjust(2)
    else:
        new_inline_kb.adjust(3)
    new_inline_kb.row(types.InlineKeyboardButton(text='Закончить выбор ✅', callback_data='Закончить'))
    return new_inline_kb
