---
id: sun2025AerialReliableCollaborative
name: EMOPPO-VLH：面向移动用户的空中协同可靠通信
field: [无人机协同通信, 多目标强化学习, 协作波束赋形]
published: 2025-01-01
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
  - track: 数模-预测与评估
    edge: 带记忆的 Gaussian-Markov 随机游走建模移动用户轨迹、LSTM 捕捉时变信道时间依赖，是移动对象轨迹预测加时序依赖建模的可迁移组件
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 进化多目标 DRL（向量值函数加超球任务选择）输出 Pareto 非支配策略集而非单点解，适合速率-能耗或性能-成本双目标权衡类赛题的差异化算法
    reuse_cost: 中
sources:
  - paper_title: Aerial Reliable Collaborative Communications for Terrestrial Mobile Users via Evolutionary Multi-Objective Deep Reinforcement Learning
    doi: 10.1109/TMC.2025.3536093
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# EMOPPO-VLH：面向移动用户的空中协同可靠通信

## 单行摘要

面向持续移动的地面用户，论文让多架 AAV 构成虚拟天线阵列（UVAA）以协作波束形成增强远距离链路，把带记忆随机游走的用户移动写入环境，再用 EMOPPO-VLH 在总可达速率与飞行能耗之间学习一组 Pareto 非支配策略——输出的是策略集而非单点最优解。

## 方法快照

- 系统场景：多 AAV 在三维空间构成 UVAA 虚拟阵列，显式考虑非关联 BS 干扰与时变信道，可靠通信不是纯 LoS 传播问题。
- 移动建模：用户轨迹用带记忆的 Gaussian-Markov 随机游走，决策从静态波束控制变成长期多目标问题。
- 问题重构：协作波束使能的可靠通信写成 multi-objective MDP，双目标为最大化总可达速率、最小化飞行能耗；决策变量同时含 AAV 位移与阵列激励权重，波束与路径完全耦合。
- EMOPPO-VLH：在 PPO 基础上扩展向量值函数，LSTM 捕捉用户移动与时变信道的时间依赖，hyper-sphere 任务选择机制提高 Pareto 集覆盖度。
- 证据：仿真验证（合成场景），对比展示不同用户偏好下的可选策略；训练软件栈与算力环境未披露。

## 比赛映射要点

- 数模预测评估类：Gaussian-Markov 记忆型移动模型加 LSTM 时序建模可直接迁移到人流/车流/终端移动预测题；「预测误差影响长期决策」的建模视角比单步预测更进一步。
- 黑客松算法类：多目标 DRL 输出 Pareto 前沿，评审可按不同偏好挑解——比单目标 RL 报一个数更契合开放性赛题的答辩结构。
- 局限：纯仿真、无开源实现（runnable 为否）；单移动用户设定，扩展到多用户需自行改环境。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Sun2025_面向地面移动用户的空中可靠协同通信`（frontmatter 4 枚举字段迁移：venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium）。
- bib 回填：citekey `sun2025AerialReliableCollaborative` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
