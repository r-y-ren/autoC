---
id: gao2025CSMAACMultiagentReinforcement
name: CSMAAC：部分可观测多UAV群智感知的安全协同飞控
field: [多智能体强化学习, 无人机协同控制, 安全强化学习]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 智慧农业植保/巡检无人机集群申报的协同飞控支撑点：部分可观测+安全防撞的 MARL 飞控且含 Gazebo 原型验证，材料可信度高
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 「必要通信筛选+安全层动作投影」两件套可迁移到多智能体/多机器人决策类算法题，区别于默认全通信的 MAPPO/GNN 基线
    reuse_cost: 中
sources:
  - paper_title: "CSMAAC: Multi-agent Reinforcement Learning Based Flight Control in Partially Observable Multi-UAV Assisted Crowd Sensing Systems"
    doi: 10.1109/TMC.2025.3586429
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# CSMAAC：部分可观测多UAV群智感知的安全协同飞控

## 单行摘要

针对部分可观测的多 UAV 群智感知系统，提出 CSMAAC：用通信伙伴预测与 critic 影响评估筛选"必要通信"、以相似性增强提升多智能体训练效率，并在 actor 输出后经安全层把动作投影回无碰撞安全域——把"通信省着用、飞得不出事"统一进一个分布式协同飞控策略，同时提升数据采集效率、降低碰撞与通信开销。

## 方法快照

- 问题结构：Dec-POMDP——每架 UAV 只观测半径内的 PoI/障碍/邻居，动作=飞行角度+距离，约束含最大通信距离、安全间距、剩余能量与区域边界。
- 必要通信：前馈网络预测候选通信伙伴，critic 评估交互影响强弱，只保留对当前决策有帮助的 one-to-one 通信，避免全广播的开销与训练扰动。
- 相似性增强：强化局部观测与其他 UAV 策略间的关联，提升多智能体训练效率与协同一致性。
- 安全层：actor 输出连续动作后求解凸二次优化，把可能违反碰撞约束的动作投影回安全域（对比 reward shaping/离散 CMDP 更适配连续动作空间）。

## 比赛映射要点

- 双创申报：智慧农业植保/巡检无人机集群的"集群低碰撞协同飞控 + 局部通信"技术支撑点；论文含仿真+物理原型（Gazebo）双重验证，申报材料可信度高于纯仿真工作。
- 黑客松：无人车/无人机编队、多机器人调度等决策类赛题可直接套用"通信筛选+安全投影"组合，作为超越端到端 MARL 基线的差异化组件。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Gao2025_CSMAAC多UAV协同飞控`；citekey `gao2025CSMAACMultiagentReinforcement`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性 medium 承自 vault 页自评（Python/Gazebo/TensorFlow，仿真+原型验证，artifact availability 未说明）；如需引用请以论文原文复核。
