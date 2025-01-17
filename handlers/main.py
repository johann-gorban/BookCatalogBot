from uuid import uuid4

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from classes import Book
from db.crud import add_book, get_book, get_random_book
from handlers.classes import AddBook, GetBook
from handlers.util import callback_send_file, message_send_file
from keyboards.main import kb_menu, kb_back, kb_list

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text='Hello! I\'m GlobusBot and I store every book you send me!', reply_markup=kb_menu)


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer(text='Hello! I\'m GlobusBot and I store every book you send me!', reply_markup=kb_menu)


@router.callback_query(lambda cmd: cmd.data.startswith('get_book'))
async def handle_get_book(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GetBook.id)
    await callback.message.answer(text='Write book\'s id')


@router.callback_query(lambda cmd: cmd.data.startswith('get_random'))
async def handle_get_random(callback: CallbackQuery):
    book = await get_random_book()
    if book is None:
        await callback.message.answer('No books found. Try again', reply_markup=kb_back)
        await callback.answer()
    else:
        await callback_send_file(book, callback)


@router.message(GetBook.id)
async def handle_book_id(message: Message, state: FSMContext):
    await state.update_data(book_id=message.text)
    data = await state.get_data()
    book = await get_book(data['book_id'])
    if book is None:
        await message.answer('No books found. Try again', reply_markup=kb_back)
    else:
        await message_send_file(book, message)
        await state.clear()


@router.callback_query(lambda cmd: cmd.data.startswith('menu'))
async def handle_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(text='That\'s all I can now', reply_markup=kb_menu)


@router.callback_query(lambda cmd: cmd.data.startswith('get_file'))
async def handle_file_callback(callback: CallbackQuery):
    book_id = callback.data.split(':')[1]
    book = await get_book(book_id)
    if book is None:
        await callback.message.answer('No books found. Try again', reply_markup=kb_back)
        await callback.answer()
    else:
        await callback_send_file(book, callback)


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
async def handle_book_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(AddBook.file)
    await message.answer('\bNow send the pdf file\b')


@router.message(AddBook.file)
async def handle_book_file(message: Message, state: FSMContext):
    file_data = message.document
    if file_data.mime_type != 'application/pdf':
        await state.set_state(AddBook.file)
        await message.answer('\bI store only PDF. Try again.\b')
    else:
        await state.update_data(file=file_data)
        data = await state.get_data()

        book = Book(id=str(uuid4())[:16],
                    name=data['name'],
                    author=data['author'],
                    year='2000',
                    url=data['file'].file_id)

        if await add_book(book):
            await message.answer(text=f'Book has been successfully added!\n Book ID: {book.id}', reply_markup=kb_menu)
        else:
            await message.answer(text=f'Something went wrong. Try again.', reply_markup=kb_menu)
        await state.clear()
