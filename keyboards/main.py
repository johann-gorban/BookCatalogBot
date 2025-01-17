from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.crud import get_books
from keyboards.config import ITEMS_PER_PAGE

kb_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Add new book 📚', callback_data='add_book')],
    # [InlineKeyboardButton(text='Delete book', callback_data='delete_book')],
    [InlineKeyboardButton(text='🙊 Get random book', callback_data='get_random')],
    [InlineKeyboardButton(text='Get book by ID 🪪', callback_data='get_book')],
    [InlineKeyboardButton(text='🗂️ Get book list', callback_data='navigate:1')]
])

kb_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🏠 Menu', callback_data='menu')]
])

kb_back_from_everywhere = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/menu')]
], resize_keyboard=True)

async def kb_list(page: int = 1):
    books = await get_books()

    total_items = books.get_size()
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    curr_books = books[start:end]

    # Objects buttons
    button_rows = []
    for book in curr_books:
        data = book.get_data()
        button_rows.append([InlineKeyboardButton(text=data['name'], callback_data=f'get_file:{data["id"]}')])

    keyboard = InlineKeyboardBuilder(button_rows)

    # Navigation buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='⬅️', callback_data=f'navigate:{page - 1}'))
    if page < total_pages and total_items > ITEMS_PER_PAGE:
        nav_buttons.append(InlineKeyboardButton(text='➡️', callback_data=f'navigate:{page + 1}'))

    if nav_buttons:
        keyboard.row(*nav_buttons)

    keyboard.add(InlineKeyboardButton(text='🏠 Menu', callback_data='menu'))

    return keyboard.as_markup()