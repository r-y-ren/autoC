"""薄装载器：按固定拓扑序 exec 十模块+planner 进共享命名空间，装载窗内急切导入 planner.runtime，重绑最后 callable=agent（死码支不迁）。

上游: R1, R10（详见 fn_docs/responsibility.md）
"""


def load_agent_modules(package_root) -> tuple:
    raise NotImplementedError("unimplemented:fn:load_agent_modules")
