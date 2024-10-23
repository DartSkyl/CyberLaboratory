import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from langchain_community.llms import YandexGPT
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
# from configuration import MODEL_URI, TOKEN_REFRESH


load_dotenv()


async def check_last_msg_time():
    if token_refresher.last_msg_time == token_refresher.previous_value:
        token_refresher.chain.invoke({'country': token_refresher.country})
        token_refresher.previous_value = int(time.time())
        token_refresher.last_msg_time = token_refresher.previous_value

    else:
        token_refresher.previous_value = token_refresher.last_msg_time


class FirstMessage:
    """Проверяем когда был последний запрос. Если когда и предыдущий,
    то делаем минимальный запрос, что бы обновить токен. Что бы не грузить запрос
    для обновления токена создадим отдельную цепочку"""
    def __init__(self):
        # Отдельно пропишем максимально простую цепочку
        self.template = "What is the capital of {country}?"
        self.prompt = PromptTemplate.from_template(self.template)
        self.llm = YandexGPT(model_uri=MODEL_URI)
        self.chain = self.prompt | self.llm
        self.country = "Russia"

        self._scheduler = AsyncIOScheduler(gconfig={'apscheduler.timezone': 'Europe/Moscow'})
        # Если с последней проверки время не изменилось, значит запросов не было и нужно его сделать
        self.last_msg_time = int(time.time())
        self.previous_value = self.last_msg_time

    async def start_checker(self):
        self._scheduler.start()
        self._scheduler.add_job(
            func=check_last_msg_time,
            kwargs={},
            trigger='interval',
            hours=TOKEN_REFRESH,
            # seconds=20,
            max_instances=1,
        )

    async def set_last_msg_time(self):
        self.last_msg_time = int(time.time())


token_refresher = FirstMessage()
