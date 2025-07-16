from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Author:
    name: str
    id: int | None = None  


@dataclass
class Genre:
    name: str
    id: int | None = None  

    def __contains__(self, substring: str) -> bool:
        return substring.lower() in self.name.lower()


@dataclass
class Book:
    title: str
    author: Author
    genre: Genre
    is_read: bool = False
    id: int | None = None 

    def mark_as_read(self) -> None:
        self.is_read = True

    def __contains__(self, substring: str) -> bool:
        return (substring.lower() in self.title.lower() or
                substring in self.author or
                substring in self.genre)
    
    def __str__(self):
        status = "✓" if self.is_read else " "
        return f"{self.id}. [{status}] {self.title} ({self.author.name}, {self.genre.name})"


class IBookRepository(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> int:
        pass
    
    @abstractmethod
    def get_all_books(self) -> list[Book]:
        pass
    
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book | None:
        pass
    
    @abstractmethod
    def universal_search(self, term: str, limit: int = 20) -> list[Book]:
        pass
    
    @abstractmethod
    def mark_as_read(self, book_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_unread_books(self, limit: int = 5) -> list[Book]:
        pass

    @abstractmethod
    def get_read_books(self) -> list[Book]:
        pass

    @abstractmethod
    def get_unread_books_by_author(self, author_id: int, limit: int = 5) -> list[Book]:
        pass


class IAuthorRepository(ABC):
    @abstractmethod
    def add_author(self, author: Author) -> int:
        pass
    
    @abstractmethod
    def get_all_authors(self) -> list[Author]:
        pass
    
    @abstractmethod
    def find_author_by_name(self, name: str) -> Author | None:
        pass
    
    @abstractmethod
    def get_author_by_id(self, author_id: int) -> Author | None:
        pass


class IGenreRepository(ABC):
    @abstractmethod
    def add_genre(self, genre: Genre) -> int:
        pass
    
    @abstractmethod
    def get_all_genres(self) -> list[Genre]:
        pass
    
    @abstractmethod
    def find_genre_by_name(self, name: str) -> Genre | None:
        pass
    
    @abstractmethod
    def get_genre_by_id(self, genre_id: int) -> Genre | None:
        pass
