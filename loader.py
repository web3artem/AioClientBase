import asyncio
import sys

from aiogram.utils.text_decorations import HtmlDecoration
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode

from tgbot.config import load_config
from tgbot.handlers import client_adding, client_change_info

config = load_config()
storage = MemoryStorage()

bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode('HTML'))
dp = Dispatcher(storage=storage)


async def main():
    from tgbot.models.db_commands import on_startup
    await on_startup(dp)
    try:
        logger.success('Бот запущен')

        dp.include_routers(client_adding.router)
        dp.include_routers(client_change_info.router)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except:
        logger.error('Бот не запущен')


if __name__ == '__main__':
    logger.add(sys.stderr, format="<white>{time:HH:mm:ss}</white>"
                                  " | <green>{level: <8}</green>"
                                  " | <cyan>{line}</cyan>"
                                  " - <white>{message}</white>")
    asyncio.run(main())
