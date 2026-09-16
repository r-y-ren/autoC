---
id: zhang2024TaskOffloadingTrajectory
name: 动态用户多UAV-MEC安全卸载与轨迹优化（JDPB）
field: [UAV-MEC, 物理层安全, 轨迹优化]
published: 2024-01-01
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
    edge: "Gauss-Markov 移动用户场景下'区域划分 + 动态规划/竞价式分配 + SCA/BCD 交替凸化'的分层求解模板，适用于含移动用户与时变链路的调度/轨迹类赛题；max-min 安全计算容量的公平性目标设计也是可复用的差异化点"
    reuse_cost: 中
  - track: 数模-数据分析与决策
    edge: "混合整数非凸问题的'离散分配 + 连续凸化'分层求解套路（竞价机制处理用户-UAV 关联、CVX/SCA 处理时隙-功率-轨迹耦合）是数模优化类题的通用求解范式，比直接上启发式更有论证力度"
    reuse_cost: 中
sources:
  - paper_title: "Task Offloading and Trajectory Optimization for Secure Communications in Dynamic User Multi-UAV MEC Systems"
    doi: 10.1109/TMC.2024.3442909
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 动态用户多UAV-MEC安全卸载与轨迹优化（JDPB）

## 单行摘要

在用户随机移动（Gauss-Markov 模型）、窃听者监听卸载链路的多 UAV MEC 系统中，地面 BS 发射友好干扰压制窃听（UAV 预知干扰信号可在接收端分离），提出 JDPB 分层求解器：先把区域划分子区域并用动态规划 + 竞价机制把用户分配到各 UAV，再用 SCA 与 BCD 交替优化时隙分配、发射功率、CPU 频率与轨迹，目标是最大化所有用户中的最小安全计算能力。

## 方法快照

- 威胁模型：窃听者截获卸载链路；BS 干扰窃听者但 UAV 因预知干扰波形不受影响——"友好干扰"直接嵌入 MEC 卸载系统而非外层补丁。
- 动态性：用户位置逐时隙按 Gauss-Markov 更新，卸载关联与轨迹必须逐时隙适应，静态关联假设失效。
- 求解分层：离散卸载决策（区域划分 + DP + bidding）与连续资源/轨迹优化（SCA + BCD，CVX 实现）解耦交替。
- 目标设计：max-min secure calculation capacity，把安全保障从"链路保密"扩展到"安全计算能力的公平保障"。
- 约束体系：用户最小安全计算需求、UAV 能量预算、速度上下限、机间安全距离、每机服务用户数上限。
- 验证：数值仿真（合成动态用户与窃听者场景，CVX 求解凸子问题，未开源）。

## 比赛映射要点

- 黑客松/算法赛：移动用户/时变拓扑下的分配与调度题可复用"分区 + 竞价 + 凸化交替"的分层结构；"安全容量 max-min"式的公平性目标在含服务质量下限约束的赛题中可直接迁移。
- 数模优化题：混合整数非凸问题的标准拆解范式——离散变量用匹配/竞价/DP，连续变量用 SCA/BCD 交替，论文给出了完整的可模仿写作结构（建模-分解-凸化-收敛）。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Zhang2024_动态用户多UAV_MEC安全通信中的卸载与轨迹优化`（4 枚举字段自 vault 页 frontmatter 迁移，reproducibility_level=medium）。
- bib 回填：citekey `zhang2024TaskOffloadingTrajectory` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，参数表完整但无代码与平台细节）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
