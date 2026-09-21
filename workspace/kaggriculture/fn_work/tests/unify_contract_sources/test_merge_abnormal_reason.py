"""merge_abnormal_reason 真实测试：双旧实现对照锚（裁决级一致 + 分叉面并集）。

对照锚 = 旧树 kgenv.arena._abnormal_reason 与 kgenv.eval_contract.
game_abnormal_reason（只读 import，不 import 旧 scripts/）。锚定口径=
裁决级（None=正常 / 非 None=异常），不锚理由文案（合并后文案为新真值）。
"""

from __future__ import annotations

import sys
from pathlib import Path

from unify_contract_sources.merge_abnormal_reason import (
    build_case_battery,
    merge_abnormal_reason,
)

# 战役根目录特征（三件齐备才算；与仓库布局约定一致）
_CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")


def _software_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / name).exists() for name in _CAMPAIGN_FEATURES):
            return candidate / "software"
    raise RuntimeError("campaign root not found upward from " + str(here))


def _old_implementations():
    software = _software_root()
    if str(software) not in sys.path:
        sys.path.insert(0, str(software))
    import kgenv.arena as arena
    import kgenv.eval_contract as eval_contract
    return arena._abnormal_reason, eval_contract.game_abnormal_reason


def _battery(kind: str):
    return [case for case in build_case_battery() if case["kind"] == kind]


def _red(reason) -> bool:
    return reason is not None


# --------------------------------------------------------------------------- #
# 双源同判面：两旧实现各自能判的用例上，三方裁决一致
# --------------------------------------------------------------------------- #
def test_normal_cases_all_three_agree_green():
    arena_fn, eval_fn = _old_implementations()
    cases = _battery("normal")
    assert cases, "battery must contain normal cases"
    for case in cases:
        game, kwargs = case["game"], case["kwargs"]
        assert merge_abnormal_reason(dict(game), **kwargs) is None, case["name"]
        assert arena_fn(dict(game)) is None, case["name"]
        assert eval_fn(dict(game), **kwargs) is None, case["name"]


def test_parity_red_cases_all_three_agree_red():
    arena_fn, eval_fn = _old_implementations()
    cases = _battery("parity_red")
    assert len(cases) >= 8, "battery must cover the shared-red surface"
    for case in cases:
        game, kwargs = case["game"], case["kwargs"]
        assert _red(merge_abnormal_reason(dict(game), **kwargs)), case["name"]
        assert _red(arena_fn(dict(game))), case["name"]
        assert _red(eval_fn(dict(game), **kwargs)), case["name"]


# --------------------------------------------------------------------------- #
# 分叉面：恰一旧实现判红，并集语义=merged 必红；逐面锚定"哪一侧红"
# --------------------------------------------------------------------------- #
# 旧源读码定案的锚定映射（kgenv/arena.py:27 vs kgenv/eval_contract.py:155）：
# case -> (arena 红?, eval 红?)
_UNION_SURFACE_ANCHOR = {
    "players_identical": (False, True),    # 仅 eval 判（arena 只查长度）
    "rewards_bool": (True, False),         # 仅 arena 判（bool 是 int 子类）
    "rewards_inf": (True, False),          # 仅 arena 判（eval 漏判非有限）
    "missing_seed": (False, True),         # 仅 eval 判（字段面分叉）
    "missing_seat": (False, True),
    "missing_seed_domain": (False, True),
    "seat_invalid": (False, True),
}


def test_union_divergence_surface_takes_union():
    arena_fn, eval_fn = _old_implementations()
    cases = {case["name"]: case for case in _battery("union_red")}
    assert set(cases) == set(_UNION_SURFACE_ANCHOR), (
        f"battery union surface drifted: "
        f"{sorted(set(cases) ^ set(_UNION_SURFACE_ANCHOR))}")
    for name, (arena_red, eval_red) in _UNION_SURFACE_ANCHOR.items():
        game = cases[name]["game"]
        assert _red(arena_fn(dict(game))) is arena_red, (name, "arena")
        assert _red(eval_fn(dict(game))) is eval_red, (name, "eval")
        assert _red(merge_abnormal_reason(dict(game))), (name, "merged-union")


# --------------------------------------------------------------------------- #
# 源 B 专属判定面：kwarg 面与导出面（arena 无对应参数）
# --------------------------------------------------------------------------- #
def test_eval_kwarg_faces():
    arena_fn, eval_fn = _old_implementations()
    cases = _battery("eval_kwarg")
    assert cases, "battery must contain eval_kwarg cases"
    for case in cases:
        game, kwargs = case["game"], case["kwargs"]
        assert arena_fn(dict(game)) is None, case["name"]
        assert _red(eval_fn(dict(game), **kwargs)), case["name"]
        assert _red(merge_abnormal_reason(dict(game), **kwargs)), case["name"]
        assert merge_abnormal_reason(dict(game)) is None, case["name"]


def test_export_faces_only_red_in_export_mode():
    arena_fn, eval_fn = _old_implementations()
    cases = _battery("export_only")
    assert cases, "battery must contain export_only cases"
    for case in cases:
        game = case["game"]
        assert merge_abnormal_reason(dict(game)) is None, case["name"]
        assert arena_fn(dict(game)) is None, case["name"]
        assert eval_fn(dict(game)) is None, case["name"]
        assert _red(merge_abnormal_reason(
            dict(game), require_export_fields=True)), case["name"]
        assert _red(eval_fn(dict(game),
                            require_export_fields=True)), case["name"]


# --------------------------------------------------------------------------- #
# 直接行为断言（不依赖旧树锚的最小面）
# --------------------------------------------------------------------------- #
def test_merged_reason_is_string_or_none():
    for case in build_case_battery():
        reason = merge_abnormal_reason(dict(case["game"]),
                                       **case["kwargs"])
        assert reason is None or isinstance(reason, str), case["name"]


def test_merged_does_not_mutate_input():
    game = build_case_battery()[0]["game"]
    snapshot = dict(game)
    merge_abnormal_reason(game, require_export_fields=True)
    assert game == snapshot


def test_missing_statuses_reported():
    reason = merge_abnormal_reason({"players": ["a", "b"]})
    assert isinstance(reason, str)
    assert "missing required game fields" in reason


def test_allowed_seeds_and_domain_faces():
    game = dict(build_case_battery()[0]["game"])
    assert merge_abnormal_reason(game, allowed_seeds={201}) is not None
    assert merge_abnormal_reason(game, expected_domain="holdout") is not None
    assert merge_abnormal_reason(game, allowed_seeds={101},
                                 expected_domain="development") is None
