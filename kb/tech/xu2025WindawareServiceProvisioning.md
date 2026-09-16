---
id: xu2025WindawareServiceProvisioning
name: MW-DSP：多包裹无人机配送风感知服务供给
field: [无人机物流, 服务组合, 不确定性优化]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: 预测风况与实时风况偏差的显式处理——不确定性不进静态规划、而在执行阶段用策略迭代与动态检测消化，可直接迁移到含「预测值 vs 实际值漂移」的预测评估类数模题
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 服务共享（ADS-GA 遗传搜索 + 凝聚聚类构造初始种群）与服务组合（PIDC 策略迭代 + 等待/充电/改路动作）解耦的两阶段决策框架，是「谁和谁一起送」与「具体怎么送」分层求解的现成范式
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空物流运营方案的天气风险感知卖点——多包裹共享降本 + 风场驱动动态改路/充电决策，正面回应评审对无人机配送「靠天吃饭」的质疑
    reuse_cost: 低
sources:
  - paper_title: "Wind-Aware Service Provisioning Strategy for Multi-Package Drone Delivery"
    doi: 10.1109/TSC.2025.3592374
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# MW-DSP：多包裹无人机配送风感知服务供给

## 单行摘要

在存在动态风场的多包裹 DaaS 配送网络中提出风感知服务供给策略 MW-DSP：第一阶段服务共享，用 ADS-GA 确定哪些包裹共用一组 DaaS 实例形成共享计划 SSP；第二阶段服务组合，用基于策略迭代的 PIDC 为每条子路线在预测风况下组合近优 DaaS 服务序列形成组合计划 SCP，并在实际飞行中按实时风况做等待、充电与改路的动态调整，以降低风场不确定性下的配送总能耗。

## 方法快照

- 服务化建模：PDR、DaaS、SSP、CS、SCP 五类对象；DaaS 的质量参数与能耗显式依赖起止位置、时间与机型，是典型时空服务对象。
- 两阶段解耦：共享层（ADS-GA——凝聚聚类构造高质量初始种群 + 选择、邻域搜索、定向变异）与组合层（PIDC——预测风况下静态策略迭代 + 实时风况下动态检测与近优动作调整）。
- 不确定性处理：风况不进入静态共享阶段，由组合执行阶段的策略迭代与按需检测消化；能耗与服务的时空耦合被正式写进供给逻辑而非当扰动项。
- 验证：simulation + trace-driven（真实配送网络与风场数据结合仿真）；开源情况未说明。

## 比赛映射要点

- 数模预测评估题：「规划用预测、执行用实测」的两段式不确定性处理是预测-决策联动题的通用骨架（共享计划保持稳定、组合计划随实测滚动修正）。
- 数模决策题：先聚类/共享降维度、再逐段组合优化的求解次序，可直接套到多包裹/多订单合并配送类赛题。
- 双创申报：低空物流运营系统里「风感知 + 服务共享」双卖点，均有明确算法支撑而非概念包装。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Xu2025_多包裹无人机配送的风感知服务供给策略`（vault 页 4 枚举字段 venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium 已迁移至本卡）。
- bib 回填：citekey `xu2025WindawareServiceProvisioning` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation + trace_driven/mixed/复现性 medium、开源未说明故 runnable=false）承自 vault 页自评，如需引用请以论文原文复核。
