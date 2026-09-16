---
id: qin2022MultiagentReinforcementLearning
name: CTDE多智能体空中计算三层卸载
field: [移动边缘计算, 多智能体强化学习, 空天地一体网络]
published: 2022-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Services Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 云端 centralized critic + 终端分布式 actor 的 CTDE 卸载框架（TensorFlow/multi-agent actor-critic，2k 迭代内收敛，对比 DDPG/Local Execution/Random 基线），是多智能体调度类赛题可直接套用的学习架构模板
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: UE-LEO-Cloud 三层架构下"本地/星上/云"离散卸载 + 连续功率联合决策的建模方式，适用于多级设施分层决策类赛题（DAG 子任务依赖 + 队列化成本结构的显式建模）
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 偏远区域（海洋/山区/灾区）IoT 数据经 LEO 星上算力分层处理的系统方案支撑，"终端自学习协同、不依赖全程中心调度"的叙事契合低基础设施智慧农业项目
    reuse_cost: 低
sources:
  - paper_title: Multi-Agent Reinforcement Learning Aided Computation Offloading in Aerial Computing for the Internet-of-Things
    doi: 10.1109/TSC.2022.3190562
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# CTDE 多智能体空中计算三层卸载

## 单行摘要

面向地面基础设施稀缺区域的 LEO 卫星移动边缘计算（SMEC），构建 UE-LEO-Cloud 三层空中计算架构：任务拆成带依赖的 DAG 子任务，终端在本地/可见 LEO/远端云之间做离散卸载选择并联合决定传输功率；采用 centralized training with distributed execution 的多智能体 actor-critic——云端 critic 汇聚全局状态、终端 actor 仅依赖局部观测独立执行——联合最小化时延与能耗成本。

## 方法快照

- 三层架构：Tier 1 多个 IoT UE 生成 DAG 型任务；Tier 2 多颗 LEO 搭载 MEC 服务器；Tier 3 远端云提供强算力但回传路径长；小时间尺度决策下卫星视作准静态。
- 任务建模：子任务带数据规模、CPU 周期需求与最大时延约束，依赖结构使卸载成为多阶段决策而非二元选择。
- 学习结构：每个 UE 部署 actor 依据本地观测选择卸载位置与功率；云端 centralized critic 用全局状态与联合动作评价决策，缓解纯独立学习不收敛问题；并估计其他 agent 策略分布以在隐私约束下协同。
- 实验结论：3 颗 LEO、9 个 UE 拓扑上约 2k 迭代收敛；总成本、协同稳定性与公平性优于 DDPG、Local Execution、Random Action 基线。
- 环境：Python 3.5.4 + TensorFlow 1.8.0，GPU 主机（Xeon Gold 5218R），场景参数按区间随机采样。

## 比赛映射要点

- 黑客松：CTDE（集中训练/分布执行）是弱通信、隐私受限环境下多智能体协同的即用架构，比赛里可替换状态/动作空间快速搭多主体调度 demo；论文的三层成本模型（本地/边缘/云）也便于做消融对比。
- 数模：分层设施决策类题（端-边-云、产地-加工-销售）可借鉴其"离散选址 + 连续资源"联合决策与 DAG 约束建模；对比基线设计（随机/本地/单智能体）可直接照搬为消融实验框架。
- 双创：无地面网络的农海场景数据回传方案，引用其三层 SMEC 架构做技术路线图（数字需自测）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Qin2022_物联网空中计算中的多智能体卸载`（frontmatter 4 枚举字段已迁移到本卡：venue_tier/evidence_tier/paper_role/reproducibility_level）。
- bib 回填：citekey `qin2022MultiagentReinforcementLearning` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2022），按 2022-01-01 填写；验证类信息（simulation/Python+TensorFlow/复现性 medium）承自 vault 页自评，开源情况未说明，如需引用请以论文原文复核。
