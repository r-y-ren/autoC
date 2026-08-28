---
competition_id: mcm-icm
last_verified: 2026-08-28
coverage: [2024]        # 2025/2026 winners 由并行分片在建，入库后刷新本文件（见文末待刷新项）
confidence: 中           # 官方评审文本为官网一级直引；方法论层仅 6 篇非随机深构、材料等级不齐（1 全文原件/1 期刊转述/2 衍生稿/1 校方新闻/1 不可得）
sources:
  - url: "https://www.contest.comap.com/undergraduate/contests/mcm/instructions.php"
    title: "MCM/ICM 2027 官方 Contest Instructions（快照 kb/raw/mcm-icm/2027-instructions.html，2026-08-28 抓；本文件全部评审原文出处）"
    accessed: "2026-08-28"
  - url: "https://comap.org/blog/item/highlights-from-comaps-2024-mcm-and-icm"
    title: "COMAP 官方博客《Highlights from COMAP's 2024 MCM and ICM》（快照 kb/raw/mcm-icm/2024-blog-highlights.html，2026-08-28 抓）"
    accessed: "2026-08-28"
  - url: "kb/competitions/mcm-icm/winners/2024.md"
    title: "本条目 2024 获奖解构（O 奖 35 队全量索引 + 6 篇深构；本文件第二/三/四/六节的主要事实源，其内引用可逐条回溯）"
    accessed: "2026-08-28"
  - url: "https://www.hmc.edu/about/2024/05/14/harvey-mudd-is-top-u-s-team-in-international-math-modeling-competition/"
    title: "Harvey Mudd 校方新闻（四维评审标准转述出处；快照 kb/raw/mcm-icm/2024-D-harveymudd-news.html）"
    accessed: "2026-08-28"
---

# MCM/ICM（美赛）模式库（patterns）

> 本文件是 KB-1 条目的解构总结层：供 K-02 赛道评分（"获奖模式重叠"维度）、验收分析报告与赛点检查表消费。
> 每个结论必须能追溯到 winners/<年份>.md 的具体条目或官方评审文件；信源不足时宁缺毋滥并标注信源等级。
> 本文件属正文层（lint 跳过）；措辞通用化，适用文书型与代码型两类作品。

**引用缩写**（与 meta.md / winners/2024.md 保持一致）：
**[INS]** 官方 instructions 页（官网一级，快照 `kb/raw/mcm-icm/2027-instructions.html`）｜ **[BLOG]** COMAP 官方博客（官网一级·主办方自媒体）｜ **[W24]** `winners/2024.md`（本库内部层，其引用链：[RES] results 页 / [PDF-A…F] 分题 Results PDF / [HMC-D] 校方新闻 / [PMC-C] Scientific Reports / [GH-E] O 队自公开原件 / [HSET-A]/[HSET-F] 同校衍生会议稿）。

---

## 一、评审偏好（官方评审文本直引优先）

### A. 官网一级原文（[INS]，2026-08-28 快照核验）

1. **摘要是一等权重项**："The judges place considerable weight on the summary, and winning papers are often distinguished from other papers based on the quality of the summary."（评委对摘要赋予相当大的权重，获奖论文常凭摘要质量与其他论文拉开差距。）并给出弱摘要的官方定义："Summaries that are mere restatements of the contest problem, or are a cut-and-paste boilerplate from the Introduction are generally considered to be weak."（仅复述题目或从引言粘贴模板的摘要通常被视为弱。）写作指引："You should write the summary last"（摘要最后写，须呈现方法与最重要的结论）。
2. **评委首要关注点**："MCM/ICM judges are primarily interested in the team's thought processes, analysis of the problem, modeling approaches, and mathematical methods."（思维过程、问题分析、建模途径、数学方法——不是结果漂亮度。）
3. **无及格线、允许部分解**："There is no passing or cut-off score, and therefore, partial solutions are acceptable and teams are encouraged to complete as much of the problem as they are able to do."——完成度优先于完美主义。
4. **官方解题结构清单**（[INS] "Overall" 节十条，节选）：目录；问题重述；变量与假设清晰陈列；"State and justify reasonable assumptions"（假设须有正当性说明）；分析应 motivating or justifying the model（模型由问题动机引出）；长推导/数据入附录；**"Include a design of the model. Discuss how the model could be tested, to include error analysis, sensitivity, and/or stability."**（检验设计+误差/灵敏度/稳定性分析是明文要求）；"Discuss any apparent strengths or weaknesses"（优劣势自评）；"Provide a conclusion and report results explicitly"（结论与结果显式报告）；文献引注。
5. **奖级阶梯的官方语义差**（[INS] IX 节 designation 原文，M→Fin→O 递进）：
   - **Meritorious**："excellent in **many aspects**… The report addressed **all requirements** in a clear, well-supported, well-organized, and well-presented manner."（多方面优秀+清晰覆盖全部要求。）
   - **Finalist**："**exemplary**… reached the final round of judging… present complete and logical analysis in an organized and clear presentation **above and beyond simply addressing the requirements**. These papers are **easy to read, easy to follow, logical, and comprehensive**."（超越"回应要求"本身；易读、易跟随、合逻辑、全面。）
   - **Outstanding**："**best of the best**… at the **highest level** relative to the contest submissions in terms of exemplary student work in modeling and problem solving, analysis, and communication."（相对当届提交的最高水平。）
6. **冠名奖标准 = 官方价值观的显式声明**（[INS]）：Ben Fusaro 奖授予 "an especially creative paper"（特别有创造性的论文，从 Finalist 中选）；Veena Mendiratta 奖（C 题）看重 "usefulness and clarity… **creative and effective use of the data**, along with a model that is **well-explained and easy to understand**"（数据使用的创造性与有效性+模型可解释易懂）；Leonhard Euler 奖（D 题）标准含 "**especially creative and innovative modeling**" 与 "**good understanding of interdisciplinary science**"。
7. **评委视角文本的官方指定载体**：UMAP Journal 夏秋卷的 Director's Article 与 **Judges' Commentary**——"These articles describe what judges look for in the various sections of solutions."（[INS]；会员墙后，见 winners/2024.md 缺口声明。O 论文选篇+评委+命题人讲评均发表于该刊 [PDF-A 新闻稿页]。）

### B. 转述与旁证层（降级标注）

- **四维标准（正确性/表述/洞察力/创造力）系校方转述**："The team's papers are judged not only on their scientific and mathematical accuracy, but also on their clarity of exposition, insight and creativity."（Harvey Mudd 校方新闻转述 COMAP 评判标准 [HMC-D]；**instructions 页无此四维原文，按二级转述降级采信**，与 [INS] 的"思维过程/分析/建模/数学方法"关注点不矛盾。）
- **COMAP 官方博客对 2024 O/Finalist 队的总结**："demonstrated their mastery of interdisciplinary problem-solving but also showcased their ability to integrate diverse perspectives and methodologies to address complex societal challenges"（跨学科问题掌握+整合多元视角与方法论）[BLOG]。注：winners/2024.md 将此句归到 [RES] 新闻稿；2026-08-28 复核其实际载体为 COMAP 官方博客页，本文件按直核快照改引 [BLOG]。

## 二、方法论分布（6 篇深构的模式归纳）

> **非随机样本声明（必读）**：样本 = winners/2024.md 的 6 篇深构（每题 1 篇，O 奖级），占 2024 年 O 奖 35 队的 17%；材料等级从全文原件（E）到官方新闻（D）不等，B 题正文不可得（降级为题目结构层）。**下表"频次"只代表这 6 篇样本内的出现情况，不代表 O 奖总体占比**；A/F 两篇为同校衍生会议稿（队级归属 verified: false，8/7 页会议体量，参赛 25 页原稿可能含本文未见的补充内容）。

| 模式 | 样本内出现 | 代表条目（材料等级） | 可迁移性 |
|---|---|---|---|
| **机制进模型结构**：把题目特有机制编码进模型参数/变量，而非套用通用模型（A：性比可变→K 与 r 双通道；C：网球交替发球→SA 二值变量；E：可持续张力→HIC×盈利双系数） | 3/5 篇可核深构（A/C/E） | [W24 §二A/C/E]（衍生稿/期刊转述/原件） | 高：政策/机理题通用，成本中 |
| **机理+数据双模型互证**：ODE 宏观 + CA 微观同源互证（CA 差分规则由 LV 方程导出） | 1/5（A） | [W24 §二A]（衍生稿） | 中：适用"个体规则→种群动态"类；需 1-2 天 CA 仿真 |
| **领域指数=少数可解释分量加权**：DPI = α×PE+β×PS+γ×SA，权重显式标定非黑箱 | 1/5（C） | [W24 §二C]（期刊转述） | 高：数据洞察题主模型性价比高；但线性上限低（见第四节） |
| **空间统计+多目标优化政策定价**：MGWR 空间异质 + 人道/盈利双系数 + 熵权 g 函数排利益相关方杠杆 | 1/5（E） | [W24 §二E]（原件） | 高：政策/可持续题通用骨架，成本中 |
| **预测+两类干预优化三段式**：BP 趋势预测 + TSP/SA 宣教路线 + 贪婪选址，与"评估+5年计划+影响建模"任务链对齐 | 1/5（F） | [W24 §二F]（衍生稿） | 高：先立骨架再填强模型；反面细节见第四节 |
| **方法-任务标准武器对齐**：每个子任务用其领域标准方法（时序→NN、路线→TSP+SA、选址→贪婪），无错配 | 1/5（F）+ B 题官方任务链佐证 | [W24 §二F/B]（衍生稿/官网） | 高：作为解题 checklist 零成本 |
| **全要素成品交付**：假设→记号→分问成章→敏感性→优劣势自评→政策信（Letter）；B 题官方要求两页 memo | 2/5（E 明证；B 题目要求） | [W24 §二E/B]（原件/官网） | 高：成品感（letter/memo）是任务书的显式要求 |
| **参数实测锚点标定**：灵敏度系数由 56%/78% 实测雄占比反推（a=0.178），模型-数据闭环 | 1/5（A） | [W24 §二A]（衍生稿） | 高：隐性参数机理模型通用，半天级 |
| **数字具象化结论**：加州 $20.1394M→$31.0054M、自由女神像 $2.5M/年等可核数字进摘要 | 1/5（E） | [W24 §二E]（原件） | 高：零成本增强可信度 |

## 三、往届差异化点（什么样的作品拿到了最高奖）

**依据**：官方奖级定义（[INS] IX）+ 2024 O 奖名单统计与深构证据（[W24 §一/§二/§三]）。样本单年，结论按证据强度排序。

1. **官方定义层：O = "best of the best"，Fin 已是"超越回应要求"**。M 级的官方语义是"清晰覆盖全部要求"，Fin/O 的分水岭在 "above and beyond simply addressing the requirements"（超越单纯回应要求的分析与呈现）+ "easy to read, easy to follow, logical, comprehensive"（[INS]）。深构 O 稿的对应行为：机制编码进模型结构（3/5，见第二节）、具象数字进摘要（E）、验证节+自评节齐备（E）。
2. **洞察与创造性是冠名奖的显式标准**：Ben Fusaro（创造性论文）、Veena Mendiratta（数据使用的创造性与有效性+可解释）、Euler（创新建模+跨学科理解）（[INS]）。2024 年 4 支 COMAP 奖学金队分布于 B/C/D/F 题，两支在中国人大（C 2401445、F 2409949）（[W24 §一]）。
3. **竞争密度事实（2024）**：O 奖 35 队中**中国内地高校 34 队 + 美国 Harvey Mudd 1 队**；校别集中：人大 4、西安交大 3、武汉理工/北理工/上交/北师大各 2（[W24 §一]，官网 results 页一级）——O 奖竞争的主战场在中国内地头部校的成熟参赛体系内。
4. **选题经济学（2024 官网计数，[W24 §一]）**：O 率区间 0.09%–0.20%；**D 题（运筹/网络科学）O 率最高 0.20% 且队数最少（1,970）**；C 题（数据洞察）队数最多（10,184）但 O 席位也最多（11 席）。B 题队数 2,643、O 率 0.15%（次高）。含义：小众题的 O 概率结构性略高，但基数小、方差大。
5. **表述的战略地位**：唯一非中国 O 队（HMC，D 题）的获胜叙事核心是"大部分赛程用于相互挑战想法与打磨报告可读性（readable, comprehensible and beautiful）"，与 [INS] Fin 级"易读易跟随"标准直接对应（[W24 §二D]，校方新闻层）。
6. **画像匹配注意**：以上共性的证据材料等级不齐（1 篇原件/1 篇期刊转述/2 篇衍生稿/1 篇校闻/1 篇不可得），"机制编码""成品交付"两条有原件级证据（E）与官方题目要求佐证（B 的 memo），其余条目证据强度递减——消费时按 [W24] 内部标注折算。

## 四、反面观察（常见失分/降级模式）

> 两类来源分开陈述：A 类 = 官方规则可证的**红线与降级事由**（[INS] IX）；B 类 = 深构"不足与可改进点"节的归纳——**注意 B 类对象是已获 O 奖的作品，其"不足"是改进空间而非失分实证**，用途是反面检查项而非因果断言。

**A. 官方红线（[INS]，Disqualified/Unsuccessful 原文依据）**
- **抄袭**：未注明来源/逐字文本/网络信息挪用，且 COMAP 使用 **pairwise comparison software**（两两相似度比对软件）+ 评委判定——模板化、共享段落式写作有实测检出手段。
- **赛中网络分享/求助**：任何形式发布题目/解法/部分工作到网络，或经社交媒体/问答系统/互动博客寻求外部帮助；**COMAP 在赛期内持续监测互联网**（"COMAP continually monitors the Internet during the contest period"）。访问公开讨论赛题的网站/社交媒体同样记 Unsuccessful（Web）。
- **AI 未引注**：LLM 可能复现他人文本，无清晰引注"可能被认定为剽窃并取消资格"（[INS] AI 政策节，详见 meta.md ai_policy）。
- **格式硬伤即出局**：文件损坏/格式错误/未按说明提交 = Not Judged；**AI 使用未申报**同样违反报告义务。

**B. 深构不足节归纳（[W24 §二]，含核对维度声明）**
- **验证节缺失或薄弱**（核对维度：验证/鲁棒性）：A 稿无灵敏度分析节（仅标定单参数 a）——对照 [INS] 明文要求"error analysis, sensitivity, and/or stability"是官方结构项；F 稿 40 个年度样本训 BP 网络，无交叉验证、无基线对比，仅"预测曲线与历史波动相似"目测级验证；E 稿 2034 年外推为单点预测、无置信区间（论文自评另认数据依赖与模型复杂度两大弱点）。
- **方法-数据量错配**（F）：小样本配深模型——同任务换 ARIMA/线性基线+交叉验证更稳（该深构自身的迁移结论）。
- **参数与机制无出处**（A）：竞争系数 σ、捕食系数、K 值均无文献/数据来源；56%/78% 实测锚点未附数据源。
- **优化无最优性讨论**（F）：贪婪选址未讨论相对 SA/整数规划的 gap；TSP"城市=宣教站"构造与"宣传深度→支持度"因果无量化传递函数。
- **可解释结构牺牲精度**（C）：O 稿 DPI 线性合成预测准确率 82.4%，被后续同行评审模型（CBRF，98.5%）在同一数据上大幅超越 [PMC-C]——**这同时是正反双面证据**：精度不是 O 的必要条件（见第六节），但追求更高名次时可用"指数可解释+GBDT 精度"双层结构补齐（该深构迁移结论）。
- **衍生稿口径声明**：A/F 不足项基于 8/7 页会议衍生稿，参赛 25 页原稿（会员墙后）可能含补充验证，不足可能被高估；B/D 因正文不可得未核对模型层（[W24 §四]）。

## 五、赛点检查表（评审标准 → 可执行检查项；快循环验收清单派生源）

> 每条 = 标准（[INS] 官方原文或深构证据）× 可验证动作。标注【官】= 官网一级原文派生，【构】= 深构证据派生（单年非随机样本，弱一等）。

**摘要与结论**
- [ ] 摘要最后写；逐问题给出方法+**结论与具象数字**（含至少一处可核量化输出）【官+构（E）】
- [ ] 摘要无"复述题目/引言粘贴"段落（官方弱摘要定义逐条对照）【官】
- [ ] 结论节显式报告结果（"Provide a conclusion and report results explicitly"）【官】

**结构与完整度**
- [ ] 目录/问题重述/变量记号/假设（每条附正当性）齐备【官】
- [ ] 模型由问题动机引出（motivating/justifying），非"模型目录式"堆砌【官】
- [ ] 检验设计节齐备：误差分析+灵敏度+稳定性至少其二【官】（对照反例：A 稿缺灵敏度节）
- [ ] 优劣势自评节（strengths/weaknesses）非空泛，含数据依赖/复杂度等实质自认【官+构（E）】
- [ ] 长推导与数据入附录，正文 25 页内（含目录/参考文献/附录/代码全部计数）【官】
- [ ] 题目要求的成品交付物（memo/letter 等）独立成节且面向真实受众【官+构（B/E）】

**建模与验证质量**
- [ ] 题目特有机制被编码进模型结构（变量/参数/约束层），非通用模型直套【构（A/C/E，3/5）】
- [ ] 每个隐性参数有标定依据（实测锚点/文献/数据反推）【构（A 反例）】
- [ ] 方法-数据量匹配：样本量/数据类型与方法复杂度对齐；有强基线对比【构（C/F 反例）】
- [ ] 预测/外推带区间或情景分析，非单点断言【构（E/F 反例）】
- [ ] 启发式求解附最优性 gap 或替代算法对比【构（F 反例）】

**合规与提交（红线项，一票否决级）**
- [ ] 全文匿名（无校名/人名），页眉每页含队号+页码，文件名=队号，单一 PDF <25MB【官】
- [ ] 若用 AI：正文行内引注+参考文献列 AI 工具+末尾附 Report on Use of AI（不计页数）【官】
- [ ] 赛期零外发：不发布任何题目/解法片段，不访问讨论赛题的网站/社区，不寻求队外人类帮助【官】
- [ ] 文本原创性自查（应对 pairwise 比对）：模板句/共享语料复用度为零【官】

## 六、对本框架的启示（喂给 K-02 / 验收报告）

**队伍画像前提**（任务包给定，非 KB 事实）：本队有美赛 **M 奖（Meritorious）** 历史。以下"M→O 差距"分析只基于已实抓证据（[INS] 官方奖级定义 + [W24] 2024 深构），单年样本，方向性结论。

**1. 差距定位（官方语义差是第一依据）**：M 级官方定义 = "多方面优秀+清晰覆盖全部要求"；Fin/O 的增量在两处——**"above and beyond simply addressing the requirements"（超越回应要求）** 与 **"easy to read, easy to follow, logical, comprehensive"（可读性进入奖级定义）**。即：M 水平的队伍通常已能"答完答好"，O 的边际不在"多做一个模型"，而在**洞察层（机制编码）与呈现层（可读性）**。

**2. 具体差距候选（按证据强度排序）**：
- **机制编码进模型结构**（3/5 可核深构共性，含唯一原件 E 的 HIC×盈利系数设计）：把题目领域特有张力/规则做成模型内的显式变量——这是"above and beyond requirements"最可操作的形态。我方若停留在"通用模型+调参"层，正是 M 与 O 的典型分界候选。
- **写作打磨占赛程大头**（HMC O 队策略级证据；E 原件的成品化完成度旁证）：建议赛程时间盒中固定分配"最后 24 小时纯写作+摘要"，摘要按第五节检查表逐项过。
- **验证节完备性**：[INS] 明文要求 error/sensitivity/stability；深构反例（A 缺灵敏度、F 无交叉验证）说明获奖队也常缺——我方补齐即是显性超越点；配合"强基线对比"（C 反例教训：先用梯度提升测天花板，再决定主模型结构，可用"指数可解释+GBDT 精度"双层）。
- **具象数字与成品交付**（E 原件证据）：摘要含可核数字（$20.1M→$31.0M 级别）、题目要求的 letter/memo 独立成节。
- **选题决策**：工具-题目匹配优先（HMC 用 OR 课程匹配反推选题）+ O 率经济学（2024：D 题 O 率 0.20% 最高且队数最少；C 题最拥挤）——两项各占一票，不单独决策。

**3. 明确不值得投入的方向（同样基于证据）**：模型复杂度本身不是 O 的门票——E/F 两篇的自认弱点恰是复杂度与数据依赖；C 题 O 稿精度被后来者大幅超越（82.4% vs 98.5%）仍是 O。**堆精度/堆复杂度对 M→O 的边际收益证据不足，机制洞察+呈现+验证完备的证据链更强。**

**4. 合规栈（对本框架的硬约束）**：本框架按"AI 辅助原创"标准产出，与 COMAP 政策兼容但义务明确——行内引注+参考文献列 AI 工具+独立 Report on Use of AI 章节；**pairwise 比对软件在案**，框架复用的模板句/通用语料必须在交付前过原创性检查（第五节红线项），这是比奖级更优先的资格线。

**5. 情报层待补**（影响上述结论强度）：O 论文全文在 Mathmodels.org/UMAP Journal 会员墙后（[W24 §四]），当前仅 1 篇原件级深构；若订阅补采 6 篇官方摘要/全文，本节"M→O 差距"假设可升级验证。

---

### 待刷新项

- [ ] **2025/2026 winners 入库后刷新**：本文件 coverage 目前仅 [2024]；并行分片建成后，第二/三/六节按新增深构重算频次与共性（尤其校别分布、O 率结构是否复现"中国内地绝对多数+D 题 O 率最高"）。
- [ ] 2025/2026 题目结构（problems 页快照已在 kb/raw/mcm-icm/）待 winners 分片消费后并入第三节选题经济学。
- [ ] UMAP Journal Judges' Commentary / Mathmodels 会员内容若补采，第一节 B 层转述（四维标准）可替换为官网一级原文。
