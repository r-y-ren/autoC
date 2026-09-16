---
id: wang2024WirelessPoweredMetaverse
name: 无线供能多设备多UAV联合调度（MURAL）
field: [无线供能, 移动边缘计算, 多任务强化学习]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Journal on Selected Areas in Communications
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 「启发式搞定设备侧充电时间分配 + 多任务 DRL（共享策略网络 + UAV 专属策略网络）学调度与轨迹」的分层耦合范式，为高维联合调度赛题提供纯启发式与纯 DRL 之外的第三条可行路线
    reuse_cost: 高
  - track: 数模-数据分析与决策
    edge: 供能与计算双网络耦合建模（能量补给流与任务流共同决定轨迹），目标为系统计算效率而非单一时延或能耗——能量采集 / 充电调度类数模题的完整决策链参考
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 能量受限的农业物联网 / 传感网「UAV 无线补能 + 边缘计算服务」一体化方案技术支撑（JSAC 2024，多设备多 UAV 双侧联合调度）
    reuse_cost: 低
sources:
  - paper_title: "Wireless Powered Metaverse：Joint Task Scheduling and Trajectory Design for Multi-Devices and Multi-UAVs"
    doi: 10.1109/JSAC.2023.3345433
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 无线供能多设备多UAV联合调度（MURAL）

## 单行摘要

面向人中心元宇宙应用的无线供能 MEC 场景：移动设备算力与电量双不足，多 UAV 经 AP 与激光发射器补能后为设备提供计算卸载服务。论文联合优化设备充电时间、任务调度与多 UAV / 设备双侧轨迹，提出 MURAL 多任务深度强化学习算法——先用启发式完成设备侧充电分配与调度，再用含共享策略网络与 UAV 专属策略网络的多任务 DRL 学习 UAV 充电调度与轨迹，交替迭代获得联合解，提升系统单位时间计算效率。

## 方法快照

- 系统实体：AP、激光发射器、多架 UAV、多台移动设备；能量流与任务流双网络耦合。
- 决策变量：充电时间、设备调度、UAV 调度、UAV 轨迹、设备轨迹；约束含设备 / UAV 剩余能量、飞行高度、最大速度、计算频率与带宽。
- 求解结构：启发式（设备侧）与多任务 DRL（UAV 侧）交替迭代，部分卸载允许。
- 场景构建：基于 Manhattan 城市地图与移动模型的合成场景；实现栈为 Python 3.9 + PyTorch 1.8.1，无开源。

## 比赛映射要点

- 黑客松算法类：调度维度跨设备与 UAV 两侧时，「启发式保底 + DRL 学高维策略」的分层方案可直接复用，训练可行性显著好于端到端黑盒。
- 数模决策类：能量补给链路与任务完成率耦合的建模方式适合「无线充电 / 能量收集 + 计算卸载」组合题型。
- 双创申报：农田传感网补能与数据回传一体化巡检服务的方案背书。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2024_无线供能元宇宙中的多设备多UAV联合调度`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2024WirelessPoweredMetaverse` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）；标题中「: 」按本跑批 YAML 约定改写为全角冒号。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
