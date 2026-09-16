---
id: wu2025TwostageDeepEnergy
name: IOPO：THz多UAV-MEC的IRS辅助卸载优化
field: [UAV 辅助边缘计算, THz 通信, 智能超表面]
published: 2025-01-01
maturity: paper
directions: [数模与时序预测, 黑客松与数据竞赛, 创新创业大赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: IEEE Transactions on Mobile Computing
  runnable: true
competition_fit:
  - track: 数模-数据分析与决策
    edge: MINLP 拆成"先离散卸载决策、后连续相位优化"的两阶段分解 + 顺序保持搜索（OPPO）加速收敛，是耦合决策问题降维求解的通用范式，可迁移到混合整数类调度/分配赛题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: 两阶段 DNN 对比 DDPG 等单阶段方法在 3 UAV、15 用户场景能耗最多降 32.8%，"分阶段近似逼近理论最优"的论证结构在算法赛答辩中可直接复用
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: THz 遮挡场景下 IRS+UAV 低空组网叙事的技术支撑点（传播控制变量引入后卸载问题升级为卸载+相位耦合，方案完整度高）
    reuse_cost: 低
sources:
  - paper_title: "Two-Stage Deep Energy Optimization in IRS-assisted UAV-based Edge Computing Systems"
    doi: 10.1109/TMC.2024.3461719
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# IOPO：THz多UAV-MEC的IRS辅助卸载优化

## 单行摘要

面向 THz 多用户多 UAV MEC 场景（链路易受阻、传播衰减强），引入 IRS 改善传播环境，把二元任务卸载矩阵与 IRS 相位的联合优化写成混合整数非线性问题（NP-hard），提出两阶段深度学习框架 IOPO（Iterative Order-Preserving Policy Optimization）：第一阶段生成较优二元卸载决策，第二阶段在此基础上优化 IRS 相位；配合 OPPO 顺序保持策略搜索单元在迭代中持续挖掘更优卸载方案——同轮训练下解更接近理论最优，能耗对比 DDPG 基线最多降 32.8%（3 UAV、15 用户）。

## 方法快照

- 系统设定：多用户 + 多 UAV（UAV 本身即 MEC 服务器）+ 单 IRS，用户任务可本地执行或卸载到某架 UAV，卸载矩阵为 U×(M+1) 二元矩阵。
- 问题建模：最小化本地计算、上传与 UAV 处理总能耗，约束为每个任务不超时可接受时延（no-overdue）。
- 两阶段求解：先定卸载决策、再调 IRS 相位，区别于单阶段方法在同一概率空间同时产两个变量导致次优。
- OPPO：顺序保持量化方法持续更新卸载决策集合，加速收敛并降低大解空间下的复杂度。
- 基线对比：LOCAL、GREEDY、DDPG。
- 验证：仿真，论文明确开源源码（https://github.com/UIC-JQ/IOPO）。

## 比赛映射要点

- 数模决策题：混合整数（离散决策+连续参数）耦合是调度/分配题常态，"先离散后连续"的两阶段分解加顺序保持枚举是可复用的降维求解模板。
- 黑客松/算法赛：对比"单阶段联合预测"基线的能耗/质量曲线是现成的差异化论据；开源实现（PyTorch DNN）可改造为在线决策组件。
- 双创申报：低空智联网、复杂遮挡环境（山区果园、城市峡谷）无人机边缘服务的方案支撑点。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wu2025_IOPO面向THz多UAV-MEC的IRS辅助卸载优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- citekey 核对：页名带方法名 IOPO，曾疑似与 citekey `wu2025TwostageDeepEnergy` 错配；经查 raw 原文（`my_LLM_valut/01_LLM_Wiki_Karpathy_Style/raw/markdown/wu2025TwostageDeepEnergy.md`），论文标题即 Two-Stage Deep Energy Optimization in IRS-Assisted UAV-Based Edge Computing Systems（DOI 10.1109/TMC.2024.3461719），citekey 语义与论文一致，**无错配**，bib 回填沿用原条目。
- bib 回填：标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- runnable 依据：论文原文明确给出源码链接 https://github.com/UIC-JQ/IOPO，与 vault 页自评 artifact_availability=open 一致；本次跑批未实际克隆运行，reproducibility_level 仍按 vault 自评如实标 medium。
