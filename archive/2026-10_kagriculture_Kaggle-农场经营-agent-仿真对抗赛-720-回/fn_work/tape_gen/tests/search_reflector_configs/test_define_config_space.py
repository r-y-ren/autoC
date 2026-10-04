"""define_config_space 真实测试（R4：空间文档+规模登记）。

不触引擎/网络：库面用 tmp 伪造（2 路由+8 变体=10 件），验证轴枚举、
空间规模（10×2^5=320）、文档落盘、确定性与 fail-closed。
"""

import json

import pytest
from search_reflector_configs.define_config_space import (
    THRESHOLD_AXES,
    define_config_space,
)

STEP = {"farmer": ["PASS"], "hands": [], "market": []}


def _fake_library(tmp_path):
    routes = {name: [dict(STEP) for _ in range(719)]
              for name in ("default", "fork_s73_e72")}
    variants = {f"v{i}": [dict(STEP) for _ in range(719)]
                for i in range(8)}
    library = tmp_path / "library"
    library.mkdir()
    (library / "routes.json").write_text(
        json.dumps(routes), encoding="utf-8")
    (library / "market_variants.json").write_text(
        json.dumps(variants), encoding="utf-8")
    return library


def test_space_axes_and_size(tmp_path):
    library = _fake_library(tmp_path)
    space = define_config_space({"library_dir": str(library),
                                 "write": False})
    assert space["n_pieces"] == 10
    assert space["n_routes"] == 2
    assert space["n_variants"] == 8
    assert space["n_switches"] == 5
    assert set(space["switch_order"]) == {
        "clone_preempt", "slot_reorder", "market_maker",
        "terminal_forced", "dead_price_guard"}
    # 空间规模登记：10 × 2^5 = 320，全枚举
    assert space["base_space_size"] == 320
    assert len(space["candidates"]) == 320
    assert len({c["id"] for c in space["candidates"]}) == 320
    # 阈值微轴登记（精化扇出，不进基空间乘法）
    assert space["threshold_axes"] == {k: list(v) for k, v in
                                       THRESHOLD_AXES.items()}
    assert space["refinement_fanout"] == 2
    # enabled_modules = 开关 ON 计数（库件/阈值不计入）
    zero = [c for c in space["candidates"] if c["id"].endswith("#00000")]
    assert len(zero) == 10 and all(
        c["enabled_modules"] == 0 for c in zero)
    full = [c for c in space["candidates"] if c["id"].endswith("#11111")]
    assert len(full) == 10 and all(
        c["enabled_modules"] == 5 for c in full)


def test_space_determinism_and_order(tmp_path):
    library = _fake_library(tmp_path)
    a = define_config_space({"library_dir": str(library), "write": False})
    b = define_config_space({"library_dir": str(library), "write": False})
    assert a["space_sha256"] == b["space_sha256"]
    assert [c["id"] for c in a["candidates"]] == \
        [c["id"] for c in b["candidates"]]
    ids = [c["id"] for c in a["candidates"]]
    assert ids == sorted(ids)  # 件字典序 × 掩码升序的全序


def test_space_doc_written(tmp_path):
    library = _fake_library(tmp_path)
    out = tmp_path / "search"
    space = define_config_space({"library_dir": str(library),
                                 "output_dir": str(out), "write": True})
    doc = (out / "config_space.md").read_text(encoding="utf-8")
    summary = json.loads((out / "config_space.json").read_text(
        encoding="utf-8"))
    assert "320" in doc and "clone_preempt" in doc \
        and "dead_price_guard" in doc
    assert summary["base_space_size"] == 320
    assert summary["n_candidates"] == 320
    assert summary["space_sha256"] == space["space_sha256"]


def test_space_fail_closed_empty_library(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(ValueError, match="fail-closed"):
        define_config_space({"library_dir": str(empty), "write": False})
