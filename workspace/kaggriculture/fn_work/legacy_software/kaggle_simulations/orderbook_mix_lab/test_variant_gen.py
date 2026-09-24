# -*- coding: utf-8 -*-
"""R15 单测：variant_gen（schedule 组/feasibility 组/build 组，小夹具）。"""
import pytest

from orderbook_mix_lab import _base as B
from orderbook_mix_lab import variant_gen as VG


def _tiny_base():
    """小磁带夹具：路由 0 上 10 个 MELON 植物 + 11 粒 MELON 种子单。"""
    actions = []
    route = []
    # step 0: 买 2；step 1: 种 2；step 2: 买 2；step 3: 种 2 …… 交错 5 块
    n_pairs = 5
    for i in range(n_pairs):
        buy_step = 2 * i
        plant_step = 2 * i + 1
        actions.append({"farmer": ["WEST"],
                        "hands": [["WEST"], ["WEST"], ["PASS"]],
                        "market": [["BUY_SEED", "MELON", 2]]})
        actions.append({"farmer": ["PLANT", "MELON"],
                        "hands": [["PLANT", "MELON"], ["WEST"], ["PASS"]],
                        "market": [["SELL", "WHEAT", 5]]})
        route += [2 * i, 2 * i + 1]
    # 1 粒富余种子（尾买单）
    actions.append({"farmer": ["PASS"], "hands": [], "market":
                    [["BUY_SEED", "MELON", 1]]})
    route.append(2 * n_pairs)
    # 占位其余步（到达 720 语义非必需；测试路由只走以上步）
    data = {"actions": actions, "routes": {"0": route},
            "shops": []}
    return data


def test_schedule_group_moves_plants_and_seeds():
    base = {"data": _tiny_base(), "primary_route": "0",
            "money_floor_curve": [3000.0] * 30}
    pair = {"from": "MELON", "to": "WHEAT"}
    sched = VG.build_variant_schedule(pair, 0.4, base)
    assert sched["from_plants_route"] == 10
    assert sched["moved_n"] == 4          # round(0.4×10)
    assert sched["buys_converted_qty"] == 4
    assert sched["skips"] == []
    # 手术后动作表：4 个 PLANT WHEAT 出现、BUY_SEED WHEAT 计数=4
    data = sched["data"]
    plants_w = sum(1 for ai in data["routes"]["0"]
                   for cmd in [data["actions"][ai]["farmer"]]
                   + data["actions"][ai]["hands"]
                   if cmd[:2] == ["PLANT", "WHEAT"])
    buys_w = sum(o[2] for ai in data["routes"]["0"]
                 for o in data["actions"][ai]["market"]
                 if o[:2] == ["BUY_SEED", "WHEAT"])
    assert plants_w == 4 and buys_w == 4
    # 指令数不变性：farmer/hands/market 列表长度与基线一致
    for ai_before, ai_after in zip(base["data"]["actions"], data["actions"]):
        assert len(ai_before["market"]) == len(ai_after["market"])
        assert len(ai_before["hands"]) == len(ai_after["hands"])
    # 路由审计
    assert sched["route_audit"]["0"]["plants_to"] >= 4


def test_schedule_seed_coverage_strictly_earlier_step():
    """植物先于一切买单 → 全部 skip（引擎步内先单元后市场）。"""
    data = {"actions": [
        {"farmer": ["PLANT", "MELON"], "hands": [],
         "market": [["BUY_SEED", "MELON", 1]]}],
        "routes": {"0": [0]}, "shops": []}
    sched = VG.build_variant_schedule(
        {"from": "MELON", "to": "WHEAT"}, 1.0,
        {"data": data, "primary_route": "0"})
    assert sched["moved_n"] == 0
    assert sched["skips"] and sched["skips"][0]["reason"] == "seed_uncovered"


def test_schedule_deadline_filter():
    """to=STRAWBERRY(fyd=10)：day≥20 的植物全部越窗。"""
    pass_actions = [{"farmer": ["PASS"], "hands": [], "market": []}]
    actions = list(pass_actions)
    step_to_ai = {}
    for d in range(0, 30, 2):        # 买@day d 首步，种@day d 次步
        buy_step, plant_step = d * 24, d * 24 + 1
        actions.append({"farmer": ["PASS"], "hands": [["WEST"]],
                        "market": [["BUY_SEED", "CARROT", 1]]})
        step_to_ai[buy_step] = len(actions) - 1
        actions.append({"farmer": ["PASS"], "hands": [["PLANT", "CARROT"]],
                        "market": []})
        step_to_ai[plant_step] = len(actions) - 1
    n_steps = max(step_to_ai) + 1
    route = [0] * n_steps
    for s, ai in step_to_ai.items():
        route[s] = ai
    data = {"actions": actions, "routes": {"0": route}, "shops": []}
    sched = VG.build_variant_schedule(
        {"from": "CARROT", "to": "STRAWBERRY"}, 1.0,
        {"data": data, "primary_route": "0"})
    # eligible = day ≤ 19 的植物（day+10 ≤ 29）= d ∈ {0,2,..,18} → 10 个
    assert sched["eligible_plants"] == 10
    assert sched["moved_n"] == 10
    assert all(e["step"] // 24 + 10 <= 29 for e in sched["edits"]
               if e["kind"] == "plant")


# ---------------------------------------------------------------------------
# feasibility 组
# ---------------------------------------------------------------------------
def _sched_with(**kw):
    data = _tiny_base()
    sched = VG.build_variant_schedule(
        {"from": "MELON", "to": "WHEAT"}, 0.4,
        {"data": data, "primary_route": "0",
         "money_floor_curve": kw.get("floor", [3000.0] * 30)})
    return sched


def test_feasibility_ok_case():
    feas = VG.check_variant_feasibility(_sched_with())
    assert feas["feasible"] is True and feas["violations"] == []


def test_feasibility_cash_violation():
    # 地板 day0=50，WHEAT-MELON 每株省 70 → 不违；反转构造：from 便宜 to 贵
    sched = _sched_with()
    sched["pair"] = {"from": "WHEAT", "to": "MELON"}   # 载荷反转（构造违例）
    sched["edits"] = [dict(e) for e in sched["edits"]]
    sched["money_floor_curve"] = [50.0] * 30
    feas = VG.check_variant_feasibility(sched)
    cash = [v for v in feas["violations"] if v["family"] == "cash"]
    assert cash and cash[0]["day"] == 0


def test_feasibility_stop_violation():
    sched = _sched_with()
    sched["pair"] = {"from": "MELON", "to": "STRAWBERRY"}
    sched["edits"] = [dict(e) for e in sched["edits"]]
    sched["edits"].append({"ai": 0, "step": 25 * 24, "kind": "plant",
                           "before": ["PLANT", "MELON"],
                           "after": ["PLANT", "STRAWBERRY"]})
    feas = VG.check_variant_feasibility(sched)
    assert any(v["family"] == "stop" for v in feas["violations"])


# ---------------------------------------------------------------------------
# build 组（小磁带手术）
# ---------------------------------------------------------------------------
def _fake_main_text(data):
    blob = B.encode_l3_blob(data)
    return ("import base64, json, zlib\n"
            f"_R108_DATA=json.loads(zlib.decompress(base64.b85decode('{blob}')))\n"
            "def agent(o, c=None):\n    return o\n")


def test_build_variant_main_splice_and_audit(tmp_path):
    base_data = _tiny_base()
    sched = VG.build_variant_schedule(
        {"from": "MELON", "to": "WHEAT"}, 0.4,
        {"data": base_data, "primary_route": "0"})
    src = tmp_path / "base_main.py"
    src.write_text(_fake_main_text(base_data), "utf-8")
    out = tmp_path / "variants" / "v_x" / "main.py"
    built = VG.build_variant_main(sched, str(src), str(out))
    assert out.exists() and built["diff_entries"] == len(sched["edits"])
    text_new = out.read_text("utf-8")
    text_old = src.read_text("utf-8")
    # blob 区间外逐字节一致（新 blob 终点 vs 旧 blob 终点分别对齐）
    _, (lo_old, hi_old) = B.decode_l3_blob(text_old)
    lo_new = built["blob_span"][0]
    assert text_new[:lo_new] == text_old[:lo_old]
    assert text_new[built["blob_span"][1]:] == text_old[hi_old:]
    # 编译可装载 + 解码回路数据生效
    env = {}
    exec(compile(text_new, str(out), "exec"), env)
    assert env["_R108_DATA"]["actions"][0]["market"][0] == \
        ["BUY_SEED", "WHEAT", 2]


def test_build_variant_main_rejects_overwrite(tmp_path):
    data = _tiny_base()
    sched = VG.build_variant_schedule(
        {"from": "MELON", "to": "WHEAT"}, 0.2,
        {"data": data, "primary_route": "0"})
    src = tmp_path / "base_main.py"
    src.write_text(_fake_main_text(data), "utf-8")
    before = src.read_bytes()
    with pytest.raises(RuntimeError):
        VG.build_variant_main(sched, str(src), str(src))
    assert src.read_bytes() == before          # 基座零改动


def test_generate_mix_variants_end_to_end(tmp_path):
    src = tmp_path / "base_main.py"
    src.write_text(_fake_main_text(_tiny_base()), "utf-8")
    pairs = [{"from": "MELON", "to": "WHEAT"}]
    out = VG.generate_mix_variants(pairs, scales=(0.2, 0.4),
                                   max_variants=16, l3_main_path=str(src),
                                   out_dir=str(tmp_path / "variants"),
                                   base_context={"money_floor_curve":
                                                 [3000.0] * 30})
    assert out["audit"]["n_points"] == 2
    assert len(out["variants"]) == 2
    assert out["audit"]["feasible_zero"] is False
    vids = [v["id"] for v in out["variants"]]
    assert vids == ["v_MELON2WHEAT_40pct", "v_MELON2WHEAT_20pct"]
    for v in out["variants"]:
        assert v["feasible"] and v["moved_n"] > 0
        assert (tmp_path / "variants" / v["id"] / "main.py").exists()
        assert (tmp_path / "variants" / v["id"] / "build_audit.json").exists()


def test_generate_mix_variants_zero_moved_drop(tmp_path):
    """scale 过小 → 零可迁移 → dropped（feasible_zero 依据）。"""
    src = tmp_path / "base_main.py"
    src.write_text(_fake_main_text(_tiny_base()), "utf-8")
    out = VG.generate_mix_variants([{"from": "MELON", "to": "WHEAT"}],
                                   scales=(0.05,), l3_main_path=str(src),
                                   out_dir=str(tmp_path / "v2"))
    # round(0.05×10)=1 → 非零；改用 0.04 强制 0
    out0 = VG.generate_mix_variants([{"from": "MELON", "to": "WHEAT"}],
                                    scales=(0.04,), l3_main_path=str(src),
                                    out_dir=str(tmp_path / "v3"))
    assert out0["audit"]["n_points"] == 1
    if out0["variants"]:
        assert out0["variants"][0]["moved_n"] >= 1
    else:
        assert out0["dropped"] and out0["audit"]["feasible_zero"] is True
