---
name: campaign-run
description: 快循环波次化交付编排（D12）：按蓝图里程碑依赖图拓扑分层成波，波内并行派发、波间质量门，验收左移与文档双阶段。当蓝图经用户确认、需要开始工程交付时使用。
---

# K-03 campaign-run：波次化交付编排（D12，2026-08-28 落地）

旧"按角色归并三包单趟派发"已废弃——它丢弃蓝图 milestones 的 depends_on 依赖图
（首场 Kaggriculture 战役实证：m1→m2→m3 实为串行，单趟结构名存实亡）。
**波次不是外加流程，是从蓝图自己的依赖图里长出来的。**

## 前置

- `workspace/blueprint.md` 已过 schema 校验**且经用户确认**（未确认先回 K-02）
- **合规模式闸门（D10）**：`compliance.mode`——prep/apply 正常交付（apply 的申报附件强制进 document 包）；**assist 拒绝启动交付**
- metrics 分片制照旧（角色写 `workspace/<role>/metrics.json`，S-09 汇总；顶层禁写）

## 流程

0. **切阶段**：`init_state --phase deliver --by campaign-run`
1. **波次计算**（协调者做，不派发）：读 milestones 的 `depends_on` 做拓扑分层——
   第 k 波 = 所有依赖均在 1..k-1 波内完成的里程碑；**检测到环 → 停止，回蓝图修依赖**。
   无任何 depends_on 的轻蓝图自然退化为单波（向后兼容，不强制分层）。
2. **逐波执行**（波内并行，波间串行）：
   - **波内派发**：该波里程碑按 owner_role 拆任务包**并行派发**（并发 ≤ budget；任务包含：输入契约、输出目录、所属验收项 ID 前缀、接口契约文件、**返回前 lint/自测 PASS** 条款）
   - **文档双阶段**：document 角色在第 1 波只派"大纲包"（产出报告骨架 + 告知工程角色需积累哪些 metrics 键）；成稿包落在**最后一波**（此时 merge_metrics 已稳定，数字直接回填）
   - **波门**（全过才进下一波，任一不过停在本波）：①该波验收项左移检查 ②可编译/测试/smoke 通过 ③接口契约兑现（双方产物对得上）④metrics 分片有新实测落盘 ⑤JOURNAL 记行 + git commit——**波门即断点**：失败修复限于本波（任务包重派 ≤1 次），前波成果不动
   - **验收左移**（可选但推荐）：波门跑 `python scripts/verify/run_acceptance.py --only <该波验收项id前缀>`——scoped 诊断不烧熔断额度、不产生可开归档闸门的 pass（脚本已硬编码封顶）
3. **末波收拢**：merge_metrics 汇总 → document 成稿（数字只引 `metrics.<role>.<键>`）→ 全量自检
4. JOURNAL 记行 + git commit → 提示执行 `/accept`（**终验必须全量跑，scoped 记录不算数**）

## 变更控制（不变）

任何角色上报范围/接口问题：回蓝图修订，**重新走用户确认**；接口冲突属蓝图缺陷 → 停止交付修蓝图。

## 失败处理

任务包失败重派 ≤1 次；波门两连不过 → 开工单回责任角色并考虑回蓝图；熔断只由全量终验触发。

## 波门质量基线（轻蓝图可直接抄的四阶段）

见 `config/templates/blueprint-template.md` 的"里程碑分层模板"：骨架层→竖切层→完整层→打磨层。
