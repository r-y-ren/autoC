---
id: kumari2025MaximizingServiceProviders
name: MaDRL+图着色的多UAV 5G服务利润最大化
field: [多智能体强化学习, 图着色, 无线资源分配]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: unknown
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 把 UAV 位置、功率档位与 PRB 复用统一进利润最大化目标（收入减飞行/传输/计算/干扰成本），半集中式分层求解（UAV 侧 MaDRL 学移动与功率、BS 侧图着色分 PRB）把高维组合决策从 RL 动作空间剥离，是选址+资源分配+收益优化类赛题可直接套用的降维求解框架，附 Gurobi 最优基线与 NP-hard 证明
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 冲突图建模+图着色做干扰感知的 PRB 复用分配是可独立复用的经典算法组件，叠加多智能体 RL 与 greedy/MADQL/MACEL 基线即可快速搭出可对比的资源调度原型
    reuse_cost: 中
sources:
  - paper_title: "Maximizing Service Provider's Profit in Multi-UAV 5G Network via Deep Reinforcement Learning and Graph Coloring"
    doi: 10.1109/TMC.2025.3571804
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# MaDRL+图着色的多UAV 5G服务利润最大化

## 单行摘要

从运营商视角把多 UAV 5G 服务传输中的位置、功率档位与 PRB 分配统一成利润最大化问题（收入减 UAV 总成本）：若把全部变量交给多智能体 DRL，动作空间会随 PRB 数量爆炸，故采用半集中式分层求解——UAV 智能体用 MaDRL 学习飞行方向与功率档位，BS 作为半中心节点用图着色算法完成干扰感知的 PRB 分配，在不显著牺牲收益的情况下逼近最优利润。

## 方法快照

- 目标函数：利润 = UE 支付收入（通信/计算/服务三部分）− UAV 总成本（飞行能耗+传输+计算+干扰管理），而非单纯效用或时延。
- 问题性质：UE 选择问题可归约到背包特例，NP-hard；约束含 UE 最大容忍时延、最小数据率、UAV 电量、最小安全间距与 PRB 冲突。
- 分层求解：MaDRL 智能体状态含位置/功率档位/已服务 UE 数，动作只输出飞行方向与功率档位；奖励按收入−成本计正、违约计罚；BS 侧图着色把 PRB 复用冲突从 RL 动作空间剥离。
- 验证：Python/PyTorch/Gurobi，与最优解（Gurobi）、MACEL、MADQL、greedy 基线比较利润、总能耗、平均时延与收敛曲线；训练轮数、网络结构与超参数记载较全。

## 比赛映射要点

- 数模：「选址 + 资源分配 + 收益最大化」是典型综合题型；把组合决策交给图着色、把连续决策交给 RL 的降维拆分思路，以及收入-成本型目标函数构造，可直接作为答卷骨架，Gurobi 最优解用于小规模对照。
- 黑客松/算法赛：图着色资源冲突分配可独立复用；RL+图着色的两层架构与多基线对比设置适合快速出可演示原型。

## 关联概念
- 图着色资源分配

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Kumari2025_多UAV5G网络中基于DRL与图着色的服务商利润最大化`（4 枚举字段自该页 frontmatter 迁移，venue_tier 按词表 Unknown→unknown 映射）。
- bib 回填：citekey `kumari2025MaximizingServiceProviders` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 PyTorch/Gurobi 数值仿真形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
