from langchain_core.messages import HumanMessage, AIMessage
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from loader import dp
from ai_core import process_chat
from telegram_module.admin_router import admin_router
from telegram_module.states import States


chat_history = []

@admin_router.message(Command('start_ai'))
async def start_command(msg: Message, state: FSMContext):
    # await token_refresher.set_last_msg_time()
    ai_answer = await process_chat('Привет', chat_history)
    await msg.answer(ai_answer)
    chat_history.append(HumanMessage(content='Привет'))
    chat_history.append(AIMessage(content=ai_answer))
    await state.set_state(States.dialogue_with_ai)


@admin_router.message(States.dialogue_with_ai)
async def dialog_with_ai(msg: Message):
    ai_answer = await process_chat(msg.text, chat_history)
    await msg.answer(ai_answer)
    chat_history.append(HumanMessage(content=msg.text))
    chat_history.append(AIMessage(content=ai_answer))
