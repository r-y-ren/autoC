---
id: cui2024DataValueBased
name: 数据价值驱动的UAV群异步联邦学习
field: [联邦学习, UAV 集群, 客户端调度]
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
    edge: Shapley Value 数据价值评估 + Network AoU 公平性建模 + Whittle Index 顺序选择构成数据异构、链路不稳下"选谁参与训练"的完整调度算法栈，弱网协同训练类赛题可整体复用
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 农田弱网环境下多机协同边缘智能训练方案——异步聚合摆脱同步等待，支撑植保/巡田无人机群"边采集边学习"的技术叙事
    reuse_cost: 低
sources:
  - paper_title: "The Data Value Based Asynchronous Federated Learning for UAV Swarm Under Unstable Communication Scenarios"
    doi: 10.1109/TMC.2023.3331906
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# 数据价值驱动的UAV群异步联邦学习

## 单行摘要

面向空空链路不稳定、本地数据异构的 UAV 群联邦学习，提出两阶段异步框架：预训练阶段把各 UAV 参与训练建模为合作博弈、用 Shapley Value 度量数据集边际贡献，训练阶段引入 Network AoU 把数据价值与"多久没被选中"的公平性统一进顺序 UAV 选择，再以 Whittle Index 最小化 AoU 得到近似最优调度，摆脱同步聚合的 straggler 瓶颈。

## 方法快照

- 系统结构：一个中心 UAV + 多个采集数据的从属 UAV，链路以连接概率建模随机可用，每轮只选一架 UAV 顺序异步更新。
- 收敛分析：分别给出凸与非凸情形的训练性能上界，指出数据量与梯度异质性共同决定单机贡献。
- 数据价值：合作博弈 Shapley Value + 分布式采样估计降低精确求解复杂度，并给出采样误差上界。
- 公平性与调度：AoU / Network AoU 显式建模参与公平，顺序选择转化为 Whittle Index 驱动的 AoU 最小化。
- 验证：MNIST、FLAME 上的数值仿真，部分实验资产公开。

## 比赛映射要点

- 黑客松/算法赛：客户端选择/任务调度题可直接搬用"价值归因（Shapley）+ 公平性（AoU）+ 指标调度（Whittle Index）"三件套，对比贪心按价值选择的基线即成差异化。
- 双创申报：农业无人机群在弱网下的协同模型训练（如田间病害识别模型持续更新）是申报书中边缘智能章节的现成技术支撑点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Cui2024_不稳定通信下基于数据价值的UAV群异步联邦学习`（4 枚举字段自该页 frontmatter 迁移）。
- bib 回填：citekey `cui2024DataValueBased` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写；复现性 medium 与 simulation/公开数据集验证形态承自 vault 页自评（artifact_availability: partial），如需引用请以论文原文复核。
