---
id: alkouz2022InflightEnergydrivenComposition
name: 飞行中能量共享的无人机群服务组合（EaaS）
field: [无人机群服务计算, 服务组合, 能量共享]
published: 2022-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 植保/物流无人机群"空中补能续航"叙事的代表作支撑——把能量共享上升为 Energy-as-a-Service 服务能力的系统设计思路，方案新颖度高
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 双层嵌套服务组合（群体配送 + 能量共享）+ 编队重排 + 增强 A* 的组合优化建模，可迁移到带同步到达约束的群体路径/充电调度赛题
    reuse_cost: 中
sources:
  - paper_title: "In-Flight Energy-Driven Composition of Drone Swarm Services"
    doi: 10.1109/TSC.2022.3203033
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 飞行中能量共享的无人机群服务组合（EaaS）

## 单行摘要

把城市 skyway 网络中的多包裹群体配送建模为 swarm-based drone service，并引入 support drone 的飞行中能量共享，将其抽象为 Energy-as-a-Service，构成嵌套双层服务组合问题：外层选编队形态与 support drone 数量/位置，内层用 priority-based 或 fairness-based 策略加 re-ordering 机制决定每段航程"充谁、充多久"，最终以增强 A* 搜索总配送时间最短的全局路径——减少中途停靠与地面充电等待。

## 方法快照

- 服务抽象：群体配送 = SDS（QoS 为总配送/充电/等待时间），支援机供能 = EaaS（QoS 为可共享能量、位置、时窗）。
- 预组合：先选编队，再按冗余理论与失败概率估计最优 support drone 数量并定其编队位置。
- 能量共享：priority-based 与 fairness-based 两种分配策略，处理充电次序与时长。
- 编队重排：support drone 只能近距离给相邻机充电，re-ordering 影响能耗与共享可行性。
- 全局组合：局部能量共享决策之上用 enhanced A* 最小化总配送时间。
- 约束分类：intrinsic（载重、电池）与 extrinsic（风、充电垫、同步到达时间窗）显式分离。
- 验证：London 城市路网数据驱动仿真 + DJI Phantom 3 / CrazyFlie 2.1 硬件参考，部分资产公开。

## 比赛映射要点

- 双创申报：农用植保/农村物流无人机群面临"作业半径受电池约束"的痛点，本篇的"飞行中补能 + 服务化建模"是申报书技术方案与商业模式（能量即服务）双料支撑。
- 黑客松/算法赛：带同步约束的群体路径规划 + 在线充电调度可直接复用"外层路径 + 内层共享"双层分解与 A* 框架；约束的 intrinsic/extrinsic 分类法也是建模利器。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Alkouz2022_飞行中能量驱动的无人机群服务组合`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `alkouz2022InflightEnergydrivenComposition` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2022），按 2022-01-01 填写。
- 复现性承自 vault 页自评（medium，真实数据驱动仿真 + 部分资产公开）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
