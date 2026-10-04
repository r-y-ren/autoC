"""入口校验器：装载 replay_profile 引擎前提取其常量集（价格公式/棚容/城镇需求等）计算指纹并与登记值比对，不符即 fail-closed 抛 EngineFingerprintError。

上游: R5（详见 fn_docs/responsibility.md）

实现要点：
- 装载期自检（无参调用即跑）：提取（经 fingerprint_engine_constants 的选定
  键集与规范化序列化）-> 与登记指纹比对 -> 不符抛 EngineFingerprintError；
  随后走 wheel 侧真值交叉比对（economy.py re-export 先例通道，14 个可比对
  键逐键核对）——语义漂移即红，双重门：未经显式重登记的镜像改动被登记指纹
  门拦下，绕过登记的改动被 wheel 真值门拦下（R5 缺陷本体=镜像与权威引擎
  静默漂移无人看护）。
- fail-closed 细则：登记指纹不符必抛；wheel 交叉比对"跑且不符"必抛；
  wheel 不可 import 仅记 skip+原因（报告字段留痕，不误伤无 wheel 的最小
  环境——此时登记指纹仍是唯一主门）。
- skip 选项仅用于测试注入（True=直接返回 skipped 报告，不做任何比对）；
  constants_source 亦为测试注入位（None=默认装载旧树 kgenv.replay_profile，
  只读消费，见叶模块 docstring）。
- 调用方：replay_profile 消费者（corpus/画像/法证件）——在装载镜像引擎
  前调用本入口，通过才继续。
"""

from __future__ import annotations

from guard_replay_profile_engine.fingerprint_engine_constants import (
    EngineFingerprintError,
    cross_check_against_wheel,
    fingerprint_engine_constants,
    get_registered_fingerprint,
)

__all__ = ["guard_replay_profile_engine", "EngineFingerprintError"]


def _drift_hint(constants_source) -> str:
    """登记指纹不符时的人读线索：借 wheel 通道点名差异键（不可用则如实说明）。"""
    cc = cross_check_against_wheel(constants_source)
    if cc["skipped"]:
        return "（wheel 通道不可用，无法点名差异键: " + cc["skip_reason"] + "）"
    keys = [m["key"] for m in cc["mismatches"]]
    if keys:
        return "（wheel 真值点名差异键: " + ", ".join(keys) + "）"
    return ("（wheel 交叉比对全绿：漂移落在 wheel 无对应物的镜像自有键上，"
            "即 S_FAILS / S_UNIT_OPS_TRACKED）")


def guard_replay_profile_engine(*, skip: bool = False,
                                constants_source=None,
                                wheel_cross_check: bool = True) -> dict:
    """装载期自检入口：镜像常量指纹 vs 登记值 + wheel 真值交叉比对。

    Args:
        skip: 仅测试注入用；True=不做任何比对直接返回 skipped 报告。
        constants_source: 常量源注入位（测试用）；None=默认装载旧树
            kgenv.replay_profile（只读）。
        wheel_cross_check: 是否追加 wheel 侧交叉比对（默认 True）。

    Returns:
        审计报告 dict：ok / skipped / fingerprint / registered_fingerprint /
        fingerprint_ok / wheel_cross_check（其内含 skipped/ok/mismatches/
        wheel_fingerprint/wheel_source 或 skip_reason）。

    Raises:
        EngineFingerprintError: 登记指纹不符，或 wheel 交叉比对跑且不符
        （fail-closed；消息附两侧指纹与差异键线索）。
        ConstantExtractionError: 常量源不可装载/键缺失（经叶模块传播）。
    """
    if skip:
        return {"ok": True, "skipped": True, "fingerprint": None,
                "registered_fingerprint": get_registered_fingerprint(),
                "fingerprint_ok": None, "wheel_cross_check": None}

    fingerprint = fingerprint_engine_constants(constants_source)
    registered = get_registered_fingerprint()
    report: dict = {
        "ok": True, "skipped": False,
        "fingerprint": fingerprint,
        "registered_fingerprint": registered,
        "fingerprint_ok": fingerprint == registered,
        "wheel_cross_check": None,
    }

    if fingerprint != registered:
        raise EngineFingerprintError(
            "replay_profile 引擎常量指纹与登记值不符（fail-closed）: "
            f"actual={fingerprint} registered={registered} "
            + _drift_hint(constants_source)
            + "；若为升版 wheel 的合法变更，走显式重登记流程"
            "（更新镜像 -> cross_check 全绿 -> 重登记 -> 固化源码默认值）。")

    if wheel_cross_check:
        cc = cross_check_against_wheel(constants_source)
        report["wheel_cross_check"] = cc
        if not cc["skipped"] and not cc["ok"]:
            keys = ", ".join(m["key"] for m in cc["mismatches"])
            raise EngineFingerprintError(
                "replay_profile 引擎常量与 wheel 真值漂移（fail-closed）: "
                f"差异键: {keys}；逐键明细见报告 wheel_cross_check."
                f"mismatches；wheel 源: {cc['wheel_source']}。"
                "镜像必须与权威引擎逐键一致，禁止以重登记方式放行漂移。")

    return report
