# -*- coding: utf-8 -*-
"""R28 测试面：构建线（判据=R28 ①构造用例原文：三件缺一即构建失败/白名单外
即抛/审计=advance 栈注入块/manifest k·视界·窗口定桩）。"""
from __future__ import annotations

import json

import pytest

from orderbook_r45 import build_r45 as b45

# ---- 三件套夹具（B47 逻辑键：账本/谷底闸门/提前层；提前层自含 _advance_agent）
BASE_SRC = '''# fixture r40 base main
MONEY = 3000

def _host_plan(obs):
    return obs

def _host_agent(observation, configuration=None):
    return {"farmer": ["PASS"], "hands": [], "market": []}
'''
LEDGER_SRC = '''def _ledger_entry(item, qty, due_step, advance_step):
    """账本条目（r36_debts 口径）。"""
    return {"item": item, "qty": qty, "due_step": due_step,
            "advance_step": advance_step}
'''
GATE_SRC = '''def _valley_gate_ok(quote, base):
    """谷底闸门（quote>=base 才提前）。"""
    return quote >= base
'''
ADV_SRC = '''def _advance_body(observation, configuration=None):
    return None


def _advance_agent(observation, configuration=None):
    """运行时包装（fail-safe）。"""
    try:
        return _ADV_HOST_AGENT(observation)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
'''
MODS = {"debt_ledger": LEDGER_SRC, "valley_gate": GATE_SRC,
        "advance_layer": ADV_SRC}


def _base_file(tmp_path, src=BASE_SRC):
    p = tmp_path / "base_main.py"
    p.write_text(src, encoding="utf-8")
    return p


def test_append_advance_stack_block():
    """注入形态：块首捕获宿主末 callable、末函数=_advance_agent、纯尾部追加。"""
    out = b45.append_advance_stack_block(BASE_SRC, dict(MODS))
    assert out.startswith(BASE_SRC)                 # 基座全文逐字节前缀
    assert b45.ADVANCE_SENTINEL in out              # 块首 sentinel
    assert "_ADV_HOST_AGENT = " in out              # 块首捕获宿主末 callable
    for key in b45.THREE_PIECES:
        assert MODS[key].rstrip("\n") in out        # 三件齐注
    ns = {}
    exec(compile(out, "<x>", "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    assert loaded[-1].__name__ == "_advance_agent"  # 末函数=_advance_agent
    assert callable(ns["_ADV_HOST_AGENT"])
    assert ns["_ADV_HOST_AGENT"].__name__ == "_host_agent"


def test_append_advance_stack_block_missing_piece_raises():
    """三件缺一即抛（宁可构建失败）。"""
    for key in b45.THREE_PIECES:
        bad = dict(MODS)
        del bad[key]
        with pytest.raises(ValueError):
            b45.append_advance_stack_block(BASE_SRC, bad)
        bad2 = dict(MODS)
        bad2[key] = "   "
        with pytest.raises(ValueError):
            b45.append_advance_stack_block(BASE_SRC, bad2)
    with pytest.raises(ValueError):
        b45.append_advance_stack_block(BASE_SRC, None)


def test_append_advance_stack_block_rejects_double_inject():
    out = b45.append_advance_stack_block(BASE_SRC, dict(MODS))
    with pytest.raises(ValueError):
        b45.append_advance_stack_block(out, dict(MODS))


def test_append_entry_invariant_unordered_piece():
    """提前层内定义序不作要求：块尾入口归一仍保末函数=_advance_agent。"""
    adv_unordered = ("def _advance_agent(observation, configuration=None):\n"
                     "    return _ADV_HOST_AGENT(observation)\n\n\n"
                     "def _measure_rival_lead(window):\n"
                     "    return 40\n")
    out = b45.append_advance_stack_block(
        BASE_SRC, {"debt_ledger": LEDGER_SRC, "valley_gate": GATE_SRC,
                   "advance_layer": adv_unordered})
    ns = {}
    exec(compile(out, "<x>", "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    assert loaded[-1].__name__ == "_advance_agent"


def test_build_r45(tmp_path):
    """构建编排：r45 main+submission.tar.gz+manifest（k/视界/窗口定桩）+sha 链。"""
    base = _base_file(tmp_path)
    out_dir = tmp_path / "pkg"
    res = b45.build_r45(str(base), {"modules": dict(MODS), "k": 3,
                                    "horizon": 44,
                                    "window": [192, 695]}, str(out_dir))
    assert res["main_path"].endswith("main.py")
    assert res["tar_path"].endswith("submission.tar.gz")
    man = json.loads((out_dir / "build_manifest.json").read_text(
        encoding="utf-8"))
    assert man["description"] == \
        "public derivative with debt-ledgered advance selling"
    # 参数定桩登记（k/视界/窗口）
    assert man["params_pinned"]["k"] == 3
    assert man["params_pinned"]["horizon"] == 44
    assert man["params_pinned"]["window"] == [192, 695]
    # sha 链（…→r40→r45）+自证
    chain = man["base_sha_chain"]
    assert all(k in chain for k in b45.CHAIN_ANCHORS)
    assert chain["r45"] == res["main_sha256"] == man["main_sha256"]
    assert man["tar_sha256"] == res["tar_sha256"]
    assert man["tar_members"] == ["main.py"]
    assert man["complete"] is True
    assert man["double_run_sha256"]["run1"] == man["double_run_sha256"]["run2"]
    # diff 审计：白名单=advance 栈注入块；磁带五区零改动
    audit = res["audit"]
    assert audit["whitelist"] == ["advance_stack_block"]
    assert audit["prefix_identical"] is True
    assert set(audit["zones_zero_change"]) == {"tape", "routing", "anti_clone",
                                               "slot_reorder", "terminal"}
    # 三件 sha 登记
    assert set(man["three_pieces"]) == set(b45.THREE_PIECES)
    # 主源=基座+注入块（装载入口）
    main_src = (out_dir / "main.py").read_text(encoding="utf-8")
    assert main_src.startswith(BASE_SRC)
    assert b45.ENTRY_NAME in main_src


def test_build_r45_deterministic_pack(tmp_path):
    base = _base_file(tmp_path)
    r1 = b45.build_r45(str(base), {"modules": dict(MODS)}, str(tmp_path / "a"))
    r2 = b45.build_r45(str(base), {"modules": dict(MODS)}, str(tmp_path / "b"))
    assert r1["tar_sha256"] == r2["tar_sha256"]     # 确定性打包（跨目录双跑）
    assert r1["main_sha256"] == r2["main_sha256"]


def test_build_r45_three_pieces_missing_raises(tmp_path):
    """三件缺一即抛（build 入口）。"""
    base = _base_file(tmp_path)
    with pytest.raises(ValueError):
        b45.build_r45(str(base), {}, str(tmp_path / "pkg"))
    with pytest.raises(ValueError):
        b45.build_r45(str(base), {"modules": {"debt_ledger": LEDGER_SRC}},
                      str(tmp_path / "pkg2"))
    with pytest.raises(FileNotFoundError):
        b45.build_r45(str(tmp_path / "none.py"), {"modules": dict(MODS)},
                      str(tmp_path / "pkg3"))


def test_build_r45_audit_whitelist_violation_raises(tmp_path, monkeypatch):
    """审计白名单外即抛（不产出）。"""
    base = _base_file(tmp_path)

    def tampered(main_src, modules):
        return main_src.replace("MONEY", "MONEE") + "\n\n" + "def x():\n    1\n"

    monkeypatch.setattr(b45, "append_advance_stack_block", tampered)
    out_dir = tmp_path / "pkg"
    with pytest.raises(RuntimeError):
        b45.build_r45(str(base), {"modules": dict(MODS)}, str(out_dir))
    assert not (out_dir / "build_manifest.json").exists()   # 不产出
    assert not (out_dir / "main.py").exists()


def test_build_r45_module_path_values(tmp_path):
    """modules 值收 .py 路径（B47 实况拼接）→同源构建。"""
    base = _base_file(tmp_path)
    adv = tmp_path / "advance_layer.py"
    adv.write_text(ADV_SRC, encoding="utf-8")
    mods = {"debt_ledger": LEDGER_SRC, "valley_gate": GATE_SRC,
            "advance_layer": str(adv)}
    res = b45.build_r45(str(base), {"modules": mods}, str(tmp_path / "pkg"))
    assert res["manifest"]["three_pieces"]["advance_layer"]["sha256"]
