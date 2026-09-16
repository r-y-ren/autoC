---
id: zhou2025HaDTHardeningDigital
name: HaDT：UAV 工业物流分发的加固双数字孪生框架
field: [数字孪生, UAV 物流, 边缘智能]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE INFOCOM 2025 - IEEE Conference on Computer Communications
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 无人机低空物流配送申报项目的技术底座——边缘侧资源调度孪生与路径规划孪生协同的系统架构（INFOCOM 2025 背书），可直接作智慧农业/乡村物流场景的系统方案图与可行性论据
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: Gazebo + ROS 仿真底座加上调度/规划解耦的双模块骨架，可迁移为无人机物流类黑客松的仿真-决策原型，比单体端到端策略更易分工实现
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 资源调度与路径规划分解建模 + Lyapunov 长期约束 + MADDPG 多智能体决策，可作数模赛中无人机配送调度/资源分配类赛题的方法组件，区别于单时隙启发式
    reuse_cost: 中
sources:
  - paper_title: HaDT：Hardening Digital Twins for UAVs-based Industrial Logistics Distribution Systems
    doi: 10.1109/INFOCOM55648.2025.11044738
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# HaDT：UAV 工业物流分发的加固双数字孪生框架

## 单行摘要

面向 UAV 工业物流分发场景提出 HaDT 加固数字孪生框架：在边缘侧以资源调度孪生（DT_RS）与路径规划孪生（DT_PP）双孪生协同，把计算/通信资源组织与位置-速度轨迹生成解耦优化，降低分发时延、提高成功分发率并兼顾能耗。

## 方法快照

- 场景建模：多架物流 UAV 部署于含仓库与城市障碍的环境，多个分发任务需及时送达目标区域；核心问题是复杂环境下 UAV 控制与决策难以实时准确执行。
- 双孪生结构：DT_RS 联合 UAV 计算与通信资源生成协同分发决策（ICC 机制组织协同资源分配）；DT_PP 依据调度结果导出可执行的位置与速度轨迹（PSO-PP，在干扰与复杂障碍下保持可执行性）。
- 优化目标与工具：降低分发时延、提高成功分发比例、兼顾能量消耗与协同效率；方法组件含 Lyapunov optimization（长期约束）与 MADDPG（多智能体决策）。
- 验证：Gazebo + ROS 仿真，UAV logistics distribution dataset；指标为分发时延、成功分发率、能耗，对比现有物流分发与路径规划方案；未说明开源，复现性 medium。
- 「加固」含义：在数字孪生外再叠加一层对复杂环境与实时约束的韧性设计，使 twin 从「建模镜像」升级为边缘侧实时控制代理。

## 比赛映射要点

- 双创申报：低空物流/乡村无人机配送项目的技术方案支撑，双孪生边缘决策架构直接作系统架构图底座。
- 黑客松/算法赛：调度与规划拆成两个模块（一个管资源分配、一个管轨迹），团队可分工并行实现，仿真环境有成熟开源栈（Gazebo/ROS）。
- 数模决策题：长期队列约束（Lyapunov）+ 多智能体强化决策（MADDPG）适合「任务持续到达、要求长期稳定服务」的调度类赛题，与单目标贪心形成差异化。

## 关联概念（vault 概念页折叠于此，不独立成卡）

- **加固数字孪生**：在传统数字孪生的状态映射基础上增强实时决策、韧性与复杂环境适应能力，使其能在边缘侧稳定支撑物理系统执行——twin 更像物理系统的在线代理而非可视化镜像；语料中代表论文即本卡 HaDT 与姊妹篇 VerDT（后者把双 twin 组织成更完整的工业物流执行架构）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhou2025_HaDT加固数字孪生物流分发`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段）；枢纽概念页 `加固数字孪生.md` 已折叠进「关联概念」节。
- bib 回填：citekey `zhou2025HaDTHardeningDigital` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）；bib 标题原文含 ASCII 冒号（HaDT 后接冒号空格），按 YAML 纪律改全角冒号写入 sources.paper_title。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation、Gazebo/ROS、复现性 medium、artifact 未知）承自 vault 页自评，如需引用请以论文原文复核。
