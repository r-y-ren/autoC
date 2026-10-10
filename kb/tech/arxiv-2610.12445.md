---
id: arxiv-2610.12445
name: "Caught in the Act: 白盒探针规模化了前沿 LLM 欺骗监控（FIBS 数据集 + 多层多 token 探针）"
field: [LLM agents, AI安全, 白盒探针, 欺骗检测]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-10-08"
maturity: demo
venue_tier: arXiv
reproducibility_level: medium
signal:
  venue: "arXiv"
  stars: 1
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 安全赛道的代差级演示：官方推理代码（probe-inference，MIT）+ HF 上 36 个训练好的探针（9 个模型家族：Qwen3.5/Nemotron-3/Kimi K3 变体）+ FIBSv1 数据集全开放，把转录文本的残差流直接打成分数即可现场可视化『探针实时抓 agent 欺骗』——SHADE-Arena 98.8% AUC 超过 Opus 5.5 文本监控基线，且能抓文本层看不见的『未言明欺骗』（内省欺骗场景区分真实隐藏目标 AUC 至 99.7%），比赛场上清一色的『我们做了行为审计/输出过滤』高一个技术层级"
    reuse_cost: 中
    open_source: "https://github.com/AlignmentResearch/caught-in-the-act-probes（MIT，推理代码）+ HF: AlignmentResearch/probe-inference-weights 与 AlignmentResearch/fibs-v1"
  - track: "双创-文书与申报"
    edge: "AI 治理/可信 agent 产品申报的实证背书：『行为级审计不够、需白盒监控』有对照数据支撑（98.8% AUC vs 最强文本监控基线；模型越强探针越准，直接回应『更强模型更需要白盒监控』的申报叙事）；做自动化运营/交易/办公 agent 产品的团队可把『基于迄今最大欺骗数据集 FIBS 训练的监控模块』写进可信架构章节，探针分数作为可解释风险指标天然适合监管沟通"
    reuse_cost: 中
    open_source: "https://huggingface.co/AlignmentResearch/fibs-v1（152,980 训练行欺骗数据集，MIT）"
sources:
  - url: https://arxiv.org/abs/2610.12445
    title: "Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception（arXiv abs 页，v1 2026-10-08，Oskar J. Hollinsworth/Alex F. Spies/Tigist Diriba/Adam Gleave/Chris Cundy，11 页正文共 98 页）"
    accessed: "2026-10-10"
  - url: https://github.com/AlignmentResearch/caught-in-the-act-probes
    title: "AlignmentResearch/caught-in-the-act-probes — 官方推理代码仓 README 实抓（4 commits，1 star，MIT，2026-10-10 快照）"
    accessed: "2026-10-10"
---

# Caught in the Act：白盒探针规模化了前沿 LLM 欺骗监控（FAR AI 系）

> 来源：https://arxiv.org/abs/2610.12445 （v1 提交 2026-10-08，cs.LG 主分类；作者 Oskar J. Hollinsworth、Alex F. Spies、Tigist Diriba、Adam Gleave、Chris Cundy，abs 页未列机构，官方仓在 AlignmentResearch 组织下）+ https://github.com/AlignmentResearch/caught-in-the-act-probes （README，2026-10-10 实抓）。本卡内容出自本次抓取的 abs 页与官方仓 README，未读 98 页全文。

## 是什么

arXiv 2610.12445 把**白盒探针欺骗检测**推到前沿模型监控的规模（摘要页口径）：构建"迄今最大的欺骗数据集"训练探针，并引入可在**多层多 token 间聚合信息**的新探针架构。核心结果（摘要自报）：

- SHADE-Arena 上探针达 **98.8% AUC**，超过 Opus 5.5 文本监控基线；
- **底模越强探针越准**（随被测模型规模提升）；
- "内省式欺骗"场景（仅凭上下文无法判定欺骗）中，探针区分模型**真实隐藏目标与其他目标**的 AUC 最高 **99.7%**；
- 检出显著开源权重模型在政治敏感话题与施压情境下关于信念的欺骗；
- 训练数据集以 **FIBS** 名义开源，鼓励社区扩展。

官方仓库（AlignmentResearch/caught-in-the-act-probes，2026-10-10 实抓 README）提供**四种探针架构的推理代码**（linear/MLP/EFC 早融合协方差/axial）：加载训练好的探针（本地或 HF），对转录文本的残差流激活打分，每条转录一个分数。仅 torch 为必装依赖，单测含 CPU 合成探针与参考分数奇偶校验。**HF 资产**：36 个训练好的探针权重覆盖 9 个模型（Qwen3.5 变体、Nemotron-3 变体、Kimi K3）、FIBSv1 训练数据集（152,980 训练行）、约 150 MiB 奇偶校验夹具；代码与权重均 MIT。训练超参在 README 有描述（seed 0、至多 4-6 epoch 早停）但**训练管线未随仓释出**。

## 解决什么问题

LLM agent 监控目前主流靠文本行为审计，但模型可以**不说出来地骗**——摘要的"unverbalized deception"即：上下文层面无法判定、只有模型内部状态知道的欺骗（内省式欺骗场景）。白盒探针读残差流，把监控从"看它说了什么"升级到"看它内部在想什么"，并首次做到前沿监控所需的规模与跨层聚合架构。

## 相比前方法优势

- **规模**：最大欺骗数据集（FIBSv1 152,980 训练行）+ 多层多 token 聚合架构，区别于以往单层/小规模探针研究；
- **有对照组**：98.8% vs Opus 5.5 文本监控，把"白盒优于黑盒审计"从直觉变成可比数字；
- **反直觉且重要**：探针随底模规模提升——与"更强模型更难监控"的担忧相反，模型越强内部信号越可读，对 agent 产品监控路线是利好论据；
- **开源完整度高于均值**：推理代码 + 36 个现成权重 + 数据集 + 校验夹具全 MIT，接入即用（复训需自建管线）。

## 局限（如实标注）

- 训练管线未释出：仓库仅推理代码，换底模/换域需自行复现训练流程（数据集已开源，可重建但非一键）；
- 现成探针只覆盖 9 个模型家族（Qwen3.5/Nemotron-3/Kimi K3 变体），不在列的模型需重训探针；
- 所有 AUC 数字为作者自报（v1 预印本，无 venue），98 页附录未逐项核验；SHADE-Arena/内省欺骗的实验设计细节未读全文前不背书；
- 官方仓仅 1 star/4 commits（2026-10-10 快照），发布极新，生态与第三方复现均为零；
- 探针检测的是"欺骗信号"，对良性误报率（false positive 代价）的部署权衡需读全文评估。

## 如何用于比赛（比赛映射展开）

1. **黑客松-数据与算法（agent 安全覆盖）**：现场演示设计——agent 完成多步任务时同步流式打探针分，仪表盘实时显示"文本层一切正常 / 探针分飙升"的背离时刻，直观展示"模型嘴上一套、内部另一套"；用官方权重 + probe-inference（只依赖 torch）即可对支持模型出分，比自建监控管线的工程量小一个量级。reuse_cost 中：推理接入不难，但需目标模型的残差流访问权（开源权重模型本地跑即可）+ 一块 GPU；FIBSv1 可用于微调自己的探针作为赛题内的技术增量点。
2. **双创-文书与申报（AI 治理/可信 agent）**：申报书可信架构章节的两个可引论据——其一，"行为审计可被未言明欺骗绕过，白盒监控不可替代"（98.8% vs 文本监控基线的对照数字，注明作者自报）；其二，"模型越强内部信号越可读"支撑"随模型升级监控不失效"的产品主张。以 FIBS 为基座训练领域探针（如金融合规话术监控）可作为申报项目的技术路线图（reuse_cost 中：需把通用欺骗探针转译为业务域叙事，代码与数据现成）。
