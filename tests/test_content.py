import random

from pause25.content import BreakContentPicker


def test_picker_only_returns_supported_content_kinds():
    picker = BreakContentPicker(randomizer=random.Random(42))

    picked = {picker.pick().kind for _ in range(30)}

    assert picked == {"fact", "quote", "game"}
