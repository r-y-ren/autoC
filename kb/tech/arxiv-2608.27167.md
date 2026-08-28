---
id: arxiv-2608.27167
name: "Calibrated Enough to Know, Not Calibrated to Act: Fabricated Evidence Makes LLM Agents Commit to the Unknowable"
field: [LLM agents, 校准与可信性, 评测方法]
directions: [黑客松与数据竞赛]
published: "2026-08-27"
maturity: paper
signal:
  venue: "arXiv"
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "可信 AI 赛道的差异化组件『act/don't-act 门控』：权威外观的证据面板（哪怕数字全伪造）把 12 个前沿模型对可证明不可知问题的承诺率从 6.5% 推到 54.0%，伪造面板 36.8% vs 真实数据 37.6% 统计不可区分——『解锁行动的不是信息而是包装的权威性』。作品形态一：决策 agent 前置知道性门控（3B 模型 540 条合成案例 SFT 即得原案例 0.0% 承诺并跨域迁移）；形态二：伪造证据金丝雀压测套件，可给任意 RAG/agent 产品做包装诱导审计。代码/数据/预注册/缓存输出全开源，评估侧零 GPU 可复算，答辩可现场重跑"
    reuse_cost: 低
    open_source: "https://github.com/Pranav-1100/confidence-calibration-evaluation"
sources:
  - url: https://arxiv.org/abs/2608.27167
    title: "Calibrated Enough to Know, Not Calibrated to Act: Fabricated Evidence Makes LLM Agents Commit to the Unknowable"
    accessed: "2026-08-28"
  - url: https://github.com/Pranav-1100/confidence-calibration-evaluation
    title: "论文配套代码与数据仓（master 分支实抓核实：data/ 含全部数字背后的缓存输出与评测案例集，PREREGISTRATION.md，scripts/v2 图表复算脚本；star=0，pushed 2026-08-27）"
    accessed: "2026-08-28"
---

# 伪造证据让 LLM 智能体对不可知问题做出承诺：行动门控失败与训练修补

> 来源：https://arxiv.org/abs/2608.27167 （arXiv v1 提交于 2026-08-27，cs.AI 跨 cs.CL，comments: 28 pages, 6 figures，代码/数据/预注册/缓存模型输出开源；单作者 Pranav Aggarwal；抓取日期 2026-08-28）

## 是什么

arXiv 2608.27167 研究"权威外观的证据包装"如何诱发 LLM agent 对**可证明不可预测问题**的方向性承诺（以下描述均来自本次抓取的摘要页与配套仓库 README）：

- **主效应**：12 个前沿模型上，随证据升级（裸问题 → 专业外观市场面板），承诺率从 **6.5% 升至 54.0%**；把面板**整体伪造**（可见数字全假）承诺率仍 24.5%→36.8%，与真实市场数据的 37.6% **统计不可区分**——"解锁自信行动的不是信息，而是包装的权威性"；
- **失败被干净隔离**：同批可答问题近乎全对（排除无能）；陈述概率在证据梯度上几乎不动且比气候学基线更差（AUROC 0.346，排除信念改变）；90% 的情况模型能正确判断问题不可约**却仍行动**——坏的是 **act/don't-act 门**，且效应集中于少数模型；
- **训练修补**：3B 模型在 **540 条合成案例**（骰子/硬币/罐子/计时器）上 SFT，原案例承诺率降到 **0.0%** 并迁移到三个未见域；但门控只在响应格式留有推理空间时稳定，刚性格式下模型"自信且错误"——"门可训练且上下文脆弱"；
- **工件**（GitHub master 分支 2026-08-28 实抓核实）：data/ 含"每个数字背后的全部缓存模型输出+评测案例集"（12 模型×4 域、4 种打乱面板构造含全伪造臂、密度剂量反应、11 个训练 checkpoint 生成等）；README 明言全部结果"无需 API 调用或 GPU 时长"即可复算（装 markdown+matplotlib 跑两个脚本）；PREREGISTRATION.md 为确认性实验前的预注册。

## 解决什么问题

校准研究只测模型"知不知道"（信念与答案的对齐），没测"该不该动手"（在证据不支持行动时拒绝行动）。该工作把 LLM agent 的**过度承诺**从能力/信念中解耦出来，定位为一个独立的、可训练的**行动门控**失效。

## 相比前方法优势

- 实验设计三重解耦（可答对照/概率梯度/可知性分类），把"承诺行为"与"信念改变"分离——比常规校准评测多切一层；
- **伪造证据臂**直接证伪"内容驱动行动"：全假面板与真数据诱导等量承诺；
- 给出极低成本的修补证据链：540 条合成案例 SFT 即可迁移跨域，且诚实报告修补的边界（格式脆弱）；
- 工件完整度罕见：预注册+原始缓存输出+零 GPU 复算脚本，全部数字可审计。

## 局限

- v1 单作者预印本、无 venue，结论待同行评审；repo star=0（2026-08-27 刚随论文推送）；
- **门控训练代码不在发布仓**：README 明言训练代码/checkpoint 评测脚本/Kaggle notebook 在另一工作仓的 RL_env/ 目录，本仓只含其产出的缓存生成——复现 SFT 需另寻该仓或按论文自写（540 案例量级小，自写可行）；
- "门控上下文脆弱"意味着产品集成须保留推理空间的响应格式，工程上有约束；
- 效应集中于 12 模型中的少数，跨模型族泛化面待验；
- arXiv comments 与 README 所记 Zenodo DOI 不一致（22043517 vs 21325375，疑为版本记录差异），存档引用以 GitHub 仓为准。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松数据与算法题中的可信 AI / AI 安全 / 金融科技决策赛道；亦有"AI 可信治理"方向的双创/大创申报叙事空间（文书层面另议，本卡以赛技映射为主）。
- **形态一：知道性门控 agent**——在任意决策/RAG agent 前加一层"该不该行动"门（开源 3B SFT 配方，540 合成案例），现场演示：同一 agent 面对伪造权威面板，无门 54% 承诺、有门拒绝行动。
- **形态二：伪造证据金丝雀压测套件**——借其面板构造（真实/打乱/全伪造臂+密度梯度）给任意 RAG/agent 产品做"包装诱导承诺"审计，输出承诺率剂量反应曲线；此类压测工具在可信 AI 赛道是稀缺品类。
- **成本**：reuse_cost=低——代码+数据+预注册全开源，评估侧零 GPU 复算（答辩可现场重跑出全部图）；训练侧 540 案例的 3B SFT 为单卡小时级，训练代码需按论文自写或另寻 RL_env 仓。
