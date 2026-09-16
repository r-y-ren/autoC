---
id: zhang2023JointTaskScheduling
name: 应急通信空中计算的任务调度与多UAV部署联合优化
field: [空中计算, 任务调度, UAV 部署优化]
published: 2023-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: low
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: "任务-UAV 匹配（swap matching）与连续部署（SCA 凸化）交替迭代的联合优化骨架，可直接套用到应急响应/资源调度类赛题中'任务派给谁 + 资源放在哪'的双决策耦合问题"
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: "地面基础设施损毁后以 UAV 自组网虚拟边缘云替代地面算力的应急通信方案叙事，可支撑应急救援/偏远地区通信类申报的技术路线章节，剩余能量权重入目标函数的'生存时间+服务质量'折中是差异化论证点"
    reuse_cost: 低
sources:
  - paper_title: "Joint Task Scheduling and Multi-UAV Deployment for Aerial Computing in Emergency Communication Networks"
    doi: 10.1007/s11432-022-3667-3
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 应急通信空中计算的任务调度与多UAV部署联合优化

## 单行摘要

面向地面通信基础设施受损的应急场景，提出基于空地自组织网络的空中计算架构：地面终端任务可本地执行或卸载到多架 UAV 组成的虚拟边缘云，通过任务调度（swap matching）与多 UAV 三维部署（SCA 近似）的交替联合优化，在时延、能耗与 UAV 剩余能量权重构成的系统成本上取得可调折中，延长网络可持续服务时间。

## 方法快照

- 架构创新：以 ad-hoc 自组网把多架 UAV 组织成空中边缘云，回避对完好地面边缘站点的依赖——部署位置不只是几何变量，而是系统成本的一部分（显式建模悬停/飞行能耗）。
- 目标设计：不是单一时延最小化，而是时延 + 能耗 + 剩余能量权重共同构成的系统成本，天然服务"生存时间 + 服务质量"的折中。
- 求解结构：任务调度子问题用 swap matching 处理离散匹配；部署子问题用 SCA 处理连续位置/速度；两阶段交替迭代成联合算法，经核心节点广播机制落到分布式协同环境。
- 方法论定位：经典"离散匹配 + 连续凸化 + 交替优化"路线（非学习型在线决策）。
- 验证：数值仿真（合成场景，实验资产链条说明有限，未开源）。

## 比赛映射要点

- 黑客松/算法赛：任何"任务分配 + 设施选址"双耦合决策（应急物资、充电车调度、边缘节点布设）都可套用"离散匹配 + SCA 凸化 + 交替迭代"骨架；把平台续航/剩余资源显式写进目标函数是容易被忽视的加分设计。
- 双创申报：应急救援、偏远农村通信保障等场景中"无人机自组网虚拟边缘云"的技术方案支撑点，范式差异（替代地面边缘而非辅助）适合写技术路线开篇。

## 关联概念
- 区域覆盖与部署模型
- 覆盖与部署优化主线
- 信道与通信速率模型
- 计算卸载模型
- 轨迹优化与协同控制
- 空中计算与UAV辅助MEC的关系
- 无人机部署优化
- 无人机能耗模型
- 多无人机协同

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhang2023_应急通信空中计算联合调度与多UAV部署`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=low）。
- bib 回填：citekey `zhang2023JointTaskScheduling` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2023），按 2023-01-01 填写。
- 复现性承自 vault 页自评（low，数值仿真、平台与代码均未披露）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
