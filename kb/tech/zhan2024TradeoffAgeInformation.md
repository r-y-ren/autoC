---
id: zhan2024TradeoffAgeInformation
name: AoI与运行时间双目标的多小区蜂窝UAV感知调度
field: [AoI, 蜂窝连接无人机, 深度强化学习]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: AoI 为「数据新鲜度」提供严格可计算的量化定义，配合其与运行时间的双目标权衡结构，可直接用于评估类赛题中数据时效性与采集成本的同时建模
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 统计信道下离线结构分析（DGA）+ 环境感知 DDQN 在线策略（DLA）的两条求解链路，可迁移到带遮挡/干扰的路径调度赛题，学会避开服务空洞的在线策略是差异点
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农田传感数据按新鲜度调度采集的论证框架（低 AoI 不等于低成本），支撑智慧农业数据采集方案的经济性设计
    reuse_cost: 低
sources:
  - paper_title: Tradeoff Between Age of Information and Operation Time for UAV Sensing Over Multi-Cell Cellular Networks
    doi: 10.1109/TMC.2023.3267656
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# AoI与运行时间双目标的多小区蜂窝UAV感知调度

## 单行摘要

面向多小区蜂窝网络中的 UAV 感知与上传任务，联合优化传输调度、基站关联与 UAV 轨迹，以平衡信息新鲜度（AoI）与任务总运行时间；先在统计信道下推导最优结构并用 DGA 近似求解，再针对城市建筑遮挡与基站下倾天线效应提出基于 DDQN 的环境感知在线策略 DLA，后者在具体环境中优于离线平均模型。

## 方法快照

- 问题本质：UAV 为降低 AoI 会绕向更好的上传位置，但拉长总运行时间——时效与新鲜度的双目标权衡是主问题。
- 双求解链路：统计信道模型下用搜索算法 + DGA 得到可解释的最优结构；site-specific 环境（building blockage、下倾天线）下用 DDQN 训练 DLA 在线决策。
- 环境感知：DLA 学会避开「服务空洞」并动态选择上传基站，把几何最短路改写为通信感知联合规划。
- 决策耦合：感知、上传、移动三种行为与调度/关联/轨迹三类变量联合设计。
- 验证为城市布局驱动仿真（双核 3.4 GHz CPU），复现性 medium。

## 比赛映射要点

- 数模评估题：AoI 定义可直接搬用为数据新鲜度度量（如疫情/环境监测数据时效评估），与成本/时间目标组成天然双目标结构。
- 黑客松/算法赛：带禁区/遮挡的采集路径题可复用「离线结构解作 benchmark + DDQN 在线策略作落地」的双链路写法与基线设计。
- 双创申报：农业物联网数据按新鲜度分级采集的论证可引用其 AoI-成本权衡结论。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhan2024_多小区蜂窝网络UAV感知的AoI与运行时间权衡`（4 枚举字段承自页 frontmatter）。
- bib 回填：citekey `zhan2024TradeoffAgeInformation` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 承自 vault 页自评：论文未明确披露仿真平台与代码开源情况，如需引用请以原文复核。
