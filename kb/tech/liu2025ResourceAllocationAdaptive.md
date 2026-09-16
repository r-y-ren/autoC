---
id: liu2025ResourceAllocationAdaptive
name: UAV辅助ISAC自适应波束对齐的感知-通信联合资源分配
field: [一体化感知与通信, 资源分配, 深度强化学习]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 用 Cramer-Rao Bound 把感知精度与通信速率下界显式耦合的建模套路，可迁移到感知投入与产出耦合的联合优化题（监测采样预算分配等）；接入/回传两段链路拆解子问题的分解思路通用
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 用 DRL 近似替代逐次凸近似（SCA）迭代求解的工程路线，适合需要实时给出资源配置的大规模调度类算法题，复杂度对比有明确卖点
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农业无人机巡田感知+数据回传一体化的 ISAC 方案技术支撑（JSAC 2025，感知辅助波束对齐，同一频谱同时完成观测与通信）
    reuse_cost: 低
sources:
  - paper_title: "Resource Allocation for Adaptive Beam Alignment in UAV-assisted Integrated Sensing and Communication Networks"
    doi: 10.1109/JSAC.2024.3492699
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# UAV辅助ISAC自适应波束对齐的感知-通信联合资源分配

## 单行摘要

面向 UAV 挂载空中基站的 ISAC 网络，利用机载雷达对地面用户与宏基站做位置感知以辅助波束对齐，联合优化通信功率、感知功率与感知驻留时间以最大化通信速率下界：先从 Cramer-Rao Bound 推导感知误差对两段链路（GU-ABS 接入、ABS-MBS 回传）速率的影响并建立联合优化问题，再用 DRL 近似替代高复杂度 SCA 求解，实现更快的资源配置。

## 方法快照

- 问题结构：感知功率/驻留时间与通信功率共享频谱且彼此耦合，波束失配误差同时侵蚀接入与回传两段链路。
- 理论连接：CRB 推导感知精度 → 波束对齐误差 → 通信速率下界，使速率优化显式依赖感知资源投入。
- 求解：联合问题按 GU-ABS 与 ABS-MBS 拆分为两个子问题；先给 SCA 近似基准，再用 DRL 替代迭代凸化，降低在线计算复杂度。
- 意义：把 ISAC 从共享硬件层面推进到感知精度直接进入速率优化层面。
- 验证：数值仿真（合成 UAV-ISAC 场景，含参数化仿真与复杂度分析）；平台与代码未披露。

## 比赛映射要点

- 数模决策题：感知投入-精度-收益的耦合目标建模（CRB 式下界思维）可迁移到采样/监测类预算分配题；两段链路拆解对应多级设施联合优化。
- 黑客松算法题：DRL 替代 SCA 的实时化路线，适合对响应时间有要求的资源调度题，可与凸优化基线做复杂度-性能对比。
- 双创申报：农业场景一网两用（巡田感知+通信回传）的降本方案支撑。

## 关联概念
- 一体化感知与通信（ISAC）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Liu2025_UAV辅助ISAC自适应波束对齐的资源分配`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `liu2025ResourceAllocationAdaptive` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
