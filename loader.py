import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from configuration import TG_TOKEN
from token_refresher import token_refresher


bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def start_up():
    await token_refresher.start_checker()
    with open('bot.log', 'a') as log_file:
        log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')

    print('Стартуем')

    await dp.start_polling(bot)
