---
id: xu2024HolisticHybridService
name: H2S2：MEC无人机末端配送整体混合服务选择
field: [无人机末端配送, 边缘计算, 服务选择]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 低空物流末端配送的服务体系设计支撑——配送服务与计算服务统一编排（DaaS 视角），且评估基于 Antwork ADNET 真实航路数据抽象的仿真场景，申报材料有真实物流场景背书
    reuse_cost: 低
  - track: 数模-数据分析与决策
    edge: 静态全局最优服务计划 + 运行时按可用性/移动性触发动态重选的两阶段决策框架，可直接迁移到服务可用性随时间变化的调度决策题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: trace-driven 仿真 + 覆盖完整配送流程的服务选择算法组合，是配送类数据赛题从「单次挑最优」升级为「连续服务系统」的建模参考
    reuse_cost: 中
sources:
  - paper_title: "A Holistic and Hybrid Service Selection Strategy for MEC-based UAV Last-Mile Delivery Systems"
    doi: 10.1109/TSC.2024.3451243
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# H2S2：MEC无人机末端配送整体混合服务选择

## 单行摘要

面向 MEC 支撑的 UAV 末端配送（last-mile delivery）智慧物流场景，提出 H2S2 整体混合服务选择策略：把负责包裹移动的 delivery services 与 MEC 提供的 computational services 统一组织，静态阶段给出全局最优服务计划，动态阶段在服务可用性、网络条件或设备移动性变化时触发重选，联合压低 UAV 能耗与服务响应时间。

## 方法快照

- 服务二分：delivery service（包裹移动）与 computational service（边缘计算）显式分模型，二者共同决定用户体验，分开优化会损失整体最优。
- 两阶段决策：静态选择给整体最优计划；动态重选是系统主干而非附加模块，覆盖服务多样性、可得性与设备移动性。
- 建模视角：从服务消费者（UAV 配送企业）视角建模，把末端配送当作连续服务系统而非单纯路径/调度问题。
- 验证：simulation + trace-driven，基于 Antwork ADNET 真实 UAV 航路数据抽象的仿真数据集；开源情况未说明。

## 比赛映射要点

- 数模/决策类赛题：「静态最优 + 动态重选」双层结构是处理环境时变的标准答案模板——凡题目含服务/资源中途失效或需求漂移，都可用该框架组织模型。
- 双创申报：低空物流 DaaS 运营方案（配送 + 边缘计算一体编排），真实航路数据案例可直接写进项目书。
- 黑客松：配送类赛题若只做路径规划，可引用本文把「计算服务可得性」纳入评价维度形成差异化。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Xu2024_MEC无人机末端配送的整体混合服务选择`（vault 页 4 枚举字段 venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium 已迁移至本卡）。
- bib 回填：citekey `xu2024HolisticHybridService` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation + trace_driven/mixed/复现性 medium、开源未说明故 runnable=false）承自 vault 页自评，如需引用请以论文原文复核。
