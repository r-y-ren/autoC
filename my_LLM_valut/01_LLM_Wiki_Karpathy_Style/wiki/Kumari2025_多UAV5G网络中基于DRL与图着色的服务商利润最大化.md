---
tags: [论文, 多无人机协同, 5G网络, 图着色, 利润最大化]
created: 2026-04-08
updated: 2026-04-08
sources:
  - ../raw/markdown/kumari2025MaximizingServiceProviders.md
venue_tier: Unknown
literature_type: method
evidence_tier: core
paper_role: anchor
use_for:
  - main_citation
  - methodology
  - system_model
validation_type:
  - simulation
data_origin:
  - synthetic
platforms:
  - Python 3.8.16
frameworks:
  - PyTorch 2.1.0
  - Gurobi
datasets: []
hardware_stack:
  - Windows 11 Pro
  - NVIDIA GeForce RTX 3050 Ti
artifact_availability: unknown
reproducibility_level: medium
---

# Kumari2025_多UAV5G网络中基于DRL与图着色的服务商利润最大化

## 单行摘要
论文从运营商视角出发，把多 UAV 5G 服务传输中的位置、功率档位和 PRB 分配统一成利润最大化问题，并用 `MaDRL + 图着色` 给出半集中式近优解。

## 题目驱动研究框架
- 研究场景：基站与多架 UAV 协同向异构用户提供 5G 服务。
- 研究对象：服务提供商、BS、多个 UAV、不同业务类型的 UE、PRB 与功率档位集合。
- 核心问题：在动态 UE 请求和有限无线资源下，如何同时决定 UAV 位置、发射功率和 PRB 复用，既控制时延/能耗/干扰，又提高服务商利润。
- 具体方法：把 UAV 作为多智能体，用 `MaDRL` 决定飞行方向和功率档位；把 BS 作为半中心节点，用图着色完成 PRB 分配。
- 期望效果：逼近最优利润，并在能耗与服务时延上优于纯 RL、贪心和已有多 UAV 分配基线。

## Algorithm Design 快照
论文把运营商利润定义为“UE 支付收入减去 UAV 服务成本”，其中成本同时受到飞行、传输、计算与干扰管理影响。难点在于，若把 `位置 + 功率 + PRB` 全部直接交给 MaDRL，动作空间会随 PRB 数量快速爆炸。为此，作者把决策拆成两层：UAV 智能体用 MaDRL 学习飞行方向与功率档位，BS 侧用图着色算法为 UAV-UE 链路分配 PRB 并抑制复用冲突。这样既保留了动态环境中的学习能力，也把高维无线资源分配从 RL 动作空间中剥离出来，使整体框架能在不显著牺牲收益的情况下接近最优解。

## 图1系统框架草案
- 系统实体：一个 BS、多个服务型 UAV、异构 UE、内容服务器、PRB 与功率档位集合。
- 任务/数据流：UE 向 BS 发起服务请求；BS 决定由哪类 UAV 提供服务；UAV 悬停或移动至服务位置；BS 用图着色分配 PRB；UAV 完成通信与服务交付。
- 控制/优化变量：UAV 位置、飞行方向、功率档位、PRB 复用关系、单 UAV 服务容量。
- 约束来源：UE 最大容忍时延、最小数据率阈值、UAV 电量约束、最小安全间距、PRB 冲突。
- 画图提醒：图中要把“UAV 智能体决策”和“BS 图着色分配器”分成两层，否则会误读成纯分布式 RL。

## System Model
### A. 5G 服务传输场景
- 系统由 BS、UAV 集合和 UE 集合构成。每架 UAV 对应一种服务类型，BS 负责把 UE 请求映射到相应 UAV。
- UE 与 UAV 都具有位置动态，系统按离散时隙运行；UAV 在每个时隙处于悬停或移动阶段。

### B. 无线通信与 PRB 复用
- BS 为 UAV-UE 链路分配 PRB 与功率档位，链路速率由信道增益、干扰项和功率档位共同决定。
- PRB 可被不同 UAV 复用，但若空间重叠严重会产生强干扰，因此作者把冲突关系抽象为图着色问题。

### C. UAV 遍历、能耗与利润
- UAV 为到达更优服务位置需要支付遍历时延和推进能耗。
- 总服务收入由通信、计算和服务支付三部分构成；运营商利润等于收入减去 UAV 总成本。
- 目标函数不是单纯多服务或低时延，而是“利润最大化”。

### D. 约束集合
- 每个 UE 最多由一个 UAV 服务。
- UAV 服务容量、最小数据率、最大能耗与最小机间距必须满足。
- 由此得到的 0/1 选择问题可归约到 knapsack 特例，因此被证明是 NP-hard。

## Algorithm Design 详解
- 第一步是把问题改写为多智能体 MDP：每架 UAV 是一个智能体，状态包括位置、当前功率档位和已服务 UE 数。
- 第二步是动作设计：智能体只输出飞行方向和功率档位，而不直接选择 PRB。
- 第三步是奖励设计：满足约束时按“收入 - 成本”给正奖励；违反容量、时延、速率、能耗或碰撞约束则施加惩罚。
- 第四步是半集中式求解：UAV 侧用 MaDRL 学习移动与功率控制；BS 侧用图着色算法分配 PRB，压缩动作空间并管理干扰。
- 第五步是训练与评估：用最优解、MACEL、MADQL 和贪心基线比较，验证该拆分式设计的有效性。

## 实验证据卡片
- 验证类型：数值仿真
- 数据来源：合成场景
- 平台与软件：`Python 3.8.16`、`PyTorch 2.1.0`、`Gurobi Optimizer`
- 硬件与算力：`Windows 11 Pro`、`NVIDIA GeForce RTX 3050 Ti`
- 评测指标：服务商总利润、UAV 总能耗、平均服务时延、训练收敛曲线
- 对比基线：`MACEL`、`MADQL`、`optimal(Gurobi)`、`greedy`
- 开源情况：未说明
- 复现判断：`medium`
- 证据备注：训练轮数、网络结构、主要超参数、平台和硬件都写得较清楚，适合方法复现与基线比较，但仍缺少公开代码。

## Introduction 写作素材
- 很多 UAV-5G 研究默认以“系统效用最大化”为目标，但对运营商来说，更直接的问题往往是“部署这些 UAV 之后值不值”。
- 当 UAV 可以复用 5G 频谱资源时，利润问题天然会和干扰管理、功率控制、容量约束绑在一起。
- 这篇论文的重要转向在于把 UAV 服务网络从“通信优化问题”改写为“运营商收益问题”。

## Related Work 写作素材
- 与只做位置优化或只做功率控制的工作相比，本文把位置、功率和 PRB 统一进同一收益框架。
- 与把全部变量直接交给 RL 的方法相比，本文利用图着色把 PRB 分配从动作空间中剥离出来，缓解了动作维数膨胀。
- 与 MACEL、MADQL 这类多 UAV RL 方法相比，本文更强调半集中式资源编排而不是完全分布式决策。

## 相关系统建模页
- [[信道与通信速率模型]]
- [[无人机能耗模型]]
- [[任务队列与时延保障模型]]

## 相关概念与主题页
- [[资源分配]]
- [[多无人机协同]]
- [[多智能体强化学习]]
- [[图着色资源分配]]
- [[任务卸载与资源分配研究主线]]

## 来源
- [原文](../raw/markdown/kumari2025MaximizingServiceProviders.md)
