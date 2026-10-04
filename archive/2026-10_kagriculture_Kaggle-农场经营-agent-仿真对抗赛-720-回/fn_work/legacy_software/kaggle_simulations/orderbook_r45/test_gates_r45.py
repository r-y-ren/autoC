# -*- coding: utf-8 -*-
"""R28 测试面：verify_r45_gates（五门 fail-closed：装载/双席 DONE+<1s/
确定性双跑/体积身份链/h2h 主对 r40≥0.55 独立 n；全跑不短路）。"""
from __future__ import annotations

import json

from orderbook_r45 import build_r45 as b45
from orderbook_r45 import gates_r45 as g45

# ---- 构建夹具（三件套真构建→真包） ---------------------------------------
BASE_SRC = '''# fixture r40 base main
MONEY = 3000

def _host_agent(observation, configuration=None):
    return {"farmer": ["PASS"], "hands": [], "market": []}
'''
LEDGER_SRC = ("def _ledger_entry(item, qty, due_step, advance_step):\n"
              "    return {'item': item, 'qty': qty, 'due_step': due_step,\n"
              "            'advance_step': advance_step}\n")
GATE_SRC = ("def _valley_gate_ok(quote, base):\n"
            "    return quote >= base\n")
ADV_SRC = ("def _advance_agent(observation, configuration=None):\n"
           "    try:\n"
           "        return _ADV_HOST_AGENT(observation)\n"
           "    except Exception:\n"
           "        return {'farmer': ['PASS'], 'hands': [], 'market': []}\n")
MODS = {"debt_ledger": LEDGER_SRC, "valley_gate": GATE_SRC,
        "advance_layer": ADV_SRC}


def build_pkg(tmp_path, name="pkg"):
    base = tmp_path / "base_main.py"
    base.write_text(BASE_SRC, encoding="utf-8")
    return b45.build_r45(str(base), {"modules": dict(MODS)},
                         str(tmp_path / name))


# ---- 假局组夹具（smoke 双席自打 + h2h 局组） ------------------------------
def make_gate_runner(smoke_ok=True, det_stable=True, h2h_margin=100.0,
                     raise_arm=None):
    calls = {"n": 0}

    def runner(specs, cfg):
        calls["n"] += 1
        run_idx = calls["n"]
        rows = []
        for s in specs:
            arm = s.get("arm")
            if arm == raise_arm:
                raise RuntimeError("gate runner boom: %s" % arm)
            sha = "sha-%s" % s["game_id"]
            if not det_stable:
                sha = "%s-run%d" % (sha, run_idx)
            row = {"game_id": s["game_id"], "seed": s["seed"], "arm": arm,
                   "our_seat": s.get("our_seat", 0), "error": None,
                   "statuses": ["DONE", "DONE"] if smoke_ok
                   else ["DONE", "ERROR"],
                   "max_step_s": 0.2 if smoke_ok else 1.5,
                   "actions_sha256": sha,
                   "margin": float(h2h_margin)}
            rows.append(row)
        return rows

    return runner


def test_verify_r45_gates(tmp_path):
    """五门全绿：overall passed；各门在场；evidence 落盘。"""
    pkg = build_pkg(tmp_path)
    out = g45.verify_r45_gates({**pkg, "runner": make_gate_runner()})
    gates = out["gates"]
    assert set(gates) == {"load", "seats_done", "determinism", "identity",
                          "h2h_vs_r40"}
    assert out["overall"]["passed"] is True
    assert out["overall"]["failed_gates"] == []
    assert gates["load"]["entry"] == g45.ENTRY_NAME
    assert gates["seats_done"]["passed"] is True
    assert gates["determinism"]["passed"] is True
    assert gates["identity"]["passed"] is True
    assert gates["h2h_vs_r40"]["passed"] is True
    assert gates["h2h_vs_r40"]["win_rate"] == 1.0
    assert gates["h2h_vs_r40"]["n_independent"] == g45.N_H2H_GATE  # 独立 n
    assert (tmp_path / "evidence" / g45.EVIDENCE_NAME).exists()


def test_verify_r45_gates_load_red_fail_closed(tmp_path):
    """装载门红（末 callable 非 _advance_agent）→fail-closed，整体红。"""
    bad = tmp_path / "bad_pkg"
    bad.mkdir()
    (bad / "main.py").write_text(
        BASE_SRC + "\ndef _bogus_agent(obs):\n    return None\n",
        encoding="utf-8")
    out = g45.verify_r45_gates({"dir": str(bad),
                                "runner": make_gate_runner()})
    assert out["gates"]["load"]["passed"] is False
    assert "load" in out["overall"]["failed_gates"]
    assert out["overall"]["passed"] is False


def test_verify_r45_gates_seats_done_red(tmp_path):
    """双席 DONE+<1s 红：非 DONE/单步超预算任一即红。"""
    pkg = build_pkg(tmp_path)
    out = g45.verify_r45_gates({**pkg,
                                "runner": make_gate_runner(smoke_ok=False)})
    assert out["gates"]["seats_done"]["passed"] is False
    assert out["gates"]["determinism"]["passed"] is True   # 全跑不短路
    assert out["overall"]["passed"] is False


def test_verify_r45_gates_determinism_red(tmp_path):
    """确定性双跑红：动作流 sha 不一致。"""
    pkg = build_pkg(tmp_path)
    out = g45.verify_r45_gates(
        {**pkg, "runner": make_gate_runner(det_stable=False)})
    assert out["gates"]["determinism"]["passed"] is False
    assert out["overall"]["passed"] is False


def test_verify_r45_gates_identity_red(tmp_path):
    """体积身份链红：manifest 篡改（sha 不符）→fail-closed。"""
    pkg = build_pkg(tmp_path)
    man_path = tmp_path / "pkg" / "build_manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    man["main_sha256"] = "00" * 32
    man_path.write_text(json.dumps(man), encoding="utf-8")
    out = g45.verify_r45_gates({**pkg, "runner": make_gate_runner()})
    assert out["gates"]["identity"]["passed"] is False
    assert out["gates"]["identity"]["checks"]["main_sha"] is False
    assert out["overall"]["passed"] is False


def test_verify_r45_gates_h2h_red(tmp_path):
    """h2h 主对 r40 门红（<0.55）→整体红；五门全跑不短路。"""
    pkg = build_pkg(tmp_path)
    out = g45.verify_r45_gates({**pkg,
                                "runner": make_gate_runner(h2h_margin=-5.0)})
    gates = out["gates"]
    assert set(gates) == {"load", "seats_done", "determinism", "identity",
                          "h2h_vs_r40"}
    assert gates["h2h_vs_r40"]["passed"] is False
    assert gates["h2h_vs_r40"]["win_rate"] == 0.0
    assert gates["load"]["passed"] is True
    assert gates["identity"]["passed"] is True
    assert "h2h_vs_r40" in out["overall"]["failed_gates"]


def test_verify_r45_gates_runner_error_fail_closed(tmp_path):
    """局组不可跑→门红（fail-closed 传递），不抛。"""
    pkg = build_pkg(tmp_path)
    out = g45.verify_r45_gates(
        {**pkg, "runner": make_gate_runner(raise_arm="smoke_selfplay")})
    assert out["gates"]["seats_done"]["passed"] is False
    assert out["gates"]["determinism"]["passed"] is False
    assert out["overall"]["passed"] is False
