"""build_candidate_package 真实测试（R6：换 RouteLibrary 字节重打包）。

真实基底（v48_derivative 外壳，只读）+ 真实库/最终件（tape_gen
library/routes.json + search/final_selection.json）构建进 tmp；手术面/
确定性/路由器语义登记逐项自证；配置漂移与基底漂移 fail-closed。
"""

import hashlib
import json
import tarfile

import pytest
from assemble_and_gate.build_candidate_package import (
    PackageError,
    ROUTER_SLOTS,
    SHELL_MAIN,
    _ROUTES_RE,
    build_candidate_package,
    decode_blob_body,
)

_CAMPAIGN = SHELL_MAIN.parents[4]
_LIB = _CAMPAIGN / "fn_work" / "tape_gen" / "library"
_SEL = _CAMPAIGN / "fn_work" / "tape_gen" / "search" / "final_selection.json"


def _build(tmp_path, **over):
    payload = {"output_dir": str(tmp_path / "cand")}
    payload.update(over)
    return build_candidate_package(payload)


def test_real_build_surgical_face_and_determinism(tmp_path):
    manifest = _build(tmp_path)
    out = tmp_path / "cand"
    main_bytes = (out / "main.py").read_bytes()
    tar_bytes = (out / "submission.tar.gz").read_bytes()

    # 产物身份与 manifest 一致
    assert manifest["products"]["main_py"]["sha256"] == \
        hashlib.sha256(main_bytes).hexdigest()
    assert manifest["products"]["main_py"]["bytes"] == len(main_bytes)
    assert manifest["products"]["submission_tar_gz"]["sha256"] == \
        hashlib.sha256(tar_bytes).hexdigest()

    # 手术面：blob 区间外逐字节一致（对外壳原文重算）
    base_text = SHELL_MAIN.read_text(encoding="utf-8")
    main_text = main_bytes.decode("utf-8")
    base_m = _ROUTES_RE.search(base_text)
    new_m = _ROUTES_RE.search(main_text)
    assert base_m and new_m
    lo = manifest["surgical_face"]["blob_span"][0]
    hi = manifest["surgical_face"]["blob_span"][1]
    assert main_text[:lo] == base_text[:lo]
    assert main_text[hi:] == base_text[base_m.span(1)[1]:]
    # 机制区/反射层零改：关键字面仍在 blob 外
    assert "_V48_GOLD_CONFIG = _V48GoldConfig" in main_text
    assert "_V48_CONFIG = _V48Config" in main_text

    # blob 解码回路 == 6 槽别名（全部 = 库最终件磁带）
    slot_map = decode_blob_body(new_m.group(1))
    assert sorted(slot_map) == sorted(ROUTER_SLOTS)
    library = json.loads(
        (_LIB / "routes.json").read_text(encoding="utf-8"))
    sel = json.loads(_SEL.read_text(encoding="utf-8"))
    final_route = sel["piece"].split(":", 1)[1]
    for slot in ROUTER_SLOTS:
        assert slot_map[slot] == library[final_route]

    # 双跑确定性 + 编译可过
    again = _build(tmp_path / "again")
    assert again["products"]["main_py"]["sha256"] == \
        manifest["products"]["main_py"]["sha256"]
    compile(main_bytes, "main.py", "exec")

    # tar 单成员确定性
    with open(out / "submission.tar.gz", "rb") as fh:
        with tarfile.open(fileobj=fh, mode="r:gz") as tar:
            assert tar.getnames() == ["main.py"]
            assert tar.extractfile("main.py").read() == main_bytes

    # 路由器语义登记：fork 未接线；字面 2 路由 fail-closed 已登记
    unwired = manifest["router_semantics"]["fork_routes_unwired"]
    assert unwired["fork_s73_e72"]["wired"] is False
    assert "fail-closed" in manifest["router_semantics"][
        "literal_library_dict"]
    # 配置面：与外壳缺省一致 → 只换库
    cfg = manifest["surgical_face"]["config_face"]
    assert cfg["selection_matches_shell_defaults"] is True
    assert cfg["surgical_face"] == "library_blob_only"
    assert cfg["shell_clone_preempt_horizon"] == 2
    assert cfg["shell_clone_streak_required"] == 24
    # 库身份对账（T2 链）
    assert manifest["library"]["routes_canonical_sha256"] == \
        manifest["library"]["library_manifest_routes_sha256"]
    assert manifest["selection"]["selection_sha256"] == \
        sel["selection_sha256"]


def test_config_divergence_fail_closed(tmp_path):
    sel = json.loads(_SEL.read_text(encoding="utf-8"))
    bad = dict(sel)
    bad["switches"] = dict(sel["switches"], clone_preempt=False)
    with pytest.raises(PackageError, match="surgical face"):
        _build(tmp_path, selection=bad)


def test_streak_threshold_divergence_fail_closed(tmp_path):
    sel = json.loads(_SEL.read_text(encoding="utf-8"))
    bad = dict(sel)
    bad["thresholds"] = dict(sel["thresholds"],
                             clone_streak_required=16)
    with pytest.raises(PackageError, match="clone_streak_required"):
        _build(tmp_path, selection=bad)


def test_unwired_switch_on_fail_closed(tmp_path):
    sel = json.loads(_SEL.read_text(encoding="utf-8"))
    bad = dict(sel)
    bad["switches"] = dict(sel["switches"], market_maker=True)
    with pytest.raises(PackageError, match="market_maker"):
        _build(tmp_path, selection=bad)


def test_unknown_final_piece_fail_closed(tmp_path):
    sel = json.loads(_SEL.read_text(encoding="utf-8"))
    bad = dict(sel, piece="route:does_not_exist")
    with pytest.raises(PackageError, match="missing from library"):
        _build(tmp_path, selection=bad)


def test_shell_base_drift_fail_closed(tmp_path):
    base_copy = tmp_path / "base_main.py"
    base_copy.write_bytes(SHELL_MAIN.read_bytes() + b"\n# drift\n")
    with pytest.raises(PackageError, match="shell base drift"):
        _build(tmp_path, base_main=base_copy)


def test_non_719_route_fail_closed(tmp_path):
    library = json.loads(
        (_LIB / "routes.json").read_text(encoding="utf-8"))
    bad = {name: steps[:100] for name, steps in library.items()}
    with pytest.raises(PackageError, match="719"):
        _build(tmp_path, routes=bad)


def test_skip_write_returns_manifest_without_touching_disk(tmp_path):
    out = tmp_path / "never"
    manifest = build_candidate_package(
        {"output_dir": str(out), "skip_write": True})
    assert not out.exists()
    assert manifest["products"]["main_py"]["bytes"] > 0
    assert manifest["deterministic_double_build"] is True
