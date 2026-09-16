---
id: zheng2024ContentDeliveryPerformance
name: 缓存使能 UBS 内容交付性能解析（元宇宙用户）
field: [随机几何, 边缘缓存, 性能建模]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: MHCPP/BPP 随机几何 + cache hit/miss 差异化关联的解析范式，可整体迁移到"设施部署 + 缓存/容量规划"类数模赛题——给出内容交付成功概率下界与平均时延上界的推导路线，MATLAB Monte Carlo 验证流程清晰
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空内容分发/近用户缓存服务的 QoS 量化论证理论锚点——把"空中缓存是否真的改善体验"从经验判断升级为成功概率与时延的解析界
    reuse_cost: 低
sources:
  - paper_title: Content Delivery Performance Analysis of a Cache-Enabled UAV Base Station Assisted Cellular Network for Metaverse Users
    doi: 10.1109/JSAC.2023.3345424
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 缓存使能 UBS 内容交付性能解析（元宇宙用户）

## 单行摘要

针对时延敏感的元宇宙用户，构建缓存使能 UBS（无人机基站）辅助蜂窝网络的解析模型：用 MHCPP/BPP 建模基站空间分布、概率缓存策略建模内容命中，在 cache hit 与 miss 两种情形采用不同基站关联逻辑，推导内容交付成功概率下界与平均内容交付时延上界，并据此给出 UBS 最优高度与最优数量。

## 方法快照

- 空地网络建模：地面 MBS 位置服从 Matérn 硬核点过程（MHCPP，刻画排斥分布更接近真实蜂窝部署），空中 UBS 位置服从二项点过程（BPP），UBS 按 Zipf 热度做概率缓存。
- 差异化关联：cache miss 时用户仅关联最近 MBS；cache hit 时按最强平均接收功率在 MBS/LBS/NBS 间选择关联对象——这是把缓存优势转化为时延收益的关键机制设计。
- 解析推导：各类型基站的关联概率、服务距离分布与 SINR 表达式 → 内容交付成功概率下界、平均交付时延上界；分析 UBS 高度、数量、缓存容量与 Zipf 参数的影响，识别最优 UAV 高度与最优 UBS 数量。
- 验证：MATLAB + Monte Carlo 仿真；代码未公开。

## 比赛映射要点

- 数模：基础设施部署 + 缓存/容量规划的赛题（充电桩、基站、冷链仓、CDN 节点选址）可直接套用其"空间点过程建模 → 关联概率 → 成功概率/时延界"的推导链；"hit/miss 双关联策略"是超越朴素最近关联基线的建模亮点。
- 双创申报：低空经济内容服务（应急广播、近用户边缘内容分发）的商业可行性论证可引用其解析结论支撑 QoS 承诺，避免纯定性描述。
- 方法论借鉴：把性能主张写成"概率下界 + 时延上界"的解析形式，是数模论文结果的规范化表达范式。

## 关联概念
- 元宇宙内容交付

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zheng2024_面向元宇宙用户的缓存使能UBS内容交付性能分析`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `zheng2024ContentDeliveryPerformance` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（theory + simulation/synthetic/复现性 medium、仿真代码未披露）承自 vault 页自评，如需引用请以论文原文复核。
