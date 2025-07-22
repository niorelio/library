import sqlite3
from core_interfaces import Book, Author, Genre, IBookRepository, IAuthorRepository, IGenreRepository


class DBConnectMethods:


    def __init__(self, db: str):
        self.db = db
        self.connection = sqlite3.connect(self.db)
        self.connection.row_factory = sqlite3.Row
    
    def execute_query(self, query: str, *params) -> None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
    
    def execute_get_data(self, query: str, *params) -> list:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def get_int(self, query: str, *params) -> int | None:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result[0] if result else None
    
    def get_lastrowid(self) -> int:
        return self.connection.cursor().lastrowid
    
    def execute_update(self, query: str, *params) -> int:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def close(self) -> None:
        self.connection.close()

class SQLiteBookRepository(IBookRepository):


    def __init__(self, db_conn: DBConnectMethods):  # Убраны зависимости
        self.db = db_conn
        self._create_tables()
    
    def _create_tables(self):
        self.db.execute_query('''
                              CREATE TABLE IF NOT EXISTS books (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              title TEXT NOT NULL,
                              author_id INTEGER NOT NULL,
                              genre_id INTEGER NOT NULL,
                              is_read BOOLEAN NOT NULL DEFAULT 0,
                              FOREIGN KEY (author_id) REFERENCES authors(id),
                              FOREIGN KEY (genre_id) REFERENCES genres(id)
                              )
                              ''')
    
    def add_book(self, book: Book) -> int:
        self.db.execute_query(
            "INSERT INTO books (title, author_id, genre_id, is_read) VALUES (?, ?, ?, ?)",
            book.title, book.author.id, book.genre.id, book.is_read
        )
        return self.db.get_lastrowid()
    
    def get_all_books(self) -> list[Book]:
        query = """
        SELECT 
        b.id, b.title, b.is_read,
        a.id AS author_id, a.name AS author_name,
        g.id AS genre_id, g.name AS genre_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.id
        LEFT JOIN genres g ON b.genre_id = g.id
        """
        rows = self.db.execute_get_data(query)
        return self._map_rows_to_books(rows)
    
    def get_book_by_id(self, book_id: int) -> Book | None:
        query = """
        SELECT 
        b.id, b.title, b.is_read,
        a.id AS author_id, a.name AS author_name,
        g.id AS genre_id, g.name AS genre_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.id
        LEFT JOIN genres g ON b.genre_id = g.id
        WHERE b.id = ?
        """
        rows = self.db.execute_get_data(query, book_id)
        if rows:
            return self._map_row_to_book(rows[0])
        return None
    
    def get_unread_books(self, limit: int = 5) -> list[Book]:
        query = """
        SELECT 
        b.id, b.title, b.is_read,
        a.id AS author_id, a.name AS author_name,
        g.id AS genre_id, g.name AS genre_name
        FROM books b
        LEFT JOIN genres g ON b.genre_id = g.id
        WHERE b.is_read = 0 
        ORDER BY b.id DESC 
        LIMIT ?
        """
        rows = self.db.execute_get_data(query, limit)
        return self._map_rows_to_books(rows)
    
    def mark_as_read(self, book_id: int) -> bool:
        rowcount = self.db.execute_update(
            "UPDATE books SET is_read = 1 WHERE id = ?",
            book_id
        )
        return rowcount > 0
    
    def universal_search(self, term: str, limit: int = 20) -> list[Book]:
        pattern = f'%{term.lower()}%'
        query = """
        SELECT 
        b.id, b.title, b.is_read,
        a.id AS author_id, a.name AS author_name,
        g.id AS genre_id, g.name AS genre_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.id
        LEFT JOIN genres g ON b.genre_id = g.id
        WHERE LOWER(b.title) LIKE ?
        OR LOWER(a.name) LIKE ? 
        OR LOWER(g.name) LIKE ?
        ORDER BY 
        CASE 
        WHEN LOWER(b.title) LIKE ? THEN 1 
        WHEN LOWER(a.name) LIKE ? THEN 2 
        ELSE 3 
        END
        LIMIT ?
        """
        rows = self.db.execute_get_data(
            query, 
            pattern, pattern, pattern,
            pattern, pattern, limit
        )
        return self._map_rows_to_books(rows)
    
    def get_read_books(self) -> list[Book]:
        query = """
            SELECT 
                b.id, b.title, b.is_read,
                a.id AS author_id, a.name AS author_name,
                g.id AS genre_id, g.name AS genre_name
            FROM books b
            LEFT JOIN authors a ON b.author_id = a.id
            LEFT JOIN genres g ON b.genre_id = g.id
            WHERE b.is_read = 1
           """
        rows = self.db.execute_get_data(query)
        return self._map_rows_to_books(rows)

    def get_unread_books_by_author(self, author_id: int, limit: int = 5) -> list[Book]:
        query = """
            SELECT 
                b.id, b.title, b.is_read,
                a.id AS author_id, a.name AS author_name,
                g.id AS genre_id, g.name AS genre_name
            FROM books b
            LEFT JOIN authors a ON b.author_id = a.id
            LEFT JOIN genres g ON b.genre_id = g.id
            WHERE b.author_id = ? AND b.is_read = 0 
            ORDER BY b.id DESC 
            LIMIT ?
            """
        rows = self.db.execute_get_data(query, author_id, limit)
        return self._map_rows_to_books(rows)
    
    def _map_rows_to_books(self, rows) -> list[Book]:
        books = []
        for row in rows:
            books.append(self._map_row_to_book(row))
        return books
    
    def _map_row_to_book(self, row) -> Book:
        author = Author(id=row['author_id'], name=row['author_name'])
        genre = Genre(id=row['genre_id'], name=row['genre_name'])
        return Book(
            id=row['id'],
            title=row['title'],
            author=author,
            genre=genre,
            is_read=bool(row['is_read'])
        )

class SQLiteAuthorRepository(IAuthorRepository):
    def __init__(self, db_conn: DBConnectMethods):
        self.db = db_conn
        self._create_tables()
    
    def _create_tables(self):
        self.db.execute_query('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
    
    def add_author(self, author: Author) -> int:
        self.db.execute_query(
            "INSERT OR IGNORE INTO authors (name) VALUES (?)",
            author.name
        )
        
        author_id = self.db.get_int(
            "SELECT id FROM authors WHERE name = ?",
            author.name
        )
        return author_id
    
    def get_all_authors(self) -> list[Author]:
        rows = self.db.execute_get_data("SELECT id, name FROM authors")
        return [Author(id=row['id'], name=row['name']) for row in rows]
    
    def find_author_by_name(self, name: str) -> Author | None:
        rows = self.db.execute_get_data(
            "SELECT id, name FROM authors WHERE name = ?",
            name
        )
        return Author(id=rows[0]['id'], name=rows[0]['name']) if rows else None
    
    def get_author_by_id(self, author_id: int) -> Author | None:
        rows = self.db.execute_get_data(
            "SELECT id, name FROM authors WHERE id = ?",
            author_id
        )
        return Author(id=rows[0]['id'], name=rows[0]['name']) if rows else None

class SQLiteGenreRepository(IGenreRepository):
    def __init__(self, db_conn: DBConnectMethods):
        self.db = db_conn
        self._create_tables()
    
    def _create_tables(self):
        self.db.execute_query('''
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
    
    def add_genre(self, genre: Genre) -> int:
        self.db.execute_query(
            "INSERT OR IGNORE INTO genres (name) VALUES (?)",
            genre.name
        )
        
        genre_id = self.db.get_int(
            "SELECT id FROM genres WHERE name = ?",
            genre.name
        )
        return genre_id

    def get_all_genres(self) -> list[Genre]:
        rows = self.db.execute_get_data("SELECT id, name FROM genres")
        return [Genre(id=row['id'], name=row['name']) for row in rows]

    def find_genre_by_name(self, name: str) -> Genre | None:
        rows = self.db.execute_get_data(
            "SELECT id, name FROM genres WHERE name = ?",
            name
        )
        return Genre(id=rows[0]['id'], name=rows[0]['name']) if rows else None

    def get_genre_by_id(self, genre_id: int) -> Genre | None:
        rows = self.db.execute_get_data(
            "SELECT id, name FROM genres WHERE id = ?",
            genre_id
        )
        return Genre(id=rows[0]['id'], name=rows[0]['name']) if rows else None
