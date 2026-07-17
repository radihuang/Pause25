from datetime import date, datetime, timezone

from pause25.storage import AppRepository


def test_sessions_persist_after_repository_is_reopened(tmp_path):
    database = tmp_path / "pause25.sqlite3"
    completed_at = datetime(2026, 7, 17, 9, 30, tzinfo=timezone.utc)

    with AppRepository(database) as repository:
        repository.record_focus_session(1500, "fact", completed_at)

    with AppRepository(database) as repository:
        summary = repository.get_daily_summary(date(2026, 7, 17))

    assert summary.completed_sessions == 1
    assert summary.focused_minutes == 25


def test_daily_summary_only_counts_requested_day(tmp_path):
    database = tmp_path / "pause25.sqlite3"
    with AppRepository(database) as repository:
        repository.record_focus_session(
            1500, "quote", datetime(2026, 7, 16, 23, 59, tzinfo=timezone.utc)
        )
        repository.record_focus_session(
            1500, "game", datetime(2026, 7, 17, 0, 1, tzinfo=timezone.utc)
        )
        summary = repository.get_daily_summary(date(2026, 7, 17))

    assert summary.completed_sessions == 1
    assert summary.focused_seconds == 1500


def test_daily_summary_ignores_incomplete_test_sessions(tmp_path):
    database = tmp_path / "pause25.sqlite3"
    completed_at = datetime(2026, 7, 17, 9, 30, tzinfo=timezone.utc)
    with AppRepository(database) as repository:
        repository.record_focus_session(3, "fact", completed_at)
        summary = repository.get_daily_summary(date(2026, 7, 17))

    assert summary.completed_sessions == 0
    assert summary.focused_seconds == 0


def test_settings_persist(tmp_path):
    database = tmp_path / "pause25.sqlite3"
    with AppRepository(database) as repository:
        repository.set_setting("window_position", "100x100")

    with AppRepository(database) as repository:
        assert repository.get_setting("window_position") == "100x100"
        assert repository.get_setting("missing", "fallback") == "fallback"
