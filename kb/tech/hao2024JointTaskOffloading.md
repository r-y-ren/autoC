---
id: hao2024JointTaskOffloading
name: 任务优先级感知多UAV协同MEC潜空间DRL联合卸载
field: [UAV 辅助边缘计算, 深度强化学习, 资源分配]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 离散-连续混合动作的潜空间处理（嵌入表+条件 VAE 与 TD3 结合）是可迁移的通用 DRL 工程技巧，凡遇"离散决策+连续调节"混合控制类赛题（调度/投放/参数控制）均可套用
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 任务优先级感知的多机协同算力调度可作为智慧农业无人机集群"紧急任务优先（病虫害告警先于常规巡检）"方案设计依据（TMC 2024）
    reuse_cost: 低
sources:
  - paper_title: "Joint Task Offloading, Resource Allocation, and Trajectory Design for Multi-UAV Cooperative Edge Computing with Task Priority"
    doi: 10.1109/TMC.2024.3350078
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 任务优先级感知多UAV协同MEC潜空间DRL联合卸载

## 单行摘要

在多 UAV 协同 MEC 中显式引入任务优先级与二元卸载模式，联合优化轨迹、卸载决策与通信/计算资源分配以最大化长期平均系统增益；核心技术亮点是用离散动作嵌入表与条件变分自编码器构造混合动作潜空间，再与 TD3 结合，优雅处理"二元卸载（离散）×资源分配（连续）"的混合动作难题。

## 方法快照

- 问题结构：时隙化多 UAV 协同 MEC；任务优先级各异，采用二元卸载（本地 / UAV / 转发至其他 UAV 或边缘云），目标是长期平均系统增益。
- 混合动作处理：嵌入表 + 条件 VAE 构建动作潜空间，避免粗暴离散化造成性能损失。
- 求解：潜空间与 TD3 结合形成 DRL 求解器；训练阶段同步更新编码器/解码器与 actor/critic，使潜空间表示持续适应环境。
- 验证：数值仿真（合成场景）；未说明平台与开源情况。

## 比赛映射要点

- 黑客松算法题：混合动作潜空间 DRL 是可直接搬运的工程组件，适用于"调度决策（离散）+速率/功率/配额（连续）"型赛题，比把离散动作 one-hot 展开的常规做法更有技术叙事。
- 双创申报：优先级感知调度对应农业场景"告警任务优先处理"的差异化卖点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Hao2024_任务优先级感知的多UAV协同边缘计算联合卸载`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `hao2024JointTaskOffloading` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
