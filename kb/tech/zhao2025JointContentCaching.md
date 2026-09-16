---
id: zhao2025JointContentCaching
name: UAV-MEC内容缓存-服务放置-任务卸载联合QoE优化
field: [UAV-MEC, 边缘缓存, 匹配博弈]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: "'缓存 + 放置 + 卸载'三联决策共享同一存储/算力预算的系统建模，配 Gibbs sampling（缓存-放置组合配置）+ matching game（多任务卸载匹配）的双求解器模板，适用于边缘资源编排类赛题，比单点优化缓存或卸载的方案更完整"
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: "把异构服务能力压成单一 QoE 指标（内容命中率 + 服务时延缩减率的加权和）的评价体系设计 + 组合优化与匹配博弈混合求解，适合资源分配/服务调度类数模题的指标设计与求解章节"
    reuse_cost: 中
sources:
  - paper_title: "Joint Content Caching, Service Placement, and Task Offloading in UAV-enabled Mobile Edge Computing Networks"
    doi: 10.1109/JSAC.2024.3460049
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# UAV-MEC内容缓存-服务放置-任务卸载联合QoE优化

## 单行摘要

面向同时存在内容请求与服务请求的 UAV-enabled MEC 网络：每架 UAV 既有存储又有算力，既要决定缓存哪些内容文件，又要决定预装哪些服务，并在服务请求到达时协调任务本地处理或卸载。论文把三者绑成一个联合问题，以平均 QoE（内容命中率与服务时延缩减率的加权和）为目标——缓存/放置用 Gibbs sampling 迭代搜索高 QoE 配置，卸载用 matching game 在 CPU 核心数与计算能量约束下决定多个独立任务是否卸载及卸向哪架 UAV。

## 方法快照

- 系统建模：内容请求与服务请求共存于同一网络模型，存储预算由内容与服务共享——只优化缓存或只优化卸载都会丢失系统真实服务能力。
- 指标设计：QoE = cache hit ratio（内容满足能力）+ service delay shrinkage ratio（服务加速能力）的加权和，比单纯时延/能耗更贴近服务系统目标。
- 求解分工：缓存-放置是高维组合配置 → Gibbs sampling 迭代；卸载是多任务-多 UAV 多对一关联 → matching game，考虑 CPU 核数与能量约束。
- 基线对比：贪心缓存、随机方案、上界穷举。
- 验证：仿真（合成 UAV/UE 部署与异构请求场景，平台未明确，代码未开源）。

## 比赛映射要点

- 黑客松/算法赛：边缘节点"存什么 + 装什么 + 算什么放哪"的资源编排题可直接套用三联决策框架与双求解器分工；"异构请求统一 QoE"的指标设计在多目标服务类赛题中有复用价值。
- 数模决策题：加权指标构造（命中率 + 时延缩减率）与"组合优化 + 匹配博弈"混合求解流程，可用于平台调度/资源分配类题目的模型与求解章节写作。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhao2025_UAV-MEC中的内容缓存服务放置与任务卸载联合优化`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=medium）。
- bib 回填：citekey `zhao2025JointContentCaching` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，方法组件与基线明确但无完整代码与平台配置）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
