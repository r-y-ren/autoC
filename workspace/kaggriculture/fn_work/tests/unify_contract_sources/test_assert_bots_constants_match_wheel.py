"""assert_bots_constants_match_wheel 真实测试：正常绿 + 篡改（注入/monkeypatch）红。"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from unify_contract_sources import assert_bots_constants_match_wheel as uamw
from unify_contract_sources.assert_bots_constants_match_wheel import (
    BOTS_CONSTANT_MODULES,
    BotsConstantsMismatch,
    WheelChannelUnavailable,
    assert_bots_constants_match_wheel,
    load_bots_constants_module,
)

# 注入用最小真值（口径同 wheel：五作物/三牲畜）
_FAKE_CROPS = {
    "WHEAT": {"seed": 10, "first_yield_day": 2, "max_yield_day": 4,
              "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT": {"seed": 20, "first_yield_day": 2, "max_yield_day": 3,
               "interval": 0, "max_yield": 4, "ongoing": False},
}
_FAKE_ANIMALS = {
    "COW": {"cost": 400, "structure": "PASTURE", "first_yield_day": 8,
            "interval": 2, "max_held": 6, "product": "MILK"},
}


def _fake_sources(**overrides):
    sources = {name: SimpleNamespace(
        CROPS_INFO={"WHEAT": dict(_FAKE_CROPS["WHEAT"])},
        ANIMALS_INFO={"COW": dict(_FAKE_ANIMALS["COW"])})
        for name in BOTS_CONSTANT_MODULES}
    sources.update(overrides)
    return sources


def _fake_wheel(crops=None, animals=None):
    return SimpleNamespace(CROPS=crops if crops is not None else _FAKE_CROPS,
                           ANIMALS=(animals if animals is not None
                                    else _FAKE_ANIMALS))


# --------------------------------------------------------------------------- #
# 正常绿：真旧树五文件 vs 真 wheel
# --------------------------------------------------------------------------- #
def test_green_against_real_tree_and_wheel():
    report = assert_bots_constants_match_wheel()
    assert report["ok"] is True
    assert report["mismatches"] == []
    assert report["checked_modules"] == list(BOTS_CONSTANT_MODULES)
    # 旧树五文件并集覆盖 wheel 全表（baseline/online_pool 抄全量，其余抄子集）
    assert sorted(report["coverage"]["CROPS"]) == [
        "CARROT", "MELON", "STRAWBERRY", "TOMATO", "WHEAT"]
    assert sorted(report["coverage"]["ANIMALS"]) == ["COW", "GOOSE", "SHEEP"]
    assert report["crops_entries"]["baseline"] == 5
    assert report["crops_entries"]["online_pool"] == 5
    assert report["animals_entries"]["expansionist"] == 1  # 只抄 GOOSE
    assert report["animals_entries"]["melon_hoarder"] == 0  # 无动物面
    assert report["wheel_source"].endswith("kaggriculture.py")


def test_injected_sources_green():
    report = assert_bots_constants_match_wheel(_fake_sources(),
                                               _fake_wheel())
    assert report["ok"] is True


# --------------------------------------------------------------------------- #
# 篡改变红：值漂移 / 条目缺失 / 模块缺失
# --------------------------------------------------------------------------- #
def test_injected_tampered_value_red():
    tampered = SimpleNamespace(
        CROPS_INFO={"WHEAT": {**_FAKE_CROPS["WHEAT"], "seed": 11}},
        ANIMALS_INFO={"COW": dict(_FAKE_ANIMALS["COW"])})
    with pytest.raises(BotsConstantsMismatch, match="seed"):
        assert_bots_constants_match_wheel(_fake_sources(baseline=tampered),
                                          _fake_wheel())


def test_injected_missing_item_red():
    ghost = SimpleNamespace(
        CROPS_INFO={"WHEAT": dict(_FAKE_CROPS["WHEAT"]),
                    "BAMBOO": {"seed": 1}},
        ANIMALS_INFO={})
    with pytest.raises(BotsConstantsMismatch, match="BAMBOO"):
        assert_bots_constants_match_wheel(_fake_sources(cow_baron=ghost),
                                          _fake_wheel())


def test_injected_module_missing_red():
    sources = _fake_sources()
    del sources["online_pool"]
    with pytest.raises(BotsConstantsMismatch, match="online_pool"):
        assert_bots_constants_match_wheel(sources, _fake_wheel())


def test_injected_wheel_drift_red():
    drifted = {k: {**v, "seed": v["seed"] + 1}
               for k, v in _FAKE_CROPS.items()}
    with pytest.raises(BotsConstantsMismatch, match="WHEAT"):
        assert_bots_constants_match_wheel(_fake_sources(), _fake_wheel(drifted))


# --------------------------------------------------------------------------- #
# monkeypatch 篡改真模块即红（装载通道返回 sys.modules 同一实例）
# --------------------------------------------------------------------------- #
def test_monkeypatch_tamper_on_real_module_red(monkeypatch):
    module = load_bots_constants_module("cow_baron")
    tampered = {"WHEAT": {**module.CROPS_INFO["WHEAT"], "max_yield": 7}}
    monkeypatch.setattr(module, "CROPS_INFO", tampered)
    with pytest.raises(BotsConstantsMismatch, match="max_yield"):
        assert_bots_constants_match_wheel()  # 缺省装载必须看到同一实例


def test_monkeypatch_tamper_restores_green(monkeypatch):
    module = load_bots_constants_module("expansionist")
    tampered = {"GOOSE": {**module.ANIMALS_INFO["GOOSE"], "cost": 301}}
    monkeypatch.setattr(module, "ANIMALS_INFO", tampered)
    with pytest.raises(BotsConstantsMismatch):
        assert_bots_constants_match_wheel()
    monkeypatch.undo()
    assert assert_bots_constants_match_wheel()["ok"] is True


# --------------------------------------------------------------------------- #
# wheel 通道 fail-closed
# --------------------------------------------------------------------------- #
def test_wheel_channel_unavailable_fail_closed(monkeypatch):
    def _raise():
        raise WheelChannelUnavailable("channel down (test)")

    monkeypatch.setattr(uamw, "load_wheel_constants", _raise)
    with pytest.raises(WheelChannelUnavailable, match="channel down"):
        assert_bots_constants_match_wheel()
