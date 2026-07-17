from pause25.ui.dpi import UiScale


def test_ui_scale_converts_logical_pixels() -> None:
    scale = UiScale.from_dpi(144)

    assert scale.factor == 1.5
    assert scale.px(440) == 660
    assert scale.px(1) == 2


def test_ui_scale_stays_within_supported_range() -> None:
    assert UiScale.from_dpi(72).factor == 1.0
    assert UiScale.from_dpi(600).factor == 4.0
