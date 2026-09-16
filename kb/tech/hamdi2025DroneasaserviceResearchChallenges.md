---
id: hamdi2025DroneasaserviceResearchChallenges
name: DaaS：无人机即服务研究挑战与方向综述
field: [无人机服务计算, 服务编排, 综述方法学]
published: 2025-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测]
venue_tier: Survey
evidence_tier: supporting
paper_role: survey
reproducibility_level: medium
signal:
  venue: Proceedings of the IEEE
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: DaaS 三维 taxonomy 与三层系统架构（用户层/计算层/无人机层）可作为智慧农业无人机服务平台申报书与商业计划书的总体框架和背景总纲，"从设备视角转向服务视角"的问题提出可直接引用
    reuse_cost: 低
  - track: 数模-数据分析与决策
    edge: 综述的不确定性感知交付 QoS 模型与挑战地图（天气、载重、续航、时延联合建模）可作数模论文问题重述与方法论定位的权威综述支撑（覆盖 2010-2025 年 214 篇文献）
    reuse_cost: 低
sources:
  - paper_title: Drone-as-a-Service：Research Challenges and Directions
    doi: 10.1109/JPROC.2025.3599126
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# DaaS：无人机即服务研究挑战与方向综述

## 单行摘要

把 Drone-as-a-Service（DaaS）正式定义为服务计算范式下的无人机系统：提出功能-研究任务-应用域三维 taxonomy、三层系统架构（用户层请求交互 / 计算层边缘云协同 / 无人机层感知执行通信）和不确定性感知的交付 QoS 模型，并系统梳理通信数据管理、不确定性、成本、服务选择与组合、能耗、网络安全等开放挑战。

## 方法快照

- 综述方法学：围绕研究问题、检索关键词、数据库来源、纳入排除标准与定量统计建立可复核的系统性文献检索流程，覆盖 2010-2025 年 214 篇研究。
- 知识组织：功能维度（sensing / inspection / delivery / entertainment / videography / communication）× 研究任务维度（communication & data management、uncertainty、cost、user control、scheduling、energy、selection & composition、cybersecurity、swarm、HDI）× 应用域维度（commercial / noncommercial）。
- 系统建模：继承 SOA 思路的松耦合服务组织（提供者-消费者-注册表），群体场景区分 orchestration 与 choreography；delivery DaaS 模型把服务表示为服务标识、功能集、QoS（飞行时长/载重/速度/环境条件）与取送货时间位置的组合。
- 定位：非求解型算法论文，而是"研究框架设计"型综述，输出一张 challenge map 而非最优算法。

## 比赛映射要点

- 双创申报：智慧农业无人机服务平台类项目的叙事总纲——把"卖无人机/卖作业"升级为"能力服务化、可发现可组合可计价"，三层架构可直接画进申报书系统方案图。
- 数模方法论背景：其不确定性感知 QoS 建模（飞行时长、载重、速度、环境条件进入 QoS）为数模赛题中"无人机配送/巡检+天气扰动"类问题的假设论证与指标设计提供综述级支撑。
- 选型参考：作为总入口文献挂具体方法论文（如 Serv-HU 服务接力、缓存 UBS 内容交付），构建"总纲+方法"的引用结构。

## 关联概念
- DaaS研究挑战与应用版图
- 服务化无人机三层架构模型
- 无人机即服务（DaaS）与空中计算的关系
- 无人机即服务（DaaS）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Hamdi2025_Drone-as-a-Service研究挑战与方向综述`（frontmatter 带 venue_tier/evidence_tier/paper_role/reproducibility_level，已映射到本卡 4 枚举字段；venue_tier=Survey、paper_role=survey）。
- bib 回填：citekey `hamdi2025DroneasaserviceResearchChallenges` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- 留痕：bib 标题原为 ASCII 冒号「Drone-as-a-Service: Research Challenges and Directions」，按分片规则改全角冒号写入 paper_title。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（literature_review/literature_corpus/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
