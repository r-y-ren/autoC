---
id: tao2024MultiagentCooperationComputing
name: 多UAV空中计算的多智能体协同算力调度
field: [空中计算, 多智能体强化学习, 无人机轨迹优化]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 出发站/悬停点选址+多UAV轨迹+能效公平双目标的联合优化建模，最小跳数标准差是现成的服务公平性指标，可迁移到设施选址、巡检服务与公平覆盖类数模赛题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 多智能体 Q-learning/soft Q-learning 调度组件适配多机器人任务分配与路径规划赛题，奖励中显式纳入公平性目标是区别于普通最短路式规划方案的差异化点
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业植保场景中起降点选址、作业航线与多机协同服务公平的联合规划技术支撑点（JSAC 2024 系统级方案）
    reuse_cost: 低
sources:
  - paper_title: Multi-Agent Cooperation for Computing Power Scheduling in UAVs Empowered Aerial Computing Systems
    doi: 10.1109/JSAC.2024.3459035
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 多UAV空中计算的多智能体协同算力调度

## 单行摘要

面向 UAV 赋能的空中计算系统，将多 UAV 协同服务拆为两层决策：用多智能体（自适应）Q-learning 做轨迹规划以提升能效，同时把出发站与悬停点位置拉回优化变量集合、以最小跳数标准差为目标优化布局以改善服务公平性——在电池受限与用户需求异质条件下同时优化能效与公平。

## 方法快照

- 场景建模：多 UAV 自单一出发站起飞，经多个悬停点为地面用户提供数据收集与轻量计算服务，需完全覆盖并限制每机往返次数。
- 轨迹层：多智能体学习/自适应 Q-learning 规划 UAV 轨迹，奖励同时包含能效与公平性目标（非单一累计收益）。
- 布局层：联合优化出发站与悬停点位置，使用户最小跳数分布更均衡，改善边缘用户可达性。
- 关键洞见：空中计算的算力调度深度依赖服务几何结构（在哪里服务与如何飞同样关键），纯能效目标会牺牲弱连接用户。
- 验证：数值仿真（合成用户场景），Python 3.9 / Ubuntu 18.04 环境，未报真实飞行实验，无开源说明。

## 比赛映射要点

- 数模决策类：选址（出发站/悬停点）+ 路径（轨迹）+ 双目标（能效/公平）的三层耦合是典型优化建模骨架；公平性用最小跳数标准差量化，比泛泛的覆盖率高更可辩护。
- 黑客松算法赛：多智能体 Q-learning 组件可替换常规贪心/最短路基线；把公平性写进奖励函数是低成本改造点。
- 双创申报：智慧农业多机植保作业中「起降点怎么选、航线怎么飞、小农户服务怎么公平」的成套说辞支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Tao2024_空中计算系统中的多智能体协同算力调度`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）。
- bib 回填：citekey `tao2024MultiagentCooperationComputing` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
