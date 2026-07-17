from __future__ import annotations

import math
import time
from collections.abc import Callable


class CountdownTimer:
    def __init__(
        self,
        duration_seconds: int = 25 * 60,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")
        self.duration_seconds = duration_seconds
        self._clock = clock
        self._remaining = float(duration_seconds)
        self._deadline: float | None = None
        self._status = "idle"
        self._completion_pending = False

    @property
    def status(self) -> str:
        self._refresh()
        return self._status

    @property
    def remaining_seconds(self) -> int:
        self._refresh()
        return max(0, math.ceil(self._remaining))

    @property
    def progress(self) -> float:
        return self.remaining_seconds / self.duration_seconds

    def start(self) -> None:
        self._refresh()
        if self._status == "running":
            return
        if self._status == "completed" or self._remaining <= 0:
            self._remaining = float(self.duration_seconds)
            self._completion_pending = False
        self._deadline = self._clock() + self._remaining
        self._status = "running"

    def pause(self) -> None:
        self._refresh()
        if self._status != "running":
            return
        self._remaining = max(0.0, self._deadline - self._clock())
        self._deadline = None
        self._status = "paused"

    def reset(self) -> None:
        self._remaining = float(self.duration_seconds)
        self._deadline = None
        self._status = "idle"
        self._completion_pending = False

    def consume_completion(self) -> bool:
        self._refresh()
        if not self._completion_pending:
            return False
        self._completion_pending = False
        return True

    def _refresh(self) -> None:
        if self._status != "running" or self._deadline is None:
            return
        self._remaining = max(0.0, self._deadline - self._clock())
        if self._remaining == 0:
            self._deadline = None
            self._status = "completed"
            self._completion_pending = True
