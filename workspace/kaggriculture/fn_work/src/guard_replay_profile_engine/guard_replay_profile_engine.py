"""入口校验器：装载 replay_profile 引擎前提取其常量集（价格公式/棚容/城镇需求等）计算指纹并与登记值比对，不符即 fail-closed 抛 EngineFingerprintError。

上游: R5（详见 fn_docs/responsibility.md）
"""


def guard_replay_profile_engine() -> None:
    raise NotImplementedError("unimplemented:fn:guard_replay_profile_engine")
