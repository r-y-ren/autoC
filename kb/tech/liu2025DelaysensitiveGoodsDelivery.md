---
id: liu2025DelaysensitiveGoodsDelivery
name: FH-MDP：多任务无人机时敏配送与在途感知的阈值策略
field: [低空物流, 有限时域 MDP, 在线决策]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 硬时限配送+软收益感知的双目标 FH-MDP 建模，通过证明 Bellman 方程单调性与次模性把动态规划压成可在线执行的阈值规则，对时限路径规划类赛题（农村物流、巡检采集）兼具最优性与可解释性
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 带可证明阈值结构的在线策略替代逐步 DP 或黑盒强化学习，在时限约束+沿途可选收益类算法题中实时性极强，明确优于贪心与通用 RL 基线
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济物流场景（农村配送+农情在途感知一机两用）的调度算法技术支撑（TMC 2025，配送硬约束优先、感知软收益兜底）
    reuse_cost: 低
sources:
  - paper_title: "Delay-Sensitive Goods Delivery and in-Situ Sensing Using a Multi-Task Drone"
    doi: 10.1109/TMC.2025.3570437
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# FH-MDP：多任务无人机时敏配送与在途感知的阈值策略

## 单行摘要

面向同时执行包裹配送与在途感知的单无人机低空物流场景，把速度选择（全速/巡航）与是否悬停感知统一为有限时域 MDP：配送按时送达为强惩罚硬约束、感知为可选软收益，通过证明 Bellman 方程的单调性与次模性得到最优动作关于剩余距离和已用时间的阈值结构，无人机在线只需比较当前状态与阈值即可实时切换动作，无需逐步重解动态规划。

## 方法快照

- 问题结构：配送截止时间与沿途 POI 感知收益都受速度与悬停行为影响，单独优化任一任务都会牺牲另一方。
- 建模：FH-MDP 状态由剩余距离、当前街区、已用时间构成；动作含全速、巡航、POI 悬停感知；超时施加强惩罚使配送优先级压过感知收益。
- 求解：证明 Bellman 方程单调性+次模性 → 最优策略呈阈值结构 → 在线执行只需阈值比较，复杂度极低。
- 验证：数值仿真（合成路线与任务参数，含完整数学结构与复杂度分析）；平台与代码未披露。

## 比赛映射要点

- 数模决策题：硬约束+软收益的双层目标写法与阈值策略推导路线，可套到带截止时间的路径/调度题，比单纯最短路或启发式多一层最优性论证。
- 黑客松算法题：把离线 DP 压成在线阈值规则的技巧可直接迁移，实时决策类题目中兼得质量与速度。
- 双创申报：低空物流+在途农情感知的一机多用运营模式支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Liu2025_多任务无人机的时敏配送与在途感知`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `liu2025DelaysensitiveGoodsDelivery` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
