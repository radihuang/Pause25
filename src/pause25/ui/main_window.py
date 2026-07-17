from __future__ import annotations

import tkinter as tk
from datetime import date

from pause25.content import BreakContentPicker
from pause25.models import BreakContent
from pause25.storage import AppRepository
from pause25.timer import CountdownTimer
from pause25.ui.break_overlay import BreakOverlay
from pause25.ui.theme import COLORS, FONT


class MainWindow:
    FOCUS_SECONDS = 25 * 60
    SNOOZE_MILLISECONDS = 60 * 1000

    def __init__(self, root: tk.Tk, repository: AppRepository) -> None:
        self.root = root
        self.repository = repository
        self.timer = CountdownTimer(self.FOCUS_SECONDS)
        self.content_picker = BreakContentPicker()
        self.current_day = date.today()
        self._snoozed_content = None
        self._overlay: BreakOverlay | None = None

        self.root.title("25分｜番茄鐘")
        self.root.configure(bg=COLORS["paper"])
        self.root.geometry("440x680")
        self.root.minsize(420, 640)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

        self._build()
        self._refresh_summary()
        self._tick()

    def _build(self) -> None:
        container = tk.Frame(self.root, bg=COLORS["paper"], padx=30, pady=24)
        container.pack(fill="both", expand=True)

        header = tk.Frame(container, bg=COLORS["paper"])
        header.pack(fill="x")
        tk.Label(
            header,
            text="25分",
            font=(FONT, 20, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["paper"],
        ).pack(side="left")
        self.status_badge = tk.Label(
            header,
            text="準備開始",
            font=(FONT, 10, "bold"),
            fg=COLORS["leaf"],
            bg=COLORS["leaf_soft"],
            padx=11,
            pady=6,
        )
        self.status_badge.pack(side="right")

        tk.Label(
            container,
            text="一次只做一件事。時間到，我會明顯提醒你。",
            font=(FONT, 11),
            fg=COLORS["muted"],
            bg=COLORS["paper"],
        ).pack(anchor="w", pady=(8, 18))

        self.timer_canvas = tk.Canvas(
            container,
            width=320,
            height=320,
            bg=COLORS["paper"],
            highlightthickness=0,
        )
        self.timer_canvas.pack()
        self.timer_canvas.create_oval(
            26,
            26,
            294,
            294,
            outline=COLORS["line"],
            width=14,
        )
        self.progress_arc = self.timer_canvas.create_arc(
            26,
            26,
            294,
            294,
            start=90,
            extent=-360,
            style="arc",
            outline=COLORS["tomato"],
            width=14,
        )
        self.timer_canvas.create_text(
            160,
            117,
            text="專注時間",
            font=(FONT, 12, "bold"),
            fill=COLORS["muted"],
        )
        self.time_text = self.timer_canvas.create_text(
            160,
            163,
            text="25:00",
            font=(FONT, 42, "bold"),
            fill=COLORS["ink"],
        )
        self.timer_canvas.create_text(
            160,
            208,
            text="完成後隨機出現休息內容",
            font=(FONT, 10),
            fill=COLORS["muted"],
        )

        controls = tk.Frame(container, bg=COLORS["paper"])
        controls.pack(pady=(4, 22))
        self.primary_button = tk.Button(
            controls,
            text="開始專注",
            command=self._toggle_timer,
            font=(FONT, 14, "bold"),
            fg=COLORS["white"],
            bg=COLORS["tomato"],
            activeforeground=COLORS["white"],
            activebackground=COLORS["tomato_dark"],
            relief="flat",
            bd=0,
            padx=32,
            pady=13,
            cursor="hand2",
        )
        self.primary_button.pack(side="left", padx=6)
        tk.Button(
            controls,
            text="重設",
            command=self._reset_timer,
            font=(FONT, 12, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["surface"],
            activebackground=COLORS["line"],
            relief="flat",
            bd=0,
            padx=20,
            pady=14,
            cursor="hand2",
        ).pack(side="left", padx=6)

        summary_card = tk.Frame(
            container,
            bg=COLORS["surface"],
            highlightbackground=COLORS["line"],
            highlightthickness=1,
            padx=20,
            pady=14,
        )
        summary_card.pack(fill="x")
        tk.Label(
            summary_card,
            text="今天",
            font=(FONT, 11, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["surface"],
        ).grid(row=0, column=0, sticky="w")
        self.session_value = tk.Label(
            summary_card,
            text="0 輪",
            font=(FONT, 18, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["surface"],
        )
        self.session_value.grid(row=1, column=0, sticky="w", pady=(3, 0))
        tk.Frame(summary_card, width=1, height=40, bg=COLORS["line"]).grid(
            row=0, column=1, rowspan=2, padx=28
        )
        tk.Label(
            summary_card,
            text="累積專注",
            font=(FONT, 11, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["surface"],
        ).grid(row=0, column=2, sticky="w")
        self.minutes_value = tk.Label(
            summary_card,
            text="0 分鐘",
            font=(FONT, 18, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["surface"],
        )
        self.minutes_value.grid(row=1, column=2, sticky="w", pady=(3, 0))

        tk.Label(
            container,
            text="休息提示  ·  小知識  /  名言  /  追點小遊戲",
            font=(FONT, 10),
            fg=COLORS["muted"],
            bg=COLORS["paper"],
        ).pack(pady=(16, 0))

    def _toggle_timer(self) -> None:
        if self.timer.status == "running":
            self.timer.pause()
        else:
            self.timer.start()
        self._update_controls()

    def _reset_timer(self) -> None:
        self.timer.reset()
        self._update_controls()
        self._render_timer()

    def _tick(self) -> None:
        if date.today() != self.current_day:
            self.current_day = date.today()
            self._refresh_summary()
        self._render_timer()
        self._update_controls()
        if self.timer.consume_completion():
            self._handle_completion()
        self.root.after(200, self._tick)

    def _render_timer(self) -> None:
        remaining = self.timer.remaining_seconds
        minutes, seconds = divmod(remaining, 60)
        self.timer_canvas.itemconfigure(self.time_text, text=f"{minutes:02d}:{seconds:02d}")
        self.timer_canvas.itemconfigure(self.progress_arc, extent=-360 * self.timer.progress)

    def _update_controls(self) -> None:
        status = self.timer.status
        if status == "running":
            self.primary_button.configure(text="暫停")
            self.status_badge.configure(text="專注中", fg=COLORS["tomato"], bg="#FBE0DA")
        elif status == "paused":
            self.primary_button.configure(text="繼續專注")
            self.status_badge.configure(text="已暫停", fg="#7B6028", bg="#F7E9C7")
        else:
            self.primary_button.configure(text="開始專注")
            self.status_badge.configure(text="準備開始", fg=COLORS["leaf"], bg=COLORS["leaf_soft"])

    def _handle_completion(self) -> None:
        content = self.content_picker.pick()
        self.repository.record_focus_session(
            focus_seconds=self.FOCUS_SECONDS,
            break_kind=content.kind,
        )
        self._refresh_summary()
        self._show_overlay(content)

    def _show_overlay(self, content: BreakContent) -> None:
        self.root.deiconify()
        self.root.lift()
        self._overlay = BreakOverlay(
            self.root,
            content,
            on_finish=self._start_next_round,
            on_snooze=lambda: self._snooze(content),
        )

    def _snooze(self, content: BreakContent) -> None:
        self._overlay = None
        self._snoozed_content = content
        self.status_badge.configure(text="稍後再提醒", fg="#7B6028", bg="#F7E9C7")
        self.root.after(self.SNOOZE_MILLISECONDS, self._repeat_snoozed_alert)

    def _repeat_snoozed_alert(self) -> None:
        if self._snoozed_content is None:
            return
        content = self._snoozed_content
        self._snoozed_content = None
        self._show_overlay(content)

    def _start_next_round(self) -> None:
        self._overlay = None
        self._snoozed_content = None
        self.timer.reset()
        self.timer.start()
        self._update_controls()

    def _refresh_summary(self) -> None:
        summary = self.repository.get_daily_summary()
        self.session_value.configure(text=f"{summary.completed_sessions} 輪")
        self.minutes_value.configure(text=f"{summary.focused_minutes} 分鐘")

    def _close(self) -> None:
        self.repository.close()
        self.root.destroy()
