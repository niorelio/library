from core import LibraryCore
from infrastructure import SQLiteStorage


class LibraryUI:

    
    def __init__(self, core: LibraryCore, storage: SQLiteStorage):
        self.core = core
        self.storage = storage
        self.storage.load(self.core)

    def show_main_menu(self):
        """Главное меню программы"""
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

    def input_choice(self, prompt: str = "Выберите действие: ") -> str:
        """Универсальный ввод выбора пользователя"""
        return input(prompt).strip()

    def run(self):
        """Основной цикл программы"""
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
                    self.storage.save(self.core)
                    print("Выход из программы. Данные сохранены.")
                    break
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def show_books_menu(self):
        """Меню работы с книгами"""
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
                case "0": break
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def show_authors_menu(self):
        """Меню работы с авторами"""
        while True:
            print("\n=== Меню Авторов ===")
            print("1. Добавить автора")
            print("2. Показать всех авторов")
            print("0. Назад")
            
            match self.input_choice():
                case "1": self.add_author()
                case "2": self.show_all_authors()
                case "0": break
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def show_genres_menu(self):
        """Меню работы с жанрами"""
        while True:
            print("\n=== Меню Жанров ===")
            print("1. Добавить жанр")
            print("2. Показать все жанры")
            print("0. Назад")
            
            match self.input_choice():
                case "1": self.add_genre()
                case "2": self.show_all_genres()
                case "0": break
                case _: print("Неверный выбор. Попробуйте еще раз.")

    def add_book(self):
        """Добавление новой книги"""
        print("\nДобавление новой книги:")
        title = input("Название книги: ").strip()
        author = input("Автор книги: ").strip()
        genre = input("Жанр книги: ").strip()

        if not all([title, author, genre]):
            print("Все поля должны быть заполнены!")
            return

        book = self.core.add_book(title, author, genre)
        print(f"\nКнига '{book.title}' успешно добавлена!")

    def show_all_books(self):
        """Отображение всех книг"""
        books = self.core.get_all_books()
        if not books:
            print("\nВ библиотеке пока нет книг.")
            return

        print("\nСписок всех книг:")
        for i, book in enumerate(sorted(books, key=lambda b: b.title.lower()), 1):
            print(f"{i}. {book}")

    def universal_search(self):
        """Универсальный поиск по всем полям"""
        print("\nУниверсальный поиск")
        print("Введите часть названия, автора или жанра:")
        search_term = self.input_choice("Поиск: ")
        
        if not search_term:
            print("Поисковый запрос не может быть пустым!")
            return

        results = self.core.universal_search(search_term)
        if not results:
            print(f"\nПо запросу '{search_term}' ничего не найдено.")
            return

        print(f"\nНайдено {len(results)} книг:")
        for i, book in enumerate(sorted(results, key=lambda b: b.title.lower()), 1):
            print(f"{i}. {book}")

    def mark_book_read(self):
        """Пометить книгу как прочитанную"""
        title = self.input_choice("Введите название прочитанной книги: ")
        if not title:
            print("Название не может быть пустым!")
            return

        if self.core.mark_book_as_read(title):
            print(f"Книга '{title}' отмечена как прочитанная!")
        else:
            print("Книга не найдена!")
