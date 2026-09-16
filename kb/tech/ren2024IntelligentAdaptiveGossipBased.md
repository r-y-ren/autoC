---
id: ren2024IntelligentAdaptiveGossipBased
name: BDGN：UAV-MEC的智能自适应Gossip广播协议
field: [UAV-MEC, 广播协议, 深度图网络]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: high
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: true
competition_fit:
  - track: 黑客松-数据与算法
    edge: 把「以什么概率转发 + 发给哪些邻居」写成部分可观测决策问题，Bitgraph 记录邻居历史收包、分支动作图网络联合求解，传播时延降超 29%、冗余消息降超 20%；信息传播/网络广播类赛题可直接改造且有开源实现可跑
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 无人机集群作为边缘池时内部数据交换效率决定协同服务能力的论证支撑，协议级优化叙事比纯硬件方案更省成本
    reuse_cost: 低
sources:
  - paper_title: Intelligent Adaptive Gossip-Based Broadcast Protocol for UAV-MEC Using Multi-Agent Deep Reinforcement Learning
    doi: 10.1109/TMC.2023.3323296
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# BDGN：UAV-MEC的智能自适应Gossip广播协议

## 单行摘要

面向多 UAV 作为边缘池协同提供 MEC 服务时的内部数据包广播问题，提出结合 Bitgraph 数据结构与 Branching Deep Graph Network（BDGN）的智能 Gossip 协议：将转发概率与转发邻居选择写成部分可观测决策问题联合求解，同时利用邻居历史收包记录打破无记忆传播，在仿真中传播时延改善超 29%、冗余消息减少超 20%，并改善连续广播场景的剩余电量。

## 方法快照

- 场景：单源节点广播需在多轮中传遍整个移动 UAV 网络，邻居集合随飞行动态变化；传统 Gossip 在传播时延与冗余消息间难平衡，且不利用新邻居的历史收包信息。
- Bitgraph：记录邻居历史上是否已收到特定消息，使新形成的邻居关系不再是完全无记忆的随机传播。
- BDGN：branching 结构同时建模「转发概率 + 邻居集合」多维离散动作，在 POMDP 中学习广播策略，优于只优化单一因素的方案。
- 验证：NS-3 3.25 + OpenAI Gym 0.25 + PyTorch 1.7.1 仿真（Intel Xeon E-2176M + Tesla T4），对比 Flood、随机 Gossip、固定邻居/固定概率变体；vault 自评 artifact open、复现性 high。

## 比赛映射要点

- 黑客松/算法赛：信息传播/网络覆盖类题（广播最少轮数、传染病传播控制、传感器网络唤醒）可复用「概率 + 对象联合决策」的问题拆解与图结构状态编码；有开源实现可跑，改造成本低。
- 双创申报：集群协同通信的协议层优化支撑点——广播协议是集群系统吞吐与能耗的真实瓶颈，可作为低成本的系统优化亮点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Ren2024_面向UAV-MEC的智能自适应Gossip广播协议`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `ren2024IntelligentAdaptiveGossipBased` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- signal.runnable 为本片唯一 true：依据 vault 页自评 artifact_availability 为 open、复现性 high（NS-3 + Gym + PyTorch 栈完整披露）；本次跑批未实测仓库链接，如引用建议先核对代码可得性。
