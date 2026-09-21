"""离线基准主流程（14 局×注入点×双口径裁决：主口径 DTSP≥反应式、参考口径 history 代差修正），rollout 全部经 seated 通道，引擎异常 fail-closed 记异常局。

上游: R2（详见 fn_docs/responsibility.md）
"""


def run_official_bench(injection_config: dict, opponent_models: list, me_seat: int) -> dict:
    raise NotImplementedError("unimplemented:fn:run_official_bench")
