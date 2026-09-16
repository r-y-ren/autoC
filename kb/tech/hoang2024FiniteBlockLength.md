---
id: hoang2024FiniteBlockLength
name: 有限块长NOMA多用户配对UAV系统性能分析与优化
field: [无人机通信, NOMA, 有限块长 URLLC]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: 短包传输下 BLER/吞吐/时延/AoI 的闭式表达式（高斯-切比雪夫求积+不完全 Gamma 函数）可替代数模中惯用的 Shannon 容量近似，对含无人机链路/可靠性约束的评估类赛题给出更真实的量化模型
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 蜂群短包控制链路的可靠性-时延折中设计依据（高度/块长/功率联合优化+贪心用户配对），为智慧农业无人机集群通信子系统选型提供 CCF-A 级论证
    reuse_cost: 高
sources:
  - paper_title: "Finite Block Length NOMA MU Pairing UAV-enable System: Performance Analysis and Optimization"
    doi: 10.1109/TMC.2024.3368159
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 有限块长NOMA多用户配对UAV系统性能分析与优化

## 单行摘要

在多天线 UAV 辅助的 NOMA 多用户配对系统中，分析有限块长（短包）条件下的 BLER、吞吐、goodput、时延与 AoI：基于高斯-切比雪夫求积和不完全 Gamma 函数推导各指标闭式表达式，再用一维搜索、迭代算法与贪心用户配对联合优化 UAV 高度、块长、传输比特数与发射功率——揭示短包场景下 Shannon 极限失效时误码与时延的真实折中。

## 方法快照

- 建模立场：有限块长假设使经典无限块长（Shannon）近似系统性高估链路性能，BLER 与时延形成显式折中。
- 解析推导：闭式给出 BLER、吞吐、goodput、可靠性、时延与 AoI 表达式（高斯-切比雪夫求积、不完全 Gamma 函数）。
- 优化组件：一维搜索+迭代算法优化高度/块长/比特数/功率；贪心用户配对优于随机调度。
- 指标扩展：从传统吞吐扩展到 AoI——UAV 高度不仅影响覆盖，也直接影响 BLER 与 AoI 最优值。
- 验证：理论分析 + Monte-Carlo 数值仿真；未说明开源。

## 比赛映射要点

- 数模评估题：涉及无人机通信链路、短包可靠传输的评估类赛题，可用其闭式指标替换 Shannon 近似，建模粒度即差异化点；配套的高度/功率参数搜索可直接复用。
- 双创申报：作为蜂群通信链路（URLLC 短包）可靠性设计的引用支撑；属通信理论，复现需通信仿真功底，标注 reuse_cost 高。

## 关联概念
- 有限块长通信
- 信息年龄（AoI）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Hoang2024_有限块长NOMA多用户配对UAV系统性能分析与优化`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter；页自评 literature_type=theory，含理论推导+数值仿真双验证）。
- bib 回填：citekey `hoang2024FiniteBlockLength` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（theory+simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
