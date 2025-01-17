from aiogram.fsm.state import StatesGroup, State

class AddBook(StatesGroup):
    name = State()
    author = State()
    # year = State()
    file = State()

class GetBook(StatesGroup):
    id = State()