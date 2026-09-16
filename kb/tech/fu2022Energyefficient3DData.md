---
id: fu2022Energyefficient3DData
name: 多UAV三维节能数据采集（3DM）
field: [移动群智感知, 三维轨迹优化, UAV 数据采集]
published: 2022-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Computers
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 以单位能耗数据率为目标、LoS/NLoS 概率链路建模叠加三维高度-能耗权衡的建模范式，是无人机数据采集/路径规划类数模题的目标函数与链路模型模板
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 双侧移动性下的 UAV-设备动态匹配（时变匹配矩阵 + 迭代重匹配防局部最优）与三维导航耦合求解，可迁移为多机-多目标动态指派与巡航调度题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 城市基础设施薄弱区域（农田/山区）的移动感知数据回收方案支撑，多机协同采集的能耗-时间联合论证素材
    reuse_cost: 低
sources:
  - paper_title: "Energy-Efficient 3D Data Collection for Multi-UAV Assisted Mobile Crowdsensing"
    doi: 10.1109/TC.2022.3227869
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 多UAV三维节能数据采集（3DM）

## 单行摘要

面向城市基础设施薄弱区域的移动群智感知，提出 3DM 框架：UAV 与地面移动设备都在运动，以"单位能耗数据率"为联合目标，先按三维链路质量构造时变 UAV-MD 匹配矩阵并通过迭代重匹配避免贪心局部最优，再综合 LoS/NLoS 概率、传输速率与旋翼推进能耗设计三维导航策略，以更低时间和能耗完成数据采集。

## 方法快照

- 建模要点：概率型 LoS/NLoS 链路随 UAV 三维位置（仰角、遮挡）变化；能耗同时计入旋翼推进与设备上传发射。
- 目标函数：data rate per energy unit 最大化，在总数据量、总时间、总能耗间联合权衡。
- 求解结构：匹配与导航两个强耦合子问题按时隙交替——定期更新设备状态、重算匹配、同步修正轨迹；TDMA 带宽划分 + 全量采集约束。
- 验证：MATLAB 数值仿真（合成场景），未开源。

## 比赛映射要点

- 数模：目标函数（单位能耗效用）+ 概率链路模型 + 时变指派的结构可直接套用到无人机巡检/采集类赛题的建模层，比单纯最小化时间或能耗的目标更易出彩。
- 黑客松/算法赛：动态匹配 + 轨迹修正的迭代框架可拆成指派问题与局部搜索两个可实现的模块。
- 双创申报：偏远农田、山区等弱基础设施场景的感知数据回收方案论证素材。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Fu2022_面向移动群智感知的多UAV三维节能数据采集`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `fu2022Energyefficient3DData` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2022），按 2022-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
