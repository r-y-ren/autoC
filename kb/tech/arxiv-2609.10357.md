---
id: arxiv-2609.10357
name: "tsfm-bench：TSFM 的领域熟悉度陷阱（时间hold-out除不掉预训练记忆）"
field: [时序基础模型, 评测方法学, 数据污染]
directions: [数模与时序预测]
published: "2026-09-09"
maturity: paper
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "arXiv（Comments：11 pages；代码+数据抓取器 github.com/mahdinaser/tsfm-bench）+ GitHub 实抓（0 stars，license NOASSERTION，2026-09-20 API）"
  stars: 0
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "TSFM 选型的纪律性检查表：核心结论『时间 hold-out 只能去除窗口记忆、去不掉领域熟悉度』——TimesFM 在 Wikipedia 域以 28% MASE 优势胜出，恰因其预训练主域就是 Wikipedia；赛队选型时第一问应从『哪个榜分高』换成『赛题数据域是否在模型预训练语料里』，避免把语料红利误当泛化能力写进论文；其 13 模型×7 域协议 + 无 API key 可重建的数据抓取器可低成本改造成赛内自评 harness"
    reuse_cost: 低
    open_source: "https://github.com/mahdinaser/tsfm-bench（代码+数据抓取器+逐序列结果，论文 comment 自述；license NOASSERTION 需复核）"
  - track: "Kaggle-竞赛"
    edge: "公共榜/NLB 换届题的防幻觉镜：榜上强 ≠ 域外强，自建 validation 时按其协议补一组『域熟悉度对照』（近域 vs 远域子集）能提前暴露过拟合叙事；负面结论『季节强度/谱熵预测不了 TSFM 优势』直接否掉一类常见特征归因写法"
    reuse_cost: 低
    open_source: "https://github.com/mahdinaser/tsfm-bench"
sources:
  - url: https://arxiv.org/abs/2609.10357
    title: "A Later Test Set Is Not a New Domain: Pretraining Familiarity Survives a Contamination-Free Hold-Out（arXiv export API 实抓：2026-09-09，Comments『11 pages, 2 figures, 5 tables. Code, data fetchers and per-series results: github.com/mahdinaser/tsfm-bench』；13 预测器×7 域、TimesFM-Wikipedia 28% MASE、-0.53 vs -0.09 排名差、Mann-Whitney p<1e-5 等均出自摘要原文）"
    accessed: "2026-09-20"
  - url: https://github.com/mahdinaser/tsfm-bench
    title: "mahdinaser/tsfm-bench 仓库实抓（GitHub API 2026-09-20：0 stars，license NOASSERTION，描述『Contamination-free benchmark for time-series foundation models』）"
    accessed: "2026-09-20"
---

# A Later Test Set Is Not a New Domain：TSFM 选型要问"它是不是在这个域里长大的"

> 来源：https://arxiv.org/abs/2609.10357 （arXiv export API 实抓，抓取日期 2026-09-20；代码仓 GitHub API 同日实抓。以下分析基于本次抓取的摘要原文）

## 是什么

针对 TSFM 评测污染的对照研究（摘要口径）：TSFM 几乎都在早于其发布的公共档案上评测，强分数无法与"预训练时见过测试集"区分。作者构造了真正干净的 hold-out——13 个预测器（4 经典 + 3 逐数据集训练 + 6 预训练）× 7 组数据（5 个域），**每条观测都发布于最后一个模型发布之后**，且每个数据集无需 API key 即可重建。结果：预训练模型 7 组胜 5 组，但输一组给 Theta 基线，在日频汇率上与 seasonal naive 及其他所有方法不可区分。进一步追问胜负规律得到负面结果：输入窗的季节强度与谱熵解释不了胜负格局（季节强度甚至负相关）。真正解释胜负的是**语料熟悉度**：最大优势（周频 Wikipedia 页面浏览量上 MASE 比最强经典方法低 28%）恰落在 TimesFM 作者自述的预训练主域 Wikipedia，且同粒度仅时间窗不同；预训练模型家族内（序列相同、难度抵消），TimesFM 家族对 Chronos 家族的排名差在 Wikipedia 为 -0.53、其他域仅 -0.09（Mann-Whitney p < 1e-5）。结论：时间 hold-out 去除的是窗口记忆、保留的是领域熟悉度；基准应声明相对于已披露语料的"域 hold-out"；实践者的问题不是"哪个模型更好"而是"我的域是否是它长大的域"。

## 解决什么问题

TSFM 评测的两个盲区：公共基准预训练可见（记忆污染），以及换新时间窗后仍残留的域熟悉度被误读为泛化。给出可复建的干净协议与归因方法。

## 相比前方法优势

- **协议设计干净**：全部观测后于模型发布 + 无 key 可重建——可被任何人复验，不是又一份"跑跑现成榜"；
- **归因有统计证据**而非轶事：家族内对照设计让序列难度自然抵消，p<1e-5 的排名差直指语料因素；
- **诚实的双重负面结果**：既打"预训练模型万能"（汇率上不敌 naive），也打"用内在性质预测适用性"（季节强度/谱熵失效）——负面结论同样可操作。

## 局限

- 代码仓 0 stars、license NOASSERTION（2026-09-20 API 实抓）——单人研究仓，工程成熟度低，直接依赖前需复核许可与数据抓取器可运行性；
- 覆盖 5 域 7 组，域样本量小，"熟悉度解释"在未测域的外推需谨慎；
- 对闭源 TSFM（语料不披露）无法事前检验熟悉度——这恰是其论点，但对赛队意味着该检查只能事后做；
- 本卡止于摘要层。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：数模-预测与评估（所有考虑用 TSFM 零样本的题）；Kaggle-竞赛（时序赛模型选型与 validation 设计）。
- **打法**：
  (a) **选型三问**：赛题数据域是否在候选 TSFM 的公开语料里（Power/Weather/Traffic 高频域通常在）？hold-out 是否只换了时间窗没换域？naive 基线是否跑过（汇率类赛题先跑 naive 防白干）？
  (b) **改造其 harness**：tsfm-bench 的数据抓取器无需 API key，取其协议做赛内"近域/远域"两组自评，论文里多一张"域熟悉度对照表"是稀缺的严谨性信号；
  (c) **写作弹药**：直接引用其"28% MASE 优势 = 语料红利"案例，论证为何我们报告多域平均而非单域最优。
- **成本**：reuse_cost=低——代码与抓取器可得；主要成本是读协议并裁剪到赛题域。
