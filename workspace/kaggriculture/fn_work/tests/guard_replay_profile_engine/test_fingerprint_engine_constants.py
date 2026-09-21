"""fingerprint_engine_constants 真实测试：提取/指纹规范化/篡改敏感性/登记值维护/wheel 交叉比对通道。"""

import re
import types

import pytest

from guard_replay_profile_engine.fingerprint_engine_constants import (
    PINNED_CONSTANT_KEYS,
    ConstantExtractionError,
    cross_check_against_wheel,
    extract_engine_constants,
    fingerprint_engine_constants,
    get_registered_fingerprint,
    reset_registered_fingerprint,
    set_registered_fingerprint,
)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _mirror_module():
    """取（并缓存）旧树 kgenv.replay_profile 模块实例。"""
    from guard_replay_profile_engine.fingerprint_engine_constants import (
        load_replay_profile_module)
    return load_replay_profile_module()


def _copy_source(tamper: dict | None = None,
                 drop: tuple[str, ...] = ()) -> types.SimpleNamespace:
    """镜像常量的副本注入源：默认与真模块逐键同值，可篡改/可缺键。"""
    values = extract_engine_constants(_mirror_module())
    for key in drop:
        values.pop(key)
    if tamper:
        values.update(tamper)
    return types.SimpleNamespace(**values)


# --------------------------------------------------------------------------- #
# 提取与指纹
# --------------------------------------------------------------------------- #
def test_extract_selects_registered_key_set():
    values = extract_engine_constants(None)
    assert set(values) == set(PINNED_CONSTANT_KEYS)
    assert len(PINNED_CONSTANT_KEYS) == 16  # 登记清单五类共 16 键


def test_fingerprint_deterministic_hex_and_registered_match():
    first = fingerprint_engine_constants(None)
    second = fingerprint_engine_constants(None)
    assert first == second
    assert _HEX64.match(first)
    # 正常装载下镜像指纹即登记值（建立时点锚定）
    assert first == get_registered_fingerprint()


def test_fingerprint_insensitive_to_dict_insertion_order():
    # 副本注入：S_MARKET_PARAMS 逆序重建（同值不同插入序）-> 指纹不变
    module = _mirror_module()
    reversed_params = {k: module.S_MARKET_PARAMS[k]
                       for k in reversed(list(module.S_MARKET_PARAMS))}
    copy = _copy_source(tamper={"S_MARKET_PARAMS": reversed_params})
    assert (fingerprint_engine_constants(copy)
            == fingerprint_engine_constants(module))


def test_fingerprint_tamper_copy_injection_changes_digest():
    module = _mirror_module()
    baseline = fingerprint_engine_constants(module)
    tampered_price = dict(module.S_MARKET_PARAMS)
    tampered_price["WHEAT"] = {**tampered_price["WHEAT"], "base": 26}
    assert (fingerprint_engine_constants(
        _copy_source(tamper={"S_MARKET_PARAMS": tampered_price})) != baseline)
    # 容量类篡改（shedCapacity）同样必须改变指纹
    tampered_cfg = dict(module.S_DEFAULT_CONFIG)
    tampered_cfg["shedCapacity"] = 101
    assert (fingerprint_engine_constants(
        _copy_source(tamper={"S_DEFAULT_CONFIG": tampered_cfg})) != baseline)
    # 城镇需求类篡改（S_MAX_SHOP_INSTANCES）同样必须改变指纹
    assert (fingerprint_engine_constants(
        _copy_source(tamper={"S_MAX_SHOP_INSTANCES":
                            module.S_MAX_SHOP_INSTANCES + 1})) != baseline)


def test_missing_pinned_key_raises_extraction_error():
    with pytest.raises(ConstantExtractionError, match="缺少应钉键"):
        fingerprint_engine_constants(_copy_source(drop=("S_HINGE_GAIN",)))


# --------------------------------------------------------------------------- #
# 登记值维护（升版 wheel 显式重登记接口）
# --------------------------------------------------------------------------- #
def test_registered_fingerprint_maintenance_roundtrip():
    original = get_registered_fingerprint()
    try:
        fake = "ab" * 32
        set_registered_fingerprint(fake)
        assert get_registered_fingerprint() == fake
        reset_registered_fingerprint()
        assert get_registered_fingerprint() == original
    finally:
        reset_registered_fingerprint()


def test_set_registered_fingerprint_rejects_non_hex64():
    with pytest.raises(ValueError):
        set_registered_fingerprint("not-a-sha256")


def test_reregistration_flow_on_mirror_own_key():
    """登记值更新流程：镜像自有键变更 -> 红 -> 显式重登记 -> 新指纹生效。"""
    module = _mirror_module()
    tampered = {"S_UNIT_OPS_TRACKED": (*module.S_UNIT_OPS_TRACKED, "NEW_OP")}
    try:
        new_fp = fingerprint_engine_constants(
            _copy_source(tamper=tampered))
        assert new_fp != get_registered_fingerprint()
        set_registered_fingerprint(new_fp)  # 显式重登记
        assert get_registered_fingerprint() == new_fp
    finally:
        reset_registered_fingerprint()


# --------------------------------------------------------------------------- #
# wheel 侧交叉比对通道（可跑则跑，不可跑记 skip+原因）
# --------------------------------------------------------------------------- #
def test_cross_check_against_wheel_channel():
    cc = cross_check_against_wheel(None)
    if cc["skipped"]:
        pytest.skip("wheel 通道不可用: " + str(cc["skip_reason"]))
    assert cc["ok"] is True
    assert len(cc["comparable_keys"]) == 14
    assert cc["mismatches"] == []
    assert _HEX64.match(cc["wheel_fingerprint"])
    assert cc["wheel_source"].endswith("kaggriculture.py")


def test_cross_check_detects_mirror_drift_via_injection():
    cc = cross_check_against_wheel(
        _copy_source(tamper={"S_HINGE_GAIN": 99.0}))
    if cc["skipped"]:
        pytest.skip("wheel 通道不可用: " + str(cc["skip_reason"]))
    assert cc["ok"] is False
    assert [m["key"] for m in cc["mismatches"]] == ["S_HINGE_GAIN"]
