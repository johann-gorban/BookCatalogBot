from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from classes import Book
from keyboards.main import kb_back, kb_back_from_everywhere

async def message_send_file(book: Book, message: Message):
    book = book.get_data()
    try:
        await message.answer_document(document=book['url'],
                                      filename=f'{book["name"]}.pdf',
                                      caption='Your book\'s here!'
                                              f'\n\"{book["name"]}\" '
                                              f'by {book["author"]}'
                                              f'\n\nID: {book["id"]}',
                                      reply_markup=kb_back_from_everywhere)
    except TelegramBadRequest:
        await message.answer('Something went wrong. Try again.', reply_markup=kb_back)


async def callback_send_file(book: Book, callback: CallbackQuery):
    book = book.get_data()
    try:
        await callback.message.answer_document(document=book['url'],
                                               filename='book.pdf',
                                               caption='Your book\'s here!'
                                                       f'\n\"{book["name"]}\" '
                                                       f'by {book["author"]}'
                                                       f'\n\nID: {book["id"]}',
                                               reply_markup=kb_back_from_everywhere)
    except TelegramBadRequest:
        await callback.message.answer('Something went wrong. Try again.', reply_markup=kb_back)
        await callback.answer()