---
id: arxiv-2609.16804
name: 'SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals'
field: [time series foundation model, 可穿戴生理信号, 不规则采样, 时序插补]
directions: [数模与时序预测]
published: "2026-09-15"
maturity: demo
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "arXiv v1（cs.LG/cs.AI，页内无 venue/comments 标注）+ 官方开源（GitHub SII-fkchen/SOTER，MIT；HF SII-fkchen/SOTER 权重，2026-09-22 实抓）"
  stars: 73
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "健康/生理监测类赛题（心率/加速度/EEG 等多通道、不规则采样、含噪信号）的首选底模（2026-09-22 起权重可取）：零样本预测/任意时刻插补/线性探针分类三任务直接推理复用——数据按 JSONL（sequence+物理时间戳+mask）整理、训练集拟合 MinMax 归一化即可跑官方 forecasting_example；『不规则采样原生+任意时刻查询』直击穿戴数据电极脱落/采样丢失这一预处理最费时痛点；PSD 引导 MoE、NCDE 解码器等组件思想保留为需要自建/微调时的架构参考（NCDE 底座 torchcde 公开）"
    reuse_cost: 中
    open_source: "官方仓 https://github.com/SII-fkchen/SOTER（推理代码+评估脚本，MIT，73 stars）+ HF 权重 https://huggingface.co/SII-fkchen/SOTER（model.safetensors，transformers 兼容；均 2026-09-22 实抓）；注意：仅推理态，无训练/微调代码，226B 时间点预训练不可复现"
  - track: "数模-数据分析与决策"
    edge: "单一预训练模型三任务评测协议模板：OOD 零样本预测 + 冻结编码器线性探针分类 + 75% 缺失率连续时间插补，外加加性采集噪声鲁棒性扫描（最强污染下仍匹敌在干净输入上评测的基线）——可直接搬为生理时序赛题的实验设计章节，且回答评委'为什么不逐任务单独建模'；协议可在官方权重上直接复跑（评估脚本已开源）"
    reuse_cost: 中
    open_source: "官方仓+HF 权重（同上，2026-09-22 实抓）；协议底座为论文所用五个公开生理数据集（MIMIC-III-Waveform/Sleep-EDF/PTB-XL/WESAD/Chapman-ECG，README 给 PhysioNet/UCI 申请链接）"
sources:
  - url: https://arxiv.org/abs/2609.16804
    title: 'SOTER: A Generative Time-Series Foundation Model for Wearable Human Physiological Signals'
    accessed: "2026-09-16"
  - url: https://github.com/patrick-kidger/torchcde
    title: "patrick-kidger/torchcde——PyTorch 神经控制微分方程求解库（组件复用底座，非论文官方代码）"
    accessed: "2026-09-16"
  - url: https://github.com/SII-fkchen/SOTER
    title: "SII-fkchen/SOTER 官方仓实抓（2026-09-22 API+README+文件树：73 stars/0 forks，MIT，Python，2026-09-09 创建、09-16 末次 push；内容为推理态——soter/models 建模代码+forecasting_example.py 评估脚本+HF 权重加载示例，无训练/微调代码；README 自述 226B 时间点预训练、每步激活 20.29M 参数、输入 JSONL 格式含物理时间戳与 mask、训练数据五集仅给申请链接不可再分发）"
    accessed: "2026-09-22"
  - url: "https://huggingface.co/api/models/SII-fkchen/SOTER"
    title: "HF 权重实抓（2026-09-22 API：model.safetensors+config.json 在库，transformers 兼容 tag，58 downloads/1 like，MIT）"
    accessed: "2026-09-22"
---

# SOTER：面向可穿戴生理信号的生成式时序基础模型

> 来源：https://arxiv.org/abs/2609.16804 （arXiv v1 提交于 2026-09-15，cs.LG/cs.AI，作者 Fangke Chen、Sirry Chen、Wei Chen、Zhongyu Wei；抓取日期 2026-09-16）；组件底座 https://github.com/patrick-kidger/torchcde （490 stars，2026-09-16 实核）；**官方开源已落地**：https://github.com/SII-fkchen/SOTER + HF 权重（2026-09-22 实抓，见文末更新记录）

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
- **开源状态**（2026-09-22 更新）：官方推理代码仓 SII-fkchen/SOTER（MIT，73 stars）+ HF 权重（model.safetensors，transformers 兼容）已放出；**仅推理态**——无训练/微调代码，226B 时间点预训练不可复现（建卡时 2026-09-16 曾实抓确认无官方实现，开源为后补发布）。

## 解决什么问题

通用 TSFM 默认规则采样、通道对齐、单一频谱尺度，穿戴生理信号三头不靠；逐任务单独建模费时且吃不到预训练红利。SOTER 的主张是把不规则采样与多尺度频谱动力学做成**架构先验**（NCDE 连续时间解码 + 频段绑定专家），而不是靠重采样/tokenizer 预处理在输入端硬掰——"域专用生成式 TSFM"路线的生理信号样本。

## 相比前方法优势

- **架构先验对齐信号物理**：任意时刻查询免重采样，频段专家显式对应生理信号的频谱结构；
- 一个预训练模型统一预测/分类/插补三任务，域内共享表示；
- 路由规则非学习、可检查——比黑箱 MoE 多一层可解释性，答辩可讲；
- 噪声鲁棒性作为一等评测维度（赛场真实穿戴数据普遍带采集噪声）。

## 局限

- **推理态开源**（2026-09-22 更新）：权重+推理/评估脚本可得，零样本预测/插补/线性探针可直接复用；但无训练与微调代码——权重固定在生理信号域，向赛题域微调的路未提供（只能 prompt 不了时退回零样本或自建组件），226B 时间点预训练仍不可复现；README 示例为自回归逐步解码（逐点预测），长 horizon 推理偏慢；
- 仓库热度快照如实：73 stars/0 forks（2026-09-22 API，创建后 13 天）、HF 58 downloads——关注度尚小，社区验证不足；
- v1 无 venue/comments，未过同行评审，全部数字为作者自报；
- 域窄：预训练语料全为生理信号，向工业/交通/金融等域外推未验证；
- 摘要未披露模型规模、推理成本与对比基线清单；线性探针分类不等于端到端微调后的任务上限；
- **库内定位**（TSFM 族去重）：2608.24033 是通用分类原生 TSFM（有官方仓）、2608.22968/24303 是 TSFM 评测协议卡、2608.20024 是 TabPFN-TS 域应用评测——本卡是族内首张**域专用生成式 TSFM 方法卡**，占"不规则采样原生"这一此前无人占的位。

## 如何用于比赛（比赛映射展开）

- **数模-预测与评估**：健康监测类题（睡眠分期/心率/跌倒检测/老年人行为）拿到不规则多通道数据时，按 SOTER 配方自建小规模模型：公开 NCDE 实现（torchcde）+ 分频段专家 + 通道间依赖建模；即使不复刻预训练，"任意时刻查询"对齐电极脱落/采样丢失场景是实打实的差异化卖点；
- **数模-数据分析与决策**：三任务协议（零样本预测/线性探针分类/高缺失插补 + 噪声扫描）搬为实验章节模板；引用论文结论作"生成式域专用 TSFM 可行"的方法佐证，赛场数字必须自测（铁律 4：metrics.json）；
- **跟踪标的已兑现**（2026-09-22）：官方仓+HF 权重落地，复用成本从"高"降为"中"——赛题拿到多通道不规则生理数据时先直接零样本推理试水（数据转 JSONL+MinMax 归一化+官方示例脚本），再决定是否值得自建组件；后续 deep-sync 继续盯微调代码是否放出与同行评审结果。

## 更新记录

- **2026-09-22**：候选队列出现 gh-SII-fkchen_SOTER（仓库信号），实抓确认官方开源已落地（论文卡建卡时 2026-09-16 尚无实现）——按同一工件处理：本卡更新（maturity paper→demo、runnable=true、stars=73 快照、复用成本降级、补仓库/HF 两条来源），gh- ID 不另建卡（记入 .rejections.yaml 防增量重复）。更新依据：GitHub API+README+文件树（推理态、无训练代码）、HF API（权重在库）2026-09-22 实抓。
