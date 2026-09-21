"""修正 2 处 Windows-only 断言（normcase 大小写折叠、Path("C:/…").is_absolute）为双平台语义。

上游: R6, R20（详见 fn_docs/responsibility.md）
"""


def relax_platform_assertions(test_sources) -> None:
    raise NotImplementedError("unimplemented:fn:relax_platform_assertions")
