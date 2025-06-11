import json
from core import LibraryCore


class FileStorage:


    def __init__(self, filename: str = "library_data.json"):
        self.filename = filename

    def save(self, core: LibraryCore):
        data = {
            "authors": list(core.authors.keys()),
            "genres": list(core.genres.keys()),
            "books": [{
                "title": book.title,
                "author": book.author.name,
                "genre": book.genre.name,
                "is_read": book.is_read
            } for book in core.books]
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    def load(self, core: LibraryCore):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Загрузка авторов и жанров
            for author_name in data.get("authors", []):
                core.add_author(author_name)
            for genre_name in data.get("genres", []):
                core.add_genre(genre_name)
            # Загрузка книг
            core.books.clear()
            for book_data in data.get("books", []):
                book = core.add_book(book_data["title"], book_data["author"], book_data["genre"])
                if book_data.get("is_read"):
                    book.mark_as_read()
        except FileNotFoundError:
            # Файл отсутствует – загрузка пропускается
            pass