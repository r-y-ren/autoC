---
id: jin2025ResourceefficientContentSharing
name: UAV 命名数据网络的合约激励内容共享（GS 匹配）
field: [命名数据网络, 机制设计, 资源共享]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Networking
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 信息不对称下合约设计（IR/IC 约束揭示生产者私有类型）+ Gale-Shapley 多对一稳定匹配的两阶段机制，可直接套到数模双边匹配/激励相容/资源共享分配类题，GS 算法实现成本极低
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 「合同揭示类型 + 双边偏好列表 + 稳定匹配」机制组件可用于众包/P2P 分发类赛题，以减少冗余传输的能效角度形成差异化论证
    reuse_cost: 中
sources:
  - paper_title: "A Resource-Efficient Content Sharing Mechanism in Large-Scale UAV Named Data Networking"
    doi: 10.1109/TNET.2024.3474888
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# UAV 命名数据网络的合约激励内容共享（GS 匹配）

## 单行摘要

面向大规模 UAV 命名数据网络（UNDN）中内容生产者掌握私有能力信息且共享意愿不足的问题，设计「合约激励 + 稳定匹配」两阶段机制：先用合约理论在信息不对称下推导满足 IR/IC 约束的最优合同、激励生产者揭示类型，再基于双方效用构造偏好列表并用 Gale-Shapley 完成多对一稳定匹配，从而减少冗余传输、提升社会福利与能效。

## 方法快照

- 范式选择：UNDN 以内容（而非 IP 地址）为核心调度对象，适配高动态无人机群；「请求-回复」范式下生产者类型（声誉/剩余电量/缓存成本）私有。
- 阶段一（合约设计）：分别推导信息对称与不对称条件下的最优合同，满足个体理性（IR）与激励相容（IC），让生产者自选合同即揭示类型。
- 阶段二（稳定匹配）：依消费者与生产者效用函数构造双边偏好列表，Gale-Shapley 算法完成多对一稳定匹配。
- 验证：Python 数值仿真，共享量、社会福利、运行时间与能耗优于 GS 贪心与随机机制等基线；无公开代码与真实网络数据。

## 比赛映射要点

- 数模：双边匹配与激励机制是数模的分叉题型（网约车派单、资源共享、任务众包都能套），「先激励揭示类型、再稳定匹配」的两段式结构叙事清晰，GS 实现量小。
- 黑客松/算法赛：机制设计组件（合同项 + 偏好表 + 匹配）可独立成模块嵌入分发/组队类赛题；以「减少冗余传输省能」作论证角度较新颖。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Jin2025_大规模UAV命名数据网络的资源高效内容共享`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `jin2025ResourceefficientContentSharing` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16），页内容与 bib 条目相符；venue 字段照录 bib 原文（IEEE Transactions on Networking，DOI 前缀为 TNET）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: unknown，故 runnable 如实标 false）；社会福利曲线等数字如需引用请以论文原文复核。
