---
id: arxiv-2609.16804
name: 'SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals'
field: [time series foundation model, 可穿戴生理信号, 不规则采样, 时序插补]
directions: [数模与时序预测]
published: "2026-09-15"
maturity: paper
signal:
  venue: "arXiv v1（cs.LG/cs.AI，页内无 venue/comments 标注）"
  runnable: false
competition_fit:
  - track: "数模-预测与评估"
    edge: "健康/生理监测类赛题（心率/加速度/EEG 等多通道、不规则采样、含噪信号）的架构配方卡：三组件——跨通道空间特征感知主干、PSD 引导的固定频段 MoE（可检查的非学习路由规则）、神经控制微分方程（NCDE）解码器支持任意时刻预测与插补——均为可小规模自建复刻的组件思想（NCDE 有成熟开源实现 torchcde，490★，2026-09-16 实核）；'不规则采样原生+任意时刻查询'直击穿戴数据电极脱落/采样丢失这一预处理最费时痛点"
    reuse_cost: 高
    open_source: "无官方实现（arXiv 页无链接、GitHub 检索 0 命中，2026-09-16 实抓；226B 时间点预训练不可复现，只能借组件与协议小规模复刻；NCDE 组件底座 https://github.com/patrick-kidger/torchcde 公开）"
  - track: "数模-数据分析与决策"
    edge: "单一预训练模型三任务评测协议模板：OOD 零样本预测 + 冻结编码器线性探针分类 + 75% 缺失率连续时间插补，外加加性采集噪声鲁棒性扫描（最强污染下仍匹敌在干净输入上评测的基线）——可直接搬为生理时序赛题的实验设计章节，且回答评委'为什么不逐任务单独建模'"
    reuse_cost: 中
    open_source: "无官方实现（同上；协议底座为论文所用五个公开生理数据集与公开 wearable benchmark，可自建复现）"
sources:
  - url: https://arxiv.org/abs/2609.16804
    title: 'SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals'
    accessed: "2026-09-16"
  - url: https://github.com/patrick-kidger/torchcde
    title: "patrick-kidger/torchcde——PyTorch 神经控制微分方程求解库（组件复用底座，非论文官方代码）"
    accessed: "2026-09-16"
---

# SOTER：面向可穿戴生理信号的生成式时序基础模型

> 来源：https://arxiv.org/abs/2609.16804 （arXiv v1 提交于 2026-09-15，cs.LG/cs.AI，作者 Fangke Chen、Sirry Chen、Wei Chen、Zhongyu Wei；抓取日期 2026-09-16）；组件底座 https://github.com/patrick-kidger/torchcde （490 stars，2026-09-16 实核）

## 是什么

arXiv 2609.16804 提出 **SOTER**——针对可穿戴人体生理信号的**生成式时序基础模型**（以下描述与数字均来自本次抓取的摘要页）：

- **动机**：现有 TSFM 的通用架构假设与生理信号特性错配——多通道、不规则采样、强噪声、跨频谱尺度的耦合连续时间动力学；
- **三个统一架构组件**：
  1. **空间特征感知主干**（spatial feature-aware backbone）：捕捉跨信号（通道间）依赖；
  2. **PSD（功率谱密度）引导的混合专家层**：把表示路由到与固定频段绑定的专家，路由规则**可检查、非学习**；
  3. **神经控制微分方程（NCDE）解码器**：支持任意时间戳的预测与插补；
- **预训练**：5 个公开生理数据集、226B（十亿级×226）时间点；
- **单一预训练模型三类任务**：OOD 零样本预测（6 数据集中 4 个最佳 RMSE、5 个最佳 MAE）、冻结编码器线性探针分类（平均 Macro-AUROC 最高）、连续时间插补（75% 缺失率下 6/6 数据集误差最低）；
- **鲁棒性**：加性采集噪声下保持性能，最强污染强度下仍"匹配或超过在干净输入上评测的基线"；
- **开源状态**：arXiv 页无代码/权重链接，GitHub 检索无官方实现（2026-09-16 实抓，runnable=false）；模型规模未披露。

## 解决什么问题

通用 TSFM 默认规则采样、通道对齐、单一频谱尺度，穿戴生理信号三头不靠；逐任务单独建模费时且吃不到预训练红利。SOTER 的主张是把不规则采样与多尺度频谱动力学做成**架构先验**（NCDE 连续时间解码 + 频段绑定专家），而不是靠重采样/tokenizer 预处理在输入端硬掰——"域专用生成式 TSFM"路线的生理信号样本。

## 相比前方法优势

- **架构先验对齐信号物理**：任意时刻查询免重采样，频段专家显式对应生理信号的频谱结构；
- 一个预训练模型统一预测/分类/插补三任务，域内共享表示；
- 路由规则非学习、可检查——比黑箱 MoE 多一层可解释性，答辩可讲；
- 噪声鲁棒性作为一等评测维度（赛场真实穿戴数据普遍带采集噪声）。

## 局限

- **无开源**（runnable=false）：226B 时间点预训练不可复现，赛队只能借组件思想小规模复刻，或等权重放出（HuggingFace 检索暂无，2026-09-16）；
- v1 无 venue/comments，未过同行评审，全部数字为作者自报；
- 域窄：预训练语料全为生理信号，向工业/交通/金融等域外推未验证；
- 摘要未披露模型规模、推理成本与对比基线清单；线性探针分类不等于端到端微调后的任务上限；
- **库内定位**（TSFM 族去重）：2608.24033 是通用分类原生 TSFM（有官方仓）、2608.22968/24303 是 TSFM 评测协议卡、2608.20024 是 TabPFN-TS 域应用评测——本卡是族内首张**域专用生成式 TSFM 方法卡**，占"不规则采样原生"这一此前无人占的位。

## 如何用于比赛（比赛映射展开）

- **数模-预测与评估**：健康监测类题（睡眠分期/心率/跌倒检测/老年人行为）拿到不规则多通道数据时，按 SOTER 配方自建小规模模型：公开 NCDE 实现（torchcde）+ 分频段专家 + 通道间依赖建模；即使不复刻预训练，"任意时刻查询"对齐电极脱落/采样丢失场景是实打实的差异化卖点；
- **数模-数据分析与决策**：三任务协议（零样本预测/线性探针分类/高缺失插补 + 噪声扫描）搬为实验章节模板；引用论文结论作"生成式域专用 TSFM 可行"的方法佐证，赛场数字必须自测（铁律 4：metrics.json）；
- **跟踪标的**：权重未放出前本卡按架构配方用；官方开源一旦落地，复用成本即从"高"降级——建议后续采集轮持续盯 SOTER/wearable TSFM 关键词。
