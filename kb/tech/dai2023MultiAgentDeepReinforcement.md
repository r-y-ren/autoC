---
id: dai2023MultiAgentDeepReinforcement
name: MADRL多机协同波束赋形（HATRPO-UCB）
field: [多智能体强化学习, 协同波束赋形, UAV 通信]
published: 2024-01-01
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
    edge: 把几何位置与通信权重联合决策建成 Markov game 的多目标 MARL 范式——HATRPO 顺序信任域更新缓解非平稳与信用分配、Beta 分布策略处理有界动作、agent-specific global state 增强观测，多智能体协同控制类赛题的方法组件
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农业无人机集群定向组网与抗干扰链路的"虚拟天线阵列"技术亮点，集群通信能力与远距回传论证的支撑点
    reuse_cost: 中
sources:
  - paper_title: "UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning"
    doi: 10.1109/TMC.2024.3419915
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# MADRL多机协同波束赋形（HATRPO-UCB）

## 单行摘要

研究多 UAV 构成虚拟天线阵列与远端基站通信的场景：把各机三维位置与激励电流权重联合建模为多目标优化问题 UCBMOP（阵列速率最大、运动能耗最小），转化为多智能体 Markov game 后提出 HATRPO-UCB——在 HATRPO 基础上加观测增强、agent-specific global state 与 Beta 分布策略，顺序信任域更新学习协同波束赋形策略，实现速率与能耗双目标同时优于基线。

## 方法快照

- 决策变量：UAV 三维悬停位置 + 激励电流权重，几何控制与通信控制耦合，不可分离优化。
- 约束：监控区域边界、高度限制、最小安全间距、运动能耗与服务时长；能耗显式建模水平/爬升/下降三阶段。
- 算法：UCBMOP → Markov game → HATRPO-UCB（observation enhancement + agent-specific global state + Beta policy + 顺序 trust-region 更新）。
- 验证：Python 3.8 + PyTorch 1.10.0 数值仿真（RTX 3090），合成场景，未开源。

## 比赛映射要点

- 黑客松/算法赛：多智能体"位置 + 资源"联合决策、双目标权衡与信用分配是无人机集群/机器人协同赛题的通用骨架，HATRPO-UCB 的三项改进可分别移植到现有 MAPPO/HAPPO 代码库。
- 双创申报：农业无人机集群作业时的定向通信与抗干扰组网（虚拟阵列增益）可作为集群通信能力章节的技术亮点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Dai2023_多智能体深度强化学习的UAV协同波束赋形`（4 枚举字段自该页 frontmatter 迁移）。
- **citekey 与 bib 错配（本次实抓核实）**：vault 溯源链给出的 citekey `dai2023MultiAgentDeepReinforcement` 在 `kb/raw/vault-bib-map.yaml` 中指向 Dai et al. 的全双工用户关联论文（TMC 2023, doi 10.1109/TMC.2022.3188473），与页内容（协同波束赋形 / UCBMOP / HATRPO-UCB）不符；经核对该 citekey 名下 raw 原文（`raw/markdown/dai2023MultiAgentDeepReinforcement.md`），其真实论文为 Liu et al. "UAV-enabled Collaborative Beamforming via Multi-Agent Deep Reinforcement Learning"，对应 bib 条目 `liu2024UAVenabledCollaborativeBeamforming`（TMC 2024）。本卡 title/doi/published 自该正确条目回填，文件名与 id 仍保留分片 citekey 以维持溯源链与去重键；错配本身建议主会话在 vault 侧修复。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/synthetic 验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
