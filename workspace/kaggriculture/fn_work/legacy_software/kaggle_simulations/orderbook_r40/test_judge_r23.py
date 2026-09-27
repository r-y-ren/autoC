# -*- coding: utf-8 -*-
"""R23 测试面：judge_r23（判决/分段统计）。

segment 组：①四指标计算（seg_delta/realized_px/fill_rate/lot_size 精确值）
②缺成交字段→UNKNOWN（seg_delta 仍出）③逐字段缺失各判 UNKNOWN+baseline 自
比 verdict。judge 组：④六判据分支聚合（判据=R23 ②分项+总判原文，5 过 1 红
→overall False）⑤单局红计入不短路（errors 记账、全跑、fail-closed）⑥并行
提速读数入账（speedup 进 evidence+改4）⑦对照降级时改4 判 False。
"""
import json
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r40 import judge_r23 as j23
except ImportError:  # pragma: no cover - 平铺装载
    import judge_r23 as j23  # type: ignore

judge_r23 = j23.judge_r23
segment_stats = j23.segment_stats


# ---------------------------------------------------------------- 工具 --

def _rows(seg=4000.0, px=10.0, fill=0.95, lot=10.0, drop=()):
    """合成状态行：day20 锚+d21-28 两拍，产四读数 (seg,px,fill,lot)。"""
    vol, orders = 10.0, 20.0
    rows = [
        {"step": 503, "day": 20, "cash": 1000.0, "opp_cash": 1000.0},
        {"step": 520, "day": 21, "cash": 1000.0, "opp_cash": 1000.0,
         "turnover": px * vol, "vol": vol, "filled_orders": fill * orders,
         "orders": orders, "qty": lot * orders},
        {"step": 695, "day": 28, "cash": 1000.0 + seg, "opp_cash": 1000.0,
         "turnover": 0.0, "vol": 0.0, "filled_orders": 0.0, "orders": 0.0,
         "qty": 0.0},
    ]
    if drop:
        rows = [{k: v for k, v in r.items() if k not in drop} for r in rows]
    return rows


def _tiny_replay(tmp_path, episode, seed):
    """最小合法 replay（供 _load_items 解析：seed/TeamNames/steps）。"""
    steps = []
    for t in range(4):
        pair = []
        for pl in (0, 1):
            pair.append({
                "observation": {
                    "step": t, "day": 0, "hour": t, "player": pl,
                    "farms": [{"money": 3000.0}, {"money": 3000.0}],
                    "market": {}, "town": {}, "private": {}},
                "action": {"farmer": ["PASS"], "hands": [], "market": []}})
        steps.append(pair)
    data = {"info": {"EpisodeId": episode, "seed": seed,
                     "TeamNames": ["renyxin", "opp"]},
            "configuration": {}, "steps": steps,
            "rewards": [3000.0, 3000.0], "statuses": ["DONE", "DONE"]}
    p = tmp_path / f"episode-{episode}-replay.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return str(p)


def _banks(sp):
    """我方胜的终局资金（按 our_seat）。"""
    return [7000.0, 3000.0] if sp["our_seat"] == 0 else [3000.0, 7000.0]


def _fake_play_factory(red_game_id=None):
    """按臂定局果：h2h 偶 seed 双胜/奇 seed 分席、strong 全胜、mirror 平。"""
    def _fake_play(specs, cfg):
        rows = []
        for sp in specs:
            row = {"game_id": sp["game_id"], "seed": sp["seed"],
                   "kind": sp["kind"], "arm": sp.get("arm"),
                   "our_seat": sp["our_seat"], "episode": sp.get("episode"),
                   "banks": _banks(sp), "error": None, "elapsed_s": 0.01,
                   "states": None, "attribution": {"ok": True}}
            if sp["kind"] == "directed":
                row["states"] = _rows(seg=4000.0, px=10.0, fill=0.95,
                                      lot=10.0)
            else:
                arm = sp["arm"]
                if arm == "h2h_r37" and sp["seed"] % 2:
                    row["banks"] = [7000.0, 3000.0] \
                        if sp["our_seat"] == 0 else [7000.0, 3000.0]
                elif arm == "mirror":
                    row["banks"] = [5000.0, 5000.0]
            if red_game_id is not None and sp["game_id"] == red_game_id:
                row["banks"] = None
                row["error"] = "RuntimeError: red"
            rows.append(row)
        return rows
    return _fake_play


def _bridge_ok(cfg, corpus):
    return {"loaded": True, "consistency": {"n_checked": 30, "n_match": 30,
                                           "rate": 1.0},
            "consistency_ok": True, "degraded": False,
            "degraded_reason": None, "engine": "sim", "wall_speedup": 5.4}


def _bridge_degraded(cfg, corpus):
    return {"loaded": True, "consistency": {"n_checked": 30, "n_match": 29,
                                           "rate": 29 / 30},
            "consistency_ok": False, "degraded": True,
            "degraded_reason": "对照未过：29/30", "engine": "official",
            "wall_speedup": 1.0}


def _speed(speedup):
    def _fake(specs, cfg):
        return {"speedup": speedup, "serial_wall_s": 96.0,
                "parallel_wall_s": round(96.0 / speedup, 3) if speedup
                else None, "n_games": len(list(specs)),
                "workers": 16, "sec_per_game_serial": 3.0}
    return _fake


def _wire(monkeypatch, tmp_path, red_game_id=None, bridge=_bridge_ok,
          speedup=12.5):
    paths = [_tiny_replay(tmp_path, 113700001, 20396171),
             _tiny_replay(tmp_path, 113700002, 98797048)]
    monkeypatch.setattr(j23, "_states_from_replay",
                        lambda replay, seat, seed: (_rows(seg=1000.0, px=8.0,
                                                          fill=0.9, lot=8.0),
                                                    {"ok": True}))
    monkeypatch.setattr(j23, "_play_batch", _fake_play_factory(red_game_id))
    monkeypatch.setattr(j23, "_bridge_crosscheck", bridge)
    monkeypatch.setattr(j23, "_measure_speedup", _speed(speedup))
    bench = {"n_games": 12, "workers": 1,
             "opponents": [
                 str(Path(j23.KSIM_DIR) / "orderbook_r37/build/main.py"),
                 str(Path(j23.KSIM_DIR)
                     / "orderbook_2965_adopt/a/main.py")],
             "seed_bases": {"h2h": 510000, "strong": 520000,
                            "mirror": 530000, "speed": 540000}}
    return paths, bench


# ================================================== segment 组（真测试） --

def test_segment_stats_four_metrics():
    """四指标计算：seg_delta=margin 段增量、成交额/量、成交单/挂单、单均量。"""
    out = segment_stats(_rows(seg=4000.0, px=10.0, fill=0.95, lot=10.0))
    assert out["seg_delta"] == 4000.0
    assert out["realized_px"] == 10.0
    assert out["fill_rate"] == 0.95
    assert out["lot_size"] == 10.0
    assert out["verdict"]["status"] == "ok"
    assert out["verdict"]["unknown"] == []
    assert out["verdict"]["seg_delta_positive"] is True


def test_segment_stats_unknown_missing_fields():
    """缺成交类字段→UNKNOWN；cash/opp_cash 在则 seg_delta 仍出。"""
    out = segment_stats(_rows(seg=-500.0, drop=("turnover", "vol",
                                                "filled_orders", "orders",
                                                "qty")))
    assert out["seg_delta"] == -500.0
    for key in ("realized_px", "fill_rate", "lot_size"):
        assert out[key] == "UNKNOWN"
    assert out["verdict"]["status"] == "UNKNOWN"
    assert set(out["verdict"]["unknown"]) == {"realized_px", "fill_rate",
                                              "lot_size"}
    assert out["verdict"]["seg_delta_positive"] is False
    # 空窗/全缺→四读数全 UNKNOWN
    empty = segment_stats([{"step": 520, "day": 21}])
    assert all(empty[k] == "UNKNOWN" for k in
               ("seg_delta", "realized_px", "fill_rate", "lot_size"))


def test_segment_stats_field_level_unknown_and_baseline_verdict():
    """逐字段缺失各判 UNKNOWN；baseline 自比进 verdict（+3% 口径读数）。"""
    out = segment_stats(_rows(drop=("orders",)), baseline={
        "seg_delta": 3000.0, "realized_px": 8.0, "fill_rate": 0.9,
        "lot_size": 8.0})
    assert out["realized_px"] == 10.0
    assert out["seg_delta"] == 4000.0
    # orders 缺→fill_rate/lot_size 双双 UNKNOWN
    assert out["fill_rate"] == "UNKNOWN"
    assert out["lot_size"] == "UNKNOWN"
    v = out["verdict"]
    assert v["status"] == "UNKNOWN"
    assert v["baseline"]["realized_px"] == 8.0
    assert v["realized_px_up_pct"] == 25.0        # (10-8)/8*100
    assert v["lot_size_up_pct"] is None           # 读数 UNKNOWN
    assert v["fill_rate_delta"] is None
    # 无基线→自比全 None；baseline 亦可传状态行序列
    out2 = segment_stats(_rows(), baseline=_rows(seg=2000.0, px=8.0))
    assert out2["verdict"]["realized_px_up_pct"] == 25.0
    assert out2["verdict"]["baseline"]["seg_delta"] == 2000.0
    with pytest.raises(TypeError):
        segment_stats("bad")


# =================================================== judge 组（真测试） --

def test_judge_six_criteria_aggregation(monkeypatch, tmp_path):
    """六判据分支聚合：c1-c5 过、c6 红（0.833<0.85）→overall False 如实。"""
    paths, bench = _wire(monkeypatch, tmp_path)
    ev = judge_r23(str(Path(j23.KSIM_DIR) / "orderbook_r40/build"),
                   paths, bench)
    c = ev["criteria"]
    assert set(c) == {"c1_rebuild_route", "c2_sell_exec", "c3_queue_hygiene",
                      "c4_sim_judge", "c5_h2h_r37", "c6_league_winrate"}
    assert c["c1_rebuild_route"]["pass"] is True
    assert c["c2_sell_exec"]["pass"] is True
    assert c["c3_queue_hygiene"]["pass"] is True
    assert c["c4_sim_judge"]["pass"] is True
    assert c["c5_h2h_r37"]["pass"] is True
    assert c["c6_league_winrate"]["pass"] is False
    # 判据读数如实（中位/倍率/一致率）
    assert c["c2_sell_exec"]["readings"]["seg_delta_median"] == 4000.0
    assert c["c2_sell_exec"]["readings"]["realized_px_up_pct"] == 25.0
    assert c["c3_queue_hygiene"]["readings"]["fill_rate"] == 0.95
    assert c["c4_sim_judge"]["readings"]["speedup"] == 12.5
    assert c["c4_sim_judge"]["readings"]["consistency_rate"] == 1.0
    assert c["c5_h2h_r37"]["readings"]["h2h_rate"] == 0.75
    assert c["c6_league_winrate"]["readings"]["league_winrate"] == \
        pytest.approx(5 / 6, abs=1e-3)
    assert ev["overall"]["pass"] is False
    assert ev["overall"]["failed"] == ["c6_league_winrate"]
    assert ev["overall"]["n_pass"] == 5
    assert ev["readings"]["league"]["top550_winrate"] == \
        pytest.approx(0.9, abs=1e-6)


def test_judge_red_game_counts_not_shortcircuit(monkeypatch, tmp_path):
    """单局红计入不短路：errors 记账、四局全跑、红局计负且判据 fail-closed。"""
    paths, bench = _wire(monkeypatch, tmp_path,
                         red_game_id="dir-113700001-s0")
    ev = judge_r23(str(Path(j23.KSIM_DIR) / "orderbook_r40/build"),
                   paths, bench)
    assert ev["counts"]["directed_games"] == 4
    assert ev["counts"]["directed_red"] == 1
    assert len(ev["readings"]["directed"]["per_game"]) == 4
    reds = [e for e in ev["errors"] if e.get("game_id")
            == "dir-113700001-s0"]
    assert reds and "red" in reds[0]["error"]
    # 不短路：league 臂照跑照聚合
    assert ev["counts"]["league_games"] == 12
    assert ev["readings"]["league"]["arms"]
    # 红局→分段判据 fail-closed False（c1/c2/c3），但聚合照出
    assert ev["criteria"]["c2_sell_exec"]["pass"] is False
    assert ev["criteria"]["c3_queue_hygiene"]["pass"] is False
    assert ev["criteria"]["c1_rebuild_route"]["pass"] is False
    assert set(ev["criteria"]) == {"c1_rebuild_route", "c2_sell_exec",
                                   "c3_queue_hygiene", "c4_sim_judge",
                                   "c5_h2h_r37", "c6_league_winrate"}


def test_judge_parallel_speedup_reading(monkeypatch, tmp_path):
    """并行提速读数入账：speedup 进 evidence.readings.speed 与改4 判据。"""
    paths, bench = _wire(monkeypatch, tmp_path, speedup=16.0)
    ev = judge_r23(str(Path(j23.KSIM_DIR) / "orderbook_r40/build"),
                   paths, bench)
    assert ev["readings"]["speed"]["speedup"] == 16.0
    assert ev["criteria"]["c4_sim_judge"]["readings"]["speedup"] == 16.0
    assert ev["criteria"]["c4_sim_judge"]["pass"] is True
    assert ev["readings"]["speed"]["workers"] == 16
    assert ev["readings"]["speed"]["serial_wall_s"] == 96.0


def test_judge_bridge_degraded_c4_false(monkeypatch, tmp_path):
    """对照降级→改4 判 False（即便提速达标），降级原因如实入 evidence。"""
    paths, bench = _wire(monkeypatch, tmp_path, speedup=16.0,
                         bridge=_bridge_degraded)
    ev = judge_r23(str(Path(j23.KSIM_DIR) / "orderbook_r40/build"),
                   paths, bench)
    assert ev["criteria"]["c4_sim_judge"]["pass"] is False
    assert ev["criteria"]["c4_sim_judge"]["readings"]["speedup"] == 16.0
    assert ev["criteria"]["c4_sim_judge"]["readings"]["consistency_ok"] \
        is False
    assert ev["readings"]["bridge"]["degraded"] is True
    assert "对照未过" in ev["readings"]["bridge"]["degraded_reason"]
    assert any(e.get("scope") == "bridge" for e in ev["errors"])
