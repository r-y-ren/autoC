---
id: wang2025PracticalOptimizingUAV
name: 充电感知绕障UAV轨迹优化（近似保证）
field: [UAV 轨迹优化, 无线充电网络, 近似算法]
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
  - track: 数模-数据分析与决策
    edge: 绕障+补能+全覆盖的闭环路径规划是数模物流配送/巡检题的高配题型，Christofides 近似框架叠加 1-1/e 与 3π/4 倍最优的解析界，可直接充当解法骨架与精度论证
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: OWGGA 绕障边构造 + TSP 近似巡回 + 按边际收益贪心插入充电站的三层解法，与朴素启发式路径规划基线有明确的拉开手段
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业植保无人机续航补给站选址与作业航线规划的技术支撑点（补能感知轨迹，飞行距离降 38.01%、完成时间降 34.00% 的量化论据）
    reuse_cost: 低
sources:
  - paper_title: "Practical Optimizing UAV Trajectory in Wireless Charging Networks: An Approximated Approach"
    doi: 10.1109/TMC.2025.3586457
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 充电感知绕障UAV轨迹优化（近似保证）

## 单行摘要

在含障碍物与无线充电站的数据采集网络中，UAV 需从基地出发访问全部服务悬停点、按需插入充电站补能并绕障返回，论文提出带近似保证的实用轨迹求解链路：先用 OWGGA 用切线与圆弧为任意两点构造带路径长度界的绕障加权边，再输入 Christofides 近似框架得到候选闭环巡回，最后用 ACSA 按边际收益最大原则逐步选入充电站，在总任务时间、路径长度与补能需求之间取得平衡。

## 方法快照

- 系统建模：基地/服务点/充电点构成候选悬停点集合，障碍物用外接圆柱近似，直连路径可能不可行。
- OWGGA：绕障图构建层——切线+圆弧生成任意两点间可飞路径并给出长度界，可独立复用。
- Christofides 融合：绕障加权边送入 TSP 1.5-近似框架，覆盖全部服务点的候选闭环。
- ACSA：电量约束下按边际收益逐步插入充电站，充电站选择从静态配置变为轨迹本体的一部分。
- 理论结果：近似比 1-1/e，总路径长度至多 3π/4 倍最优；实验飞行距离降 38.01%、完成时间降 34.00%。
- 验证：Intel i7 仿真（合成障碍环境与 50 次随机拓扑平均，未开源）。

## 比赛映射要点

- 数模优化题：无人机配送/巡线/植保作业类路径题普遍假设开阔空间与固定续航，把"障碍规避 + 补能站选择"纳入轨迹本体的建模方式即是差异化点；解析近似界可直接写进模型评价。
- 黑客松/算法赛：三层解法（绕障边权 → TSP 近似 → 贪心插入）可拆开单独复用，其中 OWGGA 绕障图构建是最通用的组件。
- 双创申报：农业无人机续航焦虑与充电桩布设的方案支撑点，量化收益数据可直接支撑可行性论证。

## 关联概念
- 无线充电网络（WCN）

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Wang2025_无线充电网络中具近似保证的实用UAV轨迹优化`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `wang2025PracticalOptimizingUAV` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）。
- `published` 仅年份已知（2025），按 2025-01-01 填写。
- 复现性承自 vault 页自评（medium，仿真级、未开源）；本次跑批未实测任何可运行实现，signal.runnable 如实标 false。
