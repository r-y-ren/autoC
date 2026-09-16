---
id: ning2024MultiAgentDeepReinforcement
name: MUTO：差异化服务下多UAV辅助MEC的MARL轨迹优化
field: [UAV 辅助边缘计算, 多智能体强化学习, 轨迹优化]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 黑客松与数据竞赛, 数模与时序预测]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: false
competition_fit:
  - track: 黑客松-数据与算法
    edge: Markov game + 集中训练分布式执行 + 优先经验回放的多智能体轨迹控制模板，目标函数从覆盖最大化换成用户短期成本与UAV长期成本的服务经济性导向，多智能体资源调度类赛题可形成差异化
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: 先在完全信息下求服务商博弈 Nash 均衡作理论参照、再在不完全信息下用 DRL 分布式执行的两段式建模，可直接迁移多主体竞争资源配置类数模决策题
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 低空经济与数字乡村叙事中多无人机边缘服务网络按服务类型差异化运营的技术支撑点
    reuse_cost: 低
sources:
  - paper_title: "Multi-Agent Deep Reinforcement Learning Based UAV Trajectory Optimization for Differentiated Services"
    doi: 10.1109/TMC.2023.3312276
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# MUTO：差异化服务下多UAV辅助MEC的MARL轨迹优化

## 单行摘要

针对多服务商差异化服务下的多 UAV 辅助 MEC 轨迹控制问题，先在完全信息下分析服务商博弈的 Nash 均衡作理论参照，再将实际系统写成 Markov game，用 MUTO 多智能体 DRL 在局部观测下学习分布式轨迹策略，同时压低地面用户短期计算成本与 UAV 长期运行成本——轨迹控制的目标从覆盖/速率最大化转向服务经济性。

## 方法快照

- 系统建模：多个服务商各自控制 UAV 边缘服务器，地面用户任务具有异构数据规模、CPU 周期需求与服务偏好向量；UAV 既是空中边缘服务器，也是通过移动改变服务能力分布的空间控制器。
- 两段式求解：完全信息静态博弈刻画 Nash 均衡（理论参照）；不完全信息实际系统写成 Markov game，各服务商仅依本地观测控制所属 UAV 位置。
- MUTO：集中训练分布式执行 + 优先经验回放（PER）提升收敛速度与稳定性。
- 成本建模：同时计入用户侧计算/传输成本与 UAV 侧长期运行成本，而非单纯覆盖或速率目标。
- 验证：400m x 400m 区域、100 用户、2 服务商/UAV、60 时隙的仿真（Python 3.9 + PyTorch 1.11.0，任务负载参考 EEG 与 YouTube 数据集）；对比随机飞行、局部执行等基线持续降低总计算成本；未开源。

## 比赛映射要点

- 黑客松/算法赛：多智能体调度/轨迹规划类赛题可套用「博弈均衡作参照 + CTDE 学习分布式策略」骨架；「差异化服务 + 服务成本目标」的问题定义本身即是与常见覆盖最大化方案的差异化论证。
- 数模决策题：多主体竞争下的资源配置可用同款两段式建模（均衡分析 + 求解算法），理论部分直接给论文式分析提供结构。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Ning2024_差异化服务的多UAV轨迹优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `ning2024MultiAgentDeepReinforcement` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源、未披露完整超参数）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
