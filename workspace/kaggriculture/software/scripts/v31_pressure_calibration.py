# 【中文】v31_pressure_calibration.py —— v3.1 对手压力自适应折扣标定（选参留痕）
# ===========================================================================
# 用途（任务包 v3.1，2026-09-20）：悲观折扣系数从全局常数改为对手压力
#   函数 plans.pressure_discount 后，按 P2.6 惯例做防挑参标定：
#   预登记网格 + smoke 子集选参 + official 一次终裁（终裁由
#   scripts/v3_readmission_suite.py --mode official 承担，本脚本只选参）。
# 预登记内容（跑前钉死，写入输出原样留痕）：
#   1) 函数形式：disc = 1-(1-STRONG)×s；s = max(s_herd, s_quads[, s_money])
#      （s_herd=clamp(opp_herd/HERD_REF)、s_quads=clamp((opp_quads-1)/
#      (QUAD_REF-1))、s_money=clamp((opp_money-max(my_money,FLOOR))/GAP)；
#      day<=PRIOR_DAYS 先验全悲观——开局承诺窗无对手产能证据）。
#   2) 网格：C0 对照（v14.2 语义：adaptive off + LIQ 0）+ C1..C8 =
#      {GATE: gated(PRIOR_DAYS=1)|open(PRIOR_DAYS=-1)}
#      × {HERD_REF: 8|12} × {LIQ_PENALTY: 0|0.3}，QUAD_REF=3 恒定，
#      STRONG=0.75 恒定（硬约束：强端不变）。
#      资金差信号预登记关闭（MONEY_GAP_REF=None）：22 局逐日轨迹实测
#      囤钱型弱对手（110683437 d13 8.1k/0.4k、110698875 d20 28.2k/2H、
#      110692292 27k）与巨人（6.3-40k）相对资金交叠（8.8x-117x）不可
#      区分——资金是"未再投资"信号，非"倾销能力"信号。
#   3) smoke 子集（6 局，按结果类分层，与 v14.2 official 逐局口径同表）：
#      巨人侧 = 110699710（base 守成挽回 +47.8%，哨兵局）+
#      110687913（V_COMB 竞速挽回 +20.2%）+ 110841464（未挽回 -14.9%，
#      风险锚）；胜局侧 = 110683437/110696787（塌方 -55.6%/-25.4%）+
#      110790899（中局抖动 -36.5%）。
#   4) 选参规则（确定性）：score = 挽回计数（3 胜局侧 gain>=-0.05 各 +1）
#      + 保 b 计数（110699710/110687913 gain>=+0.10 各 +1）
#      + 风险锚（110841464 gain>=-0.149 即不劣于 v14.2 基线 +1）；
#      同分 tie-break：①胜局侧 gain 之和更大 ②巨人侧 gain 最小值更大
#      ③网格序（C1..C8）。选中配置由本脚本打印并写入 JSON，随后人工
#      烘焙为 plans.PRESSURE_* 模块默认值再跑 official。
#   5) 方差声明：时间治理器 EWMA rung 自适应使逐黎明档位随墙钟波动
#      （v14.2 复裁三连跑判据 b 在 3-5/9 间波动）——smoke 分数含此噪声，
#      official 一次终裁为准；本脚本不做重跑挑样。
# 纪律：stdlib-only、全离线；src 九模块零改动；rollout 路径与
#   v3_readmission_suite 完全同源（复用其 rollout_v3_planner 与
#   V3_RUNTIME_CONFIG，K=6×H=1d 阶梯不变）。
# 输出：exports/probes/planner_bench/v31_pressure_calibration/
#         v31_calibration.json（网格×逐局 gain + 选参记录）
# CLI：--mode sweep（默认，全网格）| control（只跑 C0 对照，校准烟测）。
# ===========================================================================

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(SCRIPT_DIR)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import v3_readmission_suite as suite                     # noqa: E402
from kaggle_simulations.agent.planner import plans as _plans   # noqa: E402

OUT_DIR = os.path.join(SOFTWARE, "exports", "probes", "planner_bench",
                       "v31_pressure_calibration")
OUT = os.path.join(OUT_DIR, "v31_calibration.json")
TEAM = suite.TEAM

# ---- 预登记 smoke 子集（分层；理由见模块头 3)）----
SMOKE_GIANTS = (110699710, 110687913, 110841464)
SMOKE_WINS = (110683437, 110696787, 110790899)
SMOKE_EPISODES = SMOKE_GIANTS + SMOKE_WINS

# ---- 预登记网格（模块头 2)）；configs[i] = (name, patch_dict) ----
# v3.1 标定期发现的投影器选择机构缺陷（必修，证据内嵌）：
#   select.aggregate_scores 的 trimmed_mean 按【name-sorted 顺序】切片，
#   键序≠值序时裁掉的是名字居中而非值居中的模型——Ω=4 实测
#   （110683437 d5）：kept=(9496.0, 13374.2)=值min+值max，悲观
#   (10015.5) 与 wheat_sup (10960.1) 两个值中位反被裁 → 悲观折扣对
#   投影器全局失敏（v3.1 自适应折扣原样会成死代码），与 select.py
#   文档"序统计量"契约矛盾。已有契约测试 {'a':1,'b':2,'c':3,'d':4}
#   键序=值序巧合未暴露。修复=值序排序后裁切（select.py，planner 内）。
#   标定网格因此拆三层归因：C0a=v14.2 原样语义锚（legacy-trim+常数折扣
#   +LIQ0）；C0b=仅修 trim（值序+常数折扣 0.75+LIQ0）；C1..C8=值序+自适应
#   折扣网格。C0a 期望复现 v14.2 official 逐局值（方差锚），C0b 隔离
#   trim 修复本身的效应。
PRIOR_GATED = 1          # d0-d1 先验全悲观（v14.2 开局结构面）
PRIOR_OPEN = -1          # 无先验窗（day<=-1 永假）
GRID = (
    ("C0a_v142_anchor", {"SELECT_TRIM": "legacy", "PRESSURE_ADAPTIVE": False,
                         "PRESSURE_LIQ_PENALTY": 0.0}),
    ("C0b_trimfix_only", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": False,
                          "PRESSURE_LIQ_PENALTY": 0.0}),
    ("C1_gated_H8_L0", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                        "PRESSURE_PRIOR_DAYS": PRIOR_GATED,
                        "PRESSURE_HERD_REF": 8.0, "PRESSURE_LIQ_PENALTY": 0.0}),
    ("C2_gated_H8_L3", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                        "PRESSURE_PRIOR_DAYS": PRIOR_GATED,
                        "PRESSURE_HERD_REF": 8.0, "PRESSURE_LIQ_PENALTY": 0.3}),
    ("C3_gated_H12_L0", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                         "PRESSURE_PRIOR_DAYS": PRIOR_GATED,
                         "PRESSURE_HERD_REF": 12.0, "PRESSURE_LIQ_PENALTY": 0.0}),
    ("C4_gated_H12_L3", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                         "PRESSURE_PRIOR_DAYS": PRIOR_GATED,
                         "PRESSURE_HERD_REF": 12.0, "PRESSURE_LIQ_PENALTY": 0.3}),
    ("C5_open_H8_L0", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                       "PRESSURE_PRIOR_DAYS": PRIOR_OPEN,
                       "PRESSURE_HERD_REF": 8.0, "PRESSURE_LIQ_PENALTY": 0.0}),
    ("C6_open_H8_L3", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                       "PRESSURE_PRIOR_DAYS": PRIOR_OPEN,
                       "PRESSURE_HERD_REF": 8.0, "PRESSURE_LIQ_PENALTY": 0.3}),
    ("C7_open_H12_L0", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                        "PRESSURE_PRIOR_DAYS": PRIOR_OPEN,
                        "PRESSURE_HERD_REF": 12.0, "PRESSURE_LIQ_PENALTY": 0.0}),
    ("C8_open_H12_L3", {"SELECT_TRIM": "value", "PRESSURE_ADAPTIVE": True,
                        "PRESSURE_PRIOR_DAYS": PRIOR_OPEN,
                        "PRESSURE_HERD_REF": 12.0, "PRESSURE_LIQ_PENALTY": 0.3}),
)
# C0 对照的期望基线（v14.2 official 实测，供方差对照；不进选参）
C0_BASELINE = {"110699710": 0.4782, "110687913": 0.2019, "110841464": -0.149,
               "110683437": -0.5558, "110696787": -0.254, "110790899": -0.365}
RES_GAIN_FLOOR = -0.05        # 胜局侧"挽回"线（损伤收敛到 5% 内）
GIANT_KEEP_FLOOR = 0.10       # 巨人侧"保 b"线（挽回 >=10%）
RISK_ANCHOR_FLOOR = -0.149    # 风险锚不劣于 v14.2 基线
_DEFAULTS = ("PRESSURE_ADAPTIVE", "PRESSURE_PRIOR_DAYS", "PRESSURE_HERD_REF",
             "PRESSURE_QUAD_REF", "PRESSURE_MONEY_GAP_REF",
             "PRESSURE_LIQ_PENALTY")
# 导入期快照（恢复基准；禁用 importlib.reload——reload 会替换模块对象，
# opponents._plans 仍持旧引用，导致补丁面分裂）。
_ORIGINALS = {key: getattr(_plans, key) for key in _DEFAULTS}

# ---- legacy trimmed_mean（v14.2 语义锚专用；select.py 缺陷修复前的
#      实现逐字复制，仅 C0a 校准锚使用，生产代码不携带）----
import math as _math                                    # noqa: E402
from kaggle_simulations.agent.planner import select as _select  # noqa: E402
_FIXED_AGGREGATE = _select.aggregate_scores


def _legacy_aggregate(scores, strategy="trimmed_mean", weights=None,
                      trim_fraction=_select.DEFAULT_TRIM_FRACTION):
    if strategy != "trimmed_mean":
        return _FIXED_AGGREGATE(scores, strategy=strategy, weights=weights,
                                trim_fraction=trim_fraction)
    values = [float(v) for _, v in sorted(scores.items())]   # 名字序（缺陷原样）
    n = len(values)
    trim = int(_math.floor(n * float(trim_fraction)))
    trim = min(trim, (n - 1) // 2)
    kept = values[trim:n - trim] if trim else values
    return sum(kept) / len(kept)


def _patch(config_patch):
    for key in _DEFAULTS:
        if key in config_patch:
            setattr(_plans, key, config_patch[key])
    trim_mode = config_patch.get("SELECT_TRIM", "value")
    _select.aggregate_scores = (_legacy_aggregate if trim_mode == "legacy"
                                else _FIXED_AGGREGATE)


def _restore():
    for key, value in _ORIGINALS.items():
        setattr(_plans, key, value)
    _select.aggregate_scores = _FIXED_AGGREGATE


def run_config(deps, name, patch):
    """单配置 × smoke 子集全季 rollout（v14.2 复裁同路径）。"""
    _patch(patch)
    rows = {}
    t_start = time.time()
    try:
        for ep in SMOKE_EPISODES:
            replay = suite.load_replay(ep)
            teams = list((replay.get("info") or {}).get("TeamNames") or [])
            me = teams.index(TEAM)
            truth_me = float(replay["rewards"][me])
            truth_opp = float(replay["rewards"][1 - me])
            suite._runtime.reset_state()
            res = suite.rollout_v3_planner(deps, replay, me,
                                           suite.V3_RUNTIME_CONFIG)
            gain = (res["final_me"] - truth_me) / truth_me if truth_me else 0.0
            rows[str(ep)] = {
                "truth_me": truth_me, "truth_opp": truth_opp,
                "final_me": round(res["final_me"], 1),
                "gain_pct": round(gain, 4),
                "beats_truth_opp": res["final_me"] > truth_opp,
                "failopens": res["failopens"],
                "plans": len(set(res["plans"] or [])),
            }
            print(f"[v31-calib:{name}] ep{ep} truth {truth_me:8.0f} "
                  f"final {res['final_me']:8.0f} ({gain * 100:+6.1f}%) "
                  f"failopen={res['failopens']} "
                  f"[{time.time() - t_start:.0f}s]")
            del replay
    finally:
        _restore()
    return rows


def score_config(rows):
    """预登记选参规则（模块头 4)；确定性）。"""
    rescued = [ep for ep in SMOKE_WINS
               if rows[str(ep)]["gain_pct"] >= RES_GAIN_FLOOR]
    kept = [ep for ep in SMOKE_GIANTS[:2]
            if rows[str(ep)]["gain_pct"] >= GIANT_KEEP_FLOOR]
    risk_ok = rows[str(SMOKE_GIANTS[2])]["gain_pct"] >= RISK_ANCHOR_FLOOR
    failopens = sum(r["failopens"] for r in rows.values())
    return {
        "rescued_wins": len(rescued), "rescued": list(rescued),
        "kept_giants": len(kept), "kept": list(kept),
        "risk_anchor_ok": bool(risk_ok),
        "score": len(rescued) + len(kept) + int(risk_ok),
        "win_gain_sum": round(sum(rows[str(ep)]["gain_pct"]
                                  for ep in SMOKE_WINS), 4),
        "giant_gain_min": round(min(rows[str(ep)]["gain_pct"]
                                    for ep in SMOKE_GIANTS), 4),
        "failopens": failopens,
        "valid": failopens == 0 and len(rows) == len(SMOKE_EPISODES),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="v3.1 压力自适应折扣标定（预登记网格 × smoke 选参）")
    parser.add_argument("--mode", choices=("sweep", "control"),
                        default="sweep")
    args = parser.parse_args(argv)
    configs = GRID if args.mode == "sweep" else GRID[:1]
    deps = suite.bench.make_twin_deps()
    out = {
        "protocol": "v31-pressure-calibration/1.0",
        "mode": args.mode,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(
            timespec="seconds"),
        "preregistration": {
            "function_form": ("disc=1-(1-STRONG)*s; s=max(s_herd,s_quads"
                              "[,s_money]); s_herd=clamp(opp_herd/HERD_REF); "
                              "s_quads=clamp((opp_quads-1)/(QUAD_REF-1)); "
                              "s_money=clamp((opp_money-max(my_money,FLOOR))"
                              "/GAP); day<=PRIOR_DAYS -> s=1"),
            "strong_end": _plans.PRESSURE_DISC_STRONG,
            "quad_ref_fixed": 3,
            "money_gap_ref": None,
            "select_trim_defect_fix": (
                "select.aggregate_scores trimmed_mean 原按 name-sorted 切片"
                "（键序≠值序时裁掉名字居中模型；Ω=4 实测 kept=min+max，"
                "悲观模型被裁 → 折扣对投影器失敏）。修复=值序排序后裁切；"
                "C0a=修复前语义锚、C0b=仅修复、C1-C8=修复+自适应折扣"),
            "money_off_rationale": ("囤钱型弱对手（110683437/110698875/"
                                    "110692292）与巨人相对资金交叠 "
                                    "8.8x-117x，不可区分；资金=未再投资"
                                    "信号非倾销能力信号"),
            "grid": [name for name, _ in configs],
            "grid_patches": {name: {k: v for k, v in patch.items()}
                             for name, patch in configs},
            "smoke_subset": {"giants": list(SMOKE_GIANTS),
                             "wins": list(SMOKE_WINS),
                             "rationale": ("分层：哨兵局+竞速挽回局+风险锚 /"
                                           " 塌方×2+中局抖动×1")},
            "selection_rule": ("score=rescued(3 wins>=-5%)+kept(2 giants"
                               ">=+10%)+risk(110841464>=-14.9%); "
                               "tie1=win_gain_sum, tie2=giant_gain_min, "
                               "tie3=grid order"),
            "c0_baseline_v142": C0_BASELINE,
            "variance_note": ("时间治理器 EWMA rung 随墙钟自适应；smoke 分数"
                              "含规定动作噪声，official 一次终裁为准"),
        },
        "configs": {},
    }
    t_start = time.time()
    for name, patch in configs:
        print(f"\n[v31-calib] === {name} {patch} ===")
        rows = run_config(deps, name, patch)
        out["configs"][name] = {"patch": dict(patch), "episodes": rows,
                                "score": score_config(rows)}
        s = out["configs"][name]["score"]
        print(f"[v31-calib] {name}: score={s['score']} "
              f"rescued={s['rescued_wins']} kept={s['kept_giants']} "
              f"risk={s['risk_anchor_ok']} win_sum={s['win_gain_sum']} "
              f"giant_min={s['giant_gain_min']}")

    # ---- 选参（预登记规则；invalid 配置淘汰到末位）----
    # 修正记录（2026-09-20）：首版 sort_key 的 tie-break ②方向写反
    #   （giant_gain_min 升序）——与预登记文本"②巨人侧 gain 最小值更大"
    #   不符；本版修正为降序（值越大越优），从已保存的 sweep 结果重选：
    #   score=3 且 win_sum=-1.1753 的并列组中 giant_gain_min=+0.0623
    #   （C8，110841464 +6.2%）优于 -0.149（其余，110841464 -14.9%）
    #   → 选中 C8_open_H12_L3。sweep 本身不重跑（结果无变化）。
    def sort_key(item):
        name, rec = item
        s = rec["score"]
        order = [n for n, _ in configs]
        return (0 if s.get("valid") else 1, -s["score"],
                -s["win_gain_sum"], -s["giant_gain_min"], order.index(name))

    ranked = sorted(out["configs"].items(), key=sort_key)
    out["ranking"] = [{"name": n, "score": r["score"]}
                      for n, r in ranked]
    out["selected"] = ranked[0][0] if ranked else None
    out["selected_patch"] = dict(ranked[0][1]["patch"]) if ranked else None
    out["wall_seconds"] = round(time.time() - t_start, 1)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(out, handle, ensure_ascii=False, indent=1)
    print(f"\n[v31-calib] selected={out['selected']} "
          f"patch={out['selected_patch']}")
    print(f"[v31-calib] ranking: "
          f"{[(r['name'], r['score']['score']) for r in out['ranking']]}")
    print(f"[v31-calib] wall={out['wall_seconds']}s -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
