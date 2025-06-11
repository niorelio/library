from core import LibraryCore
from infrastructure import FileStorage
from ui import LibraryUI

if __name__ == "__main__":
    core = LibraryCore()
    storage = FileStorage()
    ui = LibraryUI(core, storage)
    ui.run()