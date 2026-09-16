---
id: qian2024PathPlanningAlgorithm
name: 固定翼农田监测无人机的节能覆盖路径规划
field: [精准农业, 覆盖路径规划, 固定翼无人机]
published: 2024-01-01
maturity: paper
directions: [创新创业大赛, 数模与时序预测, 黑客松与数据竞赛]
venue_tier: CCF-A
evidence_tier: core
paper_role: anchor
reproducibility_level: medium
signal:
  venue: Science China Information Sciences
  runnable: false
competition_fit:
  - track: 双创-文书与申报
    edge: 智慧农业直匹配——凸多边形农田巡检/作物监测的固定翼航线设计，显式建模最小转弯半径与航向/旁向图像重叠率约束、以能耗而非距离为目标，区别于多旋翼「之」字扫描的通用套路
    reuse_cost: 低
  - track: 数模-数据分析与决策
    edge: 直线段 + 稳态 U 形转弯的路径元分解、fmincon 求最优转弯速度-半径、条带顺序转 TSP 用 GA 求解的完整建模链，可整体迁移到数模路径/调度优化题
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: CPP 转 TSP 加 GA 的求解组件与覆盖重叠率约束处理可直接复用于路径覆盖类算法赛题
    reuse_cost: 中
sources:
  - paper_title: A Path Planning Algorithm for a Crop Monitoring Fixed-Wing Unmanned Aerial System
    doi: 10.1007/s11432-023-4087-4
    distilled_from: my_LLM_valut
    distilled_date: "2026-09-16"
---

# 固定翼农田监测无人机的节能覆盖路径规划

## 单行摘要

面向凸多边形农田的低空巡检任务，为固定翼无人机设计最小能耗覆盖路径：将直线路径与稳态 U 形转弯分解为两类飞行元件分别建立能耗表达，通过优化扫描方向减少转弯次数，用 fmincon 求解满足升力与最大载荷约束的最优转弯速度-半径组合，再把扫描条带访问顺序转化为 TSP 用遗传算法求解——把「扫哪一行、怎么转、以什么速度飞」统一成节能型覆盖路径设计。

## 方法快照

- 问题特殊性：固定翼存在最小转弯半径与稳定转弯速度约束，多旋翼式逐点路径方法不可直接套用；最优路径不等于最短几何路径（总能耗由直线巡航与各次 U-turn 能耗共同构成）。
- 覆盖约束：机载相机成像宽度与航向/旁向重叠率约束共同决定条带间距与最大飞行高度；农田建模为凸多边形、平行扫描条带完整覆盖。
- 求解链：扫描方向优化（最小化条带数间接减少 U-turn 次数）→ 路径元分解（straight / steady U-turn primitives）→ fmincon 解 U-turn 参数（满足升力与最大载荷约束）→ 条带顺序 TSP + GA 求解。
- 验证：MATLAB 数值仿真，四类凸多边形农田形状，Intel i7-1260P + 16GB RAM；vault 自评代码与 GA 求解器链接已给出但无完整实验资产（artifact partial）。

## 比赛映射要点

- 双创申报（智慧农业核心素材）：大范围农田监测选固定翼而非多旋翼的平台论证、「动力学 + 相机重叠约束重塑覆盖路径问题」的建模叙事、以能耗/换电次数为指标的节本增效量化点，均可直接写进技术方案。
- 数模路径题：覆盖路径规划 → TSP → GA 的建模链与「能耗目标替代距离目标」的目标改造是可复用的方法论；fmincon 处理连续参数子问题的分层求解也符合数模论文结构。
- 黑客松算法题：带覆盖约束与运动学约束的路径优化组件可独立复用。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Qian2024 面向农田监测固定翼无人机的节能覆盖路径规划`（4 枚举字段自 vault 页 frontmatter 迁移）。
- bib 回填：citekey `qian2024PathPlanningAlgorithm` → 标题/venue/DOI 来自 `kb/raw/vault-bib-map.yaml`（vault_bib_backfill.py，2026-09-16）；期刊为 Science China Information Sciences。
- `published` 仅年份已知（2024），按 2024-01-01 填写。
- 复现性承自 vault 页自评（medium，数值仿真级；artifact partial——论文给出代码与 GA 求解器链接但未见完整实验资产，signal.runnable 保守标 false）；本次跑批未实测该代码可用性。
