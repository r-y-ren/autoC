"""define_config_space（L1，R4）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

配置空间定义+枚举：**空间文档 + 空间规模登记**。

轴（v48 反射层真值转录自 v48_hybrid/main.py _V48_GOLD_CONFIG 与深读档
modules/；逐轴开关语义见 evaluate_ablation_tree 模块注）：

| 轴 | 类型 | 取值 | 真值来源 |
|---|---|---|---|
| 候选库件 | 枚举 10 | routes.json 2 件 + market_variants.json 8 件 | T2 产物 |
| clone_preempt | 开关 | on=horizon 2 / off=0 | v44.gold_floor（v48 gold） |
| slot_reorder | 开关 | on=影响分槽位排序(legacy) / off=磁带原生序 | v23.policy_library |
| market_maker | 开关 | on=wheat 做市专家 / off | v24.market_maker（v48 编译未启用） |
| terminal_forced | 开关 | on=step718 终局强改 / off | scripts.v19_terminal |
| dead_price_guard | 开关 | on=死价递延护栏（新增保险层） / off | 本管线自有 |
| clone_streak_required | 阈值微轴 | 24（v48 gold 缺省）/ 16（精化变体） | 深读档 |
| dead_guard_ratio | 阈值微轴 | 0.5（缺省）/ 0.65（精化变体） | 本管线自有 |

空间规模：布尔基空间 = 件数 × 2^开关数 = 10×32 = **320**（全枚举，粗筛
面）；阈值微轴为**精化阶段邻域展开**（仅在粗筛+精评最佳配置上展开，不进
基空间乘法——登记为 refinement 扇出 ≤2）。候选 id =
"<piece>#<5 位掩码>"（位序=SWITCH_ORDER），全序确定。

产物（output_dir，缺省 fn_work/tape_gen/search/）：config_space.json +
config_space.md（空间文档）。确定性：同库面同输出。
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from search_reflector_configs.evaluate_ablation_tree import (
    DEFAULT_THRESHOLDS,
    SWITCH_ORDER,
    V48_GOLD_PARAMS,
    load_library_tapes,
)

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_OUTPUT_DIR = _TAPE_GEN_ROOT / "search"

#: 阈值微轴（值序确定；首值=缺省）。
THRESHOLD_AXES = {
    "clone_streak_required": (24, 16),
    "dead_guard_ratio": (0.5, 0.65),
}

#: 微轴精化扇出上限（每微轴非缺省值 1 个变体，仅作用于模块开启的配置）。
REFINEMENT_FANOUT = sum(len(values) - 1 for values in
                        THRESHOLD_AXES.values())


def _mask(switches) -> str:
    return "".join("1" if switches[name] else "0"
                   for name in SWITCH_ORDER)


def _canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _space_doc(space) -> str:
    gold_text = json.dumps(V48_GOLD_PARAMS, sort_keys=True)
    axes_text = json.dumps(space["threshold_axes"])
    defaults_text = json.dumps(space["threshold_defaults"])
    lines = [
        "# 反射层配置空间（R4 空间定义文档）",
        "",
        "真值：v48 深读档 modules/（v44.gold_floor / v23.policy_library /",
        "v24.market_maker / scripts.v19_terminal）+ v48_hybrid/main.py",
        "_V48_GOLD_CONFIG 参数转录；死价护栏为本管线新增保险层。",
        "",
        f"- 候选库件：{space['n_pieces']} 件（{space['n_routes']} 路由 + "
        f"{space['n_variants']} 市场变体）",
        f"- 反射层开关面：{space['n_switches']} 轴 "
        f"（{'、'.join(space['switch_order'])}）",
        f"- 布尔基空间规模：{space['n_pieces']} × 2^{space['n_switches']} "
        f"= **{space['base_space_size']} 候选**（全枚举=粗筛面）",
        f"- 阈值微轴：{axes_text}（缺省 {defaults_text}；精化扇出 "
        f"≤{space['refinement_fanout']}，仅在最佳配置邻域展开，不进基空"
        "间乘法）",
        f"- v48 gold 常量（开关不改写部分）：{gold_text}",
        "- 稀疏惩罚：score = winrate − λ×启用模块数（λ 登记于账本；"
        "启用模块数=开关面 ON 计数，库件与阈值不计入）",
        f"- 候选 id：\"<件>#<掩码>\"（位序 {'|'.join(SWITCH_ORDER)}）；"
        "全序确定（件序字典序，掩码二进制升序）",
        "",
        "| 件 | 来源 |",
        "|---|---|",
    ]
    for piece in space["pieces"]:
        lines.append(f"| {piece['piece_id']} | {piece['source']} |")
    return "\n".join(lines) + "\n"


def define_config_space(payload=None):
    """意图级签名；真值在责任文档。

    payload 可覆盖：library_dir / output_dir / write。返回 {pieces,
    switch_order, threshold_axes, n_pieces, n_switches,
    base_space_size, refinement_fanout, candidates（320 项，全序确定）,
    space_sha256, paths}；write 时落盘 config_space.json（含规模登记，
    不含候选全表）+ config_space.md（空间文档）。
    """
    payload = dict(payload or {})
    library_dir = payload.get("library_dir")
    tapes = load_library_tapes(library_dir)
    output_dir = payload.get("output_dir")

    pieces = []
    for piece_id in sorted(tapes):
        kind, _, name = piece_id.partition(":")
        pieces.append({"piece_id": piece_id,
                       "source": ("routes.json" if kind == "route"
                                  else "market_variants.json"),
                       "route_name": name,
                       "n_steps": len(tapes[piece_id])})
    n_pieces = len(pieces)
    n_switches = len(SWITCH_ORDER)

    candidates = []
    for piece in pieces:
        for mask_int in range(2 ** n_switches):
            bits = format(mask_int, f"0{n_switches}b")
            switches = {name: bit == "1" for name, bit in
                        zip(SWITCH_ORDER, bits)}
            candidates.append({
                "id": f"{piece['piece_id']}#{bits}",
                "piece": piece["piece_id"],
                "switches": switches,
                "thresholds": dict(DEFAULT_THRESHOLDS),
                "enabled_modules": sum(1 for v in switches.values() if v),
            })

    space = {
        "pieces": pieces,
        "switch_order": list(SWITCH_ORDER),
        "threshold_axes": {k: list(v) for k, v in
                           THRESHOLD_AXES.items()},
        "threshold_defaults": dict(DEFAULT_THRESHOLDS),
        "n_pieces": n_pieces,
        "n_routes": sum(1 for p in pieces
                        if p["piece_id"].startswith("route:")),
        "n_variants": sum(1 for p in pieces
                          if p["piece_id"].startswith("variant:")),
        "n_switches": n_switches,
        "base_space_size": n_pieces * (2 ** n_switches),
        "refinement_fanout": REFINEMENT_FANOUT,
        "candidates": candidates,
    }
    space["space_sha256"] = hashlib.sha256(
        _canonical(space).encode("utf-8")).hexdigest()

    paths = {}
    if payload.get("write", True) and output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        json_path = output_dir / "config_space.json"
        doc_path = output_dir / "config_space.md"
        summary = {k: v for k, v in space.items() if k != "candidates"}
        summary["n_candidates"] = len(candidates)
        json_path.write_text(_canonical(summary) + "\n", encoding="utf-8")
        doc_path.write_text(_space_doc(space), encoding="utf-8")
        paths = {"space_json": str(json_path), "space_doc": str(doc_path)}

    result = dict(space)
    result["paths"] = paths
    return result
