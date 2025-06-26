import sqlite3
from core import LibraryCore, Book, Author, Genre


class SQLiteStorage:

    
    def __init__(self, db_name: str = "library.db"):
        self.db_name = db_name
        self._init_db()  # Создаем таблицы при инициализации


    def _init_db(self):
        """Создает таблицы, если их нет."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Таблица авторов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)

            # Таблица жанров
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)

            # Таблица книг (связь с авторами и жанрами)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    genre_id INTEGER NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (author_id) REFERENCES authors(id),
                    FOREIGN KEY (genre_id) REFERENCES genres(id)
                )
            """)
            conn.commit()

    def save(self, core: LibraryCore):
        """Сохраняет данные в SQLite."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Очищаем старые данные (опционально, можно и без этого)
            cursor.execute("DELETE FROM books")
            cursor.execute("DELETE FROM genres")
            cursor.execute("DELETE FROM authors")

            # Сохраняем авторов
            for author in core.authors.values():
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (author.name,)
                )

            # Сохраняем жанры
            for genre in core.genres.values():
                cursor.execute(
                    "INSERT INTO genres (name) VALUES (?)",
                    (genre.name,)
                )

            # Сохраняем книги
            for book in core.books:
                # Получаем ID автора и жанра
                cursor.execute(
                    "SELECT id FROM authors WHERE name = ?",
                    (book.author.name,)
                )
                author_id = cursor.fetchone()[0]
                
                cursor.execute(
                    "SELECT id FROM genres WHERE name = ?",
                    (book.genre.name,)
                )
                genre_id = cursor.fetchone()[0]
                
                cursor.execute(
                    """INSERT INTO books 
                    (title, author_id, genre_id, is_read) 
                    VALUES (?, ?, ?, ?)""",
                    (book.title, author_id, genre_id, book.is_read)
                )
            
            conn.commit()

    def load(self, core: LibraryCore):
        """Загружает данные из SQLite."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # Загружаем авторов
            cursor.execute("SELECT name FROM authors")
            authors = cursor.fetchall()
            for (name,) in authors:
                core.add_author(name)

            # Загружаем жанры
            cursor.execute("SELECT name FROM genres")
            genres = cursor.fetchall()
            for (name,) in genres:
                core.add_genre(name)

            # Загружаем книги
            cursor.execute("""
                SELECT b.title, a.name, g.name, b.is_read
                FROM books b
                JOIN authors a ON b.author_id = a.id
                JOIN genres g ON b.genre_id = g.id
            """)
            books_data = cursor.fetchall()

            core.books.clear()
            for title, author_name, genre_name, is_read in books_data:
                book = core.add_book(title, author_name, genre_name)
                if is_read:
                    book.mark_as_read()
