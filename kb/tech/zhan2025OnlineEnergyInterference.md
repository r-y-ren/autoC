---
id: zhan2025OnlineEnergyInterference
name: Lyapunov在线的蜂窝UAV动态目标跟踪能量干扰管理
field: [Lyapunov 优化, 蜂窝连接无人机, 目标跟踪]
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
  - track: 数模-数据分析与决策
    edge: Lyapunov 优化把长期吞吐与能量队列稳定转化为逐时隙确定性子问题（再接交替优化与 SCA），是数模动态决策题处理「长期约束+随机过程」的现成框架，可直接套写
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 把任务几何约束（跟踪半径）显式并入无线资源调度的建模手法，可差异化无人机/机器人在线调度类赛题；逐时隙决策结构便于限时赛中快速实现滚动求解器
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 无人机巡检/跟防任务的续航与通信质量联合保障论证（能量队列稳定 + 长期吞吐），支撑智慧农业低空长时作业方案
    reuse_cost: 低
sources:
  - paper_title: Online Energy and Interference Management for Dynamic Target Tracking with Cellular-Connected UAV
    doi: 10.1109/TMC.2025.3532276
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# Lyapunov在线的蜂窝UAV动态目标跟踪能量干扰管理

## 单行摘要

面向蜂窝连接 UAV 持续跟踪随机移动目标（高斯马尔可夫运动）的场景，联合优化 UAV 轨迹、功率分配、基站关联与资源块使用；用 Lyapunov 优化把长期吞吐最大化与能量队列稳定转化为逐时隙确定性问题，每时隙再以最优结构分析、交替优化与 SCA 联合求解，在目标随机运动与空地上行互扰耦合下兼顾跟踪任务与蜂窝网络性能。

## 方法快照

- 问题结构：目标运动随机导致飞行能耗不可预测；UAV 上行与地面设备共享蜂窝资源块产生互扰——跟踪几何约束与通信资源调度被显式写入同一主问题。
- Lyapunov 框架：能量队列刻画长期续航状态，把多阶段随机优化拆成逐时隙确定性子问题，无需未来目标运动信息。
- 逐时隙求解：最优结构分析 + 交替优化 + SCA 处理基站关联、功率分配与三维轨迹的耦合。
- 建模要点：目标跟踪半径作为几何可见性约束直接进入每时隙决策，说明「感知任务约束」如何进入「通信设计」。
- 验证为合成场景数值仿真，建模与参数披露较细但未给出统一仿真平台信息。

## 比赛映射要点

- 数模决策题：长期约束 + 随机 arrivals 的在线决策题（库存、能源、无人机调度）可整体套用 Lyapunov drift-plus-penalty 写法，把「约束满足」化为队列稳定性证明。
- 黑客松/算法赛：限时实现的滚动时域调度器可直接复用其逐时隙子问题分解；跟踪半径类几何约束的处理方式可移植到围捕/护航/巡线题。
- 双创申报：长时巡检任务的续航-通信联合保障论证段可复用。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhan2025_蜂窝连接UAV动态目标跟踪的在线能量与干扰管理`（4 枚举字段承自页 frontmatter）。
- bib 回填：citekey `zhan2025OnlineEnergyInterference` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性 medium 承自 vault 页自评：无统一仿真平台与开源代码披露，如需引用请以原文复核。
