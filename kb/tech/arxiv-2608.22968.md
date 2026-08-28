---
id: arxiv-2608.22968
name: 'Do Time-Series Foundation Models Pay Off for Industrial Monitoring? A Cost-Aware Empirical Study'
field: [time series foundation model, 异常检测与状态监测, 模型选型]
directions: [数模与时序预测]
published: "2026-08-24"
maturity: paper
signal:
  venue: "CIF26 (2026) poster P01013（arXiv comments：7 pages, 2 figures）"
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "'轻量拟合模型 vs TSFM'对比章节的现成协议模板：out-of-fold AUROC/AUPRC + 配对 bootstrap 置信区间 + 资源计量（时延/峰值 VRAM/state-dict 尺寸）三件套，精度与成本并列呈现——直接回答评委必问的'为什么不用大模型/为什么用大模型'，且有论文级先验结论背书（TSFM 是任务依赖选项而非默认替代）"
    reuse_cost: 低
    open_source: "无（arXiv 页与检索均未见官方实现；协议可基于公开数据集 C-MAPSS/MIMII/BDG2 与公开模型 MOMENT/Chronos/TimesFM 自建复现）"
  - track: "数模-数据分析与决策"
    edge: "工业监测类题（设备退化预测/异常检测/预测残差诊断）的选型先验矩阵：退化与异常类任务优先轻量神经模型+经典单类法，预测残差诊断类可试 TSFM——三个设定恰好覆盖工业监测三主流任务形态，可当决策树用"
    reuse_cost: 低
    open_source: "无（同上）"
sources:
  - url: https://arxiv.org/abs/2608.22968
    title: 'Do Time-Series Foundation Models Pay Off for Industrial Monitoring? A Cost-Aware Empirical Study'
    accessed: "2026-08-28"
---

# TSFM 用于工业监测值不值：成本感知实证研究

> 来源：https://arxiv.org/abs/2608.22968 （arXiv v1 提交于 2026-08-24，cs.LG，作者 Guan-Hua Wen、Kuan-Yu Chen；comments: Accepted for poster presentation at CIF26 (2026), Poster P01013, 7 pages, 2 figures；抓取日期 2026-08-28）

## 是什么

arXiv 2608.22968 是一篇**成本感知实证研究**：在真实数据、校准与资源约束下，检验时序基础模型（TSFM）在工业监测中的部署价值（以下描述与数字均来自本次抓取的摘要页）。三个设定：

1. **C-MAPSS 退化风险代理**（100 台发动机，out-of-fold）：紧凑 TCN 自编码器达折加权 AUROC/AUPRC 0.9570/0.8960，MOMENT 重建仅 0.7310/0.3080，配对 bootstrap 置信区间不含零；
2. **MIMII 异常声学检测**（仅正常样本训练，5 组匹配泵评测）：经典 OCSVM 在 AUROC 与 AUPRC 上超过 MOMENT 重建路径；
3. **BDG2 预测残差诊断**（固定 12 表计面板 + 合成目标扰动）：TimesFM 2.5 对齐预测误差最低、合成 AUROC 点估计最高，但合成 AUPRC 与拟合模型相当；
4. **成本计量**：MOMENT 的时延、峰值 VRAM、序列化 state-dict 尺寸均高于 TCN-AE。

**结论**：TSFM 是"任务依赖的部署选项"，而非轻量拟合模型的默认替代。

## 解决什么问题

TSFM 的宣传卖点（可复用表示 + 零样本预测）与部署现实（任务定义异构、轻量基线有竞争力、资源约束收紧）之间长期缺少对齐的证据——本文补上"何时值得用 TSFM"的实证决策依据。

## 相比前方法优势

- 三设定覆盖工业监测三主流任务形态（退化预测 / 异常检测 / 残差诊断），横跨经典单类方法（OCSVM）、紧凑神经模型（TCN-AE、残差预测器）与 TSFM（MOMENT-small、Chronos-T5、TimesFM 2.5）；
- **成本维度与精度并列**：时延/VRAM/state-dict 尺寸进主表，贴近部署与赛场算力现实；
- out-of-fold + 配对 bootstrap CI 的严谨性模板，可直接搬为赛场评测协议；
- 结论克制：不是"TSFM 无用论"，而是给出按任务形态分流的选型指导。

## 局限

- **无开源**（arXiv 页与网页检索均未见官方实现，runnable=false）：协议复用需自建；
- 每设定单一数据集/设备范围（C-MAPSS 100 机、MIMII 5 组泵、BDG2 固定 12 表计），外推性受限；
- poster 7 页篇幅，超参与重复实验细节需进正文核实，摘要数字为折加权/点估计口径；
- **引用须防断章**：BDG2 上 TimesFM 2.5 预测误差最低——TSFM 并非全面落败，摘自结论时须保留"任务依赖"限定；
- 仅测 MOMENT/Chronos/TimesFM 三家，未覆盖 Moirai/TTM/小型域适配路线。

## 如何用于比赛（比赛映射展开）

- **数模-预测与评估**：搬评测协议三件套（out-of-fold AUROC/AUPRC + 配对 bootstrap CI + 资源计量），作为"轻量基线 vs 基础模型"对比章节模板——这恰是评委对"为什么选这个模型"的标准问法；
- **数模-数据分析与决策**：工业监测类题的选型决策树——退化/异常类优先 TCN-AE+OCSVM 级轻量方案，预测残差诊断类再试 TimesFM；据此可写"成本感知选型矩阵"作为论文方法论骨架；
- **引用纪律**：论文数字只能作方法佐证与选型先验，对外作品的性能数字必须来自自测（铁律 4：workspace/metrics.json）。
