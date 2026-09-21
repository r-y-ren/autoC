"""定位并收集四类最小集文件（golden/灾难局回放/manifest+样例/对手池种子定义）并逐件登记来源，任一类缺失即失败。

上游: R19（详见 fn_docs/responsibility.md）
"""


def collect_gate_golden_files(category_list: list) -> tuple:
    raise NotImplementedError("unimplemented:fn:collect_gate_golden_files")
