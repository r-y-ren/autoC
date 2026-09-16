---
id: huang2024DynamicTaskOffloading
name: UVEC 多 UAV 任务卸载（SNC+Consensus ADMM）
field: [移动边缘计算, 任务卸载, 分布式优化]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 数模-数据分析与决策
    edge: 用随机网络演算把时延违约概率与缓存溢出概率变成可计算约束，再线性化 + Consensus ADMM 分布式求解能效最大化，是可靠性约束下资源分配题的高级建模与分解求解模板
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 6G 低空经济 UVEC 架构（UAV 反向把任务卸载给移动车辆与边缘服务器）叙事新颖，统计时延保障论证直接对接 mURLLC 高可靠场景
    reuse_cost: 低
sources:
  - paper_title: "Dynamic Task Offloading for Multi-UAVs in Vehicular Edge Computing with Delay Guarantees: A Consensus ADMM-based Optimization"
    doi: 10.1109/TMC.2024.3437785
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# UVEC 多 UAV 任务卸载（SNC+Consensus ADMM）

## 单行摘要

在 UAV-based vehicular edge computing（UVEC）中联合建模多 UAV 的车辆选择与卸载比例控制，用随机网络演算（SNC）把统计时延违约概率与缓存溢出概率写成显式约束，再经线性化与 Consensus ADMM 构造分布式求解算法，在高动态移动环境下兼顾服务可靠性与系统能效。

## 方法快照

- 场景反转：UAV 是任务发起方而非服务节点，把任务分流给选中的移动车辆与 BS 侧边缘服务器；车辆移动按 Markov 过程建模，车辆选择因此是动态决策变量。
- 可靠性建模：显式建模 UAV-BS 队列、UAV-车辆队列、BS 聚合队列与车辆本地队列，SNC 推导时延违约概率与缓冲溢出概率界，把 delay guarantees 转成可计算约束。
- 求解：能效最大化问题经线性变换改写为可分布式处理形式，Consensus ADMM 联合处理车辆选择与卸载比例，多 UAV 局部子问题协调收敛。
- 验证：数值仿真 + 真实轨迹驱动仿真；平台/硬件/开源情况论文未说明。

## 比赛映射要点

- 数模：资源分配类题从平均时延走向可靠性保障的论证支点——违约概率/溢出概率约束 + 分布式分解求解，适合写「统计 QoS 保障」的进阶模型。
- 双创申报：低空经济是政策热词，UVEC 的「空-车-边三层算力池化」架构与 mURLLC 可靠性指标可支撑低空智联方案的技术章节。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Huang2024_多UAV车载边缘计算动态任务卸载`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `huang2024DynamicTaskOffloading` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16），页内容与 bib 条目相符。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 承自 vault 页自评（artifact_availability: unknown，故 runnable 如实标 false）；SNC 参数与仿真设置如需引用请以论文原文复核。
