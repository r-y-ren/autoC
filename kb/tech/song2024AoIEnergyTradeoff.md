---
id: song2024AoIEnergyTradeoff
name: 空地协同MEC中AoI-能耗权衡的Pareto策略集学习
field: [多目标强化学习, 信息年龄, 移动边缘计算]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: AoI（数据新鲜度）与能耗分别写入向量奖励维度，用 MOPPO 训练多偏好个体并对策略网络做参数级进化增强，输出一组可按偏好切换的 Pareto 策略而非单一加权解——为"时效-成本权衡"类数模题提供超越线性加权的决策前沿生成方法
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: PPO 系多目标训练 + 策略网络参数级交叉变异的进化算子是可复用的多目标学习工程组件；飞行方向/距离/卸载比例的混合动作设计可迁移到调度与路由类赛题
    reuse_cost: 中
sources:
  - paper_title: "AoI and Energy Tradeoff for Aerial-Ground Collaborative MEC: A Multi-Objective Learning Approach"
    doi: 10.1109/TMC.2024.3394568
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 空地协同MEC中AoI-能耗权衡的Pareto策略集学习

## 单行摘要

在 HAP+UAV 空地协同 MEC 中，论文联合优化 UAV 飞行路径与任务卸载比例：先把 AoI-能耗权衡形式化为带向量奖励的多目标 MDP，再用 MOPPO 训练多个不同偏好权重的学习个体获得非支配策略集合，最后用进化算子（参数级交叉与变异）进一步改良策略网络，避免局部最优——系统输出随用户偏好可切换的策略前沿，而非单一固定权衡点。

## 方法快照

- 系统构成：HAP 与 UAV 共同为地面设备（GD）提供计算支持；UAV 负责机动接入与任务收集，GD 数据新鲜度以 AoI 刻画，UAV 飞行引入显著推进能耗。
- 决策变量：飞行方向、飞行距离、任务卸载比例；状态含 GD 位置与 AoI、UAV 坐标、任务队列。
- 建模要点：AoI 与能耗对应奖励向量的不同维度，各自保持独立语义，不做加权和压扁。
- 学习管线：MOPPO 按偏好权重向量训练多个个体 → 非支配策略集合 → 进化算子在参数层面交叉变异增强全局探索。
- 验证：标准数值仿真（合成场景），平台与硬件未披露，未开源。

## 比赛映射要点

- 数模：当题目要求"在时效与成本间权衡并给出方案"时，交付一组 Pareto 解并讨论偏好切换，比交一个加权最优点更符合评审预期；AoI 作为时效性指标的定义方式也可直接借用。
- 黑客松/算法赛：MOPPO+进化增强的多目标管线可整体搬到任何"多指标奖励的序列决策"任务；与单目标 RL 基线的对比协议（超体积/非支配率）有现成叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Song2024_空地协同MEC中的AoI与能耗权衡学习`（四枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `song2024AoIEnergyTradeoff` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与数值仿真形态承自 vault 页自评（artifact_availability: unknown，开源情况未说明），如需引用请以论文原文复核。
