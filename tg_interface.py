import asyncio
import telegram_module.handlers.main_menu  # noqa
from loader import start_up

if __name__ == '__main__':
    try:
        asyncio.run(start_up())
    except KeyboardInterrupt:
        print('Хорош, бро')
