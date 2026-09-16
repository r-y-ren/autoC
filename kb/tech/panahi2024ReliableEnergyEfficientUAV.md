---
id: panahi2024ReliableEnergyEfficientUAV
name: 成本感知的激光与可再生能源UAV通信供能优化
field: [UAV 通信, 能量采购优化, 无线供能]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: supporting
paper_role: supporting
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 按时段决策从机载电池、激光链路、可再生能源各采购多少能量的分时优化，加上剩余能量经 WPT 反售的成本抵消机制，多时段多能源来源成本最小化是典型数模决策题结构
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 绿色低碳叙事支撑——可再生能源 + 激光补能的无人机长航时通信/监测方案，把能源采购成本与售能收益写进运营模型让商业闭环更可信
    reuse_cost: 低
sources:
  - paper_title: "Reliable and Energy-Efficient UAV Communications: A Cost-Aware Perspective"
    doi: 10.1109/TMC.2023.3284531
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 成本感知的激光与可再生能源UAV通信供能优化

## 单行摘要

面向通信型 UAV 的长航时问题，把供能系统拆为机载电池、地面激光束与本地可再生能源三部分，联合优化运行周期内各时段的能量采购量与成本感知的 UAV 放置位置，在保障链路质量的同时最小化总能源采购成本；可再生能源富余时还可经 WPT 向低功耗地面设备售能形成成本抵消——把「能源从哪买、买多少、成本怎么算」显式写进 UAV 通信主问题。

## 方法快照

- 问题转向：既有能效文献优化「能量怎么用」，本文优化「能量怎么买」——目标函数是总能源采购成本而非推进/通信功耗。
- 分时能量采购：按时间分段决定各时段从电池与激光链路获取的能量量，最小化总体采购成本。
- 成本感知放置：UAV 位置同时决定通信链路质量与激光供能接收条件，需联合权衡。
- 售能机制：可再生能源富余时经 WPT 转给地面低功耗设备，形成「供能-通信-收益」联动。
- 验证：合成参数场景仿真（MATLAB + YALMIP）；未开源。

## 比赛映射要点

- 数模决策题：多时段、多来源、带反售收益的能量采购/调度建模可直接作为数模优化题的建模骨架（时段决策变量 + 成本目标 + 放置耦合约束）。
- 双创申报：绿色能源 + 无人机运维是智慧农业/低空经济申报的高频叙事，「能源采购成本 + 售能抵消」的运营经济性建模是区别于纯技术方案的具体支撑点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Panahi2024 激光与可再生能源协同供能的UAV通信成本优化`（4 枚举字段自 vault 页 frontmatter 迁移；shard 清单未带 paper_role，按 vault 页自评补 supporting）。
- bib 回填：citekey `panahi2024ReliableEnergyEfficientUAV` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
