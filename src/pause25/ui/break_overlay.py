from __future__ import annotations

import random
import tkinter as tk
from collections.abc import Callable

from pause25.models import BreakContent
from pause25.ui.theme import COLORS, FONT


class BreakOverlay:
    def __init__(
        self,
        parent: tk.Tk,
        content: BreakContent,
        on_finish: Callable[[], None],
        on_snooze: Callable[[], None],
    ) -> None:
        self.content = content
        self._on_finish = on_finish
        self._on_snooze = on_snooze
        self._hits = 0

        self.window = tk.Toplevel(parent)
        self.window.title("休息時間｜Pause25")
        self.window.configure(bg=COLORS["ink"])
        self.window.attributes("-topmost", True)
        try:
            self.window.attributes("-fullscreen", True)
        except tk.TclError:
            self.window.geometry(
                f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}+0+0"
            )
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.bind("<Escape>", self._show_escape_hint)

        self._build()
        self.window.after(100, self._take_focus)

    def _build(self) -> None:
        shell = tk.Frame(self.window, bg=COLORS["ink"], padx=48, pady=36)
        shell.pack(fill="both", expand=True)

        top = tk.Frame(shell, bg=COLORS["ink"])
        top.pack(fill="x")
        tk.Label(
            top,
            text="25分",
            font=(FONT, 18, "bold"),
            fg=COLORS["white"],
            bg=COLORS["ink"],
        ).pack(side="left")
        tk.Label(
            top,
            text="專注完成  ·  該讓眼睛和肩膀休息了",
            font=(FONT, 13),
            fg="#BFCBC5",
            bg=COLORS["ink"],
        ).pack(side="right")

        card = tk.Frame(
            shell,
            bg=COLORS["surface"],
            highlightbackground="#475B52",
            highlightthickness=1,
            padx=54,
            pady=42,
        )
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.78, relheight=0.72)

        tk.Label(
            card,
            text=self.content.eyebrow,
            font=(FONT, 13, "bold"),
            fg=COLORS["tomato"],
            bg=COLORS["surface"],
        ).pack(pady=(0, 16))
        tk.Label(
            card,
            text=self.content.title,
            font=(FONT, 31, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["surface"],
            wraplength=820,
            justify="center",
        ).pack()
        tk.Label(
            card,
            text=self.content.body,
            font=(FONT, 16),
            fg=COLORS["muted"],
            bg=COLORS["surface"],
            wraplength=760,
            justify="center",
        ).pack(pady=(18, 0))

        if self.content.source:
            tk.Label(
                card,
                text=f"— {self.content.source}",
                font=(FONT, 13),
                fg=COLORS["leaf"],
                bg=COLORS["surface"],
            ).pack(pady=(12, 0))

        if self.content.kind == "game":
            self._build_game(card)
        else:
            spacer = tk.Frame(card, height=42, bg=COLORS["surface"])
            spacer.pack()

        actions = tk.Frame(card, bg=COLORS["surface"])
        actions.pack(side="bottom", pady=(20, 0))
        self.primary_button = tk.Button(
            actions,
            text="我休息好了，開始下一輪",
            command=self._finish,
            font=(FONT, 14, "bold"),
            fg=COLORS["white"],
            bg=COLORS["tomato"],
            activebackground=COLORS["tomato_dark"],
            activeforeground=COLORS["white"],
            relief="flat",
            bd=0,
            padx=28,
            pady=14,
            cursor="hand2",
        )
        self.primary_button.pack(side="left", padx=8)
        tk.Button(
            actions,
            text="1 分鐘後再提醒",
            command=self._snooze,
            font=(FONT, 13, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["leaf_soft"],
            activebackground="#CBDDD2",
            relief="flat",
            bd=0,
            padx=24,
            pady=14,
            cursor="hand2",
        ).pack(side="left", padx=8)

        self.hint = tk.Label(
            shell,
            text="請選擇一個動作；Esc 不會略過休息提醒",
            font=(FONT, 11),
            fg="#91A29A",
            bg=COLORS["ink"],
        )
        self.hint.pack(side="bottom")

    def _build_game(self, card: tk.Frame) -> None:
        self.game_area = tk.Frame(
            card,
            width=700,
            height=190,
            bg=COLORS["leaf_soft"],
            highlightbackground="#C5D6CC",
            highlightthickness=1,
        )
        self.game_area.pack(pady=(24, 0), fill="x")
        self.game_area.pack_propagate(False)
        self.score_label = tk.Label(
            self.game_area,
            text="0 / 8",
            font=(FONT, 12, "bold"),
            fg=COLORS["leaf"],
            bg=COLORS["leaf_soft"],
        )
        self.score_label.place(x=14, y=12)
        self.target = tk.Button(
            self.game_area,
            text="●",
            command=self._hit_target,
            font=(FONT, 26, "bold"),
            fg=COLORS["tomato"],
            bg=COLORS["surface"],
            activeforeground=COLORS["tomato_dark"],
            activebackground=COLORS["surface"],
            relief="flat",
            bd=0,
            width=2,
            height=1,
            cursor="hand2",
        )
        self.target.place(x=325, y=70)

    def _hit_target(self) -> None:
        self._hits += 1
        self.score_label.configure(text=f"{self._hits} / 8")
        if self._hits >= 8:
            self.target.place_forget()
            self.score_label.configure(text="完成！眼睛已經換過焦點。")
            self.primary_button.configure(text="完成遊戲，開始下一輪")
            return
        self.game_area.update_idletasks()
        width = max(280, self.game_area.winfo_width())
        x = random.randint(70, max(70, width - 80))
        y = random.randint(35, 125)
        self.target.place(x=x, y=y)

    def _show_escape_hint(self, _: tk.Event[tk.Misc]) -> None:
        self.hint.configure(text="休息提醒仍在這裡：請選擇「開始下一輪」或「1 分鐘後再提醒」")
        self.window.bell()

    def _take_focus(self) -> None:
        self.window.lift()
        self.window.focus_force()
        try:
            self.window.grab_set()
        except tk.TclError:
            pass

    def _finish(self) -> None:
        self._release_and_destroy()
        self._on_finish()

    def _snooze(self) -> None:
        self._release_and_destroy()
        self._on_snooze()

    def _release_and_destroy(self) -> None:
        try:
            self.window.grab_release()
        except tk.TclError:
            pass
        self.window.destroy()
