from core_realization import BookService, AuthorService, GenreService, RecommendationService
from infrastructure import DBConnectMethods, SQLiteAuthorRepository, SQLiteGenreRepository, SQLiteBookRepository
from ui import LibraryUI


def main():
    DB_PATH = "library.db"
    db_conn = DBConnectMethods(DB_PATH)
    
    author_repo = SQLiteAuthorRepository(db_conn)
    genre_repo = SQLiteGenreRepository(db_conn)
    book_repo = SQLiteBookRepository(db_conn)  # Убраны зависимости
    
    book_service = BookService(book_repo, author_repo, genre_repo)
    author_service = AuthorService(author_repo)
    genre_service = GenreService(genre_repo)
    recommendation_service = RecommendationService(book_repo)
    
    ui = LibraryUI(book_service, author_service, genre_service, recommendation_service)
    try:
        ui.run()
    finally:
        db_conn.close()

if __name__ == "__main__":
    main()
