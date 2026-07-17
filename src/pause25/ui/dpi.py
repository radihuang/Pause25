from __future__ import annotations

import ctypes
import platform
import tkinter as tk
from dataclasses import dataclass


BASE_DPI = 96.0
MIN_SCALE = 1.0
MAX_SCALE = 4.0


@dataclass(frozen=True, slots=True)
class UiScale:
    factor: float = 1.0

    @classmethod
    def from_dpi(cls, dpi: float) -> UiScale:
        factor = min(MAX_SCALE, max(MIN_SCALE, dpi / BASE_DPI))
        return cls(factor=factor)

    def px(self, value: int | float) -> int:
        return max(1, round(value * self.factor))


def enable_high_dpi_awareness() -> None:
    if platform.system() != "Windows":
        return

    try:
        set_context = ctypes.windll.user32.SetProcessDpiAwarenessContext
        set_context.argtypes = [ctypes.c_void_p]
        set_context.restype = ctypes.c_bool
        if set_context(ctypes.c_void_p(-4)):
            return
    except (AttributeError, OSError):
        pass

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return
    except (AttributeError, OSError):
        pass

    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
        pass


def configure_tk_scaling(root: tk.Tk) -> UiScale:
    if platform.system() != "Windows":
        return UiScale()

    root.update_idletasks()
    dpi = _window_dpi(root)
    scale = UiScale.from_dpi(dpi)
    root.tk.call("tk", "scaling", dpi / 72.0)
    return scale


def _window_dpi(root: tk.Tk) -> float:
    try:
        get_dpi = ctypes.windll.user32.GetDpiForWindow
        get_dpi.argtypes = [ctypes.c_void_p]
        get_dpi.restype = ctypes.c_uint
        dpi = get_dpi(root.winfo_id())
        if dpi:
            return float(dpi)
    except (AttributeError, OSError):
        pass
    return float(root.winfo_fpixels("1i"))
