"""gym_env/llm_provider 移实验区（dormant 标注）、economy/redlines 移测试资产区、主线 import 图断言收口（主线依赖残留即失败）。

上游: R13, R14（详见 fn_docs/responsibility.md）
"""


def downgrade_dormant_assets() -> None:
    raise NotImplementedError("unimplemented:fn:downgrade_dormant_assets")
