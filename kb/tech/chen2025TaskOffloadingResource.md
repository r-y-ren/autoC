---
id: chen2025TaskOffloadingResource
name: 博弈论驱动的UAV边缘卸载与资源定价
field: [移动边缘计算, 博弈论, 资源定价]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 两阶段博弈建模（用户分配非合作博弈 + 服务器定价 Stackelberg 博弈，逆向归纳证唯一均衡），可迁移到平台定价/资源共享分配类数模赛题，均衡存在性论证可提升模型说服力
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: GBUA 迭代求 Nash 均衡 + RPATO 迭代近似 Stackelberg 均衡的算法套路，可用于多方利益冲突的分配/定价类算法题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 无人机边缘算力"按量计费/服务定价"的商业模式建模支撑（UAV 能耗约束下的最优报价叙事）
    reuse_cost: 低
sources:
  - paper_title: "Task Offloading and Resource Pricing Based on Game Theory in UAV-assisted Edge Computing"
    doi: 10.1109/TSC.2024.3512936
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 博弈论驱动的UAV边缘卸载与资源定价

## 单行摘要

在地面 BS 边缘服务器与 UAV 边缘服务器共存的 MEC 系统中，把"用户去哪卸"与"算力卖多少钱"联合建模为两阶段博弈：先以服务器总能耗最小为目标，把多用户服务器分配写成非合作博弈并证明 Nash 均衡存在（GBUA 算法迭代求解）；再把 BS-ES 与 UAV-ES 视为 leaders、用户视为 followers 建立 Stackelberg 定价-卸载博弈，经逆向归纳证明唯一均衡并用 RPATO 算法近似——从纯技术调度走向机制设计与服务交互。

## 方法快照

- 双服务器市场：BS-ES 与 UAV-ES 都向用户出售闲置算力；UAV 侧悬停与计算能耗预算约束进服务器效用。
- 用户效用：时延、能耗之外还含卸载满意度与时延超阈的 reward-penalty 项；服务器效用为收入减能耗与奖惩项。
- 阶段一（分配）：假定完全卸载，最小化服务器总能耗；非合作博弈证 NE 存在，GBUA 迭代更新用户选择。
- 阶段二（定价-卸载）：多 leader（服务器定价）-多 follower（用户卸载量）Stackelberg 模型，逆向归纳证唯一均衡，RPATO 迭代搜索近似解。
- 验证：合成场景数值仿真，未开源。

## 比赛映射要点

- 数模赛：定价与分配耦合的决策题（共享算力、平台经济）可直接借鉴"先分配后定价"的两阶段分解与均衡存在性证明写法。
- 黑客松/算法赛：多方效用冲突下的迭代均衡算法（GBUA/RPATO 思路）可迁移到拍卖、资源竞争类题。
- 双创申报：无人机边缘算力服务的计费机制与商业模式论证素材。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Chen2025_博弈论驱动的UAV辅助边缘计算卸载与资源定价`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `chen2025TaskOffloadingResource` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（low，实验资产链条说明有限，当前定位为方法理解支撑）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
