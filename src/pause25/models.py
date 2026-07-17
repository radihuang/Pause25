from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class DailySummary:
    day: date
    completed_sessions: int
    focused_seconds: int

    @property
    def focused_minutes(self) -> int:
        return self.focused_seconds // 60


@dataclass(frozen=True, slots=True)
class BreakContent:
    kind: str
    eyebrow: str
    title: str
    body: str
    source: str = ""
    options: tuple[str, ...] = ()
    correct_index: int | None = None
