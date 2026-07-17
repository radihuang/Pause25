from pause25.ui.timer_ring import render_timer_ring


def test_timer_ring_is_antialiased_at_requested_size() -> None:
    image = render_timer_ring(
        size=320,
        inset=26,
        line_width=14,
        progress=0.5,
        background="#FFFFFF",
        track_color="#DDDDDD",
        progress_color="#FF0000",
    )

    assert image.size == (320, 320)
    assert image.getpixel((160, 26))[0] > image.getpixel((26, 160))[0]


def test_timer_ring_clamps_progress() -> None:
    common = {
        "size": 64,
        "inset": 6,
        "line_width": 4,
        "background": "#FFFFFF",
        "track_color": "#DDDDDD",
        "progress_color": "#FF0000",
    }

    assert render_timer_ring(progress=-1, **common).tobytes() == render_timer_ring(
        progress=0, **common
    ).tobytes()
    assert render_timer_ring(progress=2, **common).tobytes() == render_timer_ring(
        progress=1, **common
    ).tobytes()
