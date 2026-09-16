---
id: yang2024EnergyEfficientTransmission
name: 蜂窝连接UAV巡检能效传输（加权图定序+SCA/BCD）
field: [蜂窝连接无人机, 巡检系统, 能效优化]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 电力/管线/农田巡检的空地一体方案支撑——巡检点数据采集 + 蜂窝链路卸载 + 地面站 MEC 处理的系统架构叙事（巡检是智慧农业与基础设施运维的刚需场景），CCF-A 论文背书
    reuse_cost: 低
  - track: 数模-数据分析与决策
    edge: 离散访问顺序（按通信速率与巡检点-基站拓扑构造加权图定序）与连续轨迹/通信调度/算力分配（SCA + BCD）拆解协同的建模范式，可直接迁移到「先排序后调参」的两段式决策题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: SCA/BCD 迭代联合优化组件与加权图排序策略可复用于能耗-时延联合优化类赛题，与 round tour、穷举等基线的对比设计可照搬
    reuse_cost: 中
sources:
  - paper_title: "Energy Efficient Transmission Strategy for Mobile Edge Computing Network in UAV-Based Patrol Inspection System"
    doi: 10.1109/TMC.2023.3315477
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 蜂窝连接UAV巡检能效传输（加权图定序+SCA/BCD）

## 单行摘要

面向蜂窝连接 UAV 巡检系统，UAV 沿多个预设巡检点采集数据并向邻近地面基站（GBS）的 MEC 资源卸载计算任务：先按巡检点与基站的通信拓扑构造加权边决定访问顺序（兼容轻/重任务卸载场景），再在相邻巡检点之间用 SCA 与 BCD 联合优化 UAV 轨迹、通信调度与计算资源分配，最小化飞行、通信与计算的总能耗并满足任务完成时间约束。

## 方法快照

- 双子问题结构：子问题一为巡检点遍历顺序设计（结合通信速率表现构造加权边，让顺序本身服务于后续卸载效率）；子问题二为相邻巡检点间的通信传输与轨迹联合设计。
- 联合优化变量：UAV 轨迹、通信调度时机、计算资源分配；约束含任务完成时间与持续蜂窝连接。
- 关键洞察：巡检 UAV 的瓶颈不只飞行距离，还在沿途持续数据上传与 MEC 卸载——离散调度与连续控制必须共同设计。
- 验证：数值仿真（合成巡检点与 GBS 部署场景），对比 round tour、穷举最优与传统巡检传输方案；未披露代码、求解器与统一仿真平台。

## 比赛映射要点

- 数模：巡检类/覆盖类赛题（电网、农田、河道）可整体借用「访问顺序定生死、段内传输再精调」的两段建模，加权图构图规则（边权含信道质量）是可迁移的建模细节。
- 黑客松：SCA + BCD 是处理非凸连续优化组件的标准组合，配合离散定序形成完整 pipeline，基线对比设计现成。
- 双创申报：智慧农业/基础设施巡检方案中的「采集-卸载-边缘处理」能耗优化模块，直接支撑续航与时效性论证。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Yang2024_巡检系统中蜂窝连接UAV-MEC的能效传输策略`（vault 页 4 枚举字段 venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium 已迁移至本卡）。
- bib 回填：citekey `yang2024EnergyEfficientTransmission` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium、开源未说明故 runnable=false）承自 vault 页自评，如需引用请以论文原文复核。
