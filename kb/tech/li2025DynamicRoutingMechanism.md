---
id: li2025DynamicRoutingMechanism
name: LAMAIC：边缘缓存UAV群网络的动态路由与负载分配
field: [UAV 群网络, 延迟容忍网络, 边缘缓存]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 用 Lyapunov 队列漂移把负载均衡写成队列稳定控制，综合路由度量（中心性/关系强度/剩余缓存）可直接迁移到物流配送、网络流量调度类题目的拥塞与均衡联合建模
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: DTN 携带转发 + ICN 缓存检索 + 队列稳定控制的组合拳，适配间歇连接网络/内容分发类算法题，区别于单指标最短转发或纯复制泛洪基线
    reuse_cost: 高
  - track: 双创-文书与申报
    edge: 农田弱连接环境下无人机群数据回传网络的组网与拥塞控制方案技术支撑（TMC 2025，边缘缓存+DTN 融合）
    reuse_cost: 低
sources:
  - paper_title: "Dynamic Routing Mechanism for Load Distribution in UAV Swarm Networks with Edge Caching"
    doi: 10.1109/TMC.2025.3589569
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# LAMAIC：边缘缓存UAV群网络的动态路由与负载分配

## 单行摘要

面向连接间歇、拓扑持续变化的 UAV 群网络，把延迟容忍网络（DTN）、信息中心网络（ICN）与边缘缓存融合为 LAMAIC 路由框架：兴趣包先查簇内缓存索引再决定转发，用社会中心性、关系强度、连接强度与剩余缓存空间构造综合转发打分，并以 Lyapunov 队列漂移约束单节点积压、引入 MAIC 定制化协同通信降低冗余，在动态拓扑下同时优化交付率、时延与负载均衡。

## 方法快照

- 问题结构：传统 DTN 路由依赖单一转发指标，流量吸附到少数高中心节点，造成局部拥塞与缓存利用不均。
- 缓存层：ICN 内容缓存与兴趣包检索嵌入 DTN，簇内哈希表记录内容位置，避免全网洪泛搜索。
- 路由层：中心性+关系强度+连接强度+剩余缓存空间合并为综合转发打分。
- 控制层：Lyapunov 漂移函数把负载均衡转化为队列稳定问题；MAIC 让每个代理只向特定队友发定制信息，降低稀疏网络协同开销。
- 验证：数值仿真（开源三维 Gaussian-Markov 机动模型生成拓扑，合成负载）；统一平台与开源情况未说明。

## 比赛映射要点

- 数模决策题：路由控制与负载均衡统一建模的思路，可套到"多设施流量分配+拥塞控制"类题目；Lyapunov 队列稳定是可复用的控制论工具。
- 黑客松算法题：多指标综合打分 + 队列积压约束的转发策略，在弱网/间歇连接类赛题中优于贪心最短路。
- 双创申报：农田物联网弱连接数据回传场景的组网方案支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2025_面向边缘缓存UAV群网络的动态路由负载分配`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `li2025DynamicRoutingMechanism` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 low）承自 vault 页自评，如需引用请以论文原文复核。
