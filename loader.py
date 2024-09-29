import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from configuration import TG_TOKEN, DB_INFO
from telegram_module import handlers  # noqa
from telegram_module.admin_router import admin_router
from telegram_module.database import BotBase


db = BotBase(DB_INFO[0], DB_INFO[1], DB_INFO[2], DB_INFO[3])
bot = Bot(token=TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def db_connect():
    """В этой функции идет подключение к БД и проверка ее структуры"""
    await db.connect()
    await db.check_db_structure()


async def start_up():
    # await db_connect()
    dp.include_router(admin_router)
    with open('bot.log', 'a') as log_file:
        log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
    print('Стартуем')
    await bot.delete_my_commands()
    await dp.start_polling(bot)
