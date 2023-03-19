from aiogram import Dispatcher, types
from gino import MultipleResultsFound
from loguru import logger
from .client import db, Client, Visit
from tgbot.config import get_postgres_uri
from datetime import datetime
import datetime
from sqlalchemy import desc


async def on_startup(dispatcher: Dispatcher):
    logger.info('Установка связи с PostreSQL')
    try:
        await db.set_bind(get_postgres_uri())
        await db.gino.create_all()
        logger.info('Связь с PostreSQL установлена')
    except Exception as e:
        logger.error(f'Не удалось создать связь с PostreSQL, ошибка: {e}')


async def save_client(client_dict: dict):
    logger.info(f'Сохранение клиента: {client_dict["FIO"]}')
    client_instance = Client()
    for key, value in client_dict.items():
        try:
            setattr(client_instance, key, value)
            logger.success(f'{key} - {value} успешно сохранен')
        except Exception as e:
            logger.error(f'Не удалось сохранить {key} - {value}, ошибка: {e}')
    await client_instance.create()


async def retrieve_info():
    logger.info('Получение информации о клиенте')
    client_instances = await Client.select('FIO').order_by('FIO').gino.all()
    return [i[0] for i in client_instances]


async def get_client_from_db(message: types.Message):
    age_dict = {
        '1': 'год',
        '2': 'года',
        '3': 'года',
        '4': 'года',
        '5': 'лет',
        '6': 'лет',
        '7': 'лет',
        '8': 'лет',
        '9': 'лет',
        '0': 'лет'
    }

    logger.info(f'Получение клиента из базы данных: {message.text}')
    client_instance = await Client.query.where(Client.FIO == message.text).gino.first()
    client_values = client_instance.__dict__['__values__'].values()
    client_keys = ['ФИО', 'Пол', 'Возраст', 'Номер телефона', 'Тип кожи', 'Хронические заболевания',
                   'Препараты', 'Дополнительная информация']
    client_keys = list(map(lambda key: f'{"<b>"}{key}{"</b>"}', client_keys))
    zipped = list(zip(client_keys, client_values))
    output_list = list(map(lambda x: f'{x[0]}: {x[1]} ', zipped))
    for index, value in enumerate(output_list):
        if value.startswith('<b>Возраст'):
            date = value.split(':')[1]
            age = calculate_age(date)
            output_list[index] = f'<b>Возраст</b>: {age} {age_dict.get(age[-1])}'
    return '\n'.join(output_list)


def calculate_age(birth_date):
    birth_year, birth_month, birth_day = map(int, birth_date.split('-'))
    current_year, current_month, current_day = map(int, datetime.date.today().strftime('%Y-%m-%d').split('-'))
    age = current_year - birth_year
    if (current_month, current_day) < (birth_month, birth_day):
        age -= 1
    return str(age)


async def save_visit(data: dict):
    logger.info(f'Сохранение записи: {data["fio"]}')
    visit_instance = Visit()
    for key, value in data.items():
        try:
            if key == 'fio':
                setattr(visit_instance, 'FIO', value)
            else:
                setattr(visit_instance, key, value)
            logger.success(f'{key} - {value} успешно сохранен')
        except Exception as e:
            logger.error(f'Не удалось сохранить {key} - {value}, ошибка: {e}')
    await visit_instance.create()
