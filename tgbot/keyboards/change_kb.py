from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

change_or_accept_kb = InlineKeyboardBuilder()
change_or_accept_kb.row(
    types.InlineKeyboardButton(text="Обновить ✍️", callback_data="reload"),
    types.InlineKeyboardButton(text="Посмотреть 🙄", callback_data="cancel")
)
change_or_accept_kb.row(
    types.InlineKeyboardButton(text="Записи 📖", callback_data="notes")
)

change_ikb = InlineKeyboardBuilder()
change_ikb.row(
    types.InlineKeyboardButton(text="👱🏻‍♀️ ФИО", callback_data="change_FIO"),
    types.InlineKeyboardButton(text="👼 Дата рождения", callback_data="change_birthdate"),
)
change_ikb.row(
    types.InlineKeyboardButton(text="📱 Номер телефона", callback_data="change_phone"),
    types.InlineKeyboardButton(text="🙌 Тип кожи", callback_data="change_skintype")
)
change_ikb.row(
    types.InlineKeyboardButton(text="🤒 Заболевания", callback_data="change_diseases"),
    types.InlineKeyboardButton(text="💊 Препараты", callback_data="change_medication"),
)
change_ikb.row(
    types.InlineKeyboardButton(text="📝 Доп. информация", callback_data="change_notes"),

)