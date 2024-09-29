import datetime

from aiogram.types import Message, FSInputFile
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_module.states import States
from telegram_module.admin_router import admin_router
from telegram_module.keyboards.reply_markup import  main_menu




@admin_router.message(Command('start'))
async def start_command(msg: Message):
    await msg.answer('Здравствуй, мой любимый человек 😘\nТы, как всегда, прекрасен!\nЧего ты хочешь, солнышко?', reply_markup=main_menu)


@admin_router.message(Command('add_record'))
async def add_record_1(msg: Message, state: FSMContext):
    await state.set_state(States.add_record)
    await msg.answer('Введите запись:')


@admin_router.message(States.add_record)
async def add_record_2(msg: Message, state: FSMContext):
    added_record = f'***** Запись от {datetime.datetime.now()} *****\n\n\n'
    added_record += msg.text + '\n\n\n'
    with open('notes.txt', 'a', encoding='utf-8') as file:
        file.write(added_record)
    await msg.answer('Запись добавлена')
    await state.clear()


@admin_router.message(Command('get_records'))
async def get_records_file(msg: Message):
    records_file = FSInputFile('notes.txt')
    await msg.answer_document(document=records_file)
