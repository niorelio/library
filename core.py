from dataclasses import dataclass
from typing import Self


@dataclass
class Author:
    name: str


    def __contains__(self, substring: str) -> bool:
        """Позволяет использовать 'in' для поиска по имени автора"""
        return substring.lower() in self.name.lower()


@dataclass
class Genre:
    name: str


    def __contains__(self, substring: str) -> bool:
        """Позволяет использовать 'in' для поиска по названию жанра"""
        return substring.lower() in self.name.lower()


@dataclass
class Book:
    title: str
    author: Author
    genre: Genre
    is_read: bool = False


    def mark_as_read(self) -> None:
        self.is_read = True

    def __contains__(self, substring: str) -> bool:
        """Позволяет использовать 'in' для поиска по книге"""
        return (substring.lower() in self.title.lower() or
                substring in self.author or
                substring in self.genre)

    def __str__(self) -> str:
        return f"[{'✓' if self.is_read else ' '}] '{self.title}' автор {self.author.name} ({self.genre.name})"

class LibraryCore:
    def __init__(self) -> None:
        self.books: list[Book] = []
        self.authors: dict[str, Author] = {}
        self.genres: dict[str, Genre] = {}

    def add_author(self, name: str) -> Author:
        """Добавляет автора, если его еще нет"""
        return self.authors.setdefault(name, Author(name))

    def add_genre(self, name: str) -> Genre:
        """Добавляет жанр, если его еще нет"""
        return self.genres.setdefault(name, Genre(name))

    def add_book(self, title: str, author_name: str, genre_name: str) -> Book:
        """Добавляет книгу с автором и жанром (создает их при необходимости)"""
        book = Book(
            title=title,
            author=self.add_author(author_name),
            genre=self.add_genre(genre_name)
        )
        self.books.append(book)
        return book

    def universal_search(self, search_term: str) -> list[Book]:
        """Ищет книги по подстроке в названии, авторе или жанре"""
        if not search_term.strip():
            return []
        
        return [book for book in self.books if search_term in book]

    def mark_book_as_read(self, book_title: str) -> bool:
        """Помечает книгу как прочитанную по названию (регистронезависимо)"""
        for book in self.books:
            if book.title.lower() == book_title.lower():
                book.mark_as_read()
                return True
        return False

    def get_recommendations(self) -> list[Book]:
        """Рекомендует непрочитанные книги в жанрах прочитанных книг"""
        read_genres = {book.genre.name for book in self.books if book.is_read}
        return [book for book in self.books 
                if not book.is_read and book.genre.name in read_genres]

    # Альтернативные названия для совместимости
    get_all_books = lambda self: self.books
    get_all_authors = lambda self: list(self.authors.values())
    get_all_genres = lambda self: list(self.genres.values())
    find_books = universal_search  # Для обратной совместимости
