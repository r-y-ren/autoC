# -*- coding: utf-8 -*-
"""R16 单测：build_adopt（fetch 解码/merge 三增量+layer S 移除/constants 恰三处/
audit 白名单归因/确定性打包）。真跑面用真件+tmp 出口（不触真产物目录）。"""
import base64
import gzip
import json
import os
import tarfile

import pytest

from orderbook_2965_adopt import build_adopt as B


# ---------------------------------------------------------------------------
# fetch 组
# ---------------------------------------------------------------------------
def _synth_notebook(tmp_path, text: str):
    payload = base64.b64encode(gzip.compress(text.encode("utf-8"),
                                             mtime=0)).decode("ascii")
    nb = {"cells": [{"cell_type": "code",
                     "source": ["import base64, gzip\n",
                                "AGENT_B64 = \"\"\"", payload, "\"\"\"\n",
                                "print('ok')"]}]}
    p = tmp_path / "kernel.ipynb"
    p.write_text(json.dumps(nb), encoding="utf-8")
    return str(p)


def test_decode_notebook_roundtrip(tmp_path):
    src = "x = 1\r\ndef agent(o):\n    return {}\n"
    nb = _synth_notebook(tmp_path, src)
    out = tmp_path / "main2965.py"
    sha = B._decode_notebook(nb, str(out))
    assert out.read_bytes() == src.replace("\r\n", "\n").encode()  # CRLF 归一
    import hashlib
    assert sha == hashlib.sha256(src.replace("\r\n", "\n").encode()).hexdigest()


def test_decode_notebook_no_payload(tmp_path):
    nb = tmp_path / "empty.ipynb"
    nb.write_text(json.dumps({"cells": [{"cell_type": "code",
                                         "source": ["print(1)"]}]}),
                  encoding="utf-8")
    with pytest.raises(B.BuildAdoptError, match="AGENT_B64"):
        B._decode_notebook(str(nb), str(tmp_path / "out.py"))


def test_fetch_cache_hit_with_pinned_sha(tmp_path, monkeypatch):
    # 钉死值可替换（合成缓存命中分支；网络分支由生产运行覆盖）
    good = b"# synthetic 2965 source\ndef agent(o):\n    return {}\n"
    import hashlib
    want = hashlib.sha256(good).hexdigest()
    d = tmp_path / "dec"
    d.mkdir()
    (d / "main2965.py").write_bytes(good)
    monkeypatch.setattr(B, "DECODE_DIR", str(d))
    monkeypatch.setattr(B, "EXPECTED_SHA256_2965", want)
    got = B.fetch_2965_source()
    assert got["source"] == "cache" and got["sha256"] == want


def test_fetch_sha_drift_fail_closed(tmp_path, monkeypatch):
    d = tmp_path / "dec"
    d.mkdir()
    (d / "main2965.py").write_bytes(b"tampered")
    monkeypatch.setattr(B, "DECODE_DIR", str(d))
    monkeypatch.setattr(B, "KAGGLE_BIN", "/nonexistent/kaggle")
    with pytest.raises(B.BuildAdoptError):
        B.fetch_2965_source()


# ---------------------------------------------------------------------------
# merge 组（真 L3 基座+真 2965 源，tmp 出口）
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def merged(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("r34")
    src = os.path.join(tmp, "main2965.py")
    # 优先真缓存（fetch 已在生产路径核过 sha）；缺则 pull（网络可用假设）
    fetched = B.fetch_2965_source()
    src = fetched["path"]
    a_main = str(tmp / "r34a_main.py")
    audit = B.merge_increments(B.L3_MAIN, src, a_main)
    return {"tmp": str(tmp), "src": src, "a_main": a_main, "audit": audit}


def test_merge_splice_and_layer_s_removal(merged):
    audit = merged["audit"]
    # 拼接：round-2 注释单行替换为三增量块（EXP402+EXP410/bridge/IG）
    assert audit["splice"]["inserted_lines"] == 222
    assert audit["splice"]["prefix_lines_identical"]
    assert audit["splice"]["suffix_lines_identical"]
    assert audit["increments"] == {"e402_block_lines": 56,
                                   "e410_ig_block_lines": 165}
    # layer S 移除：尾部 _cxs_* 全数不在场、字节体量=前躯+增量
    text = open(merged["a_main"], encoding="utf-8").read()
    assert "_cxs_" not in text and "_cxs_agent" not in text
    assert audit["composition"]["layer_s_removed_bytes"] > 20000
    assert audit["last_callable"] == B.R34_LAST_CALLABLE


def test_merge_constants_kept_ours(merged):
    consts = merged["audit"]["constants_kept_ours"]
    assert consts == {"_V92_P_EVERY": 2, "_CA_MARGIN": -15.0,
                      "_OR2_SLOT_MARGIN": 8.0, "V9_RACE_DEFAULT": [40, 44]}


def test_merge_increment_symbols_present(merged):
    text = open(merged["a_main"], encoding="utf-8").read()
    for sym in ("e402_agent", "e410_agent", "_ig_guard_opening",
                "_ig_close_queue", "_ig_standard", "_E402_REPORT",
                "_E410_REPORT", "_IG_REPORT"):
        assert sym in text, sym


def test_merge_missing_anchor_fail_closed(tmp_path, merged):
    src_lines = open(merged["src"], encoding="utf-8").read().split("\n")
    src_lines = [ln for ln in src_lines
                 if not ln.startswith("# EXP402: cap late seed")]
    bad = tmp_path / "bad2965.py"
    bad.write_text("\n".join(src_lines), encoding="utf-8")
    with pytest.raises(B.BuildAdoptError, match="EXP402"):
        B.merge_increments(B.L3_MAIN, str(bad), str(tmp_path / "out.py"))


# ---------------------------------------------------------------------------
# constants 组
# ---------------------------------------------------------------------------
def test_apply_constants_exactly_three(merged):
    out = os.path.join(merged["tmp"], "r34b_main.py")
    audit = B.apply_2965_constants(merged["a_main"], out)
    assert audit["n_changed_lines"] == 3
    assert [(c["name"], c["old"], c["new"]) for c in audit["changes"]] == [
        ("_V92_P_EVERY", "2", "3"),
        ("_CA_MARGIN", "-15.0", "-5.0"),
        ("_OR2_SLOT_MARGIN", "8.0", "20.0")]
    assert audit["race_untouched"] and audit["last_callable"] == "_cxd_agent"
    consts = B._constant_values(open(out, encoding="utf-8").read())
    assert consts["_V92_P_EVERY"] == 3 and consts["_CA_MARGIN"] == -5.0
    assert consts["_OR2_SLOT_MARGIN"] == 20.0
    assert consts["V9_RACE_DEFAULT"] == [40, 44]


def test_apply_constants_missing_site_fail_closed(tmp_path, merged):
    lines = open(merged["a_main"], encoding="utf-8").read().split("\n")
    lines.remove("_OR2_SLOT_MARGIN = 8.0")
    bad = tmp_path / "r34a_missing.py"
    bad.write_text("\n".join(lines), encoding="utf-8")
    with pytest.raises(B.BuildAdoptError, match="_OR2_SLOT_MARGIN"):
        B.apply_2965_constants(str(bad), str(tmp_path / "out.py"))


# ---------------------------------------------------------------------------
# audit 组
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def audited(merged):
    b_main = os.path.join(merged["tmp"], "r34b_main.py")
    B.apply_2965_constants(merged["a_main"], b_main)
    return {"b_main": b_main,
            "audit": B.audit_diff_vs_2965(merged["a_main"], b_main,
                                          merged["src"])}


def test_audit_all_attributed(audited):
    audit = audited["audit"]
    assert audit["ok"] is True
    for label in ("a", "b"):
        assert audit[label]["ok"] is True
        assert "UNATTRIBUTED" not in audit[label]["attribution"]
    # r34b 对 2965 差异恰为我方层/明示不采纳面（无常数差）
    attr_b = audit["b"]["attribution"]
    assert "constants_delta" not in json.dumps(attr_b)
    assert set(attr_b) >= {"our_carrot2_clamp", "our_tb_tomato_gate",
                           "2965_tail_not_adopted(ledger/new/constants-override/_HR)"}
    # r34a 另含恰三处常数差
    assert audited["audit"]["a"]["attribution"].get(
        "constants_delta(r34a_keeps_ours)") == 3


def test_audit_tamper_red(audited, tmp_path):
    lines = open(audited["b_main"], encoding="utf-8").read().split("\n")
    lines.insert(500, "MYSTERY_GLOBAL_LINE = 12345")
    tampered = tmp_path / "tampered.py"
    tampered.write_text("\n".join(lines), encoding="utf-8")
    audit = B.audit_diff_vs_2965(str(tampered), str(tampered), audited["src"]
                                 if False else _src_path())
    assert audit["a"]["ok"] is False
    assert audit["a"]["attribution"].get("UNATTRIBUTED") == 1


def _src_path():
    return B.fetch_2965_source()["path"]


# ---------------------------------------------------------------------------
# 打包组
# ---------------------------------------------------------------------------
def test_tar_deterministic_and_member_set(merged):
    main_bytes = open(merged["a_main"], "rb").read()
    t1, t2 = B.build_tar_bytes(main_bytes), B.build_tar_bytes(main_bytes)
    assert t1 == t2                      # 双跑逐字节一致
    with tarfile.open(fileobj=__import__("io").BytesIO(t1), mode="r:gz") as tar:
        assert tar.getnames() == ["main.py"]
        assert tar.extractfile("main.py").read() == main_bytes
        info = tar.getmember("main.py")
        assert info.mode == 0o644 and info.mtime == 0
        assert info.uid == 0 and info.gid == 0
    assert len(t1) <= B.SIZE_CAP_BYTES


def test_stub_markers_cleared():
    """桩清零：实现源件不得再含 unimplemented:fn 桩标记。"""
    for fname in ("build_adopt.py", "gates_adopt.py", "__init__.py"):
        text = open(os.path.join(os.path.dirname(B.__file__), fname),
                    encoding="utf-8").read()
        assert "unimplemented:fn" not in text, fname
