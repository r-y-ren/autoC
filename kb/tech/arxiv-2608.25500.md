---
id: arxiv-2608.25500
name: "CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval"
field: [LLM agents, skill library, skill retrieval]
directions: [黑客松与数据竞赛]
published: "2026-08-26"
maturity: paper
signal:
  venue: "arXiv (preprint, 11 pages)"
  stars: 0
  runnable: false
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "带技能库的 agent 作品的检索质量升级：技能库（自动沉淀的工具代码/修复例程）正在成为 agent 类作品的标配，但向量检索把技能当独立文本、错误配边当场翻车——CaSKG 用方向条件化反事实探针（移除/替换/重排技能对）+ 可选 LLM 裁判 + 贝叶斯平滑在赛前离线校准技能图因果边；六个 LLM 骨干在 ALFWorld/ScienceWorld 十二个模型-基准组合全部拿到最高任务分（对 Graph-of-Skills：ScienceWorld 六模型宏平均 72.62→80.50，ALFWorld 成功率 80.01%→86.79%，平均环境步数双双下降）；图离线构建、不改下游 agent 策略与任务接口，是可外挂组件"
    reuse_cost: 中
    open_source: "https://github.com/ZhiyuanLi218/Caskg（论文脚注给的官方仓库；2026-08-28 实抓仍为占位：仅 README 称'数日内放出代码'，0 star、无 license、无代码文件——引用前需复验）"
  - track: "Kaggle-竞赛"
    edge: "跨场次沉淀的参赛技能（特征工程配方、CV 方案、集成套路）组织为校准技能图，agent 辅助参赛时按数据集状态做任务条件化检索，取'经过验证的前置-后续技能链'而非文本相似度最近的孤立技能，减少无效尝试轮次与翻车率"
    reuse_cost: 中
sources:
  - url: https://arxiv.org/abs/2608.25500
    title: "CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval"
    accessed: "2026-08-28"
  - url: https://github.com/ZhiyuanLi218/Caskg
    title: "CaSKG 官方代码仓库（2026-08-28 实抓为占位，代码未放出）"
    accessed: "2026-08-28"
---

# CaSKG：反事实-因果校准的技能图，让 agent 技能检索可扩展

> 来源：https://arxiv.org/abs/2608.25500 （arXiv v1 提交于 2026-08-26 08:12:41 UTC，cs.AI 主分类、交叉 cs.CL；Comments 仅"11 pages"，无 venue；作者 Zhiyuan Li、Linyuan Gao、Xuechun Ding、Hongwei Chen、Yuan Wu、Yi Chang；摘要脚注给代码链接 github.com/ZhiyuanLi218/Caskg；抓取日期 2026-08-28）

## 是什么

arXiv 2608.25500 提出 CaSKG——在检索之前校准技能库中"程序性知识"之间关系的反事实-因果技能图框架，两阶段：

1. **高召回候选图构建（离线）**：综合语义、词法、输入/输出类型与结构证据建立有向候选边，再用修复证据（repair evidence）与可选的 LLM 裁判精修；
2. **反事实探针校准**：对候选边做方向条件化的文本反事实探针（移除、替换、重排技能对），证据用贝叶斯平滑聚合，发布经状态过滤的加权技能图，供任务条件化扩展检索。

关键工程属性：图完全离线构建，**不改动下游 agent 策略与任务接口**——是外挂件而非侵入式改造。

## 解决什么问题

技能库让 LLM agent 复用程序性知识（怎么建管线、怎么验证、怎么修），但库一大，记忆访问就变成困难检索问题。摘要归纳三条旧路的失败：全库塞 prompt 上下文成本高；向量检索把技能当独立文本（丢失"先 A 后 B"的依赖关系）；图检索又依赖不可靠的边。CaSKG 的答案是把边的可信度在检索前用反事实探针校准好。

## 相比前方法优势与局限

**优势**：六个 LLM 骨干在 ALFWorld ID-140 与 ScienceWorld U211 的十二个模型-基准组合上全部拿到最高任务分；对最强基线 Graph-of-Skills（GoS），ScienceWorld 六模型宏平均 72.62→80.50，ALFWorld 成功率 80.01%→86.79%，且两个基准的平均环境步数都下降；消融显示校准后的边保住了前置条件、状态变更动作、验证例程与完成步骤。

**局限**：
- **代码尚未放出**：摘要脚注的官方仓库 2026-08-28 实抓仍是占位（仅 README 写"The code will be released within a few days"，0 star、无 license、根目录无代码文件），signal.runnable=false；
- 基准是 ALFWorld/ScienceWorld 具身任务，迁移到数据竞赛型技能库的效果未经检验；
- 反事实探针需对技能对做移除/替换/重排的成对评估，技能库大时探针次数线性增长（离线做，但不是免费）；
- "修复证据"依赖环境反馈信号，纯文本技能库需要自定义等价的反馈来源。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：见 frontmatter 两条映射——黑客松的带技能库 agent 作品、Kaggle 的跨场次技能沉淀复用。共同逻辑：技能库的差异化价值不在"存了多少"，而在"取的时候不取错"；校准边把验证例程与前置依赖带进上下文，减少 agent 当场翻车（用了没装依赖的技能、跳过验证步骤）。
- **打法（reuse_cost=中）**：无需训练，探针机制用 LLM API 一到两天可自实现最小版——对自己的技能库建候选边（调用签名 I/O 匹配 + 描述相似度）→ 每条边跑移除/替换/重排探针让 LLM 裁判打分 → 贝叶斯平滑成边权 → 赛期按任务状态检索扩展。官方代码放出后可换原生实现，赛前复验仓库状态。
- **差异化话术**："我们的 agent 不只攒技能，还离线校准了技能因果图，检索按因果边走"——这是与"向量库 + top-k"队伍拉开代差的具体机制点。
- **风险**：技能库小于 20 条时校准收益有限（全库 prompt 或简单向量检索已够）；探针打分依赖 LLM 裁判的稳定性，需抽样人工复核边权。
