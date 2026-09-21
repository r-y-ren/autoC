"""等价判据执行器：封装"黄金哈希复验+快照套件复跑+旗关等价探针"三件的调用与结果汇总，输出单页裁决（pass/fail+逐项 name/passed/value），只编排不实现判据本体，任一判据不可执行即整体 fail（fail-closed）。

上游: R1（详见 fn_docs/responsibility.md）
"""


def run_equivalence_gate(agent_load_path, gate_options=None) -> list:
    raise NotImplementedError("unimplemented:fn:run_equivalence_gate")
