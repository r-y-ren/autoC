---
id: wang2025JointOptimizationBeamforming
name: GNN+SD3的UAV-RIS联合波束与轨迹优化
field: [UAV-mounted RIS, 图神经网络, 强化学习]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 「无监督 GNN 学拓扑相关变量（多用户波束）+ 连续控制 RL（SD3）学轨迹」的分而治之混合架构，可迁移到任何「结构相关变量 + 连续控制变量」耦合的赛题（网络资源协同、传感器联动调控），避免全变量丢给黑盒 RL 难收敛
    reuse_cost: 高
  - track: 数模-数据分析与决策
    edge: 速率 / 能耗 / 飞行时长多目标拆解为两层子问题交替求解 + reward shaping 缓解稀疏奖励的套路，是多变量耦合优化数模题的求解结构参考（TMC 2025）
    reuse_cost: 中
sources:
  - paper_title: "Joint Optimization of Beamforming and Trajectory for UAV-RIS-assisted MU-MISO Systems Using GNN and SD3"
    doi: 10.1109/TMC.2025.3563072
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# GNN+SD3的UAV-RIS联合波束与轨迹优化

## 单行摘要

面向城市建筑遮挡环境下的 UAV-mounted RIS 多用户（MU-MISO）下行系统，论文把基站主动波束、RIS 被动波束与 UAV 三维轨迹统一到多目标优化框架（最大化系统速率、最小化 UAV 能耗与飞行时长），并用两层结构化求解：GNN 以无监督方式编码多用户-基站-RIS 图结构、联合优化主动与被动波束；SD3（双 actor-critic + softmax Q 值）在连续动作空间学 UAV 轨迹，配合 reward shaping 缓解稀疏奖励。

## 方法快照

- 场景模型：建筑统计遮挡模型决定链路可达性；RIS 由 UAV 携带成为可机动反射平台，而非固定反射板。
- 波束层：图结构编码多用户与多节点耦合关系，无监督 GNN 训练输出主/被动波束。
- 轨迹层：轨迹规划写成 MDP，SD3 双 actor-critic 与 softmax Q 值提升训练稳定性。
- 求解哲学：结构化分而治之（图学习管关系变量、RL 管控制变量），而非全变量黑盒。
- 验证：PyTorch（Windows 11、i7-12700F CPU）数值仿真、合成城市遮挡场景，对比 DNN 等 UAV-RIS 基线；代码与随机种子未披露，无开源。

## 比赛映射要点

- 黑客松算法类：变量耦合型赛题可直接借用「关系变量用 GNN、控制变量用 RL」的拆分模板，这一架构模式不限于通信场景。
- 数模决策类：多目标拆层交替求解 + 稀疏奖励塑形的工程化处理，适合作为大规模连续优化题的方法论参考。

## 关联概念
- UAV-RIS协同通信

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2025_GNN与SD3驱动的UAV-RIS联合波束与轨迹优化`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2025JointOptimizationBeamforming` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
