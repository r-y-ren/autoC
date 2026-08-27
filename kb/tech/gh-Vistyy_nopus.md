---
id: gh-Vistyy_nopus
name: "nopus: 编码 agent 回复的确定性散文质量门"
field: [LLM agents, 输出质量评测]
directions: [黑客松与数据竞赛]
published: "2026-08-15"
maturity: demo
signal:
  venue: GitHub
  stars: 240
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "'LLM 输出质量/可观测性'类黑客松题的现成组件：不调 LLM、纯确定性度量（SUBTLEX 词频 + Brysbaert 具体性评分 + 名词堆叠密度 + 风格线索白名单）判定回复是否陷入抽象空话，超阈值经 Stop 钩子触发至多一次重写——零额外推理成本、可复现的质量门控，且附 5,337 条真实响应标定的灵敏度-重写率曲线（low 5.3%/medium 9.9%/high 18.6%），评测章节素材现成"
    reuse_cost: "低"
    open_source: "https://github.com/Vistyy/nopus（MIT，npm @syzom/nopus 1.1.0）"
sources:
  - url: https://github.com/Vistyy/nopus
    title: "Vistyy/nopus: Deterministic prose checks for clearer coding-agent responses"
    accessed: "2026-08-28"
---

# nopus：用确定性文本度量拦截 coding agent 的"LLM 腔"回复

## 是什么

Vistyy 2026-08-15 发布的 TypeScript 工具（npm @syzom/nopus 1.1.0，MIT，registry 实查 2026-08-28），以 Pi 扩展 / Claude Code 插件 / Codex 插件三种宿主形态安装。机制：coding agent 每次回复完成后，先剥除代码块/行内码/URL/路径/表格行，再测七类确定性指标——生僻词与超生僻词（SUBTLEX-US 会话词频 + Norvig 万亿词级网络词频打包成 JSON）、抽象词汇与跨句抽象（Brysbaert 40k 词具体性人工评分）、名词/修饰语三连堆叠、稠密短语负载、程式化风格线索（claudisms 白名单，如 here's where it gets interesting）；多指标同时越限才触发，经 Stop 钩子向 agent 发一条带原回复例证的定向重写请求，**至多重写一次**（防重试环）。数据集全部 checksum 锁源（README 附 SHA-256 与许可文件，抓取 2026-08-28）。

## 解决什么问题

coding agent 回复滑向抽象 LLM 空话（capability/strategy/governance 堆叠、"repository state mutation verification strategy"式名词串），人读着累且关键结论被淹没；用 LLM 评 LLM 又贵又不可复现。

## 相比前方法优势

- **确定性 = 可复现**：同一散文 + 同一灵敏度必然同一判定，无采样抖动；
- **零推理成本**：纯本地数据查询，对比 LLM-as-judge 每次评审都烧 token；
- **工程细节扎实**：技术术语经 Glosario 计算术语表降权（InteractiveSessionHost 不误伤）、按比例而非绝对计数（长回复不吃亏）、单指标不触发、至多一次重写；5,337 条真实 Pi 响应标定出三档灵敏度的实测重写率。

## 局限（如实标注）

- **仅英文**：词频/具体性/术语数据全为英文语料，中文或中英混排回复不适用——对本团队中文文书类赛题无用；
- 仓库 2026-08-15 创建、最后推送 2026-08-19，此后再无更新（API 实查 2026-08-28），维护活跃度待观察；
- 宿主面窄（Pi/Claude Code/Codex 三家），接到自研 agent 需自行对接其判定库；
- 度量的是"可读性/具体性"而非"正确性"——不能当正确性门控用。

## 如何用于比赛

1. **Agent 质量工具类黑客松（主用）**：题面是"agent 可观测/输出治理/AI 辅助开发工具"时，nopus 作质量门组件：确定性评分器（cheap、reproducible）+ 单次重写闭环的完整故事，配上自带的标定数据与重写率曲线，答辩有数字有方法。reuse_cost 低：npm/插件一行安装。
2. **方法论迁移**：其"打包词频+具体性评分做本地文本度量"的套路可移植成中文版（配中文词频库与具体性词典），用于自研 agent 的输出治理——工作量集中在数据层，判定逻辑可复用设计。
3. 边界提醒：不要把它包装成"正确性验证"——卡片局限已注明它只管可读性，赛题方案里越界主张会被评审戳穿。
