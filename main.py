import asyncio
import datetime
from contextlib import asynccontextmanager

from aiogram.filters import CommandStart
from aiogram.types import Update, Message
from fastapi import FastAPI
from fastapi.requests import Request
import uvicorn

from telegram_module.admin_router import admin_router
import telegram_module.handlers.main_menu  # noqa
from configuration import WEBHOOK
from loader import dp, bot


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    url_webhook = WEBHOOK
    dp.include_router(admin_router)
    await bot.set_webhook(url=url_webhook,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


@app.on_event("startup")
async def start_up():
    # await db_connect()
    dp.include_router(admin_router)
    with open('bot.log', 'a') as log_file:
        log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
    print('Стартуем')
    await bot.delete_my_commands()
    # await bot.set_webhook(WEBHOOK)
    # await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # asyncio.run(start_up())
        uvicorn.run(app, host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print('Хорош, бро')
