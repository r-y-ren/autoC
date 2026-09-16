---
id: li2024SecureOffloadingAdversarial
name: 对抗式MARL抗智能窃听的UAV-MEC安全卸载（ARL-MAPPO）
field: [UAV 辅助 MEC, 对抗式多智能体强化学习, 物理层安全]
published: 2024-01-01
maturity: paper
directions: [黑客松与数据竞赛, 数模与时序预测]
venue_tier: unknown
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 合法/窃听两侧交替训练加历史对手策略池按难度加权采样的对抗式 MARL 骨架（CTDE MAPPO），可迁移到多智能体调度与攻防鲁棒类赛题，区别于只对固定对手训练的普通 MARL
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 把安全卸载重写成合法侧最大化/攻击侧最小化 IoT 能效的 max-min 零和博弈，最坏情况鲁棒决策的建模范式适配数模博弈与鲁棒优化类题
    reuse_cost: 中
  - track: Kaggle-竞赛
    edge: 对手策略池防过拟合（更难的对手更高采样概率）直接对应 Kaggle 仿真对抗赛（Lux AI/Halite 类 agent-vs-agent）的 self-play 训练技巧
    reuse_cost: 中
sources:
  - paper_title: "Secure Offloading with Adversarial Multi-Agent Reinforcement Learning against Intelligent Eavesdroppers in UAV-enabled Mobile Edge Computing"
    doi: 10.1109/TMC.2024.3439016
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 对抗式MARL抗智能窃听的UAV-MEC安全卸载（ARL-MAPPO）

## 单行摘要

研究存在会学习、会协同机动的智能窃听 UAV 的多 UAV-MEC 安全卸载场景：把合法 UAV 与窃听 UAV 的对抗建成 max-min 零和博弈，以 MAPPO 为基础交替训练双方策略（ARL-MAPPO），并用历史对手策略池缓解过拟合，使系统在最坏窃听策略下仍保持更高的 IoT 能效、更低时延与更高任务成功率。

## 方法快照

- 问题重构：窃听者不再是固定噪声源，而是学习型智能体；安全卸载从单边优化变成真正的 min-max 对抗问题。
- 系统机制：合法 UAV 双天线（一根收卸载数据、一根发人工噪声抑制窃听），联合优化轨迹、发射功率、人工噪声功率、带宽与 CPU 分配、卸载比例。
- 能效指标：任务成功率、执行时延、能耗合并成统一 IoT 能效度量，合法侧最大化、窃听侧最小化。
- 训练流程：固定一方优化另一方交替进行；双方均 CTDE 风格 MAPPO；窃听策略存入策略池并按难度加权采样。
- 验证：Python + PyTorch 数值仿真（合成场景），对比固定/随机/圆轨迹窃听 UAV 与普通 MAPPO，未开源但给出网络结构与超参数。

## 比赛映射要点

- 黑客松/算法赛：多智能体资源调度类赛题可复用「交替训练 + 对手池」的对抗鲁棒训练骨架；「最坏情况性能而非训练分布内平均性能」的问题定义本身是差异化论证。
- 数模：max-min 博弈建模 + 能效统一指标构造，适配攻防、定价、资源争夺类决策题。
- Kaggle 仿真赛：策略池加权采样 = 防过拟合单一对手的实用 self-play 技巧，可直接用于 agent 对抗赛的训练管线。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Li2024_智能窃听对抗下的UAV辅助MEC安全卸载与资源分配`（4 枚举字段自 vault 页 frontmatter 迁移）。
- venue_tier 说明：vault 页自评 Unknown，按跑批规则映射为 unknown；bib 回填 venue 为 IEEE Transactions on Mobile Computing，供后续 deep-sync 复核升级。
- bib 回填：citekey `li2024SecureOffloadingAdversarial` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，PyTorch 仿真、结构超参齐全但未开源）；signal.runnable 如实标 false。
