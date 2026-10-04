"""unify_contract_sources 真实测试：顶层编排自检（三叶+等值断言集）与裁决口径。

活跑用例依赖旧树只读 import 与 wheel 真值通道（均属战役锁定的评估侧依赖）；
漂移路径用注入参数离线复现（不碰旧树文件）。
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from unify_contract_sources import single_opponent_roster as roster
from unify_contract_sources.assert_bots_constants_match_wheel import (
    BotsConstantsMismatch,
)
from unify_contract_sources.unify_contract_sources import (
    UnificationError,
    unify_contract_sources,
)


def _fake_roster_sites(**overrides):
    """等值基线（取自单源模块真值），覆写任一键即制造漂移。"""
    sites = {
        "bots.STRONG_OPPONENTS": roster.STRONG_OPPONENTS,
        "bots.ONLINE_STYLE_OPPONENTS": roster.ONLINE_STYLE_OPPONENTS,
        "eval_contract.STANDARD_MATRIX_ORDER": roster.STANDARD_MATRIX_ORDER,
        "regression.EXPECTED_ELO_ORDER": list(roster.EXPECTED_ELO_ORDER),
        "regression.FROZEN_POOL": set(roster.FROZEN_POOL),
        "holdout_contract.matrix_orders_v1_v5": dict(
            roster.HOLDOUT_MATRIX_ORDERS),
    }
    sites.update(overrides)
    return sites


# --------------------------------------------------------------------------- #
# 活跑：真实旧树 + 真 wheel，全绿裁决
# --------------------------------------------------------------------------- #
def test_live_run_full_verdict_green():
    verdict = unify_contract_sources(strict=False)
    assert verdict["ok"] is True
    leaves = verdict["leaves"]
    # 叶 1：异常局判定双源对照
    merge = leaves["merge_abnormal_reason"]
    assert merge["ok"] is True and merge["failures"] == []
    assert merge["by_kind"] == {"normal": 2, "parity_red": 11,
                                "union_red": 7, "eval_kwarg": 2,
                                "export_only": 2}
    assert set(merge["union_divergence_surface"]) == {
        "players_identical", "rewards_bool", "rewards_inf",
        "missing_seed", "missing_seat", "missing_seed_domain", "seat_invalid"}
    # 叶 2：名册 7 站点等值（kgenv 活 import 5 + scripts 源文本 2）
    sites = leaves["single_opponent_roster"]["sites"]
    assert set(sites) == {
        "bots.STRONG_OPPONENTS", "bots.ONLINE_STYLE_OPPONENTS",
        "eval_contract.STANDARD_MATRIX_ORDER",
        "regression.EXPECTED_ELO_ORDER", "regression.FROZEN_POOL",
        "holdout_contract.matrix_orders_v1_v5",
        "scripts/iterate_gate.REQUIRED_OPPONENTS",
        "scripts/check_eval_contract.REQUIRED_OPPONENTS"}
    for site, detail in sites.items():
        assert detail["ok"] is True, site
    assert sites["scripts/iterate_gate.REQUIRED_OPPONENTS"]["channel"] == (
        "source_text")
    assert sites["scripts/check_eval_contract.REQUIRED_OPPONENTS"][
        "channel"] == "source_text"
    # 叶 3：bots 常量 vs wheel
    assert leaves["assert_bots_constants_match_wheel"]["ok"] is True
    # 裁决携带名册真值快照（_plain 化：tuple/frozenset -> 排序表）
    assert verdict["roster_truth"]["opponent_pool_11"] == list(
        roster.OPPONENT_POOL_11)
    assert set(verdict["roster_truth"]["frozen_pool"]) == set(
        roster.FROZEN_POOL)


def test_live_run_strict_default_does_not_raise():
    verdict = unify_contract_sources()  # strict=True 缺省：全绿即不抛
    assert verdict["ok"] is True


# --------------------------------------------------------------------------- #
# 漂移路径：注入即红（strict 抛 / 非 strict 裁决记录）
# --------------------------------------------------------------------------- #
def test_roster_drift_strict_raises_and_verdict_records():
    drifted = _fake_roster_sites(
        **{"regression.EXPECTED_ELO_ORDER":
           ["submission", "baseline_wheat", "greedy_carrot", "starter",
            "random", "pass"]})  # m0 旧序（pass/random 交换）——漂移面
    with pytest.raises(UnificationError):
        unify_contract_sources(roster_sites=drifted)
    verdict = unify_contract_sources(strict=False, roster_sites=drifted)
    assert verdict["ok"] is False
    failures = verdict["leaves"]["single_opponent_roster"]["failures"]
    assert failures and failures[0]["site"] == "regression.EXPECTED_ELO_ORDER"


def test_merge_leaf_drift_detected():
    # 伪 eval 实现（恒绿）：parity_red 面上与 merged 分叉 -> 叶 1 失败
    def _always_normal(game, **kwargs):
        return None

    verdict = unify_contract_sources(strict=False, eval_reason=_always_normal)
    assert verdict["leaves"]["merge_abnormal_reason"]["ok"] is False
    assert verdict["ok"] is False
    with pytest.raises(UnificationError):
        unify_contract_sources(eval_reason=_always_normal)


def test_bots_drift_detected():
    tampered = SimpleNamespace(  # seed 11 vs 真 wheel 真值 10
        CROPS_INFO={"WHEAT": {"seed": 11, "first_yield_day": 2,
                              "max_yield_day": 4, "interval": 0,
                              "max_yield": 6, "ongoing": False}},
        ANIMALS_INFO={})
    bots_sources = {name: SimpleNamespace(CROPS_INFO={}, ANIMALS_INFO={})
                    for name in ("baseline", "cow_baron", "melon_hoarder",
                                 "expansionist", "online_pool")}
    bots_sources["baseline"] = tampered
    verdict = unify_contract_sources(strict=False,
                                     bots_sources=bots_sources)
    leaf = verdict["leaves"]["assert_bots_constants_match_wheel"]
    assert leaf["ok"] is False
    assert "BotsConstantsMismatch" in leaf["error"]
    assert verdict["ok"] is False


def test_missing_site_anchor_detected():
    # 站点锚丢失（kgenv 站点值不可取）——判失败不吞错
    verdict = unify_contract_sources(
        strict=False, roster_sites=_fake_roster_sites(**{
            "holdout_contract.matrix_orders_v1_v5": {}}))
    assert verdict["ok"] is False
    sites = verdict["leaves"]["single_opponent_roster"]["sites"]
    assert sites["holdout_contract.matrix_orders_v1_v5"]["ok"] is False
