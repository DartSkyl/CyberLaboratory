import datetime

from aiogram.types import Message, FSInputFile
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from langchain_core.messages import HumanMessage, AIMessage

from loader import dp
from ai_core import process_chat
from token_refresher import token_refresher


chat_history = []


class States(StatesGroup):
    add_record = State()


@dp.message(Command('start'))
async def start_command(msg: Message):
    await token_refresher.set_last_msg_time()
    ai_answer = await process_chat('Привет', chat_history)
    await msg.answer(ai_answer)
    chat_history.append(HumanMessage(content='Привет'))
    chat_history.append(AIMessage(content=ai_answer))


@dp.message(Command('add_record'))
async def add_record_1(msg: Message, state: FSMContext):
    await state.set_state(States.add_record)
    await msg.answer('Введите запись:')


@dp.message(States.add_record)
async def add_record_2(msg: Message, state: FSMContext):
    added_record = f'\n\n***** Новая запись от {datetime.datetime.now()} *****\n\n\n'
    added_record += msg.text + '\n'
    with open('notes.txt', 'a', encoding='utf-8') as file:
        file.write(added_record)
    await msg.answer('Запись добавлена')
    await state.clear()


@dp.message(Command('get_records'))
async def get_records_file(msg: Message):
    records_file = FSInputFile('notes.txt')
    await msg.answer_document(document=records_file)


@dp.message()
async def dialog_with_ai(msg: Message):
    ai_answer = await process_chat(msg.text, chat_history)
    await msg.answer(ai_answer)
    chat_history.append(HumanMessage(content=msg.text))
    chat_history.append(AIMessage(content=ai_answer))
