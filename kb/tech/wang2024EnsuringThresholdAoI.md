---
id: wang2024EnsuringThresholdAoI
name: 阈值AoI约束的多UAV群智感知调度
field: [信息年龄AoI, 移动群智感知, 多智能体强化学习]
published: 2024-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE/ACM Transactions on Networking
  runnable: false
competition_fit:
  - track: 数模-预测与评估
    edge: threshold AoI 把时效评估从「平均更新鲜」改为「红线违约率」，与总收集数据量构成双目标评估体系——巡检 / 应急监测类数模题的时效性评估指标设计可直接借用；Beijing 与 San Francisco 两个真实群智感知数据集可复用于实验
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 去中心化 MADRL 中 GTrXL 提取长时依赖 + RND 内在奖励自动激励探索冷门 PoI 的组合，是多机巡检 / 覆盖调度赛题的差异化算法组件（无需中央控制器即可形成分工）
    reuse_cost: 高
  - track: 双创-文书与申报
    edge: 「关键监测点不能失守」的时效红线保障方案支撑（ToN 2024 方法），贴合农业灾害预警、水体监测等申报场景的时效性承诺论证
    reuse_cost: 低
sources:
  - paper_title: "Ensuring Threshold AoI for UAV-Assisted Mobile Crowdsensing by Multi-Agent Deep Reinforcement Learning With Transformer"
    doi: 10.1109/TNET.2023.3289172
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 阈值AoI约束的多UAV群智感知调度

## 单行摘要

多 UAV 对城市 PoI 持续巡检采集数据时，仅最小化平均 AoI 会忽略边缘节点、让关键 PoI 长时间越过时效红线。论文提出 threshold AoI 新指标（显式刻画 AoI 是否越过应用给定阈值），并配套 DRL-UCS(AoIth) 分布式多智能体框架：每架 UAV 基于局部观测决策，GTrXL（门控 Transformer）负责提取时间序列长依赖，RND 内在奖励鼓励探索偏远易被忽略的区域，在有限能量下联合优化数据收集量、总 AoI 与阈值违约率。

## 方法快照

- 指标贡献：threshold AoI 使「是否越线」成为显式优化对象，与平均 AoI / 最大 AoI 目标形成区分。
- 学习框架：去中心化 MADRL（独立执行 + 共享训练），GTrXL 解决 MLP/LSTM 对复杂轨迹历史建模不足的问题。
- 探索机制：RND 内在奖励驱动 UAV 主动补位冷门区域，缓解「平均目标牺牲边缘点」的失衡。
- 证据完整度：simulation + 真实数据集 trace 驱动（Beijing、San Francisco crowdsensing dataset），PyTorch 1.11.0 + 8x RTX A6000 训练栈披露充分；代码未公开。

## 比赛映射要点

- 数模评估类：「数据收集量 + 阈值违约率」双目标评估体系可用于任何有时效红线的监测调度题；真实数据集驱动的实验设计可直接借鉴。
- 黑客松算法类：多机持续巡检赛题中，「平均指标 + 违约率」目标函数与内在奖励探索是超越贪心覆盖基线的组合拳。
- 双创申报：灾害预警 / 精准农业监测的「关键点时效 SLA」论证支撑。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2024_面向UAV群智感知的阈值AoI保障`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `wang2024EnsuringThresholdAoI` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation+trace_driven（公开数据集）验证形态承自 vault 页自评（artifact_availability: unknown），如需引用请以论文原文复核。
