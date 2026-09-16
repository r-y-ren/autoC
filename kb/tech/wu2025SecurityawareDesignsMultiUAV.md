---
id: wu2025SecurityawareDesignsMultiUAV
name: 安全感知多UAV部署卸载与服务放置（OE-MATD3）
field: [UAV 辅助边缘计算, 物理层安全, 多智能体强化学习]
published: 2025-01-01
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
  - track: 黑客松-数据与算法
    edge: 优化嵌入式 MARL——先推导设备发射功率闭式解再嵌入 MATD3 学习环，处理离散（关联/服务放置）与连续（位置/功率）耦合决策，可作多机协同调度赛题区别于纯端到端 DRL 的差异化求解组件
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: MINLP 分层建模范式——服务缓存合法性、最坏情况安全卸载速率、能量与安全间距约束统一进总时延最小化，可直接迁移到含安全与资源约束的多目标决策题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济/农业植保无人机边缘计算方案的安全通信支撑点——UAV jammer 协同干扰抑制窃听，把物理层安全写成系统主变量而非附加条件
    reuse_cost: 低
sources:
  - paper_title: "Security-Aware Designs of Multi-UAV Deployment, Task Offloading and Service Placement in Edge Computing Networks"
    doi: 10.1109/TMC.2025.3574061
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 安全感知多UAV部署卸载与服务放置（OE-MATD3）

## 单行摘要

面向无地面基础设施或覆盖不足场景的多 UAV 辅助 MEC 网络，把 UAV 部署、任务卸载、服务放置与防窃听统一建模为时延最小化问题：用 UAV jammer 协同干扰提升安全卸载速率，用 OE-MATD3（优化嵌入 MATD3）联合决策 UAV 侧离散-连续变量，设备发射功率取闭式解嵌入学习过程。

## 方法快照

- 系统实体：多 UAV 服务器、一个 UAV jammer、多个无线设备、窃听者、异构服务程序集合；任务能否卸载首先取决于目标 UAV 是否预缓存了对应服务程序。
- 问题形态：典型 MINLP——离散变量（设备-服务器关联、服务放置）+ 连续变量（UAV 与 jammer 位置、干扰功率、设备发射功率）。
- 求解链：问题分解 → 设备发射功率闭式解推导（结构化部分不交给 RL 盲搜）→ OE-MATD3 联合学习 UAV 相关变量 → 安全协同把窃听约束写进可行域。
- 约束集：缓存空间、最坏情况安全卸载速率、时延容忍、设备与 UAV 能量、UAV 最小安全间距。
- 验证：数值仿真（合成场景），Python 3.8 + TensorFlow 2.6.0；开源情况未说明。

## 比赛映射要点

- 黑客松/算法赛：「闭式解嵌入 DRL」的混合求解是可复用范式——凡遇到离散选址/分配 + 连续功率/轨迹耦合的赛题，先解析掉有结构的变量再学习剩余部分，对比纯端到端 DRL 基线有讲得清的差异化。
- 数模决策题：缓存约束决定合法卸载集合、安全速率约束塑造可行域的建模方式，适合多约束多目标决策题引用。
- 双创申报：农业植保/低空巡检无人机集群的「安全边缘计算」技术卖点（协同干扰 + 服务预缓存），有 CCF-A 论文背书。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wu2025_安全感知的多UAV部署卸载与服务放置`（vault 页 4 枚举字段 venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium 已迁移至本卡）。
- bib 回填：citekey `wu2025SecurityawareDesignsMultiUAV` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按年-01-01 填写；验证类信息（simulation/synthetic/复现性 medium、开源未说明故 runnable=false）承自 vault 页自评，如需引用请以论文原文复核。
