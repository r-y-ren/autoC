---
id: gao2024ServiceExperienceOriented
name: 服务体验比导向的缓存UAV-MEC协同计算
field: [边缘计算, 服务缓存, 分式优化]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: SER（满足体验要求的服务比例）把公平性写进目标函数，配 Dinkelbach 分式规划与四阶段交替迭代的求解框架，是资源分配-公平性权衡类数模题的方法论模板
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空服务网络中缓存、算力、轨迹联动的体验导向设计论证，支撑智慧农业按需服务分发（图像/模型推送）方案章节的差异化卖点
    reuse_cost: 低
sources:
  - paper_title: "Service Experience Oriented Cooperative Computing in Cache-Enabled UAVs Assisted MEC Networks"
    doi: 10.1109/TMC.2024.3366944
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 服务体验比导向的缓存UAV-MEC协同计算

## 单行摘要

在缓存使能 UAV 辅助 MEC 网络中引入服务体验比（SER）指标——满足体验要求的服务占申请总量的比例，把目标从平均时延最优转向用户实际体验；将任务卸载、资源分配、轨迹规划与服务缓存放置统一进一个分式混合整数非凸模型，用 Dinkelbach 方法处理分式结构、连续凸化处理子问题、四阶段交替迭代逐步逼近联合方案，在 UAV 能量预算与时延约束下让更多用户获得可接受服务质量。

## 方法快照

- 角色建模：UAV 同时是通信中继、边缘计算节点与缓存节点，体验由多类资源共同决定。
- 指标设计：SER 把用户侧感知质量（体验达标比例）写入目标，替代平均时延这类总体指标。
- 求解链：Dinkelbach 参数化分式目标 → 卸载/资源/缓存/轨迹四阶段交替迭代 → CVX 凸求解连续子问题。
- 验证：CVX 数值仿真（合成场景），未开源。

## 比赛映射要点

- 数模：体验达标比例型目标 + 公平性约束是资源分配题的高阶写法；Dinkelbach + 交替迭代的求解链有现成代码范式（CVX/scipy 可复刻），可直接搬进答卷。
- 双创申报：低空经济服务网络叙事中，缓存命中 + 算力调度 + 轨迹联动以保体验的方案，可作为智慧农业图像/模型按需分发的差异化技术点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Gao2024_面向服务体验的缓存使能UAV辅助MEC协同计算`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `gao2024ServiceExperienceOriented` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
