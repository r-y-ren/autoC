# -*- coding: utf-8 -*-
"""R23 测试面：ablation_r40（B32 修订消融组）+ components 开关。

消融组（ablation_r40）：①探针构建（V0-V5 形态/抽取序/包装链只含所选件/
确定性）②决策规则（留强砍弱三档+①优先保留档）③效应表聚合形态。
components 开关（build_r40/inject_r40 B32 修订签名）：④inject 子集抽取
（块只含所选件/校验四条照跑/默认全件字节稳）⑤build_r40 子集构建（sell_lots
关=磁带零改动+空登记注释行；审计/pack 对账照过）⑥非法 components 即抛。
"""
import ast
import hashlib
import json
import sys
from pathlib import Path

import pytest  # noqa: F401

_HERE = Path(__file__).resolve().parent
_KSIM = _HERE.parent
if str(_KSIM) not in sys.path:
    sys.path.insert(0, str(_KSIM))

try:
    from orderbook_r40 import ablation_r40 as AB
    from orderbook_r40 import build_r40 as B
    from orderbook_r40 import inject_r40 as IJ
except ImportError:  # 兜底：直接以 orderbook_r40/ 为 sys.path 根跑测
    import ablation_r40 as AB
    import build_r40 as B
    import inject_r40 as IJ


# ------------------------------ 夹具 ------------------------------

def _mini_lib():
    return {
        "version": "routelib/1.0",
        "families": {"2|1|WHEAT:5|BAKERY+FARMERS_MARKET": {
            "n_games": 2, "win_rate": 1.0, "margin_mean": 800.0,
            "best_route": 5, "segments": {}}},
        "default": {"n_games": 2, "win_rate": 1.0, "margin_mean": 800.0,
                    "best_route": 5, "segments": {}},
    }


def _lot_pkg():
    acts = [
        {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WOOL", 1]]},
        {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WOOL", 2]]},
        {"farmer": ["PASS"], "hands": [], "market": []},
    ]
    return {"actions": acts, "routes": {"0": [0, 1, 2]}, "shops": []}


def _blob_text(pkg):
    import base64
    import zlib
    blob = base64.b85encode(zlib.compress(
        json.dumps(pkg, separators=(",", ":")).encode("utf-8"))
    ).decode("ascii")
    return ("import base64, json, zlib\n"
            "# synthetic r37-like\n_R108_DATA=json.loads(zlib.decompress("
            "base64.b85decode('%s')))\n\ndef _base_agent(observation):\n"
            "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n"
            % blob)


def _patch_lib(monkeypatch, lib):
    """钉建库组件为合成迷你库（test_build_r40._patch_lib 同法）。"""
    core_sha = hashlib.sha256(
        json.dumps(lib, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")).hexdigest()

    def _fake_builder(game_dir, family_cfg=None):
        return {"library": dict(lib, build_audit={"library_sha": core_sha}),
                "build_audit": {"library_sha": core_sha, "n_games": 2,
                                "n_families": 1, "coverage": 1.0,
                                "uncovered_families": []}}

    try:
        from orderbook_r40 import route_library as _rlo
    except ImportError:
        import route_library as _rlo
    targets = [_rlo]
    _alt = sys.modules.get("route_library")
    if _alt is not None and _alt is not _rlo:
        targets.append(_alt)
    for m in targets:
        monkeypatch.setattr(m, "build_route_library", _fake_builder)


def _last_callable(text, path):
    ns = {}
    exec(compile(text, str(path), "exec"), ns)
    calls = [k for k, v in ns.items()
             if callable(v) and not k.startswith("__")]
    return calls[-1], ns


# --------------------------- 探针构建 ---------------------------

def test_probe_text_shapes_and_entries(tmp_path):
    # V0=r37 原样/尾块探针=末 callable _r40p_agent 且链只含所选件/V2=磁带手术。
    t0 = AB.build_probe_text("V0")
    assert t0 == Path(AB.R37_MAIN).read_text(encoding="utf-8")
    for variant, must, must_not in (
            ("V1", ["_route40_select(", "_R40P_LIBRARY = "],
             ["apply_race_slots(", "apply_slot_hygiene("]),
            ("V3", ["apply_race_slots("],
             ["_route40_select(", "apply_slot_hygiene("]),
            ("V4", ["apply_slot_hygiene("],
             ["_route40_select(", "apply_race_slots("])):
        text = AB.build_probe_text(variant)
        for frag in must:
            assert frag in text, (variant, frag)
        for frag in must_not:
            assert frag not in text, (variant, frag)
        name, ns = _last_callable(text, "probe_%s" % variant)
        assert name == "_r40p_agent"
        out = ns[name]({"step": 5, "player": 0, "farms": [], "market": {}})
        assert isinstance(out, dict) and "market" in out
    text2 = AB.build_probe_text("V2")
    assert "r40 消融探针" not in text2            # 纯磁带手术无尾块
    assert text2 != t0                            # 磁带已手术


def test_probe_deterministic_and_v5_snapshot(tmp_path):
    for variant in ("V1", "V2", "V3", "V4"):
        p1 = AB.build_probe(variant, str(tmp_path / "a"))
        p2 = AB.build_probe(variant, str(tmp_path / "b"))
        assert Path(p1).read_bytes() == Path(p2).read_bytes()
    paths = AB.build_all_probes(str(tmp_path / "all"))
    assert set(paths) == {"V0", "V1", "V2", "V3", "V4", "V5"}
    assert Path(paths["V5"]).read_bytes() == Path(AB.FULL_R40_MAIN).read_bytes()
    with pytest.raises(ValueError):
        AB.build_probe_text("V9")


# --------------------------- 决策规则 ---------------------------

def _face(h2h, strong, seg):
    return {"h2h_rate": h2h, "strong_rate": strong,
            "seg": {"seg_delta_median": seg}}


def test_decide_effects_rules():
    table = {
        "V0": _face(None, 0.20, -2000.0),
        "V1": _face(0.50, 0.35, -1500.0),    # 强臂显著升→keep（①）
        "V2": _face(0.60, 0.20, -1800.0),    # h2h≥0.55→keep
        "V3": _face(0.30, 0.15, -2600.0),    # 毒药→cut_or_fix
        "V4": _face(0.52, 0.18, -100.0),     # 中间→keep_annotated
        "V5": _face(0.18, 0.21, -1968.5),
    }
    out = {d["component"]: d for d in AB.decide_effects(table)}
    assert out["route_select"]["decision"] == "keep"
    assert out["sell_lots"]["decision"] == "keep"
    assert out["race_slots"]["decision"] == "cut_or_fix"
    assert out["slot_hygiene"]["decision"] == "keep_annotated"
    assert out["route_select"]["strong_delta_vs_v0"] == 0.15
    assert out["race_slots"]["seg_delta_delta_vs_v0"] == -600.0


def test_decide_effects_route_priority_fix_not_cut():
    # ①h2h 面毒药→修切换逻辑不全砍（用户裁决优先保①）。
    table = {"V0": _face(None, 0.20, 0.0),
             "V1": _face(0.20, 0.10, 0.0),
             "V2": _face(0.50, 0.20, 0.0), "V3": _face(0.50, 0.20, 0.0),
             "V4": _face(0.50, 0.20, 0.0), "V5": _face(0.18, 0.20, 0.0)}
    out = {d["component"]: d for d in AB.decide_effects(table)}
    assert out["route_select"]["decision"] == "fix"
    assert "全砍" in out["route_select"]["why"] or "修" in \
        out["route_select"]["why"]


# ------------------------- components 开关 -------------------------

def test_inject_components_subset_and_default_stable():
    main, lib = _blob_text(_lot_pkg()) + "\n", _mini_lib()
    full = IJ.inject_r40_block(main, lib)
    same = IJ.inject_r40_block(main, lib, components=None)
    assert full["block_sha"] == same["block_sha"]          # 缺省=历史形态
    assert IJ._AGENT_SRC == IJ._agent_src(IJ._BLOCK_FUNCS)  # 单一真源
    sub = IJ.inject_r40_block(main, lib,
                              components=["race_slots", "slot_hygiene"])
    payload = sub["main_text"][len(main):]
    assert "apply_race_slots(" in payload and "apply_slot_hygiene(" in payload
    assert "def _route40_select(" not in payload
    assert "def _route40_agent(" in payload
    assert sub["block_sha"] != full["block_sha"]
    name, ns = _last_callable(sub["main_text"], "sub")
    assert name == "_route40_agent"
    out = ns[name]({"step": 5, "player": 0, "farms": [], "market": {}})
    assert isinstance(out, dict)
    with pytest.raises(ValueError):
        IJ.inject_r40_block(main, lib, components=[])
    with pytest.raises(ValueError):
        IJ.inject_r40_block(main, lib, components=["nope"])


def test_build_r40_components_switch(tmp_path, monkeypatch):
    # sell_lots 关=磁带零改动+空登记注释行；审计/pack/自检照过；子集块生效。
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_lot_pkg()), encoding="utf-8", newline="\n")
    out = tmp_path / "out"
    res = B.build_r40(str(src), out_dir=str(out),
                      components=["route_select", "slot_hygiene"])
    raw = (out / "main.py").read_bytes()
    att = res["diff_attribution"]
    assert att["ok"] is True and att["unattributed"] == []
    # ②关：磁带零差异+空登记注释行照落（present=注释差异在场，rows=0）
    assert att["whitelist"]["sell_lots"]["present"] is True
    assert att["whitelist"]["sell_lots"]["rows"] == 0
    assert res["sell_lots_change_sha256"] == hashlib.sha256(
        b"[]").hexdigest()
    text = raw.decode("utf-8")
    assert "def _route40_select(" in text and "def apply_slot_hygiene(" in text
    assert "def apply_race_slots(" not in text
    marks = [ln for ln in text.splitlines()
             if ln.startswith(B._LOT_MARKER)]
    assert len(marks) == 1 and json.loads(marks[0][len(B._LOT_MARKER):]) == []
    m = res["manifest"]
    assert m["complete"] is True
    assert m["runtime_block"]["sha256"] == res["block_sha"]


def test_build_r40_components_invalid_raises(tmp_path, monkeypatch):
    _patch_lib(monkeypatch, _mini_lib())
    src = tmp_path / "r37_main.py"
    src.write_text(_blob_text(_lot_pkg()), encoding="utf-8", newline="\n")
    with pytest.raises(ValueError):
        B.build_r40(str(src), out_dir=str(tmp_path / "o1"),
                    components=["nope"])
    with pytest.raises(ValueError):
        B.build_r40(str(src), out_dir=str(tmp_path / "o2"),
                    components=["sell_lots"])        # 纯磁带件形态拦截
    with pytest.raises(ValueError):
        B.build_r40(str(src), out_dir=str(tmp_path / "o3"), components=[])
    assert not (tmp_path / "o1" / "main.py").exists()
    assert not (tmp_path / "o2" / "main.py").exists()


# --------------------------- 效应表形态 ---------------------------

def test_effect_table_shape():
    faces = {v: _face(0.5, 0.2, 0.0) for v in ("V0", "V1", "V2", "V3", "V4",
                                               "V5")}
    eff = AB.build_effect_table(faces)
    assert set(eff["table"]) == set(faces)
    assert {d["component"] for d in eff["disposition"]} == set(AB.COMPONENTS)
    assert set(eff["decision_rules"]) == {"keep", "poison", "middle",
                                          "route_priority"}
