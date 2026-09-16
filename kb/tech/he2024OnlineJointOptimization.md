---
id: he2024OnlineJointOptimization
name: UAV-MEC QoE最大化的Lyapunov在线联合优化
field: [UAV 辅助移动边缘计算, Lyapunov 在线优化]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE INFOCOM 2024 - IEEE Conference on Computer Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: Lyapunov 优化把"未来信息不可见的长期随机控制"化归为逐时隙凸问题（两阶段博弈+凸优化求解），对动态需求/排队类决策题是替代短视贪心与算力昂贵的滚动时域法的结构化框架
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 长期目标→Lyapunov 逐时隙化→实时子问题求解的在线优化管线，可直接迁移到流式到达任务的在线调度类赛题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 以 QoE（用户感知）替代平均时延作为系统指标，为智慧农业服务平台"农户体验优先"的设计论证提供方法论依据（INFOCOM 2024）
    reuse_cost: 低
sources:
  - paper_title: "An Online Joint Optimization Approach for QoE Maximization in UAV-enabled Mobile Edge Computing"
    doi: 10.1109/INFOCOM52122.2024.10621306
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# UAV-MEC QoE最大化的Lyapunov在线联合优化

## 单行摘要

在单 UAV 作空中边缘服务器、用户需求时变且未来不可见的场景下，将联合任务卸载、资源分配与轨迹规划表述为长期 QoE 最大化问题（JTRTOP）；利用 Lyapunov 优化把未来依赖的长期问题转化为逐时隙实时优化（PROP），再以"博弈论处理参与方决策 + 凸优化细化资源与轨迹"的两阶段方法求解，在不依赖未来信息的前提下逼近更优长期用户体验。

## 方法快照

- 目标升级：优化目标从时延/能耗推进到 QoE，显式对用户感知负责；UAV 能量约束使轨迹与计算分配不可分离设计。
- 主线结构：长期 QoE 目标 → Lyapunov 逐时隙化（PROP）→ 两阶段求解（game theory + convex optimization）。
- 在线性：无需未来需求信息，适合时变环境在线控制。
- 验证：CVX 数值仿真（合成场景）；未说明开源。

## 比赛映射要点

- 数模决策题：Lyapunov drift-plus-penalty 框架适合"需求随时间变化+资源预算约束"的动态决策题，逐时隙凸求解可解释、易落地，优于只看当期收益的贪心。
- 黑客松算法题：在线/流式调度赛题可直接套用"长期目标逐时隙化"管线。
- 双创申报：QoE 指标化叙事支撑"以农户体验为中心"的平台设计论证。

## 关联概念
- 服务质量体验（QoE）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `He2024_UAV辅助MEC服务质量体验最大化的在线联合优化`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `he2024OnlineJointOptimization` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
