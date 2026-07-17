from __future__ import annotations

import random
import tkinter as tk
from collections.abc import Callable

from pause25.models import BreakContent
from pause25.ui.dpi import UiScale
from pause25.ui.theme import COLORS, FONT


class BreakOverlay:
    def __init__(
        self,
        parent: tk.Tk,
        content: BreakContent,
        ui_scale: UiScale,
        on_finish: Callable[[], None],
        on_snooze: Callable[[], None],
    ) -> None:
        self.content = content
        self.ui_scale = ui_scale
        self._on_finish = on_finish
        self._on_snooze = on_snooze
        self._hits = 0
        self._quiz_answered = False
        self._quiz_buttons: list[tk.Button] = []

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
        px = self.ui_scale.px
        shell = tk.Frame(
            self.window,
            bg=COLORS["ink"],
            padx=px(48),
            pady=px(36),
        )
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
            highlightthickness=px(1),
            padx=px(54),
            pady=px(42),
        )
        if self.content.kind == "game":
            card_width, card_height = 0.92, 0.84
        elif self.content.kind == "fact":
            card_width, card_height = 0.82, 0.78
        else:
            card_width, card_height = 0.78, 0.72
        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            relwidth=card_width,
            relheight=card_height,
        )

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
            wraplength=px(820),
            justify="center",
        ).pack()
        body_label = tk.Label(
            card,
            text=self.content.body,
            font=(FONT, 16),
            fg=COLORS["muted"],
            bg=COLORS["surface"],
            wraplength=px(760),
            justify="center",
        )
        if self.content.kind != "fact":
            body_label.pack(pady=(18, 0))

        if self.content.source:
            tk.Label(
                card,
                text=f"— {self.content.source}",
                font=(FONT, 13),
                fg=COLORS["leaf"],
                bg=COLORS["surface"],
            ).pack(pady=(12, 0))

        if self.content.kind == "fact":
            self._build_quiz(card)
        elif self.content.kind == "game":
            self._build_game(card)
        else:
            spacer = tk.Frame(card, height=px(42), bg=COLORS["surface"])
            spacer.pack()

        actions = tk.Frame(card, bg=COLORS["surface"])
        actions.pack(side="bottom", pady=(20, 0))
        primary_text = (
            "先選一個答案" if self.content.kind == "fact" else "我休息好了，開始下一輪"
        )
        self.primary_button = tk.Button(
            actions,
            text=primary_text,
            command=self._finish,
            font=(FONT, 14, "bold"),
            fg=COLORS["white"],
            bg=COLORS["tomato"],
            activebackground=COLORS["tomato_dark"],
            activeforeground=COLORS["white"],
            relief="flat",
            bd=0,
            padx=px(28),
            pady=px(14),
            cursor="hand2",
            disabledforeground="#F4B2A7",
        )
        self.primary_button.pack(side="left", padx=px(8))
        if self.content.kind == "fact":
            self.primary_button.configure(state="disabled")
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
            padx=px(24),
            pady=px(14),
            cursor="hand2",
        ).pack(side="left", padx=px(8))

        self.hint = tk.Label(
            shell,
            text="請選擇一個動作；Esc 不會略過休息提醒",
            font=(FONT, 11),
            fg="#91A29A",
            bg=COLORS["ink"],
        )
        self.hint.pack(side="bottom")

    def _build_quiz(self, card: tk.Frame) -> None:
        if not self.content.options or self.content.correct_index is None:
            raise ValueError("Fact content requires quiz options and a correct answer")

        px = self.ui_scale.px
        options = tk.Frame(card, bg=COLORS["surface"])
        options.pack(fill="x", pady=(px(28), 0))
        for index, option in enumerate(self.content.options):
            button = tk.Button(
                options,
                text=option,
                command=lambda selected=index: self._answer_quiz(selected),
                font=(FONT, 14, "bold"),
                fg=COLORS["ink"],
                bg=COLORS["leaf_soft"],
                activeforeground=COLORS["ink"],
                activebackground="#CBDDD2",
                disabledforeground=COLORS["muted"],
                relief="flat",
                bd=0,
                padx=px(18),
                pady=px(16),
                cursor="hand2",
            )
            button.pack(side="left", fill="x", expand=True, padx=px(7))
            self._quiz_buttons.append(button)

        self.quiz_result = tk.Label(
            card,
            text="選一個答案後顯示解釋",
            font=(FONT, 13, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["surface"],
        )
        self.quiz_result.pack(pady=(24, 0))
        self.quiz_explanation = tk.Label(
            card,
            text="",
            font=(FONT, 15),
            fg=COLORS["muted"],
            bg=COLORS["surface"],
            wraplength=px(820),
            justify="center",
        )
        self.quiz_explanation.pack(pady=(10, 0))

    def _answer_quiz(self, selected_index: int) -> None:
        if self._quiz_answered or self.content.correct_index is None:
            return
        self._quiz_answered = True
        correct_index = self.content.correct_index

        for index, button in enumerate(self._quiz_buttons):
            if index == correct_index:
                button.configure(
                    state="disabled",
                    bg=COLORS["leaf"],
                    disabledforeground=COLORS["white"],
                )
            elif index == selected_index:
                button.configure(
                    state="disabled",
                    bg=COLORS["tomato"],
                    disabledforeground=COLORS["white"],
                )
            else:
                button.configure(state="disabled", bg="#EEEAE1")

        if selected_index == correct_index:
            result = "答對了！"
        else:
            result = f"答案是：{self.content.options[correct_index]}"
        self.quiz_result.configure(text=result, fg=COLORS["leaf"])
        self.quiz_explanation.configure(text=self.content.body)
        self.primary_button.configure(text="看完解釋，開始下一輪", state="normal")

    def _build_game(self, card: tk.Frame) -> None:
        px = self.ui_scale.px
        self.game_area = tk.Frame(
            card,
            width=px(700),
            height=px(280),
            bg=COLORS["leaf_soft"],
            highlightbackground="#C5D6CC",
            highlightthickness=px(1),
        )
        self.game_area.pack(pady=(24, 0), fill="both", expand=True)
        self.game_area.pack_propagate(False)
        self.score_label = tk.Label(
            self.game_area,
            text="0 / 8",
            font=(FONT, 12, "bold"),
            fg=COLORS["leaf"],
            bg=COLORS["leaf_soft"],
        )
        self.score_label.place(x=px(14), y=px(12))
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
        self.target.place(relx=0.5, rely=0.5, anchor="center")

    def _hit_target(self) -> None:
        self._hits += 1
        self.score_label.configure(text=f"{self._hits} / 8")
        if self._hits >= 8:
            self.target.place_forget()
            self.score_label.configure(text="完成！眼睛已經換過焦點。")
            self.primary_button.configure(text="完成遊戲，開始下一輪")
            return
        self.game_area.update_idletasks()
        px = self.ui_scale.px
        width = max(px(280), self.game_area.winfo_width())
        height = max(px(180), self.game_area.winfo_height())
        x = random.randint(px(70), max(px(70), width - px(80)))
        y = random.randint(px(55), max(px(55), height - px(65)))
        self.target.place(x=x, y=y, relx=0, rely=0, anchor="center")

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
