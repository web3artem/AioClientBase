from datetime import datetime

from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.main_kb import main_kb_builder
from tgbot.keyboards.gender_kb import gender_kb
from tgbot.keyboards.skin_type_kb import skin_type_kb, generate_new_kb
from tgbot.models.db_commands import save_client
from tgbot.states.client_add_states import ClientAdd
from tgbot.misc.funcs import validate_date, summarizing_data

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Здравствуйте, <b>Наталья</b>👩‍⚕️\n\nДобро пожаловать в персонального бота! ❤️',
                         reply_markup=main_kb_builder.as_markup(resize_keyboard=True))


@router.message(Command('cancel'))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Отменено', reply_markup=main_kb_builder.as_markup(resize_keyboard=True))


@router.message(F.text == 'Добавить клиента')
async def add_client(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите ФИО клиента')
    await state.set_state(ClientAdd.FIO)


@router.message(ClientAdd.FIO)
async def client_fio(message: types.Message, state: FSMContext):
    await state.update_data(FIO=message.text)
    await message.answer('Отлично, теперь выберите пол Вашего клиента!',
                         reply_markup=gender_kb.as_markup())
    await state.set_state(ClientAdd.gender)


@router.callback_query(ClientAdd.gender)
async def client_gender(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback_query.data)
    await state.set_state(ClientAdd.age)
    await callback_query.message.answer('Напишите, пожалуйста, дату рождения клиента в формате 01.01.2000')
    await callback_query.answer()


@router.message(ClientAdd.age)
async def client_age(message: types.Message, state: FSMContext):
    if validate_date(message.text):
        await state.update_data(age=datetime.strptime(message.text, '%d.%m.%Y').date())
        await state.set_state(ClientAdd.mobile)
        await message.answer('Теперь введите номер телефона клиента! ☎️')
    else:
        await message.answer('Введен некорректный формат! Введите, пожалуйста, дату рождения Вашего клиента!')


@router.message(ClientAdd.mobile)
async def client_mobile(message: types.Message, state: FSMContext):
    await state.update_data(mobile_phone=message.text)
    await state.set_state(ClientAdd.skin_type)
    mes = await message.answer('Выберите тип кожи/состояние кожи клиента!',
                               reply_markup=skin_type_kb.as_markup())
    await state.update_data(msg=mes)


@router.callback_query(ClientAdd.skin_type)
async def client_skin_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    if user_data.get('skin_type', False) and callback_query.data != 'Закончить':
        new_data = user_data['skin_type'] + ' ' + callback_query.data
        await state.update_data(skin_type=new_data)

    if callback_query != 'Закончить':
        user_data = await state.get_data()
        try:
            skin_type = user_data['skin_type'].split(' ')
            text = f'Ваш выбор: {", ".join(skin_type)}'
            new_kb = await generate_new_kb(skin_type_kb, skin_type)
            await callback_query.message.edit_text(text=text, inline_message_id=user_data['msg'].message_id)
            await callback_query.message.edit_reply_markup(reply_markup=new_kb.as_markup())
        except KeyError:
            await state.update_data(skin_type=callback_query.data)
            user_data = await state.get_data()
            skin_type = user_data['skin_type'].split(' ')
            text = f'Ваш выбор: {user_data["skin_type"]}'
            new_kb = await generate_new_kb(skin_type_kb, skin_type)
            await callback_query.message.edit_text(text=text, inline_message_id=user_data['msg'].message_id)
            await callback_query.message.edit_reply_markup(reply_markup=new_kb.as_markup())

    if callback_query.data == 'Закончить':
        user_data = await state.get_data()
        await callback_query.message.edit_text(text='Ваш выбор сохранен ✅\n\n'
                                                    'Укажите есть ли хронические заболевания у клиента?'
                                                    ' Если да, то какие? 🤒',
                                               inline_message_id=user_data['msg'].message_id)
        await state.set_state(ClientAdd.chronic_diseases)


@router.message(ClientAdd.chronic_diseases)
async def client_chronic_diseases(message: types.Message, state: FSMContext):
    await state.update_data(chronic_diseases=message.text)
    await message.answer('Прекрасно! Уточните принимает ли клиент медицинские препараты и какие? 💊')
    await state.set_state(ClientAdd.medication)


@router.message(ClientAdd.medication)
async def client_medication(message: types.Message, state: FSMContext):
    await state.update_data(medication=message.text)
    await message.answer('Введите дополнительную информацию 📝.')
    await state.set_state(ClientAdd.notes)


@router.message(ClientAdd.notes)
async def client_notes(message: types.Message, state: FSMContext):
    await summarizing_data(message, state)


@router.callback_query(ClientAdd.summary)
async def client_agree(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.pop('msg')
    if callback_query.data == 'yes':
        for key, value in data.items():
            print(f'{key} - {value}')
        await save_client(data)
        await callback_query.message.answer('Спасибо, клиент успешно сохранен в базу данных!',
                                            reply_markup=main_kb_builder.as_markup(resize_keyboard=True))
        await state.clear()
