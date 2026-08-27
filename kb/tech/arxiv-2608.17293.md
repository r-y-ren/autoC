---
id: arxiv-2608.17293
name: "Beyond MSE: Rethinking the Evaluation Metric and Benchmarking for Irregular Time Series Forecasting"
field: [时序预测, 机器学习, 评估方法]
published: "2026-08-18"
maturity: paper
signal:
  venue: arXiv
  stars: 4
  citations_90d: 0
  runnable: true
competition_fit:
  - track: "数模-预测/评估类赛题"
    edge: "不规则采样时序题（医疗就诊记录、稀疏传感器、缺失严重的监测流）上用 CSE 指标替代 MSE 做模型选择与评估章节，一行级改动即获得'评估方法纠偏'的论文级差异化，理论证明（渐近误差不劣于 MSE）可直接引用"
    reuse_cost: "低"
    open_source: "https://github.com/hnu-vis/ITS-Bench"
  - track: "研赛-数据分析题"
    edge: "复用 ITS-Bench（合成/半合成/8 个真实数据集 + 可跑代码）直接搭建对比实验，'MSE 排名 vs CSE 排名不一致'本身即是一个现成的分析故事线"
    reuse_cost: "低"
    open_source: "https://github.com/hnu-vis/ITS-Bench"
sources:
  - url: https://arxiv.org/abs/2608.17293
    title: "Beyond MSE: Rethinking the Evaluation Metric and Benchmarking for Irregular Time Series Forecasting (arXiv:2608.17293)"
    accessed: "2026-08-27"
  - url: https://github.com/hnu-vis/ITS-Bench
    title: "hnu-vis/ITS-Bench——论文官方代码与基准（已核实存在，含 run.py/run_all.sh/requirements.txt/tests）"
    accessed: "2026-08-27"
---

# Beyond MSE：CSE 指标与不规则时序预测基准

## 是什么

Li, Xie, Wang, Chen（2026-08-18 提交 arXiv，cs.LG）针对**不规则（irregular）时序预测**的评估问题：现有基准普遍用 MSE 作评价指标，而作者证明在不规则设定下 MSE 不仅取决于模型预测，还受**样本级时间戳采样分布**影响，导致对真实连续时间性能的有偏评估。论文提出 **CSE（Continuous-time Squared Error）**：用重要性加权消除时间戳采样分布的影响，并**理论上证明 CSE 对连续时间风险的渐近估计误差不大于 MSE**。配套构建覆盖合成、半合成与 8 个真实数据集的基准（ITS-Bench，开源）；实验显示 CSE 能更准确恢复连续时间风险，仅依赖 MSE 可能无法反映模型的连续时间预测能力。

## 解决什么问题

不规则采样（医疗记录、事件流、稀疏传感）下，两个模型按 MSE 排名可能与真实连续时间表现排名**系统性不一致**——评估指标本身污染了模型选择与基准结论。

## 相比前方法优势

- **指标级纠偏带理论保证**：不是又一个新模型，而是修正整个领域评测口径的基础设施型工作，渐近误差不劣于 MSE 有证明支撑；
- **基准 + 代码齐备**：合成/半合成/8 真实数据集基准随论文开源（github.com/hnu-vis/ITS-Bench）；
- 采纳成本极低：CSE 是对现有误差度量的加权改写，不改模型。

## 局限（如实标注）

- 它是**评估工作而非预测模型**，不能直接拿来提升预测精度，只改善"选谁、信谁"；
- 开源仓库快照（2026-08-27 实抓）：4 stars / 0 fork / 3 commits，无 README 描述——极新极冷，本次仅核实仓库结构与入口（run.py、run_all.sh、requirements.txt、pytest.ini、benchmark/ 等）齐全，**未实际执行**，赛前需自行跑通验证；
- 摘要未讨论极端稀疏采样区间下重要性加权估计的方差风险，赛题数据若高度稀疏需自行做稳健性检查；
- maturity: paper；真实赛题（规则采样、均匀网格）上 CSE 退化为常规口径，收益集中在真正不规则的场景。

## 如何用于比赛

1. **数模-预测/评估类赛题（主用）**：凡题目数据为不规则时间戳（随访记录、离散事件日志、丢包传感流），在评估章节并列报告 MSE 与 CSE 两套排名：若一致，证明结论稳健；若不一致，按论文口径解释采样分布偏差——这一"评估方法自觉"在评委面前是廉价而罕见的差异化（reuse_cost 低，加权 MSE 改写即可）。
2. **研赛-数据分析题**：直接 clone ITS-Bench 复用其基准数据与运行脚本搭对比实验，"MSE 说 A 好、CSE 说 B 好"的分歧分析本身就是完整的分析故事线。
3. 落地注意：先在小规模真值上校验重要性权重数值稳定性（与论文实验设定对齐），仓库尚无使用文档，预留跑通成本。
