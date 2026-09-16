---
id: zhu2024FissionSpectralClustering
name: FSC：FANET 无人机蜂群裂变谱聚类策略
field: [UAV 自组网, 图聚类]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 动态时序图聚类 + 尺寸/结构约束的裂变维护机制，可直接落无人机蜂群/传感网自组网赛题，超越普通谱聚类基线
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业无人机集群自组网方案的技术支撑点（TSC 2024 方法，农业植保蜂群通信组织）
    reuse_cost: 低
sources:
  - paper_title: "Fission Spectral Clustering Strategy for UAV Swarm Networks"
    doi: 10.1109/TSC.2024.3376191
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# FSC：FANET 无人机蜂群裂变谱聚类策略（样本卡 · 升级票04）

> 本文为 vault-distill 管线的**样本验证卡**（非全量产物）：证明 论文页→卡 的提炼格式、4 枚举字段与 paper-distill 溯源（含 bib 回填 DOI）可通过 lint。全量执行见票 05。

## 单行摘要

针对 FANET 中 UAV 蜂群的动态聚类问题，提出结合时间序列链路属性与尺寸/结构约束的裂变谱聚类策略 FSC：先用链路有效值构造拉普拉斯矩阵并在特征空间聚类，再对不满足约束的簇递归裂变，直到形成可维护的分层结构——聚类目标从图割质量扩展到"簇结构便于维护与通信"，以减少泛洪开销、提升簇内通信质量。

## 方法快照

- 图建模：节点与链路 → 时序加权图（链路质量随时间变化，无中心控制）。
- 初始划分：谱聚类于特征空间。
- 裂变维护：不满足尺寸/结构约束的簇继续递归切分；按需触发簇维护，减少不必要计算。
- 分层意义：稳定簇头、减少大范围泛洪与簇头频繁切换。

## 比赛映射要点

- 黑客松/算法赛：无人机蜂群或移动自组网类赛题中，"带约束的动态聚类"是可移植的差异化组件（对比 K-Means/普通谱聚类基线）。
- 双创申报：智慧农业植保无人机集群的通信组织方案支撑（多机协同作业场景）。

## 关联概念（vault 概念页折叠于此，不独立成卡）

- **裂变谱聚类**：谱聚类初始划分后，对不满足尺寸/结构约束的簇递归切分。
- **FANET 聚类**：飞行自组网中划分 UAV 节点为簇，减泛洪、稳路由、改善簇内通信。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhu2024_FANET中的UAV蜂群裂变谱聚类`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `zhu2024FissionSpectralClustering` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
