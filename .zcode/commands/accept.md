---
description: 触发验收节点（v2 可选终检工具）：执行蓝图验收清单，失败项人工修复后重验（带熔断）
---

# /accept —— 验收入口（v2）

执行流程（编排细节见 `.zcode/skills/accept-run/SKILL.md`；执行器 `scripts/verify/run_acceptance.py`）：

1. 前置检查：战役已登记；`workspace/<cid>/blueprint.md` 存在且含 acceptance 清单（蓝图为项目自用契约；`/attack` 方案书非闸门）
2. `python scripts/guard/init_state.py --campaign <cid> --phase verify --by accept`
3. 以 **acceptor 章程**（`.zcode/agents/acceptor.md`）逐项执行验收清单：
   software/hardware/document 三类记录证据路径；manual 类整理为人工测试清单
4. 结果写 `workspace/<cid>/acceptance/`（过 acceptance.schema.json）
5. 分支：
   - 全过 → 生成分析报告（对照评审标准自评 + KB-1 历年基准对比），提示可执行 `/archive`
   - 有失败 → 开失败工单（附证据），`python scripts/guard/init_state.py --campaign <cid> --phase deliver --by accept` 退回
     **人工修复（v2：修复由人工/fn-ladder 进行）**后重验；重试计数 ≥ retry.max 时**熔断**：停止自动重试，向用户呈报失败证据
6. JOURNAL 记一行；项目仓库 commit

铁律：验收者不修作品；无证据不判定。
