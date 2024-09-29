from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder


async def work_sheet_interface(work_status, pause_status):
    """Клавиатура взаимодействия с рабочим табелем"""
    wsi = InlineKeyboardBuilder()
    if not work_status:
        wsi.button(text='⏱ Начать рабочий день', callback_data='ws_start')
    else:
        wsi.button(text='🔄 Обновить', callback_data='ws_count')

        if not pause_status:
            wsi.button(text='⏸ Перерывчик, бро', callback_data='ws_pause')
        else:
            wsi.button(text='▶️ Продолжим, красавчик', callback_data='ws_resume')

        wsi.button(text='🏁 Отработал по красоте', callback_data='ws_stop')
    wsi.adjust(1)
    return wsi.as_markup()
