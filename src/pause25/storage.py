from __future__ import annotations

import os
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

from pause25.models import DailySummary

FOCUS_SESSION_SECONDS = 25 * 60


def default_database_path() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "Pause25" / "pause25.sqlite3"


class AppRepository:
    def __init__(self, database_path: Path | str | None = None) -> None:
        self.database_path = Path(database_path) if database_path else default_database_path()
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS focus_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                completed_at TEXT NOT NULL,
                focus_seconds INTEGER NOT NULL CHECK (focus_seconds > 0),
                break_kind TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        self._connection.commit()

    def record_focus_session(
        self,
        focus_seconds: int,
        break_kind: str,
        completed_at: datetime | None = None,
    ) -> int:
        if focus_seconds <= 0:
            raise ValueError("focus_seconds must be positive")
        timestamp = completed_at or datetime.now().astimezone()
        cursor = self._connection.execute(
            """
            INSERT INTO focus_sessions (completed_at, focus_seconds, break_kind)
            VALUES (?, ?, ?)
            """,
            (timestamp.isoformat(), focus_seconds, break_kind),
        )
        self._connection.commit()
        return int(cursor.lastrowid)

    def get_daily_summary(self, day: date | None = None) -> DailySummary:
        target_day = day or datetime.now().astimezone().date()
        row = self._connection.execute(
            """
            SELECT COUNT(*) AS completed_sessions,
                   COALESCE(SUM(focus_seconds), 0) AS focused_seconds
            FROM focus_sessions
            WHERE substr(completed_at, 1, 10) = ?
              AND focus_seconds = ?
            """,
            (target_day.isoformat(), FOCUS_SESSION_SECONDS),
        ).fetchone()
        return DailySummary(
            day=target_day,
            completed_sessions=int(row["completed_sessions"]),
            focused_seconds=int(row["focused_seconds"]),
        )

    def set_setting(self, key: str, value: str) -> None:
        self._connection.execute(
            """
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
        self._connection.commit()

    def get_setting(self, key: str, default: str | None = None) -> str | None:
        row = self._connection.execute(
            "SELECT value FROM settings WHERE key = ?",
            (key,),
        ).fetchone()
        return str(row["value"]) if row else default

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> AppRepository:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
