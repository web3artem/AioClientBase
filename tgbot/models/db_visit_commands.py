from aiogram import types
from datetime import datetime

from gino import MultipleResultsFound
from loguru import logger
from sqlalchemy import and_

from tgbot.models.client import Visit


async def retrieve_note_info(fio: str):
    logger.info('Получение информации о записи')
    try:
        client_instances = await Visit.query.where(Visit.FIO == fio).gino.one_or_none()
        if client_instances is None:
            return 'Нет записей о клиенте'
        else:
            return [client_instances.date]

    except MultipleResultsFound as e:
        client_instances = await Visit.select('date').where(Visit.FIO == fio).gino.all()
        return [i[0] for i in client_instances]


async def get_info_about_date(data: dict):
    date_instance = await Visit.query.where(
        (Visit.date == data['date']) &
        (Visit.FIO == data['fio'])).gino.first()
    date_values = date_instance.__dict__['__values__'].values()
    date_keys = ['ФИО', 'Дата приема', 'Процедуры', 'Рекомендации']
    client_keys = list(map(lambda key: f'{"<b>"}{key}{"</b>"}', date_keys))
    zipped = list(zip(client_keys, date_values))
    output_list = list(map(lambda x: f'{x[0]}: {x[1]} ', zipped))
    return '\n'.join(output_list)
