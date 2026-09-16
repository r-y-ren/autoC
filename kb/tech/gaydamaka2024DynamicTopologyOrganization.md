---
id: gaydamaka2024DynamicTopologyOrganization
name: 虚拟坐标驱动的自主UAV蜂群拓扑组织与维护
field: [无人机自组网, 拓扑组织, 地理路由]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 山区/林地等无 GPS 场景的智慧农业蜂群作业申报亮点：无真实坐标仍可路由的自组网机制，vault 页自评结果代码已开源、可做演示原型
    reuse_cost: 低
  - track: 黑客松-数据与算法
    edge: 无全局定位下的分布式拓扑组织+蜂群合并/解组维护，可迁移到自组网/图连通维护类算法题，与依赖坐标的常规编队方案形成差异
    reuse_cost: 中
sources:
  - paper_title: "Dynamic Topology Organization and Maintenance Algorithms for Autonomous UAV Swarms"
    doi: 10.1109/TMC.2023.3293034
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 虚拟坐标驱动的自主UAV蜂群拓扑组织与维护

## 单行摘要

针对深林、山区、室内等外部定位缺失或不可靠环境中的自主 UAV 蜂群，提出基于虚拟坐标系统的拓扑组织与维护算法：仅凭邻居广播与相对距离估计即可沿用地理路由思想组织网络，并支持蜂群合并与解组等任务级重组，对距离估计误差、移动扰动与临时链路丢失保持鲁棒。

## 方法快照

- 虚拟坐标：无需真实地理坐标，靠邻居通信与相对距离估计构建坐标系，使蜂群仍能执行地理路由。
- 拓扑维护：在移动、测距误差与链路波动下持续修正结构，维持连通与可路由性（对比只保证静态连通的方法）。
- 合并/解组：把维护机制扩展到蜂群 merge/disjoin，适配动态任务编组——核心对象是「可路由的拓扑结构」而非预定义队形。
- 验证：面向误差/扰动/丢链路的数值鲁棒性评估；vault 页自评结果生成代码已公开。

## 比赛映射要点

- 双创申报：救援、室内、复杂地形同样覆盖农业场景（山区果园/林地植保），「定位服务失效时仍保持蜂群网络」是过硬的系统级主张，且有开源实现可支撑演示。
- 黑客松：自组网/图连通维护类算法题（节点无全局坐标、链路时变、需支持节点分组合并）可直接借鉴其虚拟坐标+维护规则的设计。

## 溯源说明

- 提炼来源：my_LLM_valut wiki 页 `Gaydamaka2024_自主UAV蜂群动态拓扑组织与维护`；citekey `gaydamaka2024DynamicTopologyOrganization`。
- bib 回填：标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性 medium 承自 vault 页自评（数值仿真为主、结果代码已公开但页内无具体链接，本卡 runnable 如实标 false）；如需引用请以论文原文复核。
