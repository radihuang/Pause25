from __future__ import annotations

from PIL import Image, ImageDraw


SUPERSAMPLING = 4


def render_timer_ring(
    *,
    size: int,
    inset: int,
    line_width: int,
    progress: float,
    background: str,
    track_color: str,
    progress_color: str,
) -> Image.Image:
    progress = min(1.0, max(0.0, progress))
    render_size = size * SUPERSAMPLING
    render_inset = inset * SUPERSAMPLING
    render_width = line_width * SUPERSAMPLING
    bounds = (
        render_inset,
        render_inset,
        render_size - render_inset,
        render_size - render_inset,
    )

    image = Image.new("RGB", (render_size, render_size), background)
    draw = ImageDraw.Draw(image)
    draw.ellipse(bounds, outline=track_color, width=render_width)
    if progress > 0:
        draw.arc(
            bounds,
            start=-90,
            end=-90 + 360 * progress,
            fill=progress_color,
            width=render_width,
        )

    return image.resize((size, size), Image.Resampling.LANCZOS)
