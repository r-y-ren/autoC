---
id: hoang2025Adaptive3DPlacementa
name: 6G空中小蜂窝多UAV基站自适应三维部署
field: [UAV 基站部署, 深度强化学习]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: K-means 动态聚类划分服务区 + 队列稳定约束下的三维选址调整，是"时变需求下的动态设施选址"类决策题的可复用建模套路，比静态选址模型更贴合需求漂移场景
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: Lyapunov drift-minus-reward 引导 critic 评分（替代纯神经网络 critic）的 actor-critic 变体，附流量热力图状态编码，是部署/调度类赛题中稳定 DRL 训练的可迁移技巧
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 需求热区感知的多机空中基站动态部署可为农业应急通信保障（灾区/偏远农田覆盖）提供方案支撑
    reuse_cost: 低
sources:
  - paper_title: "Adaptive 3D Placement of Multiple UAV-mounted Base Stations in 6G Airborne Small Cells with Deep Reinforcement Learning"
    doi: 10.36227/techrxiv.174235547.72508683/v1
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 6G空中小蜂窝多UAV基站自适应三维部署

## 单行摘要

面向用户位置与业务流量持续变化的 6G 空中小蜂窝，先以 K-means 动态聚类将移动用户分配到各 UAV-BS，再用 actor-critic DRL 调整多 UAV-BS 的三维位置：actor 输入拼接用户流量热力图，critic 不用纯神经网络而以 Lyapunov drift-minus-reward 作标签引导，在队列稳定与长期推进功率约束下最大化用户长期 MOS（满意度均分）。

## 方法快照

- 问题结构：traffic-aware 动态 3D placement——未完成下载在 UAV-BS 队列形成 backlog，服务质量与队列稳定强耦合。
- 聚类层：K-means 周期性动态聚类，适应移动用户分布。
- 控制层：DNN actor 产生候选移动决策，Lyapunov-guided critic 选择最优动作；策略网络周期性重训练以跟随时变网络。
- 约束：队列稳定、UAV 最大速度、长期平均推进功率。
- 验证：数值仿真（合成场景）；未说明平台与开源。

## 比赛映射要点

- 数模决策题：动态聚类+选址+稳定性约束的组合可整体迁移到"需求随时间漂移的服务设施动态选址"题。
- 黑客松算法题：Lyapunov 引导 critic 与热力图状态编码是 DRL 训练稳定化的即用技巧。
- 双创申报：支撑应急/偏远区域空中通信覆盖类方案设计。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Hoang2025_6G空中小蜂窝中多UAV基站自适应三维部署`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `hoang2025Adaptive3DPlacementa` → 标题/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）；**bib 未回填到 venue**，DOI 指向 TechRxiv 预印本，signal.venue 按空值省略，venue_tier=CCF-A 系 vault 页自评、与预印本出处存在张力，引用前请以论文正式发表信息复核。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评。
