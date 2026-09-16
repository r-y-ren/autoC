---
id: han2024JointAssociationDeployment
name: 多UAV大规模MEC关联-部署-轨迹联合优化
field: [UAV 辅助移动边缘计算, 部署与轨迹优化]
published: 2024-01-01
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
    edge: 聚类关联（k-means）+ 落脚点选址（烟花算法）+ 贪心路径串接的三级分解，本质是选址-路径（location-routing）问题的可复用解法骨架，适配大规模服务点划分与设施选址类决策题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: "大规模场景下'聚类划分-部署优化-轨迹串联'的结构化分解套路可直接迁移到覆盖/调度类算法题，对比单点贪心或纯聚类基线有明确差异化"
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业无人机集群面向百级以上田间 IoT 节点采集数据的系统组织方案技术支撑（TMC 2024，关联/部署/轨迹一体化设计）
    reuse_cost: 低
sources:
  - paper_title: "Joint Association, Deployment and Flight Trajectory Optimization for Multi-UAV-enabled Large-Scale Mobile Edge Computing"
    doi: 10.1109/TMC.2024.3426945
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 多UAV大规模MEC关联-部署-轨迹联合优化

## 单行摘要

面向百级以上 IoT 设备的大规模 UAV 辅助 MEC 场景，将设备关联、UAV 落脚点部署与飞行轨迹拆成三个协同子问题联合求解：改进 k-means 完成设备到 UAV 的服务簇划分，带可变长度编码的改进烟花算法（IFWA）动态决定每架 UAV 的落脚点数量与位置，再在既定落脚点上用预计算贪心生成短飞行距离轨迹，以最小化系统总能耗。

## 方法快照

- 问题结构：设备归属、落脚点（foothold）数量/位置、访问轨迹三者强耦合，直接联合求解不可行，核心思想是结构化分解为可迭代协同的组合优化流程。
- 关联层：改进 k-means 把大规模设备集划分为多个服务簇，归属关系直接影响飞行与计算能耗。
- 部署层：IFWA（可变长度编码）优化每架 UAV 的落脚点个数与位置，使部署成为轨迹的中介变量。
- 轨迹层：给定落脚点后用预计算贪心缩短飞行距离。
- 验证：MATLAB 数值仿真，合成场景，含大规模实例与 Friedman 排名、Wilcoxon 显著性检验；未说明开源。

## 比赛映射要点

- 数模决策题：落脚点选址+簇划分+路径串接的分解骨架，可直接套用到"服务点分配-设施选址-访问路线"类题目（如配送站选址、巡检路线设计），比单一聚类或单一贪心基线更完整。
- 黑客松算法题：三级流水线（聚类关联→部署→轨迹）可作为覆盖/调度类赛题的主方案结构。
- 双创申报：作为"多机+大规模传感节点"农业采集系统的系统组织与能耗优化设计依据。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Han2024_大规模MEC的多UAV联合关联部署与轨迹优化`（venue_tier/evidence_tier/paper_role/reproducibility_level 承自该页 frontmatter）。
- bib 回填：citekey `han2024JointAssociationDeployment` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
