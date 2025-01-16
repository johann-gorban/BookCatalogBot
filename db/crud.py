import os

from classes import Book, BookList
from config import DB_PATH, FILE_PATH

import sqlite3

def create_database():
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
        # Подключение к базе данных
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Выполнение запроса на создание таблицы
        cursor.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")


def add_book(book: Book) -> bool:
    query = """
    INSERT INTO books (id, name, author, url, year)
    VALUES (?, ?, ?, ?, ?);
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (book.id, book.name, book.author, book.url, book.year))
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении книги: {e}")
        return False


def remove_book(id: str) -> bool:
    query = "DELETE FROM books WHERE id = ?;"
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()

        if delete_file(str(FILE_PATH / id) + '.pdf'):
            return True
        return False
    except sqlite3.Error:
        return False


def get_books() -> BookList:
    query = "SELECT * FROM books;"
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            books = BookList()
            for row in rows:
                book = Book(id=row[0],
                            name=row[1],
                            author=row[2],
                            url=row[3],
                            year=row[4])
                books.add_book(book)
        return books
    except sqlite3.Error:
        return BookList()


def get_book(id: str) -> Book | None:
    query = "SELECT * FROM books WHERE id = ?;"
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()

            if row:
                return Book(id=row[0],
                            name=row[1],
                            author=row[2],
                            url=row[3],
                            year=row[4])
            else:
                return Book()
    except sqlite3.Error as e:
        print(f"Ошибка при получении книги: {e}")
        return None


def add_file(data: bytes, url: str) -> bool:
    try:
        with open(url, 'wb') as file:
            file.write(data)
        return True
    except Exception:
        return False


def delete_file(url: str) -> bool:
    try:
        if os.path.exists(url):
            os.remove(url)
        return True
    except Exception:
        return False