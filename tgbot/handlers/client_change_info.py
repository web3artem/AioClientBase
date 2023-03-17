from datetime import datetime
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.add_or_delete import add_or_delete_ikb
from tgbot.keyboards.change_kb import change_or_accept_kb, change_ikb
from tgbot.misc.funcs import validate_date
from tgbot.models.client import Client
from tgbot.models.db_commands import retrieve_info, get_client_from_db
from tgbot.states.client_change_states import ChangeState

router = Router()


@router.message(F.text == 'Получить информацию о клиенте')
async def start(message: types.Message, state: FSMContext):
    client_list = await retrieve_info()
    client_list = list(map(lambda client: f'{"<code>"}{client}{"</code>"}', client_list))
    one_client = '\n'.join(client_list)
    await message.answer(f'Список клиентов 🧑‍⚕️:\n'
                         f'{one_client}')
    await state.set_state(ChangeState.info)


@router.message(ChangeState.info)
async def get_client_info(message: types.Message, state: FSMContext):
    output_list = await get_client_from_db(message)
    await state.clear()
    await state.update_data(fio=message.text)
    await message.answer(f'Информация о клиенте 👱🏻‍♀️:\n'
                         f'{output_list}', reply_markup=change_or_accept_kb.as_markup())


# Колбэк изменения данных
@router.callback_query(F.data == 'reload')
async def change_client(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer('Выберите, пожалуйста, какие данные необходимо изменить 👇',
                                        reply_markup=change_ikb.as_markup())


@router.callback_query(F.data == 'cancel')
async def change_client_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer('Хорошего дня! 🎉')


# Изменение ФИО
@router.callback_query(F.data == 'change_FIO')
async def change_client_fio(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(ChangeState.change_fio)
    await callback_query.message.answer('Введите, пожалуйста, новые ФИО клиента')


@router.message(ChangeState.change_fio)
async def change_client_fio_set(message: types.Message, state: FSMContext):
    data = await state.get_data()
    client = Client(FIO=data['fio'])
    await client.update(FIO=message.text).apply()
    await state.clear()
    await message.answer(f'ФИО успешно изменено на {message.text} ✅')


# Изменение даты рождения/возраста
@router.callback_query(F.data == 'change_birthdate')
async def change_client_date(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(ChangeState.change_birthdate)
    await callback_query.message.answer('Введите, пожалуйста, новую дату рождения в формате 01.01.1111')


@router.message(ChangeState.change_birthdate)
async def change_client_birthdate(message: types.Message, state: FSMContext):
    if validate_date(message.text):
        new_date = datetime.strptime(message.text, '%d.%m.%Y').date()
        data = await state.get_data()
        client = Client(FIO=data['fio'])
        await client.update(age=new_date).apply()
        await state.clear()
        await message.answer(f'Дата рождения успешно изменена ✅')
    else:
        await message.answer('К сожалению, дата рождения введена неверно. Попробуйте еще раз.')


# Изменение номера телефона
@router.callback_query(F.data == 'change_phone')
async def change_client_phone(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(ChangeState.change_phone)
    await callback_query.message.answer('Введите, пожалуйста, новый номер телефона')


@router.message(ChangeState.change_phone)
async def change_client_phone_set(message: types.Message, state: FSMContext):
    data = await state.get_data()
    client = Client(FIO=data['fio'])
    await client.update(mobile_phone=message.text).apply()
    await state.clear()
    await message.answer(f'Номер телефона успешно изменен на {message.text} ✅')


# Изменение хронических заболеваний
@router.callback_query(F.data.in_(['change_diseases', 'change_medication', 'change_date',
                                   'change_manipulations', 'change_recommendations', 'change_notes',
                                   'change_skintype']))
async def change_client_diseases(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(what_to_change=callback_query.data)
    await callback_query.answer()
    await callback_query.message.answer('Выберите, пожалуйста, действие 👇',
                                        reply_markup=add_or_delete_ikb.as_markup())


@router.callback_query(F.data == 'delete')
async def change_client_diseases_set(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Сообщите, пожалуйста, новые данные.')
    await callback_query.answer()
    await state.set_state(ChangeState.change_delete)


@router.message(ChangeState.change_delete)
async def change_client_delete(message: types.Message, state: FSMContext):
    data = await state.get_data()
    what_to_change = data['what_to_change'].split('_')[1]
    client = Client(FIO=data['fio'])
    match what_to_change:
        case 'diseases':
            await client.update(chronic_diseases=message.text).apply()
        case 'medication':
            await client.update(medication=message.text).apply()
        case 'date':
            await client.update(date_of_receipt=message.text).apply()
        case 'manipulations':
            await client.update(manipulations=message.text).apply()
        case 'recommendations':
            await client.update(recommendations=message.text).apply()
        case 'notes':
            await client.update(notes=message.text).apply()
        case 'skintype':
            await client.update(skin_type=message.text).apply()
    await state.clear()
    await message.answer(f'Данные успешно изменены ✅')


@router.callback_query(F.data == 'add')
async def change_client_add(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Сообщите, пожалуйста, какие данные нужно добавить? ✍️')
    await callback_query.answer()
    await state.set_state(ChangeState.change_add)


@router.message(ChangeState.change_add)
async def change_client_add_set(message: types.Message, state: FSMContext):
    data = await state.get_data()
    what_to_change = data['what_to_change'].split('_')[1]
    client = await Client.query.where(Client.FIO == data['fio']).gino.first()
    match what_to_change:
        case 'diseases':
            old_data = client.chronic_diseases
            new_data = old_data + ', ' + message.text
            await client.update(chronic_diseases=new_data).apply()
        case 'medication':
            old_data = client.medication
            new_data = old_data + ', ' + message.text
            await client.update(medication=new_data).apply()
        case 'date':
            old_data = client.date_of_receipt
            new_data = old_data + ', ' + message.text
            await client.update(date_of_receipt=new_data).apply()
        case 'manipulations':
            old_data = client.manipulations
            new_data = old_data + ', ' + message.text
            await client.update(manipulations=new_data).apply()
        case 'recommendations':
            old_data = client.recommendations
            new_data = old_data + ', ' + message.text
            await client.update(recommendations=new_data).apply()
        case 'notes':
            old_data = client.notes
            new_data = old_data + ', ' + message.text
            await client.update(notes=new_data).apply()
        case 'skintype':
            old_data = client.skintype
            new_data = old_data + ', ' + message.text
            await client.update(skin_type=new_data).apply()
    await state.clear()
    await message.answer('Информация успешно добавлена ✅')
