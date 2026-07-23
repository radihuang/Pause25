from __future__ import annotations

import random
from collections.abc import Sequence

from pause25.models import BreakContent


FACTS: tuple[BreakContent, ...] = (
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "為什麼海豚不是魚？",
        "海豚是哺乳類：溫血、用肺呼吸、胎生，幼豚也會喝母乳。魚類多半用鰓呼吸，身體構造和繁殖方式都不同。",
        options=("用肺呼吸、胎生並哺乳", "住在海裡但不會游泳", "有鰓也會產卵"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "海豚怎麼睡覺？",
        "海豚需要主動浮出水面呼吸，所以睡覺時常讓半邊大腦輪流休息，另一半維持游動、換氣與基本警覺。",
        options=("半邊大腦輪流休息", "完全沉到海底睡一整晚", "像人一樣完全失去意識"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "為什麼會噴水？",
        "看到的水柱主要不是海豚把海水噴出來，而是牠用力呼氣時，水氣凝結成霧，也可能帶起氣孔附近的水滴。",
        options=("呼氣時水氣凝結成霧", "把胃裡的海水噴出來", "用氣孔喝水再噴出"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "為什麼要浮出水面？",
        "海豚沒有鰓，必須到水面用氣孔吸進空氣，再把氧氣送進肺裡。牠們能憋氣，但不能一直待在水下。",
        options=("用肺呼吸，需要換氣", "鰓需要照光", "必須上岸覓食"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "為什麼會船首乘浪？",
        "船前方會形成壓力波，海豚能調整姿勢像衝浪一樣滑行，可能省力，也可能只是社交與遊戲行為。",
        options=("利用船首壓力波滑行", "被船吸住無法離開", "在替船導航"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "為什麼會跳躍？",
        "海豚跳躍可能用來溝通、觀察、社交遊戲、甩掉寄生物，快速前進時也可能降低部分游泳阻力。",
        options=("溝通、觀察或社交遊戲", "因為牠們不能在水下轉彎", "為了把鰓裡的水甩掉"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "台灣最常見四種海豚怎麼辨識？",
        "常見可看飛旋海豚的三層體色與旋轉跳、瓶鼻海豚的粗壯體型與短厚吻、熱帶點斑原海豚的斑點、瑞氏海豚的鈍圓頭與白色刮痕。",
        options=("看體色、背鰭、吻部與花紋", "只看大小就能穩定分辨", "只能靠牠們叫聲現場辨識"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "齒鯨和鬚鯨差在哪裡？",
        "齒鯨有牙齒，會用回聲定位獵食，海豚與抹香鯨都屬於齒鯨；鬚鯨用鬚板濾食小魚或浮游生物。",
        options=("齒鯨有牙，鬚鯨用鬚板濾食", "齒鯨都很大，鬚鯨都很小", "齒鯨是魚，鬚鯨是哺乳類"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "為什麼抹香鯨可以潛那麼久？",
        "抹香鯨能在血液與肌肉中儲存大量氧氣，潛水時降低心跳與耗氧，並把血流優先供應給腦和心臟。",
        options=("儲氧多，潛水時降低耗氧", "在水下改用鰓呼吸", "牠完全不需要氧氣"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "友善賞鯨",
        "為什麼賞鯨船不能包圍海豚？",
        "包圍會切斷海豚離開的路線，增加壓力，也可能拆散群體，干擾牠們休息、覓食或照顧幼豚。",
        options=("會切斷逃生路線並增加壓力", "海豚會忘記怎麼游泳", "船靠越近越能保護牠們"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "友善賞鯨",
        "為什麼不能倒車？",
        "在鯨豚附近倒車時，船尾視線死角與螺旋槳風險都會變高；保持穩定、可預測的航向，對動物比較安全。",
        options=("螺旋槳與視線死角風險高", "倒車聲會讓海豚睡著", "倒車會讓船無法浮起"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "友善賞鯨",
        "母子群怎麼觀察？",
        "看到母子群時要拉遠距離、低速平行觀察，不切入母子之間，也不要逼近幼豚，避免造成緊迫或分離。",
        options=("拉遠距離、低速平行觀察", "直接靠近幼豚方便拍照", "用食物把母親引開"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "海豚有天敵嗎？",
        "海豚有天敵，例如大型鯊魚與虎鯨。群體生活、警戒聲音與互相合作，都能幫助牠們降低被捕食的風險。",
        options=("有，大型鯊魚與虎鯨等", "沒有，所有動物都怕海豚", "只有海鳥會攻擊成年海豚"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "友善賞鯨",
        "為什麼不能餵食？",
        "餵食會改變海豚自然覓食行為，讓牠們更常靠近船隻或漁具，增加受傷、誤食與疾病傳播風險。",
        options=("會改變覓食並提高受傷風險", "海豚不能消化任何魚類", "會讓海水變甜"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "友善賞鯨",
        "為什麼不能追逐？",
        "追逐會讓海豚消耗額外能量，打斷牠們休息、覓食、社交或照顧幼豚；賞鯨應讓動物自己決定距離。",
        options=("會耗能並打亂自然行為", "會讓海豚跑到陸地上", "海豚被追就會變成魚"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "海豚如何利用回聲定位？",
        "海豚發出高頻喀喀聲，聲波碰到物體後反彈回來，牠再用回音判斷獵物或障礙物的方向、距離與大小。",
        options=("發出高頻聲，再聽回音", "用眼睛發光照亮獵物", "用尾巴拍水測量溫度"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "氣孔和鼻孔有什麼關係？",
        "氣孔就是演化後移到頭頂的鼻孔，連通呼吸道。這讓海豚只要頭頂短暫出水，就能快速呼氣和吸氣。",
        options=("氣孔是移到頭頂的鼻孔", "氣孔其實是耳朵", "氣孔是喝海水的嘴"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "鯨豚小測驗",
        "海豚如何保暖？",
        "海豚主要靠皮下脂肪層保溫，鰭和尾葉也能調節血流，減少熱量散失或在需要時散熱。",
        options=("靠脂肪層與血流調節", "靠長毛像海獅一樣保暖", "靠喝熱海水"),
        correct_index=0,
    ),
    BreakContent(
        "fact",
        "救援小提醒",
        "鯨豚遇到擱淺怎麼辦？",
        "先保持距離並通報 118 或地方救援單位；不要拖拉尾鰭或自行推回海裡，協助遮陰、保持皮膚濕潤，並讓呼吸孔暢通。",
        options=("保持距離、通報並等救援", "立刻拉尾巴拖回海裡", "圍上去摸牠、拍照打卡"),
        correct_index=0,
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
