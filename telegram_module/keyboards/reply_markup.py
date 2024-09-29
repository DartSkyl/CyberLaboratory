from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рабочий табель'), KeyboardButton(text='ИИ ассистент')],
    [KeyboardButton(text='Бухгалтерия'), KeyboardButton(text='Записная книжка')]
], resize_keyboard=True)
