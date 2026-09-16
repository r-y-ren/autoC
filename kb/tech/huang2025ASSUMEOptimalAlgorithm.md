---
id: huang2025ASSUMEOptimalAlgorithm
name: ASSUME：实测能耗驱动的无人机高度-速度联合调度
field: [UAV 能耗建模, 高度-速度调度, 数据采集]
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
    edge: 无人机巡线/数据采集类赛题中用实测速度-功率曲线替换线性能耗假设，再把高度与速度写成联合 DP 调度，是低门槛、高辨识度的建模差异化组件
    reuse_cost: 中
  - track: 黑客松-数据与算法
    edge: looking before crossing 基础算法 → 动态规划最优 → 在线启发式的三层求解结构可直接迁移到资源受限调度题，节点信息不全的在线变体对应赛题常见动态输入设定
    reuse_cost: 中
  - track: 双创-文书与申报
    edge: 智慧农业低空巡检与农田传感数据采集项目的续航优化支撑点，真实飞行实测加公开水声传感数据双重验证带来工程可信度
    reuse_cost: 低
sources:
  - paper_title: "ASSUME：An Optimal Algorithm to Minimize UAV Energy by Altitude and Speed Scheduling"
    doi: 10.1109/TMC.2025.3581929
    distilled_from: my_LLM_valut
    distilled_date: 2026-09-16
---

# ASSUME：实测能耗驱动的无人机高度-速度联合调度

## 单行摘要

基于真实飞行测试建立速度相关能耗模型，提出 ASSUME 算法以动态规划联合调度 UAV 飞行高度、速度与节点传输切换时机，最小化直线巡径数据采集的飞行能耗，并补充在线启发式应对节点信息未知的场景。

## 方法快照

- 场景与建模：单 UAV 沿直线监测路径（电力线、道路、管线、河岸等）从线性部署的异构地面节点收集数据；UAV 只能沿前进方向运动、不能回飞。
- 能耗模型：以真实飞行测试（2 kg 六旋翼、Pixhawk 3.6.5、Raspberry Pi 3b、ACS712 电流模块）拟合速度相关推进功率曲线，替代"能耗与距离或时间线性相关"的常规假设；飞行能耗在总能量中占主导，忽略无线发送能耗。
- 耦合结构：节点传输效率依赖 UAV 高度，推进能耗依赖飞行速度，高度-速度紧耦合是该问题区别于经典轨迹优化成立的前提。
- 求解链路：looking before crossing 算法处理基础速度调度 → 动态规划扩展为 ASSUME，联合优化高度、速度与节点切换 → 在线启发式处理节点信息不完全已知场景。
- 验证：数值仿真 + 真实飞行/现场测试；数据来自真实飞行测试与公开真实传感器数据（Catalonia water sensor dataset）。

## 比赛映射要点

- 数模（数据分析与决策）：巡线、数据采集类赛题中，用实测速度-功率曲线替换线性能耗假设最容易落地且最能与其他队拉开差距；高度-速度耦合会改变最优调度结构，可作为论文的机理分析亮点。
- 黑客松（数据与算法）：三层求解结构（基础调度 → DP 最优 → 在线启发式）是可移植的调度题模板；"节点信息不全"变体直接对应动态/未知输入的题目设定。
- 双创（文书与申报）：智慧农业低空巡检、农田传感器数据采集项目的续航方案支撑——实测能耗模型 + 公开数据集验证是评审可核查的工程可信度证据。

## 溯源说明（铁律 1 受控例外：paper-distill）

- 提炼来源：my_LLM_valut wiki 页 `Huang2025_ASSUME最优高度速度联合调度节能算法`（frontmatter venue_tier/evidence_tier/paper_role/reproducibility_level 已映射到本卡 4 枚举字段）。
- bib 回填：citekey `huang2025ASSUMEOptimalAlgorithm` → 标题/venue/DOI 来自 vault 自带 Zotero bib（vault_bib_backfill.py，2026-09-16）；bib 标题含 ASCII 冒号，paper_title 已改全角（ASSUME：）写入并在此留痕。
- `published` 仅年份已知（2025），按 2025-01-01 填写；验证类信息（simulation + field_test、复现性 medium）承自 vault 页自评，如需引用请以论文原文复核。
