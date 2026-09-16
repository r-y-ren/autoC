---
id: arxiv-2609.13789
name: "PPDL：Weibull 物理先验×深度学习的工业用户留存率预测（ICDM 2026）"
field: [时序预测, 用户留存, 机理数据混合建模]
directions: [数模与时序预测]
published: "2026-09-12"
maturity: paper
signal:
  venue: "arXiv（Comments: Accepted by ICDM 2026）"
  stars: 0
  runnable: false
competition_fit:
  - track: "Kaggle-竞赛"
    edge: "churn/retention 类表格时序赛的『短观察窗→长周期预测』标配结构：赛题只给前 7 天行为要预测 30/60 天留存时，套『参数化趋势（Weibull）+残差网络+多尺度趋势惩罚损失』三段式，外推有形状约束兜底，比裸 LSTM/GBM 多出结构性答辩点；趋势惩罚损失是任何 backbone 可叠加的轻量组件"
    reuse_cost: 中
  - track: "数模-数据分析与决策"
    edge: "渠道级留存预测→预算分配的完整决策链路贴合用户增长/运营优化类赛题：Weibull 衰减-饱和先验给出可解释拟合曲线与参数含义插图，正是机理+数据混合建模的加分写法；渠道身份辅助嵌入对应分组异质性处理"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2609.13789
    title: "PPDL: A Real-world Industrial User Retention Ratio Forecasting Framework Integrating Physical Priors with Deep Learning（arXiv 摘要页实抓：v1 2026-09-12，Comments 'Accepted by ICDM 2026'，cs.LG，无代码链接）"
    accessed: "2026-09-16"
---

# PPDL：物理先验（Weibull 衰减-饱和）×深度学习的工业用户留存率预测

> 来源：https://arxiv.org/abs/2609.13789 （arXiv 摘要页实抓，抓取日期 2026-09-16；v1 2026-09-12，作者 Zibo Zhao、Zhengxiong Guan、Chaoli Zhang、Linyuan Geng、Xuanbing Zhu、Zhonglong Zheng、Fan Wu；Comments "Accepted by ICDM 2026"；以下分析均基于本次抓取的摘要页内容）

## 是什么

多渠道付费获客场景下的**渠道级用户留存率早期预测**框架，服务于买量预算分配优化。三件组件（摘要口径）：

1. **趋势-残差分解**：留存曲线"先高流失后长期稳定 + 季节波动"的宏观形态用 **Weibull 分布建模趋势、参数由 MLP 学习**，残差交给深度学习骨干；
2. **渠道身份辅助嵌入模块**：在深度骨干上加辅助嵌入，防止残差建模丢失渠道异质性（channel identity awareness）；
3. **多尺度趋势惩罚损失**（Multiscale Trend-penalized loss）：放大模型对趋势的敏感度。

工业验证：覆盖 3 个应用、平均每应用 30+ 渠道的大规模数据；跨不同骨干均有提升，自称显著优于现有在线方案（"significantly outperforms existing online solutions"）。

## 解决什么问题

渠道级留存的早期准确预测决定预算往哪个渠道投。摘要列出三重难点：**渠道异质性**（各渠道曲线形态不同）、**全局衰减-饱和趋势**（先高 churn 后稳定的共同形态）、**观察窗短**（上线初期就得给出预测）——纯深度模型在短窗下趋势学不稳，纯机理模型刻不动渠道差异。

## 相比前方法优势

- **机理与数据分工明确**：Weibull 先验把"衰减-饱和"的结构性知识固化在趋势项，DL 只学残差——短观察窗下外推行为有物理形状约束兜底；
- **趋势惩罚损失可移植**：轻量损失设计，与任何 backbone 正交叠加；
- **有真实工业规模验证与 venue 背书**：3 应用 × 30+ 渠道的实际部署数据（摘要口径）+ ICDM 2026 接收——非纯基准刷子。

## 局限

- **无代码发布**（摘要页无任何链接，2026-09-16 实抓）：Weibull-MLP 趋势项、辅助嵌入与损失的细节需按正文自实现；
- **场景绑定付费投放**：Weibull 形态先验是否迁移到非买量场景（学生留存、设备活跃留存等）需自行验证，不能默认成立；
- 摘要未披露相对基线的具体提升数字（只有定性"significantly outperforms"），定量口径须读正文核对后才能引用；
- "在线方案"对比对象与评测协议在摘要层不可见。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：Kaggle-竞赛（churn/retention 类表格时序赛高频题型）；数模-数据分析与决策（用户增长、运营优化、渠道预算分配类赛题）；黑客松-数据与算法的风控/运营题同型。
- **打法**：
  (a) **短窗长预测标配结构**：赛题只给前期行为要求远期留存时，直接套"参数化趋势 + 残差网络 + 趋势惩罚损失"三段式——外推段有形状约束是裸 LSTM/GBM 写不出的答辩点；
  (b) **数模论文叙事**：Weibull 衰减-饱和拟合曲线与参数含义天然构成可解释性插图，机理+数据混合建模是评审加分写法；渠道身份辅助嵌入对应赛题的分组异质性处理章节；
  (c) **决策链路闭环**：渠道级留存预测输出直接接预算分配优化（留存率→LTV 估计→分配方案），"预测→决策"完整链路正是数据分析与决策类赛题的评分结构。
- **成本**：reuse_cost=中——无代码，但损失函数与分解结构一天级可自实现，backbone 自备；主要工作量在趋势项与损失的正文中细节核对。
