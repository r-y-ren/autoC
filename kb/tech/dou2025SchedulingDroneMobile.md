---
id: dou2025SchedulingDroneMobile
name: 无人机-移动充电车混合动作协同调度（HaDMC）
field: [混合动作强化学习, 充电调度, 无人机持续作业]
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
    edge: 离散-连续混合动作的 RL 解法组件（latent action + embedding/AAE action decoder + mutual learning）是双主体异构协同调度赛题的通用模块，代码公开可直接改造复现
    reuse_cost: 低
  - track: 双创-文书与申报
    edge: 植保/巡田无人机持续作业叠加移动充电车途中补能的整系统方案，直击农业无人机续航痛点，技术方案与原型演示都易落地
    reuse_cost: 低
sources:
  - paper_title: "Scheduling Drone and Mobile Charger via Hybrid-Action Deep Reinforcement Learning"
    doi: 10.1109/TMC.2025.3551386
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 无人机-移动充电车混合动作协同调度（HaDMC）

## 单行摘要

面向单无人机持续观测多 PoI、移动充电车随行补能的协同场景，把两侧"去哪儿/充放电点"的离散选择与"观察多久/充多久"的连续控制建模为混合动作多阶段决策问题，提出 HaDMC：策略网络先输出潜在连续动作，再由 embedding table 与 AAE 组成的 action decoder 分别恢复离散与连续动作，并以 mutual learning 保留离散-连续、无人机-充电车之间的动作耦合，学出时间效率更高的 drone-charger 联合调度。

## 方法快照

- 问题结构：无人机按序访问 PoI（观测时长有上下限、效用随之变化），仅能在指定充电点与移动充电车会合补能；双方都从仓库出发并返回。
- 混合动作建模：两个异构主体的动作均为离散 + 连续耦合，传统单一动作空间 RL 难以直接处理。
- HaDMC 三件套：latent action 表示 + action decoder（embedding table 恢复离散动作、AAE 恢复连续动作）+ mutual learning 保耦合。
- 训练与目标：经验回放 + 噪声探索下优化潜在策略，目标为观测效用与总时间之比最大化。
- 验证：custom Python simulator + PyTorch 2.0.1（RTX 4070 Ti），代码公开，复现性 high。

## 比赛映射要点

- 黑客松/算法赛：混合动作空间（是否转移 + 停留/充电时长）在续航受限调度题里高频出现；action decoder 方案可整体搬进已有 RL 代码库，也可退化为"离散选择 + 连续时长两阶段启发式"做快速基线，开源代码降低复现成本。
- 双创申报：农业无人机换电/充电车协同的持续作业方案可直接以此为技术蓝本，演示原型成本低。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Dou2025_无人机与移动充电车混合动作协同调度`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `dou2025SchedulingDroneMobile` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 high、验证形态 simulation/synthetic 承自 vault 页自评（artifact_availability: open，代码已公开）；本卡 signal.runnable 依章程按"是否找到可跑实现"如实标 true（依据 vault 页开源自评），与分片模板默认 false 不同，特此声明。
