from __future__ import annotations

import tkinter as tk

from pause25.storage import AppRepository
from pause25.ui.main_window import MainWindow


def main() -> None:
    root = tk.Tk()
    repository = AppRepository()
    MainWindow(root, repository)
    root.mainloop()


if __name__ == "__main__":
    main()
