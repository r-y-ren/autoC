---
id: sun2024MultiobjectiveOptimizationMultiUAVassisted
name: 多UAV辅助MEC三目标联合优化（JTORATC）
field: [UAV 辅助 MEC, 多目标优化, 凸优化]
published: 2024-01-01
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
    edge: 时延/能耗/可服务任务数三目标折中 + 混合整数非凸问题三段分解（distributed splitting 与 threshold rounding 处理离散变量、KKT 解资源分配、SCA 凸化轨迹），是 NP-hard 多目标题「低复杂度工程求解」的完整模板，且求解工具链（MATLAB+CVX）披露完整
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 「固定其余变量逐一击破」的交替分解骨架可直接迁移到带截止期与能量预算的多机调度/分配类赛题，对比单目标方案的权衡分析话术现成
    reuse_cost: 中
sources:
  - paper_title: "Multi-Objective Optimization for Multi-UAV-assisted Mobile Edge Computing"
    doi: 10.1109/TMC.2024.3446819
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 多UAV辅助MEC三目标联合优化（JTORATC）

## 单行摘要

把多 UAV 辅助 MEC 中的任务完成时延、UAV 总能耗（飞行推进 + 计算）与卸载任务总数统一为多目标优化问题：三个目标天然冲突、决策变量混合离散连续且问题 NP-hard。提出 JTORATC 将原问题拆为三个可控子问题交替求解——卸载子问题用 distributed splitting 松弛二进制变量、threshold rounding 恢复整数结构；资源分配子问题借助 KKT 条件求每架 UAV 的最优配置；轨迹控制子问题用 SCA 逐步凸化——在复杂度可控前提下获得适配不同负载强度的多目标折中解。

## 方法快照

- 系统实体：多用户（任务带截止期）、多架 UAV（能量同时消耗于推进与计算，轨迹与资源分配紧耦合）、本地/空中两级计算。
- 目标体系：时延、总能耗、卸载任务数三目标并列，而非单纯时延最小化。
- 卸载子问题：distributed splitting 松弛 + threshold rounding 恢复二进制决策。
- 资源分配子问题：KKT 条件闭式求最优计算频率配置。
- 轨迹子问题：SCA 逐步逼近非凸约束。
- 验证：MATLAB R2022b + CVX 数值仿真（合成多 UAV 多用户场景，i7-8750H/8GB），求解工具链披露完整；未开源，复现性 medium。

## 比赛映射要点

- 数模：多目标权衡是数模论文的高频考点，本卡提供「三目标问题定义 + 三段分解求解 + 复杂度论证」的成套写法；分布式分裂与阈值取整处理 0-1 变量的技巧可替代粗暴整数规划。
- 黑客松：截止期约束下多机任务调度类题可复用「卸载-资源-轨迹」交替求解骨架与折中解评价方式（Pareto 思路的低配版）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Sun2024_多UAV辅助MEC多目标优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `sun2024MultiobjectiveOptimizationMultiUAVassisted` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、平台与求解器已披露但代码未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
