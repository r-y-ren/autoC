---
id: arxiv-2609.02093
name: "Compositional Spectral Prompts for LLM-based Online Time Series Forecasting"
field: [时序预测, LLM, 在线学习, 频域提示]
directions: [数模与时序预测]
published: "2026-09-02"
maturity: paper
signal:
  venue: "arXiv (Comments: CIKM 2026)"
  stars: 1
  runnable: true
competition_fit:
  - track: "数模-预测与评估"
    edge: "非平稳/在线预测题的免训练适配方案：冻结预训练 LLM 作在线预测器，时序分解为频率基、按幅值组合出谱基提示，未见模式=已学基提示的新组合，在线期只更新提示参数——正对'数据分布随时间漂移'与'目标域历史数据少'（跨数据集设置下 ETTh1 训练迁移 ETTh2/ETTm1 这类实质分布漂移仍可用）两类赛题形态；CIKM 2026 接收 + 官方代码可跑"
    reuse_cost: "高"
  - track: "Kaggle-竞赛"
    edge: "在线/滚动评测赛（rolling leaderboard）的'冻结基座+轻量在线适配'路线：相比 memory-buffer 检索式在线方法长程适应更稳、对未见模式泛化更好；但每步 LLM 推理成本与算力依赖在赛期内必须权衡，官方仓无 license 声明，商赛需自查合规"
    reuse_cost: "高"
sources:
  - url: https://arxiv.org/abs/2609.02093
    title: "CoSPOT (arXiv:2609.02093) 摘要页，Choi 等 4 人"
    accessed: "2026-09-04"
  - url: https://export.arxiv.org/api/query?id_list=2609.02093
    title: "arXiv API 元数据实抓（Comments: CIKM 2026；摘要内代码链接）"
    accessed: "2026-09-04"
  - url: https://github.com/seungyoon-Choi/CoSPOT
    title: "官方代码仓（Python，1 star，无 license，2026-09-04 api.github.com 实抓核验存在）"
    accessed: "2026-09-04"
---

# CoSPOT：冻结 LLM + 组合式频域提示的在线时序预测

## 是什么

Choi 等 4 人（KAII/KAIST 系，2026-09-02 提交 arXiv:2609.02093，Comments 标注 CIKM 2026）提出 LLM-based 在线时序预测（OTSF）框架（摘要页+API 元数据 2026-09-04 实抓）：以预训练 LLM 为冻结在线预测器，把输入时序分解为频率基，按各分量幅值组合出谱基提示（spectral basis prompts）引导模型捕捉输入整体分布；在线适配只更新提示参数。未见模式被表示为已学基提示的新组合。**官方代码 https://github.com/seungyoon-Choi/CoSPOT 已核验存在（Python，1 star，无 license，最后推送 2026-05-23），runnable=true**。

## 解决什么问题

现有在线时序预测靠记忆缓冲检索策略适应非平稳环境，但作者观察到这类框架**长程适应乏力、对未见模式无法泛化**；LLM 的少样本能力是替代基座的动机，但全参在线更新不可行。

## 相比前方法优势（论文实证结论）

- 冻结 LLM + 仅调提示，大幅减少在线阶段更新参数量；
- 频域基的组合式提示让未见模式有表示路径（基组合而非记忆检索）；
- 真实数据集上在扩展在线阶段（extended online phases）与实质分布漂移的跨数据集设置（如 ETTh1 训练迁移 ETTh2/ETTm1，arXiv 页面文本 2026-09-04 实抓）均显示优势与实用性。

## 局限（如实标注）

- LLM 基座推理成本高，在线逐步调用对赛期算力/时延敏感；
- 官方仓 1 star、无 license 声明，社区验证少；最后推送早于论文挂网（2026-05-23），代码与论文版本对应关系需自行确认；
- CIKM 2026 尚未正式出版，结论以预印本为准；频域分解依赖输入窗口的谱结构，超低采样/强非周期流未验证。

## 如何用于比赛

1. **非平稳流预测题（数模-预测与评估，主用）**：'分布随时间漂移''历史数据有限'类赛题（如滚动负荷、指标漂移）以 CoSPOT 为在线适配基线或方案骨架——冻结基座 + 频域提示轻调，跨数据集设置的结果支撑'目标域历史少'论证；
2. **在线赛 / 滚动评测（Kaggle-竞赛）**：与 memory-buffer 检索式在线方法（如 OFA 类）对照选型，CoSPOT 主打长程适应与未见模式泛化；每步推理成本需折算进赛期预算；
3. **方法迁移**：谱基提示的'未见模式=基组合'思想可平移到任何需要轻量在线适配的预测管线（未必用 LLM）。
