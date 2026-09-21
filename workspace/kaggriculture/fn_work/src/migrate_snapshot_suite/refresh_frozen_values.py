"""仅更新受 R2/R3 修复影响的冻结值（select 名字序→值序、bench 错位→seated），每处留旧值/新值/原因双口径注记，其余冻结值零改动。

上游: R1（详见 fn_docs/responsibility.md）
"""


def refresh_frozen_values(impact_list: list) -> tuple:
    raise NotImplementedError("unimplemented:fn:refresh_frozen_values")
