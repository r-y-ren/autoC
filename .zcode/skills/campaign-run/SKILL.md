---
name: campaign-run
description: 快循环交付编排：按已确认蓝图拆任务包，并发派发 Software/Hardware，汇合后汇总指标并派发 Document。当蓝图经用户确认、需要开始工程交付时使用。
---

# K-03 campaign-run：并发交付编排

## 前置

- `workspace/blueprint.md` 已过 schema 校验**且经用户确认**（未确认先回 K-02）
- K-03 前置项已裁决（DESIGN §6.2 处置记录）：指标采用**分片制**——角色各写 `workspace/<role>/metrics.json`，顶层 `workspace/metrics.json` 由 merge_metrics.py 生成（守卫已拦角色直写）；角色身份级守卫不引入（钩子负载无调用者身份，全局 active_role 破坏并发），跨角色越界靠章程 + git 审计

## 流程

1. **任务包化**：从蓝图 milestones 按 owner_role 归并为三个任务包（software/hardware/document），每个任务包注明：输入契约、输出目录、所属验收项 ID、接口契约文件
2. **切阶段**：`python scripts/guard/init_state.py --phase deliver --by campaign-run`
3. **并发派发**：Software 与 Hardware 两个子 agent **并行**（各自章程 `.zcode/agents/`；提示：metrics 只写各自分片；测试不过=未完成；禁改蓝图）
4. **汇合**：收拢两包结构化结论 → `python scripts/verify/merge_metrics.py` 生成顶层指标
5. **文档派发**：Document 子 agent 消费工程产物 + 汇总指标（数字只能引 `metrics.<role>.<键>`）
6. JOURNAL 记行 + git commit → 提示执行 `/accept`

## 变更控制

- 任何角色上报范围/接口问题：回到蓝图修订，**重新走用户确认**后才继续——不允许边做边改
- 角色上报缺输入：协调者补齐后重派该任务包，不整体重来

## 失败处理

任务包失败重派 ≤1 次；接口冲突属蓝图缺陷 → 停止交付，修蓝图。
