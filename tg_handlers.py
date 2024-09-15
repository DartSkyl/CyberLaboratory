from aiogram.types import Message
from aiogram import F
from aiogram.filters import Command

from langchain_core.messages import HumanMessage, AIMessage

from loader import dp
from ai_core import process_chat


chat_history = []


@dp.message(Command('start'))
async def start_command(msg: Message):
    ai_answer = await process_chat('Привет', chat_history)
    await msg.answer(ai_answer)
    chat_history.append(HumanMessage(content='Привет'))
    chat_history.append(AIMessage(content=ai_answer))


@dp.message()
async def dialog_with_ai(msg: Message):
    ai_answer = await process_chat(msg.text, chat_history)
    await msg.answer(ai_answer)
    chat_history.append(HumanMessage(content=msg.text))
    chat_history.append(AIMessage(content=ai_answer))
