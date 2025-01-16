from uuid import uuid4

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from classes import Book
from db.crud import add_book, get_book
from handlers.classes import AddBook
from keyboards.main import kb_menu, kb_back, kb_list

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(text='Hello! I\'m GlobusBot and I store every book you send me!', reply_markup=kb_menu)


@router.callback_query(lambda cmd: cmd.data.startswith('menu'))
async def handle_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(text='That\'s all I can now', reply_markup=kb_menu)


@router.callback_query(lambda cmd: cmd.data.startswith('get_file'))
async def handle_file_callback(callback: CallbackQuery):
    book_id = callback.data.split(':')[1]
    book = get_book(book_id).get_data()
    try:
        await callback.message.answer_document(document=book['url'],
                                               filename='book.pdf',
                                               caption='Your book\'s here!'
                                                       f'\n\"{book["name"]}\" '
                                                       f'by {book["author"]}')
        await callback.answer()
    except TelegramBadRequest:
        await callback.message.answer('Something went wrong. Try again.', reply_markup=kb_back)
        await callback.answer()


@router.callback_query(lambda cmd: cmd.data.startswith('navigate'))
async def handle_nav_callback(callback: CallbackQuery):
    page = int(callback.data.split(':')[1])
    try:
        new_kb = await kb_list(page)
        await callback.message.edit_text(text='That\'s all I have', reply_markup=new_kb)
        await callback.answer()
    except Exception as e:
        raise e
        # await callback.message.edit_text(text='A error occurred. Try again.', reply_markup=kb_back)



@router.callback_query(lambda cmd: cmd.data.startswith('add_book'))
async def handle_add_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddBook.name)
    await callback.message.answer('\bEnter book name\b\nExample: "OOP in C++"')


@router.message(AddBook.name)
async def handle_book_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddBook.author)
    await message.answer('\bEnter book\'s author\b\nExample: "R. Lafore"')


@router.message(AddBook.author)
async def handle_book_name(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(AddBook.file)
    await message.answer('\bNow send the pdf file\b')


@router.message(AddBook.file)
async def handle_book_name(message: Message, state: FSMContext):
    file_data = message.document
    if file_data.mime_type != 'application/pdf':
        await state.set_state(AddBook.file)
        await message.answer('\bNo PDF received. Try again.\b')
    else:
        await state.update_data(file=file_data)
        data = await state.get_data()

        book = Book(id=str(uuid4())[:16],
                    name=data['name'],
                    author=data['author'],
                    year='2000',
                    url=data['file'].file_id)

        if add_book(book):
            await message.answer(text=f'Book has been successfully added!\n Book ID: {book.id}', reply_markup=kb_menu)
        else:
            await message.answer(text=f'Something went wrong. Try again.', reply_markup=kb_menu)
        await state.clear()
