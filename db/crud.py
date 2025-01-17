from classes import Book, BookList
from config import DB_PATH

import aiosqlite


async def _create_database():
    """
    Создаёт таблицу в SQLite базе данных.

    Таблица содержит следующие поля:
    - id: TEXT, уникальный идентификатор, автоинкремент с началом от 1000.
    - name: TEXT, не может быть NULL.
    - author: TEXT, не может быть NULL.
    - url: TEXT, не может быть NULL.
    - year: TEXT, не может быть NULL.

    Параметры:
        db_path (str): Путь к SQLite базе данных.
    """
    query = """
    CREATE TABLE IF NOT EXISTS books (
        id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        author TEXT NOT NULL,
        url TEXT NOT NULL,
        year TEXT NOT NULL
    );
    """
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            await conn.commit()
    except aiosqlite.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")


async def add_book(book: Book) -> bool:
    query = """
    INSERT INTO books (id, name, author, url, year)
    VALUES (?, ?, ?, ?, ?);
    """
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cursor = await conn.cursor()
            await cursor.execute(query, (book.id, book.name, book.author, book.url, book.year))
            await conn.commit()
        return True
    except aiosqlite.Error as e:
        print(f"Ошибка при добавлении книги: {e}")
        return False


async def get_books() -> BookList:
    query = "SELECT * FROM books;"
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            rows = await cursor.fetchall()

            books = BookList()
            for row in rows:
                book = Book(id=row[0],
                            name=row[1],
                            author=row[2],
                            url=row[3],
                            year=row[4])
                books.add_book(book)
        return books
    except aiosqlite.Error:
        return BookList()


async def get_book(id: str) -> Book | None:
    query = "SELECT * FROM books WHERE id = ?;"
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cursor = await conn.cursor()
            await cursor.execute(query, (id,))
            row = await cursor.fetchone()

            if row:
                return Book(id=row[0],
                            name=row[1],
                            author=row[2],
                            url=row[3],
                            year=row[4])
            else:
                return Book()
    except aiosqlite.Error as e:
        print(f"Ошибка при получении книги: {e}")
        return None


async def get_random_book() -> Book | None:
    query = """
    SELECT * FROM books
    ORDER BY RANDOM()
    LIMIT 1 OFFSET 1;
    """
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cursor = await conn.cursor()
            await cursor.execute(query)
            row = await cursor.fetchone()

            if row:
                return Book(id=row[0],
                            name=row[1],
                            author=row[2],
                            url=row[3],
                            year=row[4])
            else:
                return Book()
    except aiosqlite.Error as e:
        print(f"Ошибка при получении книги: {e}")
        return None