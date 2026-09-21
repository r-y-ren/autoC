"""guard_replay_profile_engine 真实测试：正常装载通过/篡改常量红/登记值更新流程/skip 注入/wheel 双重门。"""

import types

import pytest

from guard_replay_profile_engine.fingerprint_engine_constants import (
    PINNED_CONSTANT_KEYS,
    fingerprint_engine_constants,
    get_registered_fingerprint,
    load_replay_profile_module,
    reset_registered_fingerprint,
    set_registered_fingerprint,
)
from guard_replay_profile_engine.guard_replay_profile_engine import (
    EngineFingerprintError,
    guard_replay_profile_engine,
)


@pytest.fixture
def mirror():
    """已装载的旧树镜像模块实例（monkeypatch 目标；守卫与其共享同一实例）。"""
    return load_replay_profile_module()


# --------------------------------------------------------------------------- #
# ① 正常装载 -> 指纹匹配 -> 通过
# --------------------------------------------------------------------------- #
def test_normal_load_matches_registered_and_passes(mirror):
    report = guard_replay_profile_engine()
    assert report["ok"] is True
    assert report["skipped"] is False
    assert report["fingerprint"] == get_registered_fingerprint()
    assert report["fingerprint_ok"] is True
    cc = report["wheel_cross_check"]
    if cc is not None and cc["skipped"]:
        pytest.skip("wheel 通道不可用: " + str(cc["skip_reason"]))
    assert cc["ok"] is True


# --------------------------------------------------------------------------- #
# ② 篡改常量（monkeypatch / 副本注入）-> 红
# --------------------------------------------------------------------------- #
def test_tampered_price_constant_raises(monkeypatch, mirror):
    monkeypatch.setattr(mirror, "S_HINGE_GAIN", 99.0)
    with pytest.raises(EngineFingerprintError, match="登记值不符"):
        guard_replay_profile_engine()


def test_tampered_capacity_constant_raises(monkeypatch, mirror):
    tampered_cfg = dict(mirror.S_DEFAULT_CONFIG)
    tampered_cfg["shedCapacity"] = 200
    monkeypatch.setattr(mirror, "S_DEFAULT_CONFIG", tampered_cfg)
    with pytest.raises(EngineFingerprintError, match="登记值不符"):
        guard_replay_profile_engine()


def test_tampered_copy_injection_raises(mirror):
    """副本注入变体：不碰真模块，经 constants_source 注入篡改副本。"""
    forged = types.SimpleNamespace(
        **{key: getattr(mirror, key) for key in PINNED_CONSTANT_KEYS})
    forged.S_MARKET_PARAMS = {k: dict(v) for k, v in mirror.S_MARKET_PARAMS.items()}
    forged.S_MARKET_PARAMS["WHEAT"] = {
        **forged.S_MARKET_PARAMS["WHEAT"], "base": 26}
    with pytest.raises(EngineFingerprintError, match="登记值不符"):
        guard_replay_profile_engine(constants_source=forged)


# --------------------------------------------------------------------------- #
# ③ 登记值更新流程（升版 wheel 显式重登记）
# --------------------------------------------------------------------------- #
def test_registration_update_flow_on_mirror_own_key(monkeypatch, mirror):
    """镜像自有键（wheel 无对应物）变更：红 -> 显式重登记 -> 绿。"""
    monkeypatch.setattr(mirror, "S_UNIT_OPS_TRACKED",
                        (*mirror.S_UNIT_OPS_TRACKED, "NEW_OP"))
    with pytest.raises(EngineFingerprintError, match="登记值不符"):
        guard_replay_profile_engine()
    try:
        set_registered_fingerprint(fingerprint_engine_constants())
        report = guard_replay_profile_engine()
        assert report["ok"] is True
        assert report["fingerprint_ok"] is True
        cc = report["wheel_cross_check"]
        if cc is not None and not cc["skipped"]:
            assert cc["ok"] is True  # 自有键漂移不应触碰 wheel 可比对集
    finally:
        reset_registered_fingerprint()


def test_rogue_reregistration_of_comparable_drift_still_raises(monkeypatch, mirror):
    """绕过流程的重登记放不了行：可比对键漂移即使重登记，wheel 真值门仍红。"""
    tampered = {k: dict(v) for k, v in mirror.S_MARKET_PARAMS.items()}
    tampered["CARROT"] = {**tampered["CARROT"], "base": 36}
    monkeypatch.setattr(mirror, "S_MARKET_PARAMS", tampered)
    try:
        set_registered_fingerprint(fingerprint_engine_constants())
        if _wheel_available():
            with pytest.raises(EngineFingerprintError, match="wheel 真值漂移"):
                guard_replay_profile_engine()
        else:
            report = guard_replay_profile_engine()
            assert report["wheel_cross_check"]["skipped"] is True
    finally:
        reset_registered_fingerprint()


def _wheel_available() -> bool:
    try:
        from kaggle_environments.envs.kaggriculture import kaggriculture  # noqa: F401
        return True
    except ImportError:
        return False


# --------------------------------------------------------------------------- #
# ④ skip 选项（仅测试注入）
# --------------------------------------------------------------------------- #
def test_skip_option_returns_without_checking(monkeypatch, mirror):
    monkeypatch.setattr(mirror, "S_HINGE_GAIN", 99.0)  # 篡改在场也不比对
    report = guard_replay_profile_engine(skip=True)
    assert report["skipped"] is True
    assert report["ok"] is True
    assert report["fingerprint"] is None
