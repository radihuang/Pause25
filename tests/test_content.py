import random

from pause25.content import FACTS, BreakContentPicker


EXPECTED_FACT_TITLES = [
    "為什麼海豚不是魚？",
    "海豚怎麼睡覺？",
    "為什麼會噴水？",
    "為什麼要浮出水面？",
    "為什麼會船首乘浪？",
    "為什麼會跳躍？",
    "台灣最常見四種海豚怎麼辨識？",
    "齒鯨和鬚鯨差在哪裡？",
    "為什麼抹香鯨可以潛那麼久？",
    "為什麼賞鯨船不能包圍海豚？",
    "為什麼不能倒車？",
    "母子群怎麼觀察？",
    "海豚有天敵嗎？",
    "為什麼不能餵食？",
    "為什麼不能追逐？",
    "海豚如何利用回聲定位？",
    "氣孔和鼻孔有什麼關係？",
    "海豚如何保暖？",
    "鯨豚遇到擱淺怎麼辦？",
]


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


def test_fact_titles_match_dolphin_question_bank():
    assert [fact.title for fact in FACTS] == EXPECTED_FACT_TITLES
