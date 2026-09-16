---
id: chang2024NearoptimalUAVDeployment
name: 时延约束IoT采集的最少UAV部署（GPUDA）
field: [无人机部署, 组合优化, 物联网数据采集]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: IEEE INFOCOM 2024 - IEEE Conference on Computer Communications
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 把"到底需要多少架无人机"本身作为优化目标的覆盖-路径耦合建模（几何分区 + 数据舍入 + 动态规划，3-approx 保证），直接适配数模中无人机部署/采集调度类赛题，近似比可写进模型评价
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 带时延预算的最小覆盖采集问题抽象与近似算法设计框架（分区缩空间 + DP），可迁移到设施选址/车辆回路类算法题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农田物联网巡检方案中无人机数量-成本论证的理论依据（部署规模作为一等成本变量）
    reuse_cost: 低
sources:
  - paper_title: "Near-Optimal UAV Deployment for Delay-Bounded Data Collection in IoT Networks"
    doi: 10.1109/INFOCOM52122.2024.10621135
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 时延约束IoT采集的最少UAV部署（GPUDA）

## 单行摘要

在缺乏固定基础设施的物联网采集场景中，把能量限制与数据新鲜度合并为每架 UAV 的采集回路时延预算，并直接以"完成全覆盖采集所需的最少 UAV 数量"为目标，提出几何分区与动态规划结合的 GPUDA 近似算法，通过数据舍入与分区构造获得 3-approx 性能保证（优于先前 4-approx），并讨论存在空洞/障碍区域时的部署情形。

## 方法快照

- 问题抽象：所有 IoT 设备必须被某条 UAV 闭环回路覆盖，每条回路受时延预算约束——不是单条路径最短，而是把设备划分到若干条可行回路。
- 目标函数：最小化所需 UAV 数量，把部署规模与路径规划统一进同一组合优化模型。
- 算法：几何分区缩小组合空间 → 数据舍入离散化 → 分区上动态规划；证明 3-approx。
- 扩展：空洞/障碍区域下的回路构造与连通划分讨论。
- 验证：合成场景数值仿真，未开源。

## 比赛映射要点

- 数模赛：无人机巡检/采集调度类赛题常默认无人机数已知，本篇"部署规模是一等优化目标 + 回路时延预算写进可行性条件"的建模角度可直接借用，近似保证可支撑模型合理性论证。
- 黑客松/算法赛：最小覆盖 + 回路约束的组合结构与"分区 + DP + 舍入"近似套路可迁移到选址、VRP 变体题。
- 双创申报：植保/巡检无人机的机队规模测算依据。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Chang2024_时延约束物联网数据采集的近最优UAV部署`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `chang2024NearoptimalUAVDeployment` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（low，纯数值仿真、未开源，当前定位为覆盖与部署建模的理论锚点）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
