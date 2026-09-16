---
id: zhao2025MobileCollusiveEavesdroppers
name: 移动合谋窃听下UAV-MEC安全传输与计算协同优化（CSTC）
field: [无人机通信, 物理层安全, 移动边缘计算]
published: 2025-01-01
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
  - track: 数模-数据分析与决策
    edge: 轨迹/干扰波束/功率/卸载决策的多变量联合优化范式（BCD 分块迭代 + SDR 秩松弛 + 随机化恢复解）可整体迁移到无人机资源分配类赛题；UDoU（剩余计算负载 + 剩余可用时间）实时调度度量可直接复用到带任务时限的调度建模，论文 UO/RO/UJ/RJ/WBF 消融变体是对比基线设计模板
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业数据链路安全叙事的技术支撑点——采集数据回传面临窃听威胁时，UAV 与中继设备兼任干扰节点、传输与计算协同设计的方案（TMC 2025）可作为数据安全章节背书
    reuse_cost: 低
sources:
  - paper_title: "Against Mobile Collusive Eavesdroppers：Cooperative Secure Transmission and Computation in UAV-assisted MEC Networks"
    doi: 10.1109/TMC.2025.3529929
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 移动合谋窃听下UAV-MEC安全传输与计算协同优化（CSTC）

## 单行摘要

面向移动合谋窃听者威胁下的 UAV 辅助 MEC 网络，提出 CSTC 策略：联合优化 UAV 轨迹、干扰波束、发射功率、卸载决策与基于 UDoU 的实时计算调度，让 UAV 与中继设备（RDs）同时扮演中继和干扰器，在任务时延约束下最大化 sum secrecy transmission rate——把通常分开处理的安全传输与计算调度捆成同一系统问题。

## 方法快照

- 威胁建模：多个窃听者可在时隙间协同机动、共享截获收益，两跳卸载链路保密性因此急剧下降，比静态窃听者模型更贴近高威胁环境。
- 传输侧：联合优化 UAV 轨迹、干扰波束、发射功率与卸载量，BCD 分解为多个子问题；含秩约束子问题用 SDR + 随机化恢复，凸子问题用 CVX 求解。
- 计算侧：UDoU 指标（剩余计算负载与剩余可用时间）驱动 BS 侧任务抢占与优先计算，保证时限任务与保密链路真正联通。
- 验证：合成时隙化 MEC 与窃听场景仿真，指标为 sum STR、时延满足与运行时间；补充材料有提供但代码未明确公开（页内自评复现 medium）。

## 比赛映射要点

- 数模赛：多变量联合优化 + 分块迭代求解是无人机轨迹/资源类赛题的主力套路，本篇提供"安全约束 + 时延约束"双约束建模与消融基线设计的完整参照。
- 双创申报：农业无人机数据采集/回传的数据安全论证素材（合谋窃听威胁模型 + 干扰协同方案）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhao2025_移动合谋窃听下的UAV辅助MEC安全传输与计算`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `zhao2025MobileCollusiveEavesdroppers` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）；bib 标题含 ASCII 冒号，已改全角写入 paper_title 并在此留痕。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真验证、补充材料有提供但代码未明确公开）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
