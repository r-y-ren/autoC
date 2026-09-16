---
id: alam2024JointTrajectoryControl
name: 多UAV群网络跨层联合控制（MA-DDPG）
field: [UAV 自组网, 多智能体强化学习, 跨层优化]
published: 2024-01-01
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
  - track: 黑客松-数据与算法
    edge: 两跳邻居 LSTM actor + 多头注意力 critic 的分布式 MARL 模板，可迁移到多智能体协同调度/路由类赛题，相比单智能体 DRL 或最短路启发式有差异化
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业植保/灾后监测蜂群的自组网通信组织方案支撑点（轨迹-频谱-路由一体化叙事）
    reuse_cost: 低
sources:
  - paper_title: "Joint Trajectory Control, Frequency Allocation, and Routing for UAV Swarm Networks: A Multi-Agent Deep Reinforcement Learning Approach"
    doi: 10.1109/TMC.2024.3403890
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 多UAV群网络跨层联合控制（MA-DDPG）

## 单行摘要

面向灾后监测与空中通信覆盖的 UAV 群网络，把轨迹控制、频段分配与多跳路由统一为一个跨层 link utility 最大化问题：每架 UAV 作为 agent，用三组 LSTM 提取一跳/两跳邻居的时序状态生成连续轨迹控制，用多头注意力 critic 有选择地建模邻居影响，离散输出频段与下一跳中继——路由决策不再是纯拓扑最短路，而是综合链路持续时间、SINR、排队时延与剩余能量的联合序列决策。

## 方法快照

- 问题抽象：稳定链路、SINR、排队负载与剩余能量组合成 link utility，在高机动、频谱共享、多跳中继耦合下做联合优化。
- MDP 建模：观测含运动规则、信道/频段状态、队列信息与两跳邻居特征；动作为连续轨迹控制 + 离散频段/中继选择。
- actor：三组 LSTM state representation 缓解时变拓扑导致的状态非平稳。
- critic：多头注意力只关注一跳邻居，不做全局集中式拼接，降低复杂度并提升协同学习稳定性。
- 轨迹底层：cohesion/alignment/separation 群体行为规则维持编队稳定，两跳信息避免拓扑分裂。
- 验证：NS-3 v3.35 + PyTorch 1.7.1 数值仿真（合成场景，未开源）。

## 比赛映射要点

- 黑客松/算法赛：多智能体协同调度、动态网络路由类赛题可直接套用"局部时序观测 + 注意力 critic + 混合动作空间"的 MARL 骨架；"跨层联合决策优于分层独立优化"的问题定义方式本身即是差异化论证。
- 双创申报：灾后通信覆盖、植保蜂群等场景中"多机自组网 + 频谱避让 + 稳定路由"的技术方案支撑点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Alam2024_多UAV群网络联合轨迹频谱与路由控制`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `alam2024JointTrajectoryControl` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
