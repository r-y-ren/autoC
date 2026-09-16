---
id: yu2025HybridTransformerBased
name: HTransRL：空中走廊多UAV协同混合Transformer强化学习
field: [多智能体强化学习, Transformer, 无人机协同]
published: 2025-01-01
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
    edge: Transformer 编码可变规模局部观测 + actor-critic + curriculum learning 的 MAPOMDP 求解范式，多机避碰/协同通行类赛题可整链复用；vault 页自评工件开源、复现性 high，可作直接起点
    reuse_cost: 低
  - track: Kaggle-竞赛
    edge: Kaggle 模拟对抗赛（多智能体环境、单位数量可变）中「可变数量实体的观测编码 + 课程式由易到难训练」是通用技巧，对固定维度策略网络是明确升级点
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济空中走廊（空域基础设施化）管理方案的协同通行技术支撑点——部分可观测下高到达率、低碰撞/越界的量化指标体系可直接写进申报书
    reuse_cost: 低
sources:
  - paper_title: "Hybrid Transformer Based Multi-Agent Reinforcement Learning for Multiple Unpiloted Aerial Vehicle Coordination in Air Corridors"
    doi: 10.1109/TMC.2025.3532204
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# HTransRL：空中走廊多UAV协同混合Transformer强化学习

## 单行摘要

面向空中走廊约束下的多 UAV 协同通行，把问题建成部分可观测多智能体决策过程（MAPOMDP）：每架 UAV 只感知局部观测球内的他机与非协同飞行物（NCFO），状态规模随 UAV 数量动态变化；提出 HTransRL 用 Transformer 编码可变长度局部观测、与 actor-critic 联合训练，并叠加 curriculum learning 从低复杂度走廊渐进过渡到高复杂度空域，兼顾到达率、避碰、不越界与旅行时间。

## 方法快照

- 建模：MAPOMDP——局部球形观测、走廊连接方式与长度训练中随机变化，属典型部分可观测 + 动态规模场景。
- 网络架构：hybrid Transformer + actor-critic——Transformer 负责可变规模邻居/障碍集合的时空依赖编码，RL 侧保证控制效率；对比普通注意力/MLP 策略的优势在可变维度输入的优雅处理。
- 训练策略：curriculum learning 由简到繁提升泛化与可扩展性，是一次性固定难度训练的显式升级。
- 评测指标：到达率、碰撞次数、越界次数、旅行时间。
- 验证：仿真（合成走廊与随机移动障碍），硬件 NVIDIA RTX 3090；vault 页自评工件开源（artifact_availability=open）、复现判断 high；缺真实飞行闭环验证。

## 比赛映射要点

- 黑客松：多机调度/避碰类赛题（无人机、AGV、机器人）可直接复用「可变规模观测编码 + 课程训练」整条链；开源工件降低复现成本。
- Kaggle：Lux AI 等模拟赛的多智能体环境里，单位数量可变导致的观测维度问题与本文完全同构，Transformer 编码是现成解法。
- 双创申报：低空经济叙事下「空中走廊协同通行」的量化安全指标（到达率/碰撞/越界）可直接引用为方案评估框架。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Yu2025_空中走廊多UAV协同的混合Transformer强化学习`（vault 页 4 枚举字段 venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=high 已迁移至本卡）。
- bib 回填：citekey `yu2025HybridTransformerBased` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；`signal.runnable=true` 依据 vault 页自评（artifact_availability=open、开源情况 open、复现判断 high），本分片未获具体仓库链接，如需引用请先核对论文与公开仓库；其余验证类信息承自 vault 页自评。
