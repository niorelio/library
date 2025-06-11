from core import LibraryCore
from infrastructure import FileStorage

class LibraryUI:
    def __init__(self, core: LibraryCore, storage: FileStorage):
        self.core = core
        self.storage = storage
        self.storage.load(self.core)

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

    def input_choice(self) -> str:
        return input("Выберите действие: ").strip()

    def run(self):
        while True:
            self.show_main_menu()
            choice = self.input_choice()
            if choice == "1":
                self.show_books_menu()
            elif choice == "2":
                self.show_authors_menu()
            elif choice == "3":
                self.show_genres_menu()
            elif choice == "4":
                self.search_books()
            elif choice == "5":
                self.show_recommendations()
            elif choice == "0":
                self.storage.save(self.core)
                print("Выход из программы. Данные сохранены.")
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    def show_books_menu(self):
        while True:
            print("""
            === Меню Книг ===
            1. Добавить книгу
            2. Показать все книги
            3. Отметить книгу как прочитанную
            0. Назад
            """)
            choice = self.input_choice()
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_all_books()
            elif choice == "3":
                self.mark_book_read()
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    def show_authors_menu(self):
        while True:
            print("""
            === Меню Авторов ===
            1. Добавить автора
            2. Показать всех авторов
            0. Назад
            """)
            choice = self.input_choice()
            if choice == "1":
                self.add_author()
            elif choice == "2":
                self.show_all_authors()
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    def show_genres_menu(self):
        while True:
            print("""
            === Меню Жанров ===
            1. Добавить жанр
            2. Показать все жанры
            0. Назад
            """)
            choice = self.input_choice()
            if choice == "1":
                self.add_genre()
            elif choice == "2":
                self.show_all_genres()
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")

    def add_book(self):
        title = input("Название книги: ").strip()
        author = input("Автор книги: ").strip()
        genre = input("Жанр книги: ").strip()
        if title and author and genre:
            book = self.core.add_book(title, author, genre)
            print(f"Книга '{book.title}' добавлена.")
        else:
            print("Все поля должны быть заполнены.")

    def show_all_books(self):
        books = self.core.get_all_books()
        if not books:
            print("Книг нет.")
            return
        books_sorted = sorted(books, key=lambda b: b.title.lower())
        print("Список книг:")
        for book in books_sorted:
            print(book)

    def search_books(self):
        print("Поиск книг. Оставьте поле пустым, чтобы пропустить фильтр.")
        title = input("Название: ").strip()
        author = input("Автор: ").strip()
        genre = input("Жанр: ").strip()
        results = self.core.find_books(
            title=title if title else None,
            author_name=author if author else None,
            genre_name=genre if genre else None
        )
        if not results:
            print("Книги не найдены.")
            return
        results_sorted = sorted(results, key=lambda b: b.title.lower())
        print("Результаты поиска:")
        for book in results_sorted:
            print(book)

    def mark_book_read(self):
        title = input("Введите название прочитанной книги: ").strip()
        success = self.core.mark_book_as_read(title)
        if success:
            print(f"Книга '{title}' отмечена как прочитанная.")
        else:
            print("Книга не найдена.")

    def add_author(self):
        name = input("Имя автора: ").strip()
        if name:
            author = self.core.add_author(name)
            print(f"Автор '{author.name}' добавлен.")
        else:
            print("Имя автора не может быть пустым.")

    def show_all_authors(self):
        authors = self.core.get_all_authors()
        if not authors:
            print("Авторов нет.")
            return
        authors_sorted = sorted(authors, key=lambda a: a.name.lower())
        print("Список авторов:")
        for author in authors_sorted:
            print(author.name)

    def add_genre(self):
        name = input("Название жанра: ").strip()
        if name:
            genre = self.core.add_genre(name)
            print(f"Жанр '{genre.name}' добавлен.")
        else:
            print("Название жанра не может быть пустым.")

    def show_all_genres(self):
        genres = self.core.get_all_genres()
        if not genres:
            print("Жанров нет.")
            return
        genres_sorted = sorted(genres, key=lambda g: g.name.lower())
        print("Список жанров:")
        for genre in genres_sorted:
            print(genre.name)

    def show_recommendations(self):
        recommendations = self.core.get_recommendations()
        if not recommendations:
            print("Нет рекомендаций. Почитайте что-нибудь сначала.")
            return
        recommendations_sorted = sorted(recommendations, key=lambda b: b.title.lower())
        print("Рекомендации на основе прочитанных книг:")
        for book in recommendations_sorted:
            print(book)
