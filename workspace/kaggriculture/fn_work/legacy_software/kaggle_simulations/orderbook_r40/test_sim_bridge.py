# -*- coding: utf-8 -*-
"""R23 测试面：sim_bridge（加载/对照一致性/降级/真跑）。

①加载失败降级（monkeypatch 安装缺失→loaded=False 语义）②对照口径（mock
双引擎 30 局 30 匹配→consistency_ok / 29 匹配→False）③降级留档（对照不过→
降级回官方引擎+留档文件追加，run_games 回退留档）④真跑（仿真器真装上则
≥30 局对照+speedup 记 evidence/sim_bridge_realrun.json；装不上则 evidence
记 degraded 与官方引擎耗时基线）。
"""
import json
from pathlib import Path

import pytest  # noqa: F401

try:
    from orderbook_r40 import sim_bridge as sb
except ImportError:  # pragma: no cover - 平铺装载
    import sim_bridge as sb  # type: ignore

SEEDS30 = [1000 + i for i in range(30)]


def _fake_handle():
    return {"kaggsim_path": "<fake>", "kagg_bin": "/bin/true",
            "version": "fake/0", "tools_dir": "<fake>"}


def _rows(seeds, banks):
    return [{"seed": int(s), "banks": [float(x) for x in b], "error": None,
             "elapsed_s": 0.01} for s, b in zip(seeds, banks)]


# ① 加载失败降级 -----------------------------------------------------------

def test_load_failure_degrades(monkeypatch, tmp_path):
    """装不上（缺件）→ loaded=False+原因留档+wall_speedup=1.0，不抛。"""
    def _boom(config):
        raise FileNotFoundError("kagg binary not found (install missing)")
    monkeypatch.setattr(sb, "_load_simulator", _boom)
    rec = tmp_path / "degraded.json"
    res = sb.sim_bridge(config={"record_path": str(rec)}, corpus=SEEDS30)
    assert res["loaded"] is False
    assert res["degraded"] is True
    assert res["consistency_ok"] is False
    assert res["wall_speedup"] == 1.0                      # 官方引擎口径
    assert res["consistency"] == {"n_checked": 0, "n_match": 0, "rate": None}
    assert res["engine"] == "official"
    assert "kagg" in res["degraded_reason"]
    saved = json.loads(rec.read_text(encoding="utf-8"))
    assert saved["records"] and "kagg" in saved["records"][-1]["reason"]


# ② 对照口径（mock 双引擎）--------------------------------------------------

def test_consistency_ok_30_of_30(monkeypatch):
    """30 局 30 匹配→consistency_ok=True，wall_speedup=官方/仿真实测比值。"""
    monkeypatch.setattr(sb, "_load_simulator", lambda config: _fake_handle())
    banks = [[1000.0 + i, 2000.0 + i] for i in range(30)]
    monkeypatch.setattr(
        sb, "_run_official_batch",
        lambda games, config: (_rows([g["seed"] for g in games], banks), 3.0))
    monkeypatch.setattr(
        sb, "_run_sim_batch",
        lambda games, handle, config: (
            _rows([g["seed"] for g in games], banks), 1.5))
    res = sb.sim_bridge(config={"n_games": 30}, corpus=SEEDS30)
    assert res["loaded"] is True
    assert res["consistency"] == {"n_checked": 30, "n_match": 30, "rate": 1.0}
    assert res["consistency_ok"] is True
    assert res["degraded"] is False
    assert res["engine"] == "sim"
    assert res["wall_speedup"] == pytest.approx(2.0)       # 3.0 / 1.5
    assert res["record_path"] is None                      # 过对照不留档


def test_consistency_29_of_30_fails(monkeypatch, tmp_path):
    """30 局 29 匹配→consistency_ok=False 降级，实测比值留档 timing。"""
    monkeypatch.setattr(sb, "_load_simulator", lambda config: _fake_handle())
    banks = [[1000.0 + i, 2000.0 + i] for i in range(30)]
    sim_banks = [list(b) for b in banks]
    sim_banks[-1] = [1001.0, 2000.0]                       # 一局终局资金不一致
    monkeypatch.setattr(
        sb, "_run_official_batch",
        lambda games, config: (_rows([g["seed"] for g in games], banks), 3.0))
    monkeypatch.setattr(
        sb, "_run_sim_batch",
        lambda games, handle, config: (
            _rows([g["seed"] for g in games], sim_banks), 1.5))
    res = sb.sim_bridge(config={"n_games": 30,
                                "record_path": str(tmp_path / "deg.json")},
                        corpus=SEEDS30)
    assert res["consistency"]["n_checked"] == 30
    assert res["consistency"]["n_match"] == 29
    assert res["consistency"]["rate"] == pytest.approx(29 / 30)
    assert res["consistency_ok"] is False
    assert res["degraded"] is True
    assert res["engine"] == "official"                     # 降级回官方引擎
    assert res["wall_speedup"] == 1.0                      # 降级=官方口径
    assert res["timing"]["measured_speedup"] == pytest.approx(2.0)
    assert "29/30" in res["degraded_reason"]


# ③ 降级留档 + run_games 回退留档 -------------------------------------------

def test_degrade_record_and_run_games_fallback(monkeypatch, tmp_path):
    """对照不过→降级留档文件追加；run_games 未认证→回退官方引擎并留档。"""
    rec = tmp_path / "deg.json"
    monkeypatch.setattr(sb, "_load_simulator", lambda config: _fake_handle())
    banks = [[1000.0 + i, 2000.0 + i] for i in range(30)]
    sim_banks = [list(b) for b in banks]
    sim_banks[7] = [0.0, 0.0]
    monkeypatch.setattr(
        sb, "_run_official_batch",
        lambda games, config: (_rows([g["seed"] for g in games], banks), 3.0))
    monkeypatch.setattr(
        sb, "_run_sim_batch",
        lambda games, handle, config: (
            _rows([g["seed"] for g in games], sim_banks), 1.5))
    res = sb.sim_bridge(config={"n_games": 30, "record_path": str(rec)},
                        corpus=SEEDS30)
    assert res["degraded"] is True and res["engine"] == "official"
    saved = json.loads(rec.read_text(encoding="utf-8"))
    assert len(saved["records"]) == 1
    assert "对照未过" in saved["records"][0]["reason"]
    assert saved["records"][0]["consistency"]["n_match"] == 29

    off_rows = _rows([7], [[9.0, 8.0]])
    monkeypatch.setattr(sb, "_run_official_batch",
                        lambda games, config: (off_rows, 0.5))
    out = sb.run_games([{"seed": 7}],
                       config={"bridge": res, "record_path": str(rec)})
    assert out["engine"] == "official"
    assert out["fallback_reason"] and "对照" in out["fallback_reason"]
    assert out["games"] == off_rows
    assert out["degraded"] is True
    saved = json.loads(rec.read_text(encoding="utf-8"))
    assert len(saved["records"]) == 2
    assert saved["records"][-1]["kind"] == "run_games_fallback"


def test_run_games_sim_path_and_fail_safe(monkeypatch, tmp_path):
    """已认证走仿真器；仿真器运行异常→回退官方引擎（fail-safe 不抛）。"""
    bridge = {"loaded": True, "consistency_ok": True}
    sim_rows = _rows([1, 2], [[1.0, 2.0], [3.0, 4.0]])
    monkeypatch.setattr(sb, "_load_simulator", lambda config: _fake_handle())
    monkeypatch.setattr(sb, "_run_sim_batch",
                        lambda games, handle, config: (sim_rows, 0.2))
    out = sb.run_games([1, 2], config={
        "bridge": bridge, "sim_handle": _fake_handle(),
        "record_path": str(tmp_path / "ok.json")})
    assert out["engine"] == "sim"
    assert out["fallback_reason"] is None
    assert out["degraded"] is False
    assert out["games"] == sim_rows

    def _boom(games, handle, config):
        raise RuntimeError("kagg serve crashed")
    monkeypatch.setattr(sb, "_run_sim_batch", _boom)
    off_rows = _rows([1, 2], [[1.0, 2.0], [3.0, 4.0]])
    monkeypatch.setattr(sb, "_run_official_batch",
                        lambda games, config: (off_rows, 1.0))
    rec = tmp_path / "fb.json"
    out2 = sb.run_games([1, 2], config={
        "bridge": bridge, "sim_handle": _fake_handle(),
        "record_path": str(rec)})
    assert out2["engine"] == "official"
    assert "kagg serve crashed" in out2["fallback_reason"]
    assert out2["degraded"] is True
    assert out2["games"] == off_rows
    saved = json.loads(rec.read_text(encoding="utf-8"))
    assert saved["records"][-1]["kind"] == "run_games_fallback"


# ④ 真跑（加载+对照+提速 → evidence/sim_bridge_realrun.json）----------------

def test_realrun_dual_engine_evidence():
    """仿真器真装上→≥30 局对照+speedup 落 evidence；装不上→记 degraded 与
    官方引擎耗时基线。"""
    corpus = None
    for cand in ("/tmp/kagr23", "/tmp/kagr22"):
        if Path(cand).is_dir():
            corpus = cand
            break
    if corpus is None:
        pytest.skip("对照语料缺失（/tmp/kagr23、/tmp/kagr22）")
    ev_path = Path(__file__).resolve().parent / "evidence" / \
        "sim_bridge_realrun.json"
    res = sb.sim_bridge(config={"n_games": 30}, corpus=corpus)
    ev = {"corpus": corpus, "result": res, "install": res.get("install"),
          "record_version": sb.RECORD_VERSION}
    if res["loaded"]:
        assert res["consistency"]["n_checked"] >= 30       # 抽样 ≥30 局
        if res["consistency_ok"]:
            assert res["consistency"]["rate"] == 1.0
            assert res["wall_speedup"] > 1.0               # 提速读数为正
            assert res["degraded"] is False
            ev["verdict"] = "certified"
        else:
            assert res["degraded"] is True
            assert res["wall_speedup"] == 1.0
            ev["verdict"] = "degraded_inconsistent"
    else:
        assert res["degraded"] is True

        def _idle(obs, configuration=None):
            return {"farmer": ["PASS"]}
        games = [{"seed": 900000 + i, "agents": [_idle, _idle]}
                 for i in range(3)]
        rows, elapsed = sb._run_official_batch(games, {})
        ev["verdict"] = "degraded_install"
        ev["degraded"] = {"reason": res.get("degraded_reason")}
        ev["official_baseline"] = {
            "n_games": len(rows), "elapsed_s": round(elapsed, 3),
            "sec_per_game": round(elapsed / max(len(rows), 1), 3),
            "rows": rows,
        }
        assert rows and all(r.get("banks") for r in rows)  # 官方引擎可跑
    ev_path.parent.mkdir(parents=True, exist_ok=True)
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=1),
                       encoding="utf-8")
    assert ev_path.exists()
    saved = json.loads(ev_path.read_text(encoding="utf-8"))
    assert saved["result"]["loaded"] == res["loaded"]
    assert saved["verdict"] == ev["verdict"]
