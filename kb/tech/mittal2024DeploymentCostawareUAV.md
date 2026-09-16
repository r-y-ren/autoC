---
id: mittal2024DeploymentCostawareUAV
name: DCE：部署成本效率驱动的空地一体UAV与BS协同
field: [空地一体网络, 部署优化, 联盟博弈]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 目标函数从总速率改为速率与部署能耗成本之比（DCE），网格化遗传算法定数量位置+污染感知聚类+联盟博弈定协作的三段式分解，是设施选址+服务分组+协作结构类成本效益决策题的完整解法骨架
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 遗传算法+联盟形成博弈的混合流水线可迁移到组队/聚类协作类算法题；每架 UAV 边际收益是否划算的停机判据，优于无限制堆资源的方案
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业组网方案的投入产出论证框架（每架 UAV 的边际收益对比部署成本），申报书成本效率叙事的直接技术支撑（TMC 2024）
    reuse_cost: 低
sources:
  - paper_title: "Deployment Cost-Aware UAV and BS Collaboration in Cell-Free Integrated Aerial-Terrestrial Networks"
    doi: 10.1109/TMC.2023.3341809
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# DCE：部署成本效率驱动的空地一体UAV与BS协同

## 单行摘要

在 clustered cell-free 大规模 MIMO 支撑的空地一体网络（IATN）中，以部署成本效率 DCE（网络总速率与部署+能耗成本之比）为核心目标，联合优化 UAV 数量、位置与 BS/UAV 聚类协作关系：三段式求解先用网格化遗传算法决定 UAV 密度与位置，再做 pilot-contamination 感知的用户聚类，最后用 coalition formation game 形成 BS/UAV 协作簇，在成本与吞吐间显式找平衡。

## 方法快照

- 问题结构：UAV 数量、位置、用户聚类与 BS/UAV 协作彼此耦合；性能更好但太贵不是可接受的设计。
- 目标函数：DCE = 总速率 /（部署成本+能耗成本），而非单一速率或最少数量。
- 求解三段：网格化候选位置离散化部署 → 遗传算法搜索数量与位置组合 → pilot 污染感知聚类 → 联盟博弈形成稳定协作簇。
- 关键结论：IATN 存在明显的最优 UAV 数量（越多并非越好）；部署面积增大时最优数量随之变化。
- 验证：数值仿真（10 km×10 km 区域、100 个拓扑平均、50 次 coalition 重复）；软件栈未披露。

## 比赛映射要点

- 数模决策题：比值型目标（收益/成本）+ 部署-聚类-协作三段分解，可套到基站/服务点/充电桩选址与分组服务类题目，论证边际收益递减。
- 黑客松算法题：GA+联盟博弈流水线与最优规模判据可直接迁移到组队协作、资源投放类题。
- 双创申报：农业组网预算论证的技术依据（每架无人机的边际收益曲线）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Mittal2024_面向部署成本效率的空地一体UAV与BS协同`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `mittal2024DeploymentCostawareUAV` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
