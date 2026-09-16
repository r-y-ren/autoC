---
id: li2025AnchorNovelModeling
name: Anchor：Delaunay三UAV协同卸载的随机几何建模
field: [UAV 辅助 MEC, 随机几何, 协同卸载建模]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: unknown
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE INFOCOM 2025 - IEEE Conference on Computer Communications
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: SUPH×SCP 把通信成功与计算成功合成统一可靠性指标的两层评估范式（handoff 概率、上行成功、计算成功逐层推导），可迁移到数模评估类题的复合成功率指标构建
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: Delaunay 三角剖分动态划分三节点协作单元加协同切换建模，为动态网络分组/覆盖类赛题提供几何分组组件，区别于就近单点关联
    reuse_cost: 中
sources:
  - paper_title: "Anchor: A Novel Modeling Methodology for Cooperative UAV-MEC Based on Stochastic Geometry"
    doi: 10.1109/INFOCOM55648.2025.11044603
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# Anchor：Delaunay三UAV协同卸载的随机几何建模

## 单行摘要

提出基于 Poisson-Delaunay 三角剖分的协同 UAV-MEC 动态卸载模型 Anchor：每个 UE 不再关联单个 UAV，而是向三个 UAV 构成的 Delaunay 三角 CoMP 集联合卸载，并用随机几何把协同切换概率、上行通信成功（SUPH）与计算成功（SCP）统一推导成综合指标 SECP——把 UAV-MEC 的评价从「单链路可靠性」推进到「通信-计算协同可靠性」。

## 方法快照

- 网络建模：UAV 与 UE 均服从 PPP；Delaunay 三角单元作为卸载 CoMP 服务集，随 UAV 运动动态变化。
- 切换建模：定义协同 handoff 事件（三角单元重组），用等效 UAV 分析方法给出切换概率。
- 通信分析：TDD + Rayleigh 衰落下推导 SUCP，再纳入 handoff 失败得 SUPH。
- 计算分析：任务按概率 p 送中央服务器、其余在 CoMP 集内执行，MEC 侧选瞬时队列负载最小者，得 SCP。
- 综合评估：SECP = SUPH × SCP，形成可比较不同协同卸载机制的统一评价框架。
- 验证：理论推导 + Monte Carlo 数值仿真（合成场景），对比单 BS 关联/规则六边形协作/传统卸载模型，未开源。

## 比赛映射要点

- 数模评估题：SUPH×SCP 的「分阶段成功率相乘合成综合指标」范式可直接迁移到多环节系统可靠性评估（通信/计算/服务链）；随机几何逐层推导的过程是论文里指标可信度的来源。
- 黑客松/算法赛：Delaunay 三角剖分做动态三点协作分组是现成的几何算法组件，可用于覆盖、分簇、中继选择类题目的分组层。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_Anchor协同UAV-MEC的动态CoMP卸载建模`（4 枚举字段自 vault 页 frontmatter 迁移）。
- venue_tier 说明：vault 页自评 Unknown，按跑批规则映射为 unknown；bib 回填 venue 为 INFOCOM 2025，供后续 deep-sync 复核升级。
- bib 回填：citekey `li2025AnchorNovelModeling` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（low，公式完整但无实现平台与代码资产，更适合建模参考而非工程复现）；signal.runnable 如实标 false。
