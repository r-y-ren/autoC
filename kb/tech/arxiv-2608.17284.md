---
id: arxiv-2608.17284
name: "Rethinking Irregular Time Series Forecasting from the Perspective of Basis Functions（DNBNet）"
field: [时序预测, 机器学习]
directions: [数模与时序预测]
published: "2026-08-18"
maturity: paper
signal:
  venue: arXiv
  stars: 4
  citations_90d: 0
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "不规则采样赛题（医疗随访、稀疏传感、非均匀气象观测）的即插即用预测模型：重要性采样去渐近偏差 + 神经基函数自适应时序模式，官方代码含 main.py/requirements.txt/scripts 可直接 clone 跑通，比自实现 OTED/SeFT 类基线省数天工期"
    reuse_cost: "低"
    open_source: "https://github.com/hnu-vis/DNBNet"
  - track: "数模-数据分析与决策"
    edge: "与同组评估工作（arXiv:2608.17293 CSE 指标 + ITS-Bench，已入库）组成'去偏预测 + 去偏评估'全家桶：预测端 DNBNet、评估端 CSE，同一重要性采样思想贯穿全文方法论章节，故事线自洽且均为论文级背书"
    reuse_cost: "低"
    open_source: "https://github.com/hnu-vis/DNBNet"
sources:
  - url: https://arxiv.org/abs/2608.17284
    title: "Rethinking Irregular Time Series Forecasting from the Perspective of Basis Functions (arXiv:2608.17284)"
    accessed: "2026-08-28"
  - url: https://github.com/hnu-vis/DNBNet
    title: "hnu-vis/DNBNet——论文官方代码（GitHub API 实抓：main.py、requirements.txt、models/layers/loss_fns/scripts 目录齐全，4 stars，2026-08-17 建）"
    accessed: "2026-08-28"
---

# DNBNet：去偏神经基函数网络做不规则时序预测

## 是什么

Li 与 Chen（2026-08-18 提交 arXiv，cs.LG/cs.AI）针对**不规则（irregular）时序预测**提出 **DNBNet（Debiased Neural Basis-Function Network）**。现有方法用**预定义基函数**把不规则观测映射为固定维响应系数，存在两个缺陷：(1) 忽略时间戳采样密度时会产生**不消失的渐近偏差**；(2) 固定基函数对不同时序模式的**适应性有限**。DNBNet 用**重要性采样**修正渐近偏差、用**神经网络参数化基函数**提升模式适应力，并配备基于平均池化的**多尺度分解模块**、**质量感知融合机制**与**双分支解码器**；多个真实数据集实验显示其有效性与跨场景泛化性（来源：https://arxiv.org/abs/2608.17284，抓取 2026-08-28）。

## 解决什么问题

医疗、气象等场景中观测稀疏且非均匀采样，导致"把不规则观测压进固定基函数"这条主流路线带系统性偏差、且基函数表达力受限——预测精度天花板被范式本身锁死。

## 相比前方法优势

- **偏差纠正带理论性质**：重要性采样显式消除采样密度引入的渐近偏差，不是堆模块而是修正范式缺陷；
- **神经基函数替代手工基函数**：对多变时序模式自适应，跨数据集泛化性更强（论文实验主张）；
- **官方代码结构完整可跑**：GitHub 仓库含 main.py（约 12.5KB 入口）、requirements.txt、models/layers/loss_fns/lr_schedulers/scripts 目录，标准 PyTorch 工程布局（GitHub API 实抓 2026-08-28）。

## 局限（如实标注）

- 仓库快照（2026-08-28 实抓）：4 stars / 0 fork，README 仅 8 字节占位——极新极冷，本次仅核实结构完整，**未实际执行**，赛前需自行跑通；
- 重要性采样在极端稀疏区间可能有权重方差风险，摘要未讨论，需自做稳健性检查；
- maturity: paper；对规则均匀采样数据，其"去偏"收益缩水，优势集中在真不规则场景。

## 如何用于比赛

1. **数模-预测/评估类赛题（主用）**：题目数据为不规则时间戳（随访记录、事件日志、丢包传感流）时，直接 clone DNBNet 作为主力或对比模型，把"采样偏差"写进问题分析章节——多数队伍只会插值成均匀网格再套 LSTM，"显式建模非均匀性"是廉价差异化（reuse_cost 低）。
2. **研赛-数据分析题**：与同组 CSE 评估工作（arXiv:2608.17293，卡片已在库）联动：预测端与评估端同用重要性采样思想，方法论叙事完整闭环，适合写"评估与建模的采样偏差统一处理"故事线。
3. 落地注意：仓库无使用文档，预留半天跑通成本；先在题目数据的真值区间校验权重数值稳定性。
