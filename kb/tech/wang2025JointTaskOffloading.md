---
id: wang2025JointTaskOffloading
name: ILCTS：动态UAV-MEC卸载与迁移模仿学习
field: [UAV 辅助边缘计算, 模仿学习, 任务调度]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 移动用户场景下把"初始卸载+执行中迁移"拆成两级动态重调度决策（CTMiG 问题），比一次性静态分配更贴近动态服务维持类赛题的真实约束
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 改进 PPO 造专家数据、GAIL 模仿学习逼近、在线持续修正的三段式训练流水线，是专家样本稀缺时加速复杂调度决策收敛的通用模板
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济/UAV-MEC 弹性服务叙事的技术支撑点（移动用户下的服务连续性保障，硬/软时延分级 QoS）
    reuse_cost: 低
sources:
  - paper_title: "Joint Task Offloading and Migration Optimization in UAV-enabled Dynamic MEC Networks"
    doi: 10.1109/TSC.2025.3576644
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# ILCTS：动态UAV-MEC卸载与迁移模仿学习

## 单行摘要

针对移动用户导致链路波动的 UAV 辅助 MEC 网络，把"任务卸载到哪"扩展为"卸载之外还要不要在执行中迁移"的两级决策问题（CTMiG），提出 ILCTS 框架：离线用改进 PPO 训练专家策略生成高质量状态-动作对，在线用 GAIL 对抗模仿学习逼近专家行为并持续与环境交互修正，以更快的收敛拿到高质量卸载/迁移决策，满足硬/软时延分级要求并降低平均时延。

## 方法快照

- 系统设定：多架固定 UAV 提供 MEC 服务，用户连续移动并随机生成任务；SDN 控制器集中收集状态做服务决策。
- 问题建模：CTMiG 转化为 MDP，状态含用户位置、UAV 服务状态与任务时延要求；决策含初始卸载与执行中迁移，任务分硬/软时延两类。
- 训练流水线：离线改进 PPO 生成专家策略 → GAIL 生成对抗模仿 + 在线学习持续修正，避免只会复刻专家而缺乏自适应。
- 验证：Python 3.8 + PyTorch 1.10 仿真，BonnMotion-3.0.1 生成 1000 条移动轨迹（合成场景，未开源）。

## 比赛映射要点

- 数模决策题：动态环境下的服务分配/再分配（如应急资源调度、共享运力调度）可直接套用"初始分配 + 重分配"两级决策建模，把迁移成本显式写进目标函数即是与静态分配基线的差异化论证。
- 黑客松/算法赛：PPO 生成专家数据 + GAIL 模仿的三段式训练适用于交互环境昂贵、随机策略起步慢的在线决策题。
- 双创申报：低空智联网、无人机边缘服务平台的方案支撑点（服务连续性、QoS 分级叙事）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2025_动态UAV_MEC网络中的任务卸载与迁移优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `wang2025JointTaskOffloading` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
