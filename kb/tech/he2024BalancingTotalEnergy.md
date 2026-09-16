---
id: he2024BalancingTotalEnergy
name: SAGIN数据卸载的总能耗与平均工期权衡
field: [空天地一体网络, 多目标优化, 任务调度]
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
  - track: 数模-数据分析与决策
    edge: 能耗-工期双目标的归一化加权建模 + 低 SNR 场景闭式功率分配 + 常数因子近似保证的调度算法 + 混合遗传扩展，为多目标权衡类数模赛题提供"解析解与启发式分层求解"的完整方法论模板
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 大区域农业遥感/物联网数据经星间与星地链路回传的能量-时效协同方案支撑（MATLAB/YALMIP 工具链可复刻），适配智慧农业星地一体化数传叙事
    reuse_cost: 低
sources:
  - paper_title: Balancing Total Energy Consumption and Mean Makespan in Data Offloading for Space-Air-Ground Integrated Networks
    doi: 10.1109/TMC.2022.3222848
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# SAGIN 数据卸载的总能耗与平均工期权衡

## 单行摘要

在卫星、空中与地面链路共存的空天地一体网络（SAGIN）中，把数据卸载建模为总能耗与平均工期（mean makespan）归一化加权和的混合整数非线性规划；给定功率下设计具有常数因子保证的近似调度算法，低 SNR 场景导出最优功率分配闭式解，一般场景用基于遗传框架的混合算法求解，实现能耗与完工时间的显式折中。

## 方法快照

- 双目标构造：总能耗与平均工期归一化加权，显式建模两者的冲突关系，而非只优化其一。
- 分层求解一：给定功率分配下设计近似调度算法并分析近似质量（常数因子保证）。
- 分层求解二：低 SNR 场景利用更强的解析结构导出闭式最优功率分配；一般场景切换到混合遗传算法。
- 耦合关系：功率配置改变完成时延与总能耗，调度与功率控制相互影响，必须交替/联合处理。
- 链路建模：任务沿星间链路（ISL）或星地链路（SGL）传输，多域链路的容量与能耗差异直接进入调度目标。

## 比赛映射要点

- 数模：任何"时间-能耗/成本双目标"调度赛题（生产排程、车辆充放电调度、数据回传计划）都可套用其"归一化加权目标 + 分场景分层求解（闭式解兜底解析、启发式兜一般）+ 近似比背书"的论证结构，比纯启发式答卷多一层理论保障。
- 双创：智慧农业中大范围农情数据回传（卫星 + 空中平台）的能量与时效权衡方案，其 MATLAB + YALMIP 验证链路在申报书技术路线图中容易复刻描述（实测数字需自建）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `He2024_空天地一体网络数据卸载中的总能耗与平均工期权衡`（frontmatter 4 枚举字段已迁移到本卡：venue_tier/evidence_tier/paper_role/reproducibility_level）。
- bib 回填：citekey `he2024BalancingTotalEnergy` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；验证类信息（theory+simulation/MATLAB/YALMIP/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
