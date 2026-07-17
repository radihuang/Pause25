from __future__ import annotations

import tkinter as tk

from pause25.storage import AppRepository
from pause25.ui.dpi import configure_tk_scaling, enable_high_dpi_awareness
from pause25.ui.main_window import MainWindow


def main() -> None:
    enable_high_dpi_awareness()
    root = tk.Tk()
    ui_scale = configure_tk_scaling(root)
    repository = AppRepository()
    MainWindow(root, repository, ui_scale)
    root.mainloop()


if __name__ == "__main__":
    main()
