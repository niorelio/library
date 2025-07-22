from core_interfaces import Author, Book, Genre, IAuthorRepository, IBookRepository, IGenreRepository


class BookService:


    def __init__(self, book_repo: IBookRepository, author_repo: IAuthorRepository, genre_repo: IGenreRepository):
        self.book_repo = book_repo
        self.author_repo = author_repo
        self.genre_repo = genre_repo
    
    def get_all_books(self):
        return self.book_repo.get_all_books()
    
    def add_book(self, title, author_name, genre_name):
        if not all([title, author_name, genre_name]):
            raise ValueError("Title, author and genre must be provided")
        
        author = self.author_repo.find_author_by_name(author_name)
        if not author:
            author = Author(id=None, name=author_name)
            author.id = self.author_repo.add_author(author)

        genre = self.genre_repo.find_genre_by_name(genre_name)
        if not genre:
            genre = Genre(id=None, name=genre_name)
            genre.id = self.genre_repo.add_genre(genre)
        
        try:
            book = Book(
                title=title,
                author=author,
                genre=genre
            )
            book.id = self.book_repo.add_book(book)
            return book
        except Exception as e:
            raise RuntimeError(f"Failed to add book: {str(e)}")

    def universal_search(self, term: str, limit: int = 20) -> list[Book]:
        return self.book_repo.universal_search(term, limit)

    def mark_book_as_read(self, book_id):
        return self.book_repo.mark_as_read(book_id)


class AuthorService:


    def __init__(self, author_repo: IAuthorRepository):
        self.author_repo = author_repo

    def add_author(self, name):
        author = Author(name=name)
        return self.author_repo.add_author(author)

    def get_all_authors(self):
        return self.author_repo.get_all_authors()


class GenreService:


    def __init__(self, genre_repo: IGenreRepository):
        self.genre_repo = genre_repo

    def add_genre(self, name):
        genre = Genre(name=name)
        return self.genre_repo.add_genre(genre)

    def get_all_genres(self):
        return self.genre_repo.get_all_genres()


class RecommendationService:

    
    def __init__(self, book_repo: IBookRepository):
        self.book_repo = book_repo

    def get_recommendations(self) -> list[Book]:
        read_books = self.book_repo.get_read_books()
        if not read_books:
            return self.book_repo.get_unread_books(limit=5)

        # Считаем количество прочитанных книг по авторам
        author_read_count = {}
        for book in read_books:
            author_id = book.author.id
            author_read_count[author_id] = author_read_count.get(author_id, 0) + 1

        # Сортируем авторов по количеству прочитанных книг (убывание)
        sorted_authors = sorted(
            author_read_count.items(),
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []
        added_book_ids = set()

        # Собираем рекомендации от самых любимых авторов
        for author_id, _ in sorted_authors:
            if len(recommendations) >= 5:
                break
                
            author_books = self.book_repo.get_unread_books_by_author(author_id, limit=5)
            for book in author_books:
                if book.id not in added_book_ids and not book.is_read:
                    recommendations.append(book)
                    added_book_ids.add(book.id)
                    if len(recommendations) >= 5:
                        break

        # Добираем книги из общего пула если нужно
        if len(recommendations) < 5:
            additional = self.book_repo.get_unread_books(limit=10)
            for book in additional:
                if book.id not in added_book_ids and not book.is_read:
                    recommendations.append(book)
                    added_book_ids.add(book.id)
                    if len(recommendations) >= 5:
                        break

        return recommendations[:5]
