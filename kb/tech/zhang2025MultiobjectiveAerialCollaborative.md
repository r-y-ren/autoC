---
id: zhang2025MultiobjectiveAerialCollaborative
name: GDMTD3：扩散模型驱动的多目标空中协同安全通信
field: [无人机集群通信, 物理层安全, 扩散模型强化学习]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 在 TD3 的 actor 生成过程中嵌入扩散模型以刻画高维连续动作分布（阵列权重与三维位置耦合），可作 DRL 优化类赛题超越 PPO/TD3 基线的差异化算法组件
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 保密速率与飞行能耗的双目标权衡建模（非凸 NP-hard 且环境动态），多目标折中策略适合权衡决策类赛题的问题形式化
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 无人机集群数据回传的物理层安全技术点（协同波束对抗移动窃听者），可支撑涉农监测与巡检数据回传方案的保密性卖点；仿真环境披露完整、引用门槛低
    reuse_cost: 低
sources:
  - paper_title: Multi-Objective Aerial Collaborative Secure Communication Optimization via Generative Diffusion Model-Enabled Deep Reinforcement Learning
    doi: 10.1109/TMC.2024.3502685
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# GDMTD3：扩散模型驱动的多目标空中协同安全通信

## 单行摘要

面向移动窃听者威胁下的 UAV 集群协同波束安全通信，论文把问题形式化为保密速率与飞行能耗的 ASCEE-MOP 双目标优化，提出 GDMTD3——在 TD3 的 actor 中引入扩散模型以更好建模高维连续动作分布（激励电流权重与三维位置耦合），学到比常规 TD3 更平滑稳定的保密-能耗折中策略。

## 方法快照

- 场景建模：多架 UAV 构成空中虚拟天线阵列（UVAA），将敏感监视数据远程回传基站；移动窃听者使最优阵列构型与飞行位置持续变化。
- 决策与状态：动作含各 UAV 激励电流权重与三维位置调整；状态含基站位置、窃听者位置、当前编队与链路信息。
- ASCEE-MOP：双目标（提升空地链路保密速率、限制编队调整飞行能耗），非凸、NP-hard 且环境动态变化。
- GDMTD3：TD3 actor 生成过程加入扩散模型，比常规全连接 actor 更适合高维连续动作分布建模——生成式 AI 工具链进入空中协同安全通信优化的代表案例。
- 证据：仿真对比四类部署策略与五类 DRL 基线；环境披露较完整（Ubuntu 22.04.3、PyTorch 2.2.2、CUDA 11.8、RTX 3090、i9-13900K、128GB 内存），但未开源代码。

## 比赛映射要点

- 黑客松算法类：扩散模型 actor 是当前 DRL 赛题里少见的差异化点——同样训练 TD3 框架，动作分布建模能力不同，答辩时可对照 PPO/TD3 基线讲清收益来源。
- 数模决策类：「保密性能 vs 机动成本」的双目标形式化与折中求解，可迁移到性能-成本-风险类权衡决策题。
- 双创申报：无人机集群回传数据的防窃听物理层安全是涉农监测、电力巡检等方案的数据安全卖点；属技术支撑点引用，非方案主体。
- 局限：纯仿真、未开源（runnable 为否）；扩散 actor 的训练开销高于常规 TD3，算力受限的赛题环境需权衡。

## 关联概念（vault 概念页折叠于此，不独立成卡）

- **空中协同安全通信**：多架 UAV 通过协同波束、协同中继、协同机动或角色分工共同提升空中链路保密性与抗窃听能力的通信范式；在本卡中表现为虚拟天线阵列加协同波束。该概念页另锚定 Zhang2024 时间域合谋窃听下的协同安全中继工作（对应既有卡，本次不改动）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhang2025_生成扩散模型驱动的多目标空中协同安全通信`（frontmatter 4 枚举字段迁移：venue_tier=CCF-A、evidence_tier=core、paper_role=anchor、reproducibility_level=medium）；概念页 `空中协同安全通信.md` 已折叠进「关联概念」节。
- bib 回填：citekey `zhang2025MultiobjectiveAerialCollaborative` → 标题/venue/DOI 来自 vault 自带 Zotero bib（`vault_bib_backfill.py`，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation/synthetic/复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
