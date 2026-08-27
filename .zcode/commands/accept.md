---
description: 触发验收节点：执行蓝图验收清单，失败工单路由回责任角色（带熔断）
---

# /accept —— 验收入口

执行流程（K-04 技能与 run_acceptance.py 固化前按 DESIGN.md §3.4 手工编排）：

1. 前置检查：`workspace/blueprint.md` 存在且含 acceptance 清单
2. `python scripts/guard/init_state.py --phase verify --by accept`
3. 以 **acceptor 章程**（`.zcode/agents/acceptor.md`）逐项执行验收清单：
   software/hardware/document 三类记录证据路径；manual 类整理为人工测试清单
4. 结果写 `workspace/acceptance/`（过 acceptance.schema.json）
5. 分支：
   - 全过 → 生成分析报告（对照评审标准自评 + KB-1 历年基准对比），提示可执行 `/archive`
   - 有失败 → 开失败工单（附证据），`init_state --phase deliver` 路由回责任角色修复后重验；
     重试计数 ≥ retry.max 时**熔断**：停止自动重试，向用户呈报失败证据
6. JOURNAL 记一行；git commit

铁律：验收者不修作品；无证据不判定。
