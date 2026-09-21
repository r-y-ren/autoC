"""影子遥测+sink 注入（异常全吞旁路），按现状迁移，永不抛。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def record_shadow_telemetry(event: dict) -> None:
    raise NotImplementedError("unimplemented:fn:record_shadow_telemetry")
