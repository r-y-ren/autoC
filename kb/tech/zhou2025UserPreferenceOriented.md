---
id: zhou2025UserPreferenceOriented
name: 用户偏好导向的UAV-MEC服务缓存与任务卸载
field: [服务缓存, 任务卸载, UAV 边缘计算]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 期望命中率目标证明次模性后用带理论保证的贪心缓存（GCA），长期能量约束经加权因子转单时隙、再交替优化轨迹与卸载（IAU+CVX+dependent rounding）——多层级联合决策建模与"理论保证的贪心"是数模优化的差异化模板
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 缓存更新门控（命中率低于阈值才重构）+ 在线卸载闭环可直接迁移到边缘服务调度、内容分发类赛题，避免高频重构的工程思路通用
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业无人机按需服务组织（农事任务个性化分发、区域化服务缓存）的文献支撑，TSC 2025 方法名与闭环图可直接用于申报书方案章节
    reuse_cost: 低
sources:
  - paper_title: User Preference Oriented Service Caching and Task Offloading for UAV-assisted MEC Networks
    doi: 10.1109/TSC.2025.3536319
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 用户偏好导向的UAV-MEC服务缓存与任务卸载

## 单行摘要

论文提出在线算法 OOA：在 UAV-assisted MEC 中依据用户显式偏好与历史任务统计估计服务命中收益，命中率低于阈值才触发缓存重构（次模贪心 GCA）；随后把长期能量预算经能量加权因子转为单时隙目标，交替优化 UAV 轨迹（CVX）与任务卸载（松弛 + dependent rounding 整数化），持续最小化整体服务时延。

## 方法快照

- 问题组织：服务缓存直接约束任务卸载可行域（UAV 存储决定可提供服务集合），两者必须同一在线框架协调。
- 缓存层：期望命中率目标具次模性 → 贪心算法 GCA 带理论保证；命中率显著低于期望才触发重构，避免频繁缓存更新。
- 在线控制层：能量权重因子把长期能量约束转成每时隙延迟-能量加权目标，卸载决策随剩余能量自适应。
- 单时隙求解：IAU 交替优化轨迹与卸载，轨迹子问题 CVX，卸载子问题松弛后 dependent rounding 恢复整数解。
- 验证：EUA 真实用户位置数据 + 合成服务请求的 trace-driven 仿真；未说明开源，论文自报结果。

## 比赛映射要点

- 数模：次模性证明 + 贪心保证、长期约束在线化（Lyapunov 风格加权）是两段可直接套用的建模/求解套路。
- 黑客松："命中率触发重构"的门控机制与缓存-卸载闭环是边缘计算类赛题的现成算法骨架。
- 双创：用户偏好驱动的服务组织叙事适合农业无人机按需服务场景的方案论证。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2025_用户偏好导向的UAV辅助MEC服务缓存与任务卸载`（venue_tier/evidence_tier/paper_role/reproducibility_level 自页 frontmatter 迁移）。
- bib 回填：citekey `zhou2025UserPreferenceOriented` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/trace_driven、复现性 medium、无开源说明）承自 vault 页自评，如需引用请以论文原文复核。
