---
id: chen2025EneOveCom
name: 部分参与式UAV空中计算能效优化
field: [UAV 辅助边缘计算, 空中计算, 数据聚合]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 农田/园区无线传感监测的"少上传+相关性补全"节能聚合方案——只让部分传感器参与空中计算、其余由空间相关性估计补足，为申报书中低功耗监测网络寿命与带宽论证提供方法支撑
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 传感器子集选择、UAV 悬停位置与预编码的联合 MSE 优化可抽象为带精度约束的选择与选址题，DFS/采样枚举组合 + Gurobi 求近似最优的求解流程可迁移
    reuse_cost: 中
sources:
  - paper_title: "Energy-Efficient over-the-Air Computation in UAV-assisted IIoT Networks"
    doi: 10.1109/TMC.2025.3556382
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 部分参与式UAV空中计算能效优化

## 单行摘要

面向远程工业物联网监测，把 UAV 辅助空中计算（AirComp）改造成"部分传感器参与上传"的数据聚合系统：利用相邻传感器观测的空间相关性，只选 M 个节点同频上传，其余观测由相关性估计补全，并联合优化 UAV 悬停位置与传感器预编码，在保住聚合 MSE 的前提下降低总能耗、延长网络寿命。

## 方法快照

- 场景建模：分布式电池供电传感器 + 一架悬停 UAV，AirComp 利用无线叠加在同一资源块完成函数级聚合。
- 核心机制：部分节点参与 + 空间相关性补全——"少发一些节点"靠统计相关性变为可行，节能目标优先于时延。
- 误差分析：对每种传感器组合推导 MSE 闭式表达，消去 UAV 侧归一化因子，把变量集中到 UAV 位置与预编码。
- 求解流程：小规模 DFS 穷举组合、大规模采样逼近平均 MSE，再经辅助变量转化后用 Gurobi 求近似最优部署与预编码。

## 比赛映射要点

- 双创申报：智慧农业低功耗广域监测（土壤/气象传感 + 周期性 UAV 收集）的网络寿命与带宽论证，可引用"部分参与 + 相关性补全"作为差异化技术点，区别于全员上传的经典 AirComp。
- 黑客松/算法赛：子集选择 + 站址优化 + 精度约束的组合结构可直接出题或解题，枚举/采样 + 混合整数求解器的流水线是现成解法骨架。

## 关联概念
- 空中聚合计算（AirComp）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Chen2025_无人机辅助IIoT空中聚合计算能效优化`（4 枚举字段自该页 frontmatter 迁移）。
- citekey 与 bib 回填：分片 citekey `chen2025EneOveCom` 未直接收录于 `kb/raw/vault-bib-map.yaml`；经标题/venue/年份逐项核对，与映射中 `chen2025EnergyefficientOvertheairComputation` 为同一论文（TMC 2025），DOI/venue 自该条回填（vault_bib_backfill.py，2026-09-16），未编造任何字段。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评，如需引用请以论文原文复核。
