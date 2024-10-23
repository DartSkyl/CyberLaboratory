from typing import List
from configuration import ADMIN_ID
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsAdminFilter(BaseFilter):
    """Фильтр, проверяющий является ли отправитель сообщения админом"""
    def __init__(self, admin_id: int):

        # Список ID администраторов прописывается вручную
        self.admins_id = admin_id

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.admins_id


admin_router = Router()

# Выше описанный фильтр добавляем прямо в роутер
admin_router.message.filter(IsAdminFilter(ADMIN_ID))
