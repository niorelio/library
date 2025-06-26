from core import LibraryCore
from infrastructure import SQLiteStorage  # <-- Заменяем FileStorage на SQLiteStorage
from ui import LibraryUI


if __name__ == "__main__":
    core = LibraryCore()
    storage = SQLiteStorage()  # Теперь используем SQLite
    ui = LibraryUI(core, storage)
    ui.run()
