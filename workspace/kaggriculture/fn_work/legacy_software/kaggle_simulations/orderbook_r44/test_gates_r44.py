# -*- coding: utf-8 -*-
"""R27 测试面：verify_r44_gates 五门各自红绿分支（假包/夹具，不跑真局）。
判据=R27 原文：装载 last-callable/双席 DONE+<1s/确定性双跑逐字节/
体积<100MB+sha 身份链/h2h 主对 r40 ≥0.55 独立 n。"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile

import pytest

from orderbook_r44 import gates_r44 as g44


def _mk_pkg(tmp_path, name="pkg", form="A", entry=None, chain_key=None):
    """假包：main.py+确定性 tar+build_manifest（四门单实现同打包口径）。"""
    pkg = tmp_path / name
    pkg.mkdir(parents=True, exist_ok=True)
    entry = entry or g44.ENTRY_BY_FORM[form]
    main_src = ("def %s(observation, configuration=None):\n"
                "    return {'farmer': ['PASS'], 'hands': [], 'market': []}\n"
                % entry)
    main_bytes = main_src.encode("utf-8")
    (pkg / "main.py").write_bytes(main_bytes)
    buf = io.BytesIO()
    gz = gzip.GzipFile(filename="", mode="wb", fileobj=buf, mtime=0)
    with tarfile.open(fileobj=gz, mode="w") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main_bytes)
        info.mode = 0o644
        info.mtime = 0
        info.uid = 0
        info.gid = 0
        tar.addfile(info, io.BytesIO(main_bytes))
    gz.close()
    tar_bytes = buf.getvalue()
    (pkg / "submission.tar.gz").write_bytes(tar_bytes)
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    chain = {"a16e0e9b": "anchor", "r34a": "anchor", "r40": "anchor",
             chain_key or ("r44_" + form.lower()): main_sha}
    man = {"form": form, "main_sha256": main_sha,
           "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
           "base_sha_chain": chain}
    (pkg / "build_manifest.json").write_text(json.dumps(man),
                                             encoding="utf-8")
    return pkg


def _ep(seed, statuses=("DONE", "DONE"), max_ms=120.0,
        rewards=(1000.0, 900.0), h="aa"):
    return {"seed": seed, "statuses": list(statuses),
            "rewards": list(rewards), "max_step_ms": max_ms,
            "action_stream_sha256": h}


def _h2h_play(margin_fn):
    def _play(specs, cfg):
        return [{"game_id": s["game_id"], "seed": s["seed"],
                 "seat": s["our_seat"],
                 "margin": margin_fn(s["seed"], s["our_seat"]),
                 "error": None} for s in specs]
    return _play


# ------------------------------------------------------------ 门①装载 --
def test_gate_load_green_red(tmp_path):
    pkg = _mk_pkg(tmp_path, name="ok", form="A")
    assert g44._gate_load(str(pkg)) == {"passed": True, "form": "A",
                                        "entry": "_dayhigh_agent"}
    bad = _mk_pkg(tmp_path, name="bad", form="A",
                  entry="_glutgate_agent")          # 入口名与形态不符
    with pytest.raises(g44.GateR44Error):
        g44._gate_load(str(bad))
    nomani = tmp_path / "nomani"
    nomani.mkdir()
    (nomani / "main.py").write_text("def _dayhigh_agent(o, c=None):\n"
                                    "    return {}\n", encoding="utf-8")
    with pytest.raises(g44.GateR44Error):           # manifest.form 缺失
        g44._gate_load(str(nomani))


# --------------------------------------------------- 门②双席 DONE+<1s --
def test_gate_health_green_red(monkeypatch, tmp_path):
    pkg = _mk_pkg(tmp_path)
    monkeypatch.setattr(g44, "_run_episode",
                        lambda pkg_dir, seed: _ep(seed))
    assert g44._gate_health(str(pkg))["passed"] is True
    monkeypatch.setattr(g44, "_run_episode",
                        lambda pkg_dir, seed: _ep(seed, max_ms=1500.0))
    with pytest.raises(g44.GateR44Error):           # 单步超 1s 预算
        g44._gate_health(str(pkg))
    monkeypatch.setattr(
        g44, "_run_episode",
        lambda pkg_dir, seed: _ep(seed, statuses=("DONE", "TIMEOUT")))
    with pytest.raises(g44.GateR44Error):           # 双席未全 DONE
        g44._gate_health(str(pkg))


# ------------------------------------------------------ 门③确定性双跑 --
def test_gate_determinism_green_red(monkeypatch, tmp_path):
    pkg = _mk_pkg(tmp_path)
    monkeypatch.setattr(g44, "_run_episode",
                        lambda pkg_dir, seed: _ep(seed, h="same"))
    assert g44._gate_determinism(str(pkg))["hashes"]["run1"] == "same"

    n = {"runs": 0}

    def _drift(pkg_dir, seed):
        n["runs"] += 1
        return _ep(seed, h="run%d" % n["runs"])

    monkeypatch.setattr(g44, "_run_episode", _drift)
    with pytest.raises(g44.GateR44Error):           # 双跑逐字节不一致
        g44._gate_determinism(str(pkg))


# ------------------------------------------------ 门④体积+sha 身份链 --
def test_gate_identity_green_red(monkeypatch, tmp_path):
    pkg = _mk_pkg(tmp_path, form="AB")
    res = g44._gate_identity(str(pkg))
    assert res["passed"] is True and "r44_ab" in res["chain"]

    tampered = _mk_pkg(tmp_path, name="tampered", form="A")
    man = json.loads((tampered / "build_manifest.json").read_text(
        encoding="utf-8"))
    man["main_sha256"] = "00" * 32
    (tampered / "build_manifest.json").write_text(json.dumps(man),
                                                  encoding="utf-8")
    with pytest.raises(g44.GateR44Error):           # sha 身份链不符
        g44._gate_identity(str(tampered))

    broken_chain = _mk_pkg(tmp_path, name="chain", form="B",
                           chain_key="r44_a")       # 链锚挂错形态
    with pytest.raises(g44.GateR44Error):
        g44._gate_identity(str(broken_chain))

    monkeypatch.setattr(g44, "SIZE_CAP_BYTES", 10)  # 体积门红（假包>10B）
    with pytest.raises(g44.GateR44Error):
        g44._gate_identity(str(pkg))


# --------------------------------------------- 门⑤h2h 主对 r40 独立 n --
def test_gate_h2h_green_red(monkeypatch, tmp_path):
    pkg = _mk_pkg(tmp_path)
    monkeypatch.setattr("orderbook_r43.judge_r26._play",
                        _h2h_play(lambda seed, seat: 1000.0))
    res = g44._gate_h2h(str(pkg))
    assert res["passed"] is True and res["h2h_rate"] == 1.0
    assert res["n_independent"] == g44.N_H2H_GATE   # 席位翻转不双计

    monkeypatch.setattr("orderbook_r43.judge_r26._play",
                        _h2h_play(lambda seed, seat: -1000.0))
    with pytest.raises(g44.GateR44Error):
        g44._gate_h2h(str(pkg))

    monkeypatch.setattr("orderbook_r43.judge_r26._play",
                        _h2h_play(lambda seed, seat: None))  # 红局计入
    with pytest.raises(g44.GateR44Error):
        g44._gate_h2h(str(pkg))


# ------------------------------------------------------------ 汇总/fail-closed --
def test_verify_runs_all_gates_fail_closed(monkeypatch, tmp_path):
    pkg = _mk_pkg(tmp_path, name="good", form="A")
    monkeypatch.setattr(g44, "_run_episode",
                        lambda pkg_dir, seed: _ep(seed))
    monkeypatch.setattr("orderbook_r43.judge_r26._play",
                        _h2h_play(lambda seed, seat: 1000.0))
    out = g44.verify_r44_gates(str(pkg))
    assert set(out["gates"]) == {"load", "health", "determinism",
                                 "identity", "h2h"}
    assert out["overall"]["passed"] is True
    assert (pkg / "evidence" / "gates_r44_realrun.json").is_file()

    bad = _mk_pkg(tmp_path, name="bad", form="A", entry="_wrong_agent")
    out = g44.verify_r44_gates(str(bad))            # 全跑不短路
    assert out["overall"]["passed"] is False
    assert out["overall"]["failed_gates"] == ["load"]
    assert out["gates"]["health"]["passed"] is True
    assert out["gates"]["identity"]["passed"] is True


def test_verify_broken_package_fail_closed(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    out = g44.verify_r44_gates(str(empty))          # 不抛逃逸，整体必红
    assert out["overall"]["passed"] is False
    assert len(out["overall"]["failed_gates"]) == 5
