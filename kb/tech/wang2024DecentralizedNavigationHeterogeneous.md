---
id: wang2024DecentralizedNavigationHeterogeneous
name: 异构联邦强化学习的UAV-MEC分布式导航
field: [联邦强化学习, 多UAV导航, 移动边缘计算]
published: 2024-01-01
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
    edge: 「上层技能策略抽象通用导航技能 + 云端聚合相似策略 + UAV 端自适应梯度过滤」三层结构，是多智能体协同控制赛题中异构智能体（性能 / 载荷不同）知识共享的可复用架构，规避朴素参数共享的负迁移坑
    reuse_cost: 高
  - track: 双创-文书与申报
    edge: 异构无人机混编机队（不同续航 / 覆盖 / 算力）协同作业方案的算法支撑点，论文实证约三分之一训练轮数达到约 2.7 KB/J 能效且对异构度变化更稳健
    reuse_cost: 低
sources:
  - paper_title: "Decentralized Navigation with Heterogeneous Federated Reinforcement Learning for UAV-enabled Mobile Edge Computing"
    doi: 10.1109/TMC.2024.3439696
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 异构联邦强化学习的UAV-MEC分布式导航

## 单行摘要

面向异构 UAV-enabled MEC 的分布式导航：各 UAV 覆盖半径、最大速度与算力不同，集中式训练不现实，直接参数共享又会破坏个体差异。论文提出 SHDRLN 分层强化学习（上层技能策略把原子动作抽象为通用 skill、下层技能网络执行），配合 DFRL 异构联邦方法——服务器端只聚合相似 SPN 参数、UAV 端对不适合自身的更新做自适应梯度过滤——在保留分布式执行的同时实现跨异构 UAV 的知识共享，提升整体任务卸载能效。

## 方法快照

- 系统实体：多架异构 UAV、移动用户、云端聚合服务器；各 UAV 仅凭局部观测独立决策。
- 分层抽象：SHDRLN 用高层 skill 策略压缩异构策略差异，使不同性能 UAV 的知识可对齐。
- 联邦个性化：DFRL 聚合相似策略参数 + 本地梯度过滤，避免负迁移。
- 实验结论：SHDRLN(DFRL) 比 SHDRLN 与 SAC 能效更稳、更大异构差异下下降更平缓；约 1/3 训练轮数达到约 2.7 KB/J 平均能效。
- 验证：数值仿真、合成多 UAV-MEC 场景，多组异构性敏感性实验；平台与代码未披露，无开源。

## 比赛映射要点

- 黑客松算法类：多机协同 / 集群控制赛题中，「skill 抽象 + 相似策略聚合 + 本地过滤」可直接作为异构智能体团队学习的架构参考，区别于常规 CTDE 基线的差异化点。
- 双创申报：农业 / 巡检混编机队（多机型协同）申报书的协同学习与能效数据支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2024_异构联邦强化学习的UAV_MEC分布式导航`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2024DecentralizedNavigationHeterogeneous` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
