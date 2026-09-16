---
id: karmakar2024NovelFederatedLearningBased
name: FairLearn：联邦学习驱动的安全公平UAV-MEC控制
field: [联邦学习, 移动边缘计算, 公平性优化]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 把公平性显式写进优化目标（长期保密速率公平而非总和吞吐），合法 UAV 与干扰 UAV 的角色分工使轨迹、功率与安全速率高度耦合，是带安全/公平约束的动态决策类赛题的可借鉴建模框架
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: RL 在线生成训练数据、DNN 预测 3D 轨迹/功率/调度时间、联邦学习聚合多机模型的训练管线，适配边缘算力受限且数据分散的场景，可直接复用为多机协同控制类题目原型
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 安全公平的 UAV-MEC 服务体系（成对 UAV 执行+干扰压制保障用户保密卸载）可支撑智慧农业数据回传链路安全方案的申报叙事
    reuse_cost: 低
sources:
  - paper_title: "A Novel Federated Learning-Based Smart Power and 3D Trajectory Control for Fairness Optimization in Secure UAV-Assisted MEC Services"
    doi: 10.1109/TMC.2023.3298935
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# FairLearn：联邦学习驱动的安全公平UAV-MEC控制

## 单行摘要

针对 UAV 辅助 MEC 中安全、公平与轨迹控制三者难以兼顾的问题，提出 FairLearn 框架：成对 UAV 中一架执行用户卸载任务、另一架作为干扰机压制窃听者，先用 RL 模块在不同网络状态下生成训练数据，再用 DNN 预测 3D 轨迹、发射功率与调度时间，并通过联邦学习在多架 UAV 间聚合模型参数，最大化用户间保密速率公平性而非单纯总吞吐。

## 方法快照

- 双 UAV 角色分工：合法 UAV 负责任务卸载，干扰 UAV 对窃听链路施加抑制，执行与安全保护解耦。
- RL 造数据 + DNN 监督学习：RL 模块在多样场景生成训练集，DNN 离线预测轨迹/功率/调度，避免端到端在线 RL 的高成本探索。
- 联邦学习聚合：各 UAV 本地训练后共享模型参数，提高跨场景泛化与适应性。
- 公平性目标：以长期保密速率/吞吐公平指标刻画，而非仅最大化总和；NS-3.35 仿真验证保密速率、平均吞吐与公平性提升。

## 比赛映射要点

- 数模：安全约束下的多用户公平资源分配（Jain 公平类目标）+ 轨迹/功率耦合决策，是带公平性要求的动态优化题型可套用的建模范式。
- 黑客松/算法赛：RL 生成数据→DNN 预测控制量→FL 聚合的管线可在算力受限场景快速原型；双 UAV 攻防角色设计是安全类题目的差异化点。
- 双创申报：多机协同保障数据回传安全的完整方案叙事。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Karmakar2024_联邦学习驱动的安全公平UAV辅助MEC控制`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `karmakar2024NovelFederatedLearningBased` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 NS-3 合成场景仿真形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
