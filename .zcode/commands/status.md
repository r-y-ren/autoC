---
description: 查看当前阶段、战役状态、熔断计数与最近日志
---

# /status —— 状态播报

立即执行（全部只读）：

1. 读取并解读 `.flow/state.json`：当前 phase（idle/collect/decide/deliver/verify/archive）、
   campaign、retry 计数与熔断标记（tripped=true 时优先醒目提示并说明升级人工的出口）
2. 读取 `workspace/JOURNAL.md` 最后 5 行，概括战役进展
3. `git log --oneline -3` 展示最近提交
4. 若 `.flow/state.json` 缺失：提示执行 `python scripts/guard/init_state.py` 引导（守卫当前处于 fail-closed）

输出格式：一张紧凑状态卡（阶段/战役/重试/最近动作/建议下一步）。
