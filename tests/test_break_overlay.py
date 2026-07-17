from unittest.mock import Mock, patch

from pause25.ui.break_overlay import BreakOverlay
from pause25.ui.dpi import UiScale


def test_first_game_hit_resets_relative_position() -> None:
    overlay = object.__new__(BreakOverlay)
    overlay._hits = 0
    overlay.ui_scale = UiScale()
    overlay.score_label = Mock()
    overlay.target = Mock()
    overlay.primary_button = Mock()
    overlay.game_area = Mock()
    overlay.game_area.winfo_width.return_value = 1000
    overlay.game_area.winfo_height.return_value = 500

    with patch("pause25.ui.break_overlay.random.randint", side_effect=(320, 180)):
        overlay._hit_target()

    overlay.target.place.assert_called_once_with(
        x=320,
        y=180,
        relx=0,
        rely=0,
        anchor="center",
    )
    overlay.score_label.configure.assert_called_once_with(text="1 / 8")
