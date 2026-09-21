"""契约单源化编排与一致性测试收口（双源残留即失败）。

上游: R8, R9（详见 fn_docs/responsibility.md）

实现要点（[改造]件，L0 编排）：
- 三叶自检 + 等值断言集，输出裁决 dict：
    1. merge_abnormal_reason——以 build_case_battery() 锚定用例集对旧双实现
       （kgenv/arena._abnormal_reason 与 kgenv.eval_contract.game_abnormal_reason，
       只读 import）做裁决级对照：双源同判面行为一致（normal/parity_red）、
       分叉面取并集（union_red：恰一旧实现判红，merged 必红）、B 专属
       kwarg/导出面保留（eval_kwarg/export_only）。
    2. single_opponent_roster——名册 7 站点等值断言：kgenv 侧 5 站点
       （bots×2 / eval_contract / regression / holdout_contract）活 import
       比对；scripts 侧 2 站点（iterate_gate REQUIRED_OPPONENTS 11 池、
       check_eval_contract REQUIRED_OPPONENTS 9 网格）经源文本提取列表
       字面比对（不 import 旧 scripts/，读源即比对）。
    3. assert_bots_constants_match_wheel——五文件手抄常量 vs wheel 真值
       交叉断言（漂移即 ok=False；strict 下升级抛错）。
- 双源残留语义（R8"双源残留即失败"的冻结树落地口径）：旧树冻结——物理
  改线属战后（见各叶模块头适配说明）；改线完成前，"残留"的可判定形态=
  旧定义与新单源**等值漂移**（任何一站不等即失败）；旧定义站点被删除
  （锚丢失）同样判失败（import/提取错误进 failures）。
- strict=True（缺省）：ok=False 即抛 UnificationError（裁决 dict 已含
  全部明细）；strict=False 供测试与巡检只取裁决。三叶各自内部异常
  （含 bots 交叉断言的 BotsConstantsMismatch）捕获进裁决不吞错。
- 旧树只读：kgenv 可 import、scripts 只读源文本；不写任何旧树文件。

适配说明（旧树冻结——物理改线属战后，登记于此）：
- 战后改线完成后，本编排的 kgenv/scripts 等值断言转为防回归保留；
  名册/异常判定/常量的真值源自此唯一=fn_work/src/unify_contract_sources。
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from unify_contract_sources.assert_bots_constants_match_wheel import (
    BotsConstantsMismatch,
    assert_bots_constants_match_wheel,
)
from unify_contract_sources.merge_abnormal_reason import (
    build_case_battery,
    merge_abnormal_reason,
)
from unify_contract_sources.single_opponent_roster import (
    EXPECTED_ELO_ORDER,
    FROZEN_POOL,
    GRID_REQUIRED_OPPONENTS,
    HOLDOUT_MATRIX_ORDERS,
    ONLINE_STYLE_OPPONENTS,
    OPPONENT_POOL_11,
    STANDARD_MATRIX_ORDER,
    STRONG_OPPONENTS,
    single_opponent_roster,
)

__all__ = ["UnificationError", "unify_contract_sources"]

# 战役根目录特征（三件齐备才算；与仓库布局约定一致，不写字面战役路径）
_CAMPAIGN_FEATURES = ("blueprint.md", "software", "fn_docs")


class UnificationError(RuntimeError):
    """契约单源化裁决不通过（双源漂移/锚丢失/常量不符 wheel）——fail-closed。"""


def _campaign_software_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        if all((candidate / name).exists() for name in _CAMPAIGN_FEATURES):
            return candidate / "software"
    raise UnificationError(
        "未找到战役根（特征=" + "+".join(_CAMPAIGN_FEATURES) + "），"
        f"上溯起点: {here}")


def _import_old_kgenv():
    """只读 import 旧树 kgenv（返回 (arena 模块, eval_contract 模块,
    bots 包, regression 模块, holdout_contract 模块)）。"""
    software = _campaign_software_root()
    if str(software) not in sys.path:
        sys.path.insert(0, str(software))
    import kgenv.arena as arena
    import kgenv.bots as bots
    import kgenv.eval_contract as eval_contract
    import kgenv.holdout_contract as holdout_contract
    import kgenv.regression as regression
    return arena, eval_contract, bots, regression, holdout_contract


def _extract_list_literal(text: str, name: str) -> Optional[list]:
    """从源文本提取 `name = [...]` 列表字面（含行间注释；非字面返回 None）。"""
    match = re.search(rf"^{name}\s*=\s*(\[.*?\])", text,
                      re.MULTILINE | re.DOTALL)
    if match is None:
        return None
    try:
        return ast.literal_eval(match.group(1))
    except (ValueError, SyntaxError):
        return None


# --------------------------------------------------------------------------- #
# 叶 1：异常局判定双源对照（裁决级：None=正常 / 非 None=异常）
# --------------------------------------------------------------------------- #
def _check_merge_abnormal_reason(
        arena_reason: Callable[[dict], Optional[str]],
        eval_reason: Callable[..., Optional[str]]) -> dict:
    failures: List[dict] = []
    union_surface: List[str] = []
    by_kind: Dict[str, int] = {}
    for case in build_case_battery():
        kind = case["kind"]
        by_kind[kind] = by_kind.get(kind, 0) + 1
        name, game, kwargs = case["name"], case["game"], case["kwargs"]
        merged = merge_abnormal_reason(dict(game), **kwargs)
        old_arena = arena_reason(dict(game))
        old_eval = eval_reason(dict(game), **kwargs)
        red = lambda r: r is not None  # noqa: E731
        if kind in ("normal", "parity_red"):
            want = kind == "normal"
            for label, got in (("merged", merged), ("arena", old_arena),
                               ("eval_contract", old_eval)):
                if red(got) != (not want):
                    failures.append({"case": name, "kind": kind, "impl": label,
                                     "verdict": got})
        elif kind == "union_red":
            if not red(old_arena) ^ red(old_eval):
                failures.append({"case": name, "kind": kind,
                                 "impl": "battery-design",
                                 "verdict": f"arena={old_arena!r} "
                                            f"eval={old_eval!r}（须恰一红）"})
            if not red(merged):
                failures.append({"case": name, "kind": kind,
                                 "impl": "merged", "verdict": merged})
            union_surface.append(name)
        elif kind == "eval_kwarg":
            # 用例本体正常：旧 arena 无 kwarg 面必绿；红只来自 kwarg 面。
            merged_plain = merge_abnormal_reason(dict(game))
            if red(old_arena):
                failures.append({"case": name, "kind": kind,
                                 "impl": "arena", "verdict": old_arena})
            if not red(old_eval) or not red(merged):
                failures.append({"case": name, "kind": kind,
                                 "impl": "eval/merged-with-kwargs",
                                 "verdict": f"eval={old_eval!r} merged={merged!r}"})
            if red(merged_plain):
                failures.append({"case": name, "kind": kind,
                                 "impl": "merged-without-kwargs",
                                 "verdict": merged_plain})
        elif kind == "export_only":
            merged_export = merge_abnormal_reason(dict(game),
                                                  require_export_fields=True)
            old_eval_export = eval_reason(dict(game),
                                          require_export_fields=True)
            for label, got in (("merged", merged),
                               ("arena", old_arena), ("eval", old_eval)):
                if red(got):
                    failures.append({"case": name, "kind": kind,
                                     "impl": f"{label}-plain", "verdict": got})
            if not red(merged_export) or not red(old_eval_export):
                failures.append({"case": name, "kind": kind,
                                 "impl": "export-mode",
                                 "verdict": f"eval={old_eval_export!r} "
                                            f"merged={merged_export!r}"})
    return {"ok": not failures,
            "battery_cases": sum(by_kind.values()),
            "by_kind": by_kind,
            "union_divergence_surface": union_surface,
            "failures": failures}


# --------------------------------------------------------------------------- #
# 叶 2：名册 7 站点等值断言（kgenv 活 import 5 站 + scripts 源文本 2 站）
# --------------------------------------------------------------------------- #
def _check_single_opponent_roster(roster_sites: Optional[dict]) -> dict:
    failures: List[dict] = []
    sites: Dict[str, dict] = {}

    def compare(site: str, old_value, new_value, channel: str) -> None:
        ok = old_value == new_value
        sites[site] = {"ok": ok, "channel": channel,
                       "old": _plain(old_value), "new": _plain(new_value)}
        if not ok:
            failures.append({"site": site, "channel": channel,
                             "old": _plain(old_value),
                             "new": _plain(new_value)})

    try:
        if roster_sites is None:
            _, eval_contract_mod, bots, regression, holdout_contract = (
                _import_old_kgenv())
            roster_sites = {
                "bots.STRONG_OPPONENTS": bots.STRONG_OPPONENTS,
                "bots.ONLINE_STYLE_OPPONENTS": bots.ONLINE_STYLE_OPPONENTS,
                "eval_contract.STANDARD_MATRIX_ORDER":
                    eval_contract_mod.STANDARD_MATRIX_ORDER,
                "regression.EXPECTED_ELO_ORDER": regression.EXPECTED_ELO_ORDER,
                "regression.FROZEN_POOL": regression.FROZEN_POOL,
                "holdout_contract.matrix_orders_v1_v5": {
                    i: holdout_contract.holdout_matrix_order(i)
                    for i in range(1, 6)},
            }
    except Exception as exc:  # 锚丢失（kgenv 站点不可取）——判失败不吞错
        return {"ok": False, "sites": sites, "failures": [
            {"site": "kgenv-live-import", "error": repr(exc)}]}

    compare("bots.STRONG_OPPONENTS",
            tuple(roster_sites["bots.STRONG_OPPONENTS"]),
            tuple(STRONG_OPPONENTS), "import")
    compare("bots.ONLINE_STYLE_OPPONENTS",
            tuple(roster_sites["bots.ONLINE_STYLE_OPPONENTS"]),
            tuple(ONLINE_STYLE_OPPONENTS), "import")
    compare("eval_contract.STANDARD_MATRIX_ORDER",
            tuple(roster_sites["eval_contract.STANDARD_MATRIX_ORDER"]),
            tuple(STANDARD_MATRIX_ORDER), "import")
    compare("regression.EXPECTED_ELO_ORDER",
            list(roster_sites["regression.EXPECTED_ELO_ORDER"]),
            list(EXPECTED_ELO_ORDER), "import")
    compare("regression.FROZEN_POOL",
            set(roster_sites["regression.FROZEN_POOL"]),
            set(FROZEN_POOL), "import")
    holdout_old = {int(k): tuple(v) for k, v in
                   roster_sites["holdout_contract.matrix_orders_v1_v5"].items()}
    holdout_new = {k: tuple(v) for k, v in HOLDOUT_MATRIX_ORDERS.items()}
    compare("holdout_contract.matrix_orders_v1_v5", holdout_old,
            holdout_new, "import")

    # scripts 侧 2 站：源文本提取列表字面（不 import 旧 scripts/）
    try:
        software = _campaign_software_root()
        iterate_gate_src = (software / "scripts" / "iterate_gate.py").read_text(
            encoding="utf-8")
        check_eval_src = (software / "scripts" / "check_eval_contract.py"
                          ).read_text(encoding="utf-8")
        gate = _extract_list_literal(iterate_gate_src, "GATE_OPPONENTS")
        guard = _extract_list_literal(iterate_gate_src, "GUARD_OPPONENTS")
        online = _extract_list_literal(iterate_gate_src, "ONLINE_OPPONENTS")
        if None in (gate, guard, online):
            failures.append({"site": "scripts/iterate_gate.py",
                             "channel": "source_text",
                             "error": "GATE/GUARD/ONLINE_OPPONENTS 列表字面提取失败"})
            sites["scripts/iterate_gate.REQUIRED_OPPONENTS"] = {
                "ok": False, "channel": "source_text", "error": "提取失败"}
        else:
            compare("scripts/iterate_gate.REQUIRED_OPPONENTS",
                    list(gate) + list(guard) + list(online),
                    list(OPPONENT_POOL_11), "source_text")
        grid = _extract_list_literal(check_eval_src, "REQUIRED_OPPONENTS")
        if grid is None:
            failures.append({"site": "scripts/check_eval_contract.py",
                             "channel": "source_text",
                             "error": "REQUIRED_OPPONENTS 列表字面提取失败"})
            sites["scripts/check_eval_contract.REQUIRED_OPPONENTS"] = {
                "ok": False, "channel": "source_text", "error": "提取失败"}
        else:
            compare("scripts/check_eval_contract.REQUIRED_OPPONENTS",
                    grid, list(GRID_REQUIRED_OPPONENTS), "source_text")
    except Exception as exc:  # scripts 源不可读——判失败不吞错
        failures.append({"site": "scripts-source-text", "error": repr(exc)})

    return {"ok": not failures, "sites": sites, "failures": failures}


def _plain(value: Any) -> Any:
    """站点值转 JSON 友好形态（frozenset/tuple -> 排序表）。"""
    if isinstance(value, frozenset):
        return sorted(value)
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    return value


# --------------------------------------------------------------------------- #
# 顶层编排
# --------------------------------------------------------------------------- #
def unify_contract_sources(*, strict: bool = True,
                           arena_reason: Optional[Callable] = None,
                           eval_reason: Optional[Callable] = None,
                           roster_sites: Optional[dict] = None,
                           bots_sources: Optional[dict] = None,
                           wheel_source=None) -> dict:
    """单源化编排自检（三叶+等值断言集），输出裁决 dict。

    Args:
        strict: True（缺省）时 ok=False 抛 UnificationError（fail-closed，
            R8"双源残留即失败"）；False 只返回裁决（巡检/测试用）。
        arena_reason / eval_reason: 注入的旧双实现（缺省=只读 import 旧树
            kgenv.arena._abnormal_reason / kgenv.eval_contract.game_abnormal_reason）。
        roster_sites: 注入的名册站点值（缺省=kgenv 活 import；scripts 两站
            恒经源文本提取，不受注入影响）。
        bots_sources / wheel_source: 透传 assert_bots_constants_match_wheel。

    Returns:
        裁决 dict：{ok, campaign_root, leaves: {merge_abnormal_reason,
        single_opponent_roster, assert_bots_constants_match_wheel}}，
        各叶含 ok 与明细（failures/sites/battery 统计/交叉报告）。
    """
    try:
        if arena_reason is None or eval_reason is None:
            arena_mod, eval_mod, _, _, _ = _import_old_kgenv()
            if arena_reason is None:
                arena_reason = arena_mod._abnormal_reason
            if eval_reason is None:
                eval_reason = eval_mod.game_abnormal_reason
        leaf_merge = _check_merge_abnormal_reason(arena_reason, eval_reason)
    except Exception as exc:
        leaf_merge = {"ok": False, "failures": [
            {"site": "kgenv-live-import", "error": repr(exc)}]}

    leaf_roster = _check_single_opponent_roster(roster_sites)

    try:
        leaf_bots = assert_bots_constants_match_wheel(bots_sources,
                                                      wheel_source)
    except BotsConstantsMismatch as exc:
        leaf_bots = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    except Exception as exc:  # wheel 通道等环境性失败——判失败不吞错
        leaf_bots = {"ok": False, "error": repr(exc)}

    verdict = {
        "ok": bool(leaf_merge.get("ok") and leaf_roster.get("ok")
                   and leaf_bots.get("ok")),
        "campaign_root": str(_campaign_software_root().parent),
        "roster_truth": _plain(single_opponent_roster()),
        "leaves": {
            "merge_abnormal_reason": leaf_merge,
            "single_opponent_roster": leaf_roster,
            "assert_bots_constants_match_wheel": leaf_bots,
        },
    }
    if strict and not verdict["ok"]:
        raise UnificationError(
            "契约单源化裁决不通过：merge_abnormal_reason="
            f"{leaf_merge.get('ok')} single_opponent_roster="
            f"{leaf_roster.get('ok')} assert_bots_constants_match_wheel="
            f"{leaf_bots.get('ok')}（明细见裁决 dict；strict=False 可取回）")
    return verdict
