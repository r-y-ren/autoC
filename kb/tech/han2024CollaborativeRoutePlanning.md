---
id: han2024CollaborativeRoutePlanning
name: 灾害响应UAV-工人-车辆异构协同路径规划 MANF-RL-RP
field: [群智感知, 多智能体强化学习, 路径规划]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: high
signal:
  venue: IEEE/ACM Transactions on Networking
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 速度/续航/可达性异构的多代理任务分配与路线协同，本质是异构 VRP/任务指派的强化版，为"多类型资源协同调度"类决策题提供超越同质 TSP 建模的差异化框架
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 全局-局部双信息融合的异构 MARL 路径规划（MANF-RL-RP），且论文开放了实验代码与数据示例，是本组内少见的可落地参照实现
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 空-地异构机群协同作业架构可平移到农业灾害应急监测场景（灾情巡查、农田受灾评估），强化智慧农业申报的应急能力叙事
    reuse_cost: 低
sources:
  - paper_title: "Collaborative Route Planning of UAVs, Workers, and Cars for Crowdsensing in Disaster Response"
    doi: 10.1109/TNET.2024.3395493
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 灾害响应UAV-工人-车辆异构协同路径规划 MANF-RL-RP

## 单行摘要

面向灾害响应群智感知，提出异构多智能体路径规划算法 MANF-RL-RP：将 UAV、地面工人、车辆三类机动能力/续航/可达性差异显著的代理组织成互补任务系统，通过全局-局部信息融合与针对异构代理的 MARL 网络结构联合调度路线，以最大化任务完成率而非单一移动距离。

## 方法快照

- 异构建模：三类代理在速度、可达区域、地形适应性上互补，显式按代理类型建模，避免"把异构代理当同类"造成的协同效率损失。
- 信息结构：网络同时处理全局信息（跨类型协作关系）与局部信息（个体状态），兼顾协作与个体决策。
- 求解：面向异构代理的 MARL 路径规划；与 Greedy-SC-RP、MANF-DNN-RP 等基线比较任务完成率。
- 验证：数值仿真（合成场景）；论文开放实验代码与数据示例（vault 自评 artifact open、复现性 high，本卡未独立核实仓库可用性）。

## 比赛映射要点

- 数模决策题：异构 VRP/指派建模思路可直接迁移到"多类型车队/人员协同调度"题，比同质 TSP/VRP 建模更能体现代理差异性。
- 黑客松算法题：MARL 多代理调度 + 开放代码参照，适合作为多智能体路径规划类赛题的起点实现。
- 双创申报：异构协同架构支撑农业应急监测子场景（受灾巡查、多平台数据采集）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Han2024_面向灾害响应群智感知的UAV工人车辆协同路径规划`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `han2024CollaborativeRoutePlanning` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 high）承自 vault 页自评，如需引用请以论文原文复核。
