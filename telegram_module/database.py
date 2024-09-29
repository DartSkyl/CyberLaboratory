import time
from typing import List
import asyncpg as apg
from asyncpg import Record


class BotBase:
    """Через данный класс реализованы конект с базой данных и методы взаимодействия с БД"""
    def __init__(self, db_user, db_pass, db_name, db_host):
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.connection = None

    async def connect(self) -> None:
        """Метод создания соединения с базой"""
        self.connection = await apg.connect(database=self.db_name, user=self.db_user, password=self.db_pass,
                                            host=self.db_host)

    async def check_db_structure(self) -> None:
        await self.connection.execute("CREATE TABLE IF NOT EXISTS work_sheet"
                                      "(id SERIAL PRIMARY KEY,"
                                      "project_name VARCHAR(155),"
                                      "reporting_day DATE,"
                                      "time_worked INTEGER);")

        await self.connection.execute("CREATE TABLE IF NOT EXISTS projects"
                                      "(id SERIAL PRIMARY KEY,"
                                      "project_name VARCHAR(155),"
                                      "count_time INTEGER,"
                                      "")

    async def get_users_messages(self):
        """Метод выгружает сохраненные настройки пользовательских сообщений"""
        result = await self.connection.fetch("SELECT * FROM public.users_mess")  # Пример!
        return result