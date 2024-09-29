from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    add_record = State()
    dialogue_with_ai = State()
