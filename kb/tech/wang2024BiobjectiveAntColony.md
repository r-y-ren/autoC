---
id: wang2024BiobjectiveAntColony
name: 双目标蚁群优化的UAV-MEC轨迹与多阶段卸载
field: [UAV辅助MEC, 多目标优化, 蚁群算法]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: bi-ACO 用目标偏好各异的异构蚁群 + 多组信息素矩阵输出近似 Pareto 解集，「总成本 vs 总完成时间」双目标权衡可直接套用到调度 / 路径类多目标数模题，表达力优于单目标 ACO 与 NSGA-II 等基线
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 把三阶段任务依赖（上传-计算-回传、同一设备需二次访问）直接嵌入 UAV 路径生成的结构化处理，适配带优先级约束的巡检 / 配送 / 任务编排类赛题的耦合调度需求
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 「保留 UAV + 高成本按需 UAV」混合资源与多机协同作业调度的技术支撑点，贴合农业植保、设施巡检等多机作业申报场景
    reuse_cost: 低
sources:
  - paper_title: "Bi-Objective Ant Colony Optimization for Trajectory Planning and Task Offloading in UAV-assisted MEC Systems"
    doi: 10.1109/TMC.2024.3408603
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 双目标蚁群优化的UAV-MEC轨迹与多阶段卸载

## 单行摘要

在多 UAV 辅助 MEC 系统中，「去哪飞」与「每阶段任务在哪执行」强耦合——任务被拆为数据上传、计算执行、结果回传三阶段，同一地面设备可能需要 UAV 访问两次。论文提出 bi-ACO 双目标蚁群框架：FSGM 快速构造满足能量与任务阶段约束的可行解，SDM 拆分重组高质量解提升多样性，PUM 按任务阶段维护多对信息素矩阵，异构蚁群各自探索不同目标偏好，最终输出平衡系统总成本与总完成时间的非支配解集。

## 方法快照

- 系统实体：地面智能设备、保留 UAV、按需 UAV（成本更高）、基站 / 停机点。
- 任务模型：三阶段任务（传输-计算-回传）带先后依赖与优先级，能量预算与截止期共同定义可行域。
- 算法组件：FSGM（可行解生成）→ SDM（解多样性提升）→ PUM（多信息素矩阵更新）→ 异构 colony 并行探索形成 Pareto 前沿。
- 实验结论：多种规模与设备分布下优于 NSGA-II、SA、VND、GLS、ACO-DSP，并附可行性现场测试（细节在附录）。
- 验证：数值仿真 + 现场可行性测试（混合数据来源），平台未披露，无开源。

## 比赛映射要点

- 数模决策类：异构蚁群 + 多信息素矩阵的 Pareto 求解模板可整体移植；「任务阶段依赖反向决定路径结构」是 VRP 带优先约束题型的建模亮点。
- 黑客松算法类：无人机巡检路线规划类赛题中，二次访问 / 阶段约束的显式建模是超越普通 TSP 基线的差异化点。
- 双创申报：多机混合调度（自有机队 + 按需租用）的成本-时效权衡方案支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2024_双目标蚁群优化的UAV辅助MEC轨迹与卸载规划`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2024BiobjectiveAntColony` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation+field_test 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
