---
name: campaign-run
description: 快循环波次化交付编排（D12）：按蓝图里程碑依赖图拓扑分层成波，波内并行派发、波间质量门，验收左移与文档双阶段。当蓝图经用户确认、需要开始工程交付时使用。v2 起多战役并行，全程带 --campaign <cid>。
---

# K-03 campaign-run：波次化交付编排（D12，2026-08-28 落地；v2 多战役 2026-09-01）

旧"按角色归并三包单趟派发"已废弃——它丢弃蓝图 milestones 的 depends_on 依赖图
（首场 Kaggriculture 战役实证：m1→m2→m3 实为串行，单趟结构名存实亡）。
**波次不是外加流程，是从蓝图自己的依赖图里长出来的。**

## 战役标识（v2 多战役）

- 本技能全程作用于**单个战役** `<cid>`；其他战役可并行推进，互不干扰。
- 战役在决策阶段已登记（`init_state --campaign <cid> --phase decide`，root=workspace/<cid>/）。
  （kaggriculture 已于 2026-09-01 迁入标准布局 workspace/kaggriculture/；守卫兼容层仍支持 legacy root=workspace 的登记读取。）
- 所有阶段流转 / 验收 / 汇总命令都带 `--campaign <cid>`；蓝图 cmd 内的路径写战役根全路径。

## 前置

- `workspace/<cid>/blueprint.md` 已过 schema 校验**且经用户确认**（未确认先回 K-02）
- **合规模式闸门（D10）**：`compliance.mode`——prep/apply 正常交付（apply 的申报附件强制进 document 包）；**assist 拒绝启动交付**
- metrics 分片制照旧（角色写 `<战役根>/<role>/metrics.json`，S-09 汇总；战役根顶层禁写）
- 外部材料归宿：任何角色在交付期抓取/下载的规则、数据集、第三方包、情报摘要统一写 `<战役根>/references/`（子目录与登记规则见其 README/INDEX），任务包里须写明这一点，禁止散落到工程目录

## 流程

0. **切阶段**：`init_state --campaign <cid> --phase deliver --by campaign-run`
1. **波次计算**（协调者做，不派发）：读 milestones 的 `depends_on` 做拓扑分层——
   第 k 波 = 所有依赖均在 1..k-1 波内完成的里程碑；**检测到环 → 停止，回蓝图修依赖**。
   无任何 depends_on 的轻蓝图自然退化为单波（向后兼容，不强制分层）。
2. **逐波执行**（波内并行，波间串行）：
   - **波内派发**：该波里程碑按 owner_role 拆任务包**并行派发**（并发 ≤ budget；任务包含：输入契约、**输出目录=战役根下对应角色目录**、所属验收项 ID 前缀、接口契约文件、**返回前 lint/自测 PASS** 条款）
   - **文档双阶段**：document 角色在第 1 波只派"大纲包"（产出报告骨架 + 告知工程角色需积累哪些 metrics 键）；成稿包落在**最后一波**（此时 merge_metrics 已稳定，数字直接回填）
   - **波门**（全过才进下一波，任一不过停在本波）：①该波验收项左移检查 ②可编译/测试/smoke 通过 ③接口契约兑现（双方产物对得上）④metrics 分片有新实测落盘 ⑤JOURNAL 记行 + git commit——**波门即断点**：失败修复限于本波（任务包重派 ≤1 次），前波成果不动
   - **验收左移**（可选但推荐）：波门跑 `python scripts/verify/run_acceptance.py --campaign <cid> --only <该波验收项id前缀>`——scoped 诊断不烧熔断额度、不产生可开归档闸门的 pass（脚本已硬编码封顶）
3. **末波收拢**：`merge_metrics --campaign <cid>` 汇总 → document 成稿（数字只引 `metrics.<role>.<键>`）→ 全量自检
4. JOURNAL 记行 + git commit → 提示执行 `/accept <cid>`（**终验必须全量跑，scoped 记录不算数**）

## 变更控制（不变）

任何角色上报范围/接口问题：回蓝图修订，**重新走用户确认**；接口冲突属蓝图缺陷 → 停止交付修蓝图。

## 失败处理

任务包失败重派 ≤1 次；波门两连不过 → 开工单回责任角色并考虑回蓝图；熔断只由全量终验触发（retry 是战役级计数，各战役独立熔断）。

## 波门质量基线（轻蓝图可直接抄的四阶段）

见 `config/templates/blueprint-template.md` 的"里程碑分层模板"：骨架层→竖切层→完整层→打磨层。
