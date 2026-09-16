---
id: zhou2024JointOptimizationMobility
name: 可靠性保障空地通信的UAV移动性联合优化
field: [空地通信, 双层优化, 能耗优化]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: 把通信可靠性下界显式化为一等约束（而非平均吞吐目标），用 epsilon-constraint 生成能耗-可靠性 Pareto 前沿——直接对应评估类赛题的多目标折中分析；Lagrangian + 顺序二次规划迭代并证明收敛到 KKT 点的求解论证可支撑模型求解章节
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农田巡检/植保场景的无人机链路可靠性论证依据——以"能否稳定完成任务"而非平均速率倒推轨迹与功率设计，可转写为作业链路保障章节
    reuse_cost: 低
sources:
  - paper_title: "Joint Optimization of Mobility and Reliability-Guaranteed Air-to-Ground Communication for UAVs"
    doi: 10.1109/TMC.2022.3228870
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 可靠性保障空地通信的UAV移动性联合优化

## 单行摘要

研究单 UAV 空地数据卸载中的移动性-可靠性耦合问题：可靠性由发射功率、链路距离、数据调度与路径损耗共同决定并被设为显式约束，而严格可靠性会改写最优轨迹——通过双层优化联合控制加速度、发射功率与数据调度，在可靠性下界约束下最小化飞行与通信总能耗。

## 方法快照

- 问题结构：UAV 高度固定、二维平面机动，在给定起终状态与时间窗内向多个地面基站执行数据传输；总能耗 = 飞行能耗 + 通信能耗，轨迹与通信策略天然耦合。
- 建模关键：可靠性作为显式下界约束进入问题，而非事后指标；只用最短飞行或最低功率无法保证可靠传输。
- 求解管线：epsilon-constraint 把可靠性要求转为可控阈值并生成不同可靠性等级下的 Pareto 前沿 → Lagrangian + SQP 迭代求解加速度/功率/调度 → 收敛到 KKT 点有证明。
- 敏感性：系统分析飞行高度、任务时长、数据负载与路径损耗指数对能耗-可靠性折中的影响。
- 验证：合成道路基站布局与 A2G 参数仿真，含收敛、性能比较与 Pareto 折中分析（页内自评复现 medium）；平台、代码与真实飞行验证均未披露。

## 比赛映射要点

- 数模赛：可靠性显式化 + epsilon-constraint 生成 Pareto 前沿是评估/折中类赛题的标准工具组合；KKT 收敛论证写法可参照。
- 双创申报：作业链路"稳定性优先于速率"的设计论证素材。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2024_UAV移动性与可靠性保障空地通信联合优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `zhou2024JointOptimizationMobility` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，纯数值仿真、无公开代码与真实飞行支撑）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
