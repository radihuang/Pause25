from __future__ import annotations

import platform


COLORS = {
    "ink": "#21352D",
    "muted": "#6D7C74",
    "paper": "#F5F1E8",
    "surface": "#FFFCF6",
    "line": "#DDD8CC",
    "tomato": "#E45F49",
    "tomato_dark": "#C94936",
    "leaf": "#3D6655",
    "leaf_soft": "#DCE8E0",
    "sun": "#F0C46A",
    "white": "#FFFFFF",
}


def font_family() -> str:
    return "SF Pro Display" if platform.system() == "Darwin" else "Segoe UI"


FONT = font_family()
