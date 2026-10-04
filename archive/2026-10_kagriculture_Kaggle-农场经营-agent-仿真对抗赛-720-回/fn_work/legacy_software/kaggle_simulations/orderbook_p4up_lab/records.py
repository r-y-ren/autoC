# -*- coding: utf-8 -*-
"""records —— EpisodeRecord 归一模型 + 两种动作指纹（canon / bundle）。

动作原始形态（kaggle-environments 回放 action dict）：
    {"farmer": ["PLANT","MELON"], "hands": [["MOVE","NORTH"], ...],
     "market": [["SELL","WOOL", 6], ...]}
canon 指纹（x-ray cell 10）：farmer 整条 + hands 逐条 + market 逐条，全有序逐位比。
bundle 指纹（leoprovorov cell 11 数学区）：op=(class,good)，N/S/E/W 并为 MOVE，
数量丢弃、market 按集合比、hands 按排序列表比、附 n_hands——比 canon 宽松。

turn 约定（x-ray cell 40 自述陷阱）：**拍 t 的动作存在 steps[t+1]**，从回放
steps 抽流必须 +1 对齐；本模块的 adapters.replay_to_record 已做对齐。
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

# 游戏品目词表（对齐 fingerprint_scan 的 CROPS/ANIMALS/PRODUCTS 口径）
CROPS = {"CARROT", "MELON", "STRAWBERRY", "TOMATO", "WHEAT"}
ANIMALS = {"COW", "GOOSE", "SHEEP"}
GAME_GOODS = CROPS | ANIMALS | {"EGG", "MILK", "WOOL", "FERTILIZER"}

MOVE_VERBS = {"NORTH", "SOUTH", "EAST", "WEST", "MOVE"}

# x-ray cell 6 的 PASS 哨兵（缺拍/空拍按此处理）
PASS_ACTION: Dict[str, Any] = {"farmer": ["PASS"], "hands": [], "market": []}


def canon(a: Optional[dict]) -> tuple:
    """x-ray cell 10 指纹：(farmer tuple, hands tuple-of-tuple, market tuple-of-tuple)。"""
    if not a:
        return ("PASS", (), ())
    return (
        tuple(a.get("farmer") or ["PASS"]),
        tuple(tuple(h) for h in (a.get("hands") or [])),
        tuple(tuple(o) for o in (a.get("market") or [])),
    )


def op(unit: Optional[Sequence[Any]]) -> Tuple[str, Optional[str]]:
    """leoprovorov 口径的命令算子：(class, good)。

    class=命令名（NORTH/SOUTH/EAST/WEST/MOVE 并为 MOVE）；good=命令点名的
    作物/动物/产品（找不到=None）。数量、坐标参数丢弃。
    """
    if not unit:
        return ("PASS", None)
    cls = str(unit[0]).upper()
    if cls in MOVE_VERBS:
        return ("MOVE", None)
    good = None
    for tok in unit[1:]:
        if isinstance(tok, str) and tok.upper() in GAME_GOODS:
            good = tok.upper()
            break
    return (cls, good)


def bundle_key(a: Optional[dict]) -> tuple:
    """leoprovorov f_g(t)：(op(farmer), n_hands, sorted{op(h)}, set{op(m)})。"""
    act = a or PASS_ACTION
    hands = act.get("hands") or []
    market = act.get("market") or []
    return (
        op(act.get("farmer") or ["PASS"]),
        len(hands),
        tuple(sorted(op(h) for h in hands)),
        tuple(sorted({op(m) for m in market})),
    )


def bundle_key_jsonable(a: Optional[dict]) -> str:
    """bundle 指纹的稳定字符串形（用于计数/哈希）。"""
    f, nh, hs, ms = bundle_key(a)
    return "|".join(
        [
            f"{f[0]}:{f[1] or ''}",
            str(nh),
            ",".join(f"{c}:{g or ''}" for c, g in hs),
            ",".join(f"{c}:{g or ''}" for c, g in ms),
        ]
    )


@dataclass
class EpisodeRecord:
    """一局归一记录。

    window=None 表示全季 720 拍覆盖；window=24 表示仅 day0 片段（feats-band 入口）。
    lossy_notes 记录入口的已知丢真（如 feats-band 无 hands 通道、无价格/棋盘）。
    """

    episode: Any
    seat: int
    team: str
    opp: str
    margin: float
    stream: List[Optional[dict]] = field(default_factory=list)
    opp_stream: List[Optional[dict]] = field(default_factory=list)
    world: Optional[str] = None          # 前两店有序对 "__".join(shops)；缺=None
    opp_sub: Optional[Any] = None
    date: Optional[str] = None
    seed: Optional[int] = None
    window: Optional[int] = None
    prices_t: Optional[List[Dict[str, float]]] = None
    money_me: Optional[List[float]] = None
    money_op: Optional[List[float]] = None
    occ: Optional[List[List[int]]] = None        # 10x10 占位计数（逐拍有物格 +1）
    pres: Optional[List[List[int]]] = None       # 10x10 在场计数（farmer+hands 位置）
    unlocked: Optional[List[List[int]]] = None   # 10x10 解锁计数（逐拍非 LOCKED 格 +1）
    lossy_notes: List[str] = field(default_factory=list)

    def to_compact(self) -> dict:
        d = asdict(self)
        return d

    @staticmethod
    def from_compact(d: dict) -> "EpisodeRecord":
        known = {f for f in EpisodeRecord.__dataclass_fields__}  # type: ignore[attr-defined]
        return EpisodeRecord(**{k: v for k, v in d.items() if k in known})


def new_grid() -> List[List[int]]:
    return [[0] * 10 for _ in range(10)]
