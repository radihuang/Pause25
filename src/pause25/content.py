from __future__ import annotations

import random
from collections.abc import Sequence

from pause25.models import BreakContent


FACTS: tuple[BreakContent, ...] = (
    BreakContent(
        "fact",
        "換換腦袋",
        "章魚有幾顆心臟？",
        "其中兩顆負責把血液送往鰓，另一顆把血液送到身體其他部位。游泳時，主要心臟甚至會暫停跳動。",
        options=("1 顆", "2 顆", "3 顆"),
        correct_index=2,
    ),
    BreakContent(
        "fact",
        "一分鐘冷知識",
        "為什麼蜂蜜能保存很久？",
        "低含水量、高糖分與酸性環境，讓多數微生物很難在蜂蜜裡生長。",
        options=("含水量低且偏酸", "天然溫度很低", "完全不含糖"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "換換腦袋",
        "植物學上，哪一種水果屬於莓果？",
        "植物學以果實的形成方式分類；香蕉符合莓果定義，草莓反而不符合。",
        options=("草莓", "香蕉", "覆盆莓"),
        correct_index=1,
    ),
    BreakContent(
        "fact",
        "一分鐘冷知識",
        "樹懶大約可以憋氣多久？",
        "牠們能降低心率，讓身體在水下更慢地消耗氧氣。",
        options=("4 分鐘", "20 分鐘", "40 分鐘"),
        correct_index=2,
    ),
    BreakContent(
        "fact",
        "換換腦袋",
        "炎熱天氣會讓艾菲爾鐵塔怎樣？",
        "金屬熱脹冷縮，炎熱天氣可能讓塔身增加約十多公分。",
        options=("變高十多公分", "變矮一公尺", "重量減少"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "一分鐘冷知識",
        "海獺睡覺時為什麼有時會牽手？",
        "海獺有時會彼此牽住，或纏在海藻裡，避免休息時隨水流漂散。",
        options=("互相取暖", "避免隨水流漂散", "分配食物"),
        correct_index=1,
    ),
)

QUOTES: tuple[BreakContent, ...] = (
    BreakContent(
        "quote",
        "帶一句話走",
        "知之為知之，不知為不知，是知也。",
        "承認不知道，也是清楚思考的一部分。",
        "《論語》",
    ),
    BreakContent(
        "quote",
        "帶一句話走",
        "千里之行，始於足下。",
        "再大的進度，都從眼前這一小步開始。",
        "《道德經》",
    ),
    BreakContent(
        "quote",
        "停一下，再出發",
        "不積跬步，無以至千里。",
        "穩定的小步，比偶爾的衝刺更可靠。",
        "《荀子》",
    ),
    BreakContent(
        "quote",
        "帶一句話走",
        "行到水窮處，坐看雲起時。",
        "卡住的時候，停下來也可能看見新的方向。",
        "王維〈終南別業〉",
    ),
    BreakContent(
        "quote",
        "停一下，再出發",
        "欲速則不達。",
        "留一點呼吸的空間，反而能走得更遠。",
        "《論語》",
    ),
)

GAME = BreakContent(
    "game",
    "30 秒小遊戲",
    "抓住跑走的小番茄",
    "點到它 8 次，讓眼睛和注意力離開剛才的工作。",
)


class BreakContentPicker:
    def __init__(
        self,
        facts: Sequence[BreakContent] = FACTS,
        quotes: Sequence[BreakContent] = QUOTES,
        randomizer: random.Random | None = None,
    ) -> None:
        self._facts = tuple(facts)
        self._quotes = tuple(quotes)
        self._random = randomizer or random.Random()

    def pick(self) -> BreakContent:
        kind = self._random.choice(("fact", "quote", "game"))
        if kind == "fact":
            return self._random.choice(self._facts)
        if kind == "quote":
            return self._random.choice(self._quotes)
        return GAME
