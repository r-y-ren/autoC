---
id: qin2025MultiagentReinforcementLearning
name: PFSAC：异构UAV通信的个性化联邦抗干扰策略学习
field: [抗干扰通信, 个性化联邦强化学习, 博弈论]
published: 2025-01-01
maturity: paper
directions: [黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: 随机 Stackelberg 博弈（干扰者先手 leader）+ 全局联邦模型与本地模型按权重混合的个性化策略学习，对抗环境多智能体决策赛题的差异化骨架；本地与全局 7:3 混合更优等结论可直接借鉴
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 植保/巡检无人机蜂群在复杂电磁环境下通信可靠性保障的技术支撑点，异构机型的个性化策略设定比统一策略方案更贴近真实机队
    reuse_cost: 低
sources:
  - paper_title: "Multi-Agent reinforcement learning in Adversarial Game Environments: Personalized Anti-Interference Strategies for Heterogeneous UAV Communication"
    doi: 10.1109/TMC.2025.3559123
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# PFSAC：异构UAV通信的个性化联邦抗干扰策略学习

## 单行摘要

在异构 UAV 对间通信与智能干扰器共存的环境中，把抗干扰过程建模为随机 Stackelberg 博弈（jammer 为先行动的 leader、UAV 网络为 follower），提出个性化联邦软 actor-critic 算法 PFSAC：各 UAV 对下载全局联邦模型后与本地模型按权重混合，既共享干扰模式知识又保留个体硬件与任务偏好，学习个性化的信道与功率联合抗干扰策略。

## 方法快照

- 场景：多个异构 UAV pair（功率范围、任务速率门限各异）在智能 jammer 与同频干扰双重压力下周期性频谱感知，联合选择信道与离散功率级别；不依赖全局完美 CSI。
- 博弈建模：jammer 先手 leader、UAV follower 的随机 Stackelberg 博弈，比纯协作 MARL 更贴合干扰环境的先后手关系。
- 信道模型：LoS/NLoS 概率路径损耗 + Nakagami-m 小尺度衰落，通信成功以速率超过任务门限判定。
- PFSAC：全局模型汇聚跨 UAV 干扰环境共性，本地模型保留个体差异，加权融合形成个性化策略；联邦学习在此直接进入抗干扰控制闭环而非仅训练预测模型。
- 验证：4-12 对 UAV、1-4 个 jammer、5-10 信道的合成场景仿真；对比 FSAC、FD3PG、ISAC、IDQN 与随机策略，平均奖励与抗干扰性能持续更优；本地与全局混合权重约 7:3 最佳；未开源、训练软硬件栈未披露。

## 比赛映射要点

- 黑客松/算法赛：对抗博弈类题（干扰-反干扰、攻防决策）可复用 leader-follower 博弈设定 + 个性化联邦 RL 骨架；「共享知识 + 个性决策」的双层设计是与统一策略、独立学习两类基线对比时的现成差异化论证。
- 双创申报：农业无人机作业环境的通信可靠性章节可用「异构机队个性化抗干扰」作为技术亮点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Qin2025_异构UAV通信的个性化抗干扰策略学习`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `qin2025MultiagentReinforcementLearning` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）；注意 bib 中另有 `qin2022MultiagentReinforcementLearning`（不同论文），已按页内容与年份核对无误。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源、未披露完整超参数）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
