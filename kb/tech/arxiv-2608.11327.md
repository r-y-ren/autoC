---
id: arxiv-2608.11327
name: "Long-Horizon Forecasting of Complete Financial Statements with Forma"
field: [金融时序预测, 财务报表建模, 机器学习]
directions: [数模与时序预测]
published: "2026-08-11"
maturity: paper
signal:
  venue: arXiv
  runnable: true
competition_fit:
  - track: "数模-数据分析与决策"
    edge: "财务/估值类赛题（DCF、盈利预测）把 Forma 当'财务假设引擎'：开箱输出 1-20 季 78 个报表科目的联合概率预测，自带会计恒等式近勾稽与'钉住收入路径→锐化其余科目'的场景分析接口，直接支撑估值模型假设层与敏感性分析；其 change-space R²（在变化空间评分）思想可平移为答卷评估设计——预测变化率而非水平值，规避水平值惯性陷阱"
    reuse_cost: "中"
    open_source: "https://github.com/forma-lab-mccombs/forma-release（模型+竞赛代码 Apache-2.0，权重在 Hugging Face 为非商业许可）+ https://github.com/forma-lab-mccombs/proforma-20q（基准仓，Apache-2.0；均 2026-08-28 实抓核验存在）"
  - track: "双创-文书与申报"
    edge: "商业计划书财务预测章节：以同业公司历史报表为基底生成 3-5 年联动报表预测，科目间自动勾稽 + 不确定性区间，比手工 Excel 假设表多出'一致性 + 区间论证'两个维度；但必须如实标注两条硬限制——权重非商业许可、新创企业无历史报表需同业代理（论文未验证此用法）"
    reuse_cost: "中"
sources:
  - url: https://arxiv.org/abs/2608.11327
    title: "Long-Horizon Forecasting of Complete Financial Statements with Forma (arXiv:2608.11327)"
    accessed: "2026-08-28"
  - url: https://github.com/forma-lab-mccombs/forma-release
    title: "forma-lab-mccombs/forma-release——Forma 模型与权重发布仓（仓库描述注明权重非商业许可；2026-08-28 gh api 实抓核验）"
    accessed: "2026-08-28"
  - url: https://github.com/forma-lab-mccombs/proforma-20q
    title: "forma-lab-mccombs/proforma-20q——ProForma-20Q 基准仓（Apache-2.0，2026-08-28 gh api 实抓核验）"
    accessed: "2026-08-28"
---

# Forma：完整财务报表的长时程联合预测

## 是什么

Johnson 等 6 人（2026-08-11 提交 arXiv:2608.11327，cs.LG + q-fin.CP，46 页）发布两件东西：**ProForma-20Q**——可复现基准，对匿名公司联合预测 78 个报表科目、1-20 季前瞻，输入为历史报表 + 行业代码，以变化空间 R²（change-space R²）评分；**Forma**——把报表读作（科目， 季度， 数值）元组集合的 Transformer，以 masked-tuple 高斯似然训练。模型与权重、基准代码均已放出（arXiv Comments 链接 2026-08-28 实抓核验两仓均存在，signal.runnable 记 true）。

## 解决什么问题

此前没有工作联合预测"完整报表"超过一年，而 DCF 估值中大部分企业价值恰好落在一年之后；论文的核心主张是"**专才训练胜过通才规模**"（specialist training beats generalist scale）。

## 相比前方法优势（论文实证结论）

- 完胜经典 ML、链式梯度提升、零样本时序基础模型与前沿 LLM，且**时域越长优势越大**；
- 高斯预测区间"从不低估覆盖率"（never under-cover）；预测近满足会计恒等式，且可以不显著损失精度恢复精确勾稽一致；
- 元组接口**免重训做场景分析**：钉住未来收入路径即可锐化报表其余科目——敏感性分析的天然接口。

## 局限（如实标注）

- **数据可得性硬约束**：基准为匿名公司，无法与真实证券代码/公司数据 join；赛题若给真实公司报表，需自建映射或只把 Forma 作方法参考；
- **权重非商业许可**（forma-release 仓库描述注明 trained weights on Hugging Face under a non-commercial licence；代码 Apache-2.0）：数模/黑客松非商业场景一般可用，双创商业化路径需重训或仅作方法论引用；
- 训练语料为美股季报口径，对 A 股/中小企业报表的迁移未在摘要中验证；
- 双创场景的新创企业无历史报表，"同业公司报表作基底"的代理用法论文未验证，属赛队自担风险的外推，卡片如实标注不拔高；
- 性能结论仅在其基准成立，引用须注明出处。

## 如何用于比赛

1. **财务/估值类数模题（数模-数据分析与决策，主用）**：DCF/盈利预测题将 Forma 作为财务假设引擎——1-20 季 78 科目联合预测 + 区间输出，场景钉住接口直接做敏感性分析；change-space R² 平移为答卷评估设计（在变化空间评分，避免"只会预测水平值惯性"的低分陷阱）。
2. **商业计划书财务章节（双创-文书与申报）**：以同业历史报表为基底生成 3-5 年联动预测，科目自动勾稽 + 不确定性区间，比手工假设表多"一致性论证"维度（必须标注非商业许可与同业代理两条局限）。
3. **多维联动长时程外推的方法论借鉴**：不靠链式单科目递推，而用联合分布保持科目间相关性——该思想可平移到任何"多维联动长时程预测"赛题（多区域负荷-经济变量联动等），即使不用其权重也可复用其建模范式。
