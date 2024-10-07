from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_module.keyboards.reply_markup import main_menu
from telegram_module.states import States
from telegram_module.admin_router import admin_router
from telegram_module.utils.work_sheet_model import work_sheet
from telegram_module.keyboards.inline_markup import work_sheet_interface


@admin_router.message(F.text == 'Рабочий табель')
async def open_work_sheet(msg: Message):
    """Открывает интерфейс рабочего табеля"""
    msg_text = 'Рабочий табель\n\n' + await work_sheet.info_string()
    await msg.answer(msg_text, reply_markup=await work_sheet_interface(await work_sheet.get_work_status(), await work_sheet.get_pause_status()))


@admin_router.callback_query(F.data.startswith('ws_'))
async def work_sheet_actions(callback: CallbackQuery):
    """Обработка действий рабочего табеля"""
    await callback.answer()
    action_dict = {
        'ws_start': work_sheet.start_work,
        'ws_pause': work_sheet.start_pause,
        'ws_resume': work_sheet.stop_pause,
        'ws_count': work_sheet.get_worked_time_count  # В данном случае, вызов функции не имеет эффекта. Нужно для обновления
    }
    if callback.data != 'ws_stop':
        await action_dict[callback.data]()
        msg_text = 'Рабочий табель\n\n' + await work_sheet.info_string()
        await callback.message.edit_text(msg_text, reply_markup=await work_sheet_interface(await work_sheet.get_work_status(),
                                                                           await work_sheet.get_pause_status()))
    else:
        count_time = await work_sheet.stop_work()
        msg_text = f'Сегодня отработано *_{count_time}_*'
        await callback.message.delete()
        await callback.message.answer(msg_text, reply_markup=main_menu)
