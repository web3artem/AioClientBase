from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

change_or_accept_kb = InlineKeyboardBuilder()
change_or_accept_kb.row(
    types.InlineKeyboardButton(text="Обновить данные ✍️", callback_data="reload"),
    types.InlineKeyboardButton(text="Просто посмотреть 🙄", callback_data="cancel")
)

change_ikb = InlineKeyboardBuilder()
change_ikb.row(
    types.InlineKeyboardButton(text="ФИО", callback_data="change_FIO"),
    types.InlineKeyboardButton(text="Дата рождения", callback_data="change_birthdate"),
)
change_ikb.row(
    types.InlineKeyboardButton(text="Номер телефона", callback_data="change_phone"),
    types.InlineKeyboardButton(text="Тип кожи", callback_data="change_skintype")
)
change_ikb.row(
    types.InlineKeyboardButton(text="Хронические заболевания", callback_data="change_diseases"),
    types.InlineKeyboardButton(text="Препараты", callback_data="change_medication"),
)
change_ikb.row(
    types.InlineKeyboardButton(text="Дата приема", callback_data="change_date"),
    types.InlineKeyboardButton(text="Процедуры", callback_data="change_manipulations"),
    types.InlineKeyboardButton(text="Рекомендации", callback_data="change_recommendations"),
)
change_ikb.row(
    types.InlineKeyboardButton(text="Дополнительная информация", callback_data="change_notes"),

)