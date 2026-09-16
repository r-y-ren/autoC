---
id: huang2025FastUAVTrajectory
name: FedX：RIS 辅助 UAV 轨迹规划的联邦加速学习
field: [RIS 辅助通信, 轨迹规划, 强化学习加速]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 把训练速度提为一等系统目标——多线程视作类联邦聚合的协作代理（FedX），FedSAC/FedPPO 两个实例化可在 RL 类赛题限时训练场景整体移植，显著缩短从开题到可用策略的时间
    reuse_cost: 中
  - track: Kaggle-竞赛
    edge: Kaggle simulation/code competition 有严格运行时上限，并行采样 + 模型聚合的加速配方适配限时训练预算，协作代理聚合思想亦可扩展到多 seed 策略集成
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: RIS 增强 UAV-地面链路且考虑不完整信道信息的低空覆盖方案，是低空经济通信基础设施申报的差异化技术点
    reuse_cost: 低
sources:
  - paper_title: "A Fast UAV Trajectory Planning Framework in RIS-assisted Communication Systems with Accelerated Learning via Multithreading and Federating"
    doi: 10.1109/TMC.2025.3544903
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# FedX：RIS 辅助 UAV 轨迹规划的联邦加速学习

## 单行摘要

针对 RIS 辅助 UAV 通信中轨迹规划响应慢的问题，提出 FedX 训练加速框架：把多个线程当作协作训练代理，以类联邦学习的方式聚合模型并行训练 RL 求解器，并实例化出 FedSAC 与 FedPPO 两种快速轨迹规划算法——在保持轨迹质量的同时显著缩短训练时间，把「更快收敛」当作与性能并列的一等系统目标。

## 方法快照

- 系统建模：RIS 辅助 UAV-地面终端通信，考虑不完整信道信息与四旋翼能耗模型；动作空间含水平/垂直运动、终端调度与时间片长度。
- FedX 核心：多线程即协作代理，按联邦学习式聚合并行训练，线程间模型互补加速收敛。
- 两个实例化：FedSAC 与 FedPPO，分别继承各自 RL 求解器的能力并叠加聚合加速。
- 验证：Python 3.10 数值仿真（合成场景），对比标准 RL 的训练速度与轨迹性能；硬件与开源情况论文未说明。

## 比赛映射要点

- 黑客松/算法赛：限时内要交出可用策略是常态，FedX 的「线程即代理 + 聚合」不改算法本体即可加速，工程移植面小。
- Kaggle：simulation 赛题训练预算紧张，加速配方直接对位 code competition 的运行时限制；聚合机制还能顺手做多 seed 集成。
- 双创申报：RIS + UAV 的低空通信增强叙事贴合低空经济政策方向。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Huang2025_RIS辅助通信中基于FedX加速学习的快速UAV轨迹规划`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `huang2025FastUAVTrajectory` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16），页内容与 bib 条目相符。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: unknown，故 runnable 如实标 false）；加速比等数字如需引用请以论文原文复核。
