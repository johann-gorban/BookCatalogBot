from typing import List


class Book:
    id:     str
    name:   str
    author: str
    url:    str
    year:   str

    def __init__(self,
                 id: str | None = None,
                 name: str | None = None,
                 author: str | None = None,
                 url: str | None = None,
                 year: str | None = None):
        self.id = id
        self.name = name
        self.author = author
        self.url = url
        self.year = year

    def get_url(self) -> str:
        return self.url

    def get_data(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'url': self.url,
            'year': self.year
        }


class BookList:
    books: List[Book]
    size:  int

    def __init__(self):
        self.books = []
        self.size = 0

    def __iter__(self):
        return iter(self.books)

    def __getitem__(self, item):
        return self.books[item]

    def get_book(self, id: str) -> Book | None:
        for book in self.books:
            if book.id == id:
                return book
        else:
            return None

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        self.size = len(self.books)

    def get_size(self) -> int:
        return self.size

