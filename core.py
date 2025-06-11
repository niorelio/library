from typing import List, Optional, Dict, Set


class Author:


    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Author(name='{self.name}')"
    

class Genre:


    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Genre(name='{self.name}')"
    

class Book:


    def __init__(self, title: str, author: Author, genre: Genre):
        self.title = title
        self.author = author
        self.genre = genre
        self.is_read = False

    def mark_as_read(self):
        self.is_read = True

    def __repr__(self):
        read_status = "✓" if self.is_read else " "
        return f"[{read_status}] '{self.title}' автор {self.author.name} ({self.genre.name})"
    

class LibraryCore:


    def __init__(self):
        self.books: List[Book] = []
        self.authors: Dict[str, Author] = {}
        self.genres: Dict[str, Genre] = {}

    def add_author(self, name: str) -> Author:
        if name not in self.authors:
            author = Author(name)
            self.authors[name] = author
        return self.authors[name]
    
    def get_all_authors(self) -> List[Author]:
        return list(self.authors.values())
    
    def add_genre(self, name: str) -> Genre:
        if name not in self.genres:
            genre = Genre(name)
            self.genres[name] = genre
        return self.genres[name]
    
    def get_all_genres(self) -> List[Genre]:
        return list(self.genres.values())
    
    def add_book(self, title: str, author_name: str, genre_name: str) -> Book:
        author = self.add_author(author_name)
        genre = self.add_genre(genre_name)
        book = Book(title, author, genre)
        self.books.append(book)
        return book
    
    def get_all_books(self) -> List[Book]:
        return self.books
    
    def find_books(self, title: Optional[str] = None,
                   author_name: Optional[str] = None,
                   genre_name: Optional[str] = None) -> List[Book]:
        results = self.books
        if title is not None:
            results = [b for b in results if title.lower() in b.title.lower()]
        if author_name is not None:
            results = [b for b in results if author_name.lower() in b.author.name.lower()]
        if genre_name is not None:
            results = [b for b in results if genre_name.lower() in b.genre.name.lower()]
        return results
    
    def mark_book_as_read(self, book_title: str) -> bool:
        for book in self.books:
            if book.title.lower() == book_title.lower():
                book.mark_as_read()
                return True
        return False
    
    def get_recommendations(self) -> List[Book]:
        read_genres: Set[str] = set()
        for book in self.books:
            if book.is_read:
                read_genres.add(book.genre.name)
        if not read_genres:
            return []
        recommendations = [book for book in self.books
                           if (book.genre.name in read_genres) and (not book.is_read)]
        return recommendations