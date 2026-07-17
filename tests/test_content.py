import random

from pause25.content import FACTS, BreakContentPicker


def test_picker_only_returns_supported_content_kinds():
    picker = BreakContentPicker(randomizer=random.Random(42))

    picked = {picker.pick().kind for _ in range(30)}

    assert picked == {"fact", "quote", "game"}


def test_every_fact_is_a_three_choice_quiz_with_an_explanation():
    for fact in FACTS:
        assert len(fact.options) == 3
        assert fact.correct_index is not None
        assert 0 <= fact.correct_index < len(fact.options)
        assert fact.body
