from core_interfaces import Book, Author, Genre
from core_realization import BookService, AuthorService, GenreService, RecommendationService

class LibraryUI:
    def __init__(self, 
                 book_service: BookService,
                 author_service: AuthorService,
                 genre_service: GenreService,
                 recommendation_service: RecommendationService):
        self.book_service = book_service
        self.author_service = author_service
        self.genre_service = genre_service
        self.recommendation_service = recommendation_service

    def show_main_menu(self):
        print("""
 ████─█──█─████───██─█──█─████─███─███─█──█─████
 █────█──█─█─────█─█─█──█─█──█──█──█───█─█──█──█
 ████─█─██─████─█──█─█─██─█──█──█──███─██───████
 █──█─██─█─█──█─█──█─██─█─█──█──█──█───█─█──█──█
 ████─█──█─████─█──█─█──█─████──█──███─█──█─█──█
        """)
        print("""
        1. Книги
        2. Авторы
        3. Жанры
        4. Поиск
        5. Рекомендации
        0. Выход
        """)

    def input_choice(self, prompt="Выберите действие: "):
        return input(prompt).strip()

    def run(self):
        while True:
            self.show_main_menu()
            choice = self.input_choice()

            match choice:
                case "1": self.show_books_menu()
                case "2": self.show_authors_menu()
                case "3": self.show_genres_menu()
                case "4": self.universal_search()
                case "5": self.show_recommendations()
                case "0": 
                    print("Выход из программы.")
                    return
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def show_books_menu(self):
        while True:
            print("\n=== Меню Книг ===")
            print("1. Добавить книгу")
            print("2. Показать все книги")
            print("3. Отметить книгу как прочитанную")
            print("0. Назад")
            
            match self.input_choice():
                case "1": self.add_book()
                case "2": self.show_all_books()
                case "3": self.mark_book_read()
                case "0": return
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def show_authors_menu(self):
        while True:
            print("\n=== Меню Авторов ===")
            print("1. Добавить автора")
            print("2. Показать всех авторов")
            print("0. Назад")
            
            match self.input_choice():
                case "1": self.add_author()
                case "2": self.show_all_authors()
                case "0": return
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def show_genres_menu(self):
        while True:
            print("\n=== Меню Жанров ===")
            print("1. Добавить жанр")
            print("2. Показать все жанры")
            print("0. Назад")
            
            match self.input_choice():
                case "1": self.add_genre()
                case "2": self.show_all_genres()
                case "0": return
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def add_book(self):
        print("\nДобавление новой книги:")
        title = input("Название книги: ").strip()
        author = input("Автор книги: ").strip()
        genre = input("Жанр книги: ").strip()

        if not all([title, author, genre]):
            print("Все поля должны быть заполнены!")
            return

        try:
            book = self.book_service.add_book(title, author, genre)
            print(f"\nКнига '{book.title}' успешно добавлена! (ID: {book.id})")
        except Exception as e:
            print(f"\nОшибка при добавлении книги: {str(e)}")

    def show_all_books(self):
        books = self.book_service.get_all_books()
        if not books:
            print("\nВ библиотеке пока нет книг.")
            return

        print("\nСписок всех книг:")
        for book in books:
            print(book)

    def universal_search(self):
        print("\n=== Универсальный поиск ===")
        print("Введите часть названия, автора или жанра")
        print("Для выхода оставьте поле пустым")
        search_term = self.input_choice("Поиск: ").strip()
    
        if not search_term:
            return

        try:
            results = self.book_service.universal_search(search_term, limit=50)
        except Exception as e:
            print(f"\nОшибка при выполнении поиска: {e}")
            return

        if not results:
            print(f"\nПо запросу '{search_term}' ничего не найдено.")
            return

        print(f"\nНайдено {len(results)} книг:")
        for i, book in enumerate(results, start=1):
            status = "✓" if book.is_read else " "
            title = self.highlight_term(book.title, search_term)
            author_name = self.highlight_term(book.author.name, search_term)
            genre_name = self.highlight_term(book.genre.name, search_term)
            print(f"{i}. [{status}] {title} ({author_name}, {genre_name})")
    
        print("\nДополнительные действия:")
        print("1. Отметить книгу как прочитанную")
        print("2. Вернуться в главное меню")
    
        choice = self.input_choice("Выберите действие: ")
        if choice == "1":
            try:
                book_num = int(self.input_choice("Введите номер книги: "))
                if 1 <= book_num <= len(results):
                    book = results[book_num-1]
                    if self.book_service.mark_book_as_read(book.id):
                        print(f"Книга '{book.title}' отмечена как прочитанная!")
                    else:
                        print("Книга не найдена!")
                else:
                    print("Некорректный номер книги")
            except ValueError:
                print("Номер должен быть числом")

    def highlight_term(self, text: str, term: str) -> str:
        if not term:
            return text
    
        try:
            start = text.lower().find(term.lower())
            if start == -1:
                return text
        
            original_term = text[start:start+len(term)]
            highlighted = f"\033[1;31m{original_term}\033[0m"
            return text[:start] + highlighted + text[start+len(term):]
        except:
            return text

    def mark_book_read(self):
        self.show_all_books()
        if not self.book_service.get_all_books():
            return
            
        try:
            book_id = int(self.input_choice("\nВведите ID прочитанной книги: "))
            if self.book_service.mark_book_as_read(book_id):
                print(f"Книга с ID {book_id} отмечена как прочитанная!")
            else:
                print("Книга не найдена!")
        except ValueError:
            print("ID должен быть числом!")

    def show_recommendations(self):
        recommendations = self.recommendation_service.get_recommendations()
        if not recommendations:
            print("\nНет рекомендаций. Прочитайте несколько книг, чтобы получить рекомендации.")
            return

        print("\nРекомендуемые книги:")
        for i, book in enumerate(recommendations, start=1):
            print(f"{i}. {book.title} ({book.author.name}, {book.genre.name})")

    def add_author(self):
        name = input("Имя автора: ").strip()
        if not name:
            print("Имя автора не может быть пустым!")
            return
        self.author_service.add_author(name)
        print(f"Автор '{name}' успешно добавлен!")

    def show_all_authors(self):
        authors = self.author_service.get_all_authors()
        if not authors:
            print("\nВ библиотеке нет авторов.")
            return

        print("\nСписок авторов:")
        for author in authors:
            print(f"{author.id}. {author.name}")

    def add_genre(self):
        name = input("Название жанра: ").strip()
        if not name:
            print("Название жанра не может быть пустым!")
            return
        self.genre_service.add_genre(name)
        print(f"Жанр '{name}' успешно добавлен!")

    def show_all_genres(self):
        genres = self.genre_service.get_all_genres()
        if not genres:
            print("\nВ библиотеке нет жанров.")
            return

        print("\nСписок жанров:")
        for genre in genres:
            print(f"{genre.id}. {genre.name}")
