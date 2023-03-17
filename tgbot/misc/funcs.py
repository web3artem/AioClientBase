from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.main_kb import yes_kb_builder
from tgbot.models.client import Client
from tgbot.states.client_add_states import ClientAdd


def validate_date(date_string):
    try:
        datetime.strptime(date_string, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def validate_int(number: str):
    try:
        int(number)
        return True
    except ValueError:
        return False


async def summarizing_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(notes=message.text)
    data.pop('msg')
    await state.update_data(skin_type=', '.join(data['skin_type'].split(' ')))
    data = await state.get_data()

    await message.answer(f'Проверьте все ли данные корректны? ✅\n\n'
                         f'<b>ФИО</b>: {data["FIO"]}\n'
                         f'<b>Пол</b>: {data["gender"]}\n'
                         f'<b>Дата рождения</b>: {data["age"]}\n'
                         f'<b>Мобильный телефон</b>: {data["mobile_phone"]}\n'
                         f'<b>Тип</b> кожи: {data["skin_type"]}\n'
                         f'<b>Хронические</b> заболевания: {data["chronic_diseases"]}\n'
                         f'<b>Препараты</b>: {data["medication"]}\n'
                         f'<b>Дата</b> последнего приема клиента: {data["date_of_receipt"]}\n'
                         f'<b>Процедуры</b>: {data["manipulations"]}\n'
                         f'<b>Рекомендации</b>: {data["recommendations"]}\n'
                         f'<b>Дополнительная информация</b>: {data["notes"]}',
                         reply_markup=yes_kb_builder.as_markup(resize_keyboard=True))
    await state.set_state(ClientAdd.summary)

