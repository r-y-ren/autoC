---
id: zhao2025MultiUAVCooperativeTask
name: 动态环境多UAV协同任务调度（TF-PPO+MOGS）
field: [多无人机协同, 任务调度, 稳定匹配]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Computers
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: "'学习层管怎么飞 + 匹配层管接谁的活'的双层结构：TF-PPO 用任务因子化网络稳定多 UAV 协同训练，Many-to-One Gale-Shapley（MOGS）免中心服务器完成动态任务流的多对一快速匹配——动态任务到达 + 用户移动类调度赛题的现成骨架"
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: "把完成任务数/时延/吞吐统一压成吞吐最大化的目标归并手法，以及 Gale-Shapley 稳定匹配改造多对一关联的调度求解器，可用于动态匹配/调度类数模题，与整数规划基线形成对照"
    reuse_cost: 低
sources:
  - paper_title: "A Multi-UAV Cooperative Task Scheduling in Dynamic Environments：Throughput Maximization"
    doi: 10.1109/TC.2024.3483636
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 动态环境多UAV协同任务调度（TF-PPO+MOGS）

## 单行摘要

把动态环境中的多 UAV 协作计算统一写成吞吐最大化问题（同时压合完成任务数、时延与吞吐三个指标）：TF-PPO 在 PPO 上叠加任务因子化（task factorization）网络学习多 UAV 协同部署与动作选择，保持动态环境下的训练稳定性；Many-to-One Gale-Shapley 机制（MOGS）基于稳定匹配思想改造，处理持续移动设备与随机到达异构任务（含依赖任务与独立任务）到 UAV 的多对一快速关联，免中心服务器介入。

## 方法快照

- 问题定位：任务集与用户位置持续变化的连续时间环境——静态时隙优化假设失效，协同部署与任务调度必须统一考虑，任何一端都会成为瓶颈。
- 目标归并：完成任务数、时延、吞吐统一进吞吐最大化单目标。
- 学习层 TF-PPO：任务因子化改善多 UAV 全局动作选择质量与协同训练稳定性。
- 匹配层 MOGS：多对一稳定匹配，支持动态到达任务，无需额外中心服务器。
- 验证：Windows 10 仿真，RTX 3090 + Xeon Gold 6226R，对比不同协同与调度策略；无标准化代码与环境封装（未开源）。

## 比赛映射要点

- 黑客松/算法赛：动态任务流 + 移动服务节点的调度题可复用"部署层 RL + 匹配层博弈"双层分工；MOGS 的多对一稳定匹配可单独抽出作为任务分配组件，比每轮重解整数规划更快。
- 数模决策题：多指标归并为吞吐单目标的建模手法 + 改造稳定匹配做动态关联，适合作为动态调度类题的求解方案与对比论证素材。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhao2025_动态环境中的多UAV协同任务调度`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=medium）。
- bib 回填：citekey `zhao2025MultiUAVCooperativeTask` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- YAML 留痕：bib 标题原文含 ASCII「冒号+空格」（Environments: Throughput），按分片协议改全角「：」写入 paper_title。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，硬件与超参有披露但无标准化代码）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
