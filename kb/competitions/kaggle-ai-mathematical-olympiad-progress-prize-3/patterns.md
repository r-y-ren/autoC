---
competition_id: kaggle-ai-mathematical-olympiad-progress-prize-3
last_verified: 2026-08-28
coverage: [2026]           # 单届：五队获奖方案全量深构（award_levels 前两级超标覆盖——1st–5th Place 全部；Overall Grand Prize 本届未颁出）；AIMO1/2 仅 meta 层前史注记，未深构
confidence: 中             # 加分：获奖五队全样本 + #2/#3/#5 一手材料（HF 仓库/writeup 全文）+ 官方公告双源；扣分：#1/#7 writeup 正文 SPA 阻断（共享基线结论对这两队为推断层）、私榜分数出自 #5 参赛者表格非官方 leaderboard 直抓、arXiv 代理材料身份映射未确认、Kaggle Rules 全文未直抓（时限/开源截止原文二手）
sources:
  - url: https://aimoprize.com/updates/2026-06-24-aimo-3-winners-announced
    title: "AIMO 3 Winners Announced（五队名单 #1/#2/#3/#5/#7、分数密集、gpt-oss-120b 主导、stricter rules、HF 公开）——评审偏好与差异化节的官方口径"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/714435
    title: "Kaggle 官方 winners 公示讨论（名单第二源，快照口径）"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3
    title: "Kaggle AIMO-3 赛站（总池/奖金/H100 挂赛限制/开源 LLM 规则节，SPA 经搜索索引快照交叉）"
    accessed: "2026-08-27"
  - url: https://aimoprize.com/updates/2023-12-19-frequently-asked-questions
    title: "AIMO FAQ（§7.2 仅开源模型与工具、§7.1 赛期时限/算力限制、§8.2 公开共享与可复现）"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/writeups/3rd-place-solution-for-the-aimo3-competition
    title: "3rd Place writeup 全文（错误分析闭环/反过拟合框架/负结果清单——一手最强，方法论节主力源）"
    accessed: "2026-08-28"
  - url: https://huggingface.co/varianceofx/aimo3-2nd-place-solver-adapted
    title: "varianceofx 官方改编版求解器 README（锁参数硬上限/流式抽取/早停数学化，一手；赛后改编版差异已标注）"
    accessed: "2026-08-28"
  - url: https://huggingface.co/spaces/peiranli0930/AIMO3-TAMU-TACO
    title: "TAMU-TACO 官方 HF Space（五队私榜分数表/what didn't work 清单/64×H100 离线分诊未迁移，一手）"
    accessed: "2026-08-28"
  - url: https://arxiv.org/html/2603.27844v1
    title: "Inference-Time Optimization Lessons from AIMO 3（同族工程/消融代理材料，二手：与五队身份映射未确认；σ≈1.7 方差与提交预算彩票数学的唯一源）"
    accessed: "2026-08-28"
---

# AI Mathematical Olympiad – Progress Prize 3（AIMO 3）模式库（patterns）

> 本文件是 KB-1 条目的解构总结层：全部结论重组自 `winners/2026.md`（五队深构，逐条含原始 URL+抓取日期）与 `meta.md`（章程/AI 政策实抓），供 K-02 赛道评分（"获奖模式重叠"维度）、验收分析报告与赛点检查表消费；未新增任何上网抓取。
> 引用键（正文内联使用，键即回溯路径，明细证据链在 winners/2026.md 对应条目）：**[公]**=官方 winners 公告（aimoprize.com，2026-08-27）；**[K-dis]**=Kaggle 官方 discussion #714435（2026-08-27，快照口径）；**[K-site]**=Kaggle 赛站（2026-08-27，SPA 经搜索索引快照交叉）；**[FAQ]**=AIMO FAQ（2026-08-27）；**[W1]–[W7]**=winners/2026.md 深构条目 1–5（#1/#2/#3/#5/#7，2026-08-28 抓，材料等级见该文件）；**[arXiv]**=arXiv 2603.27844v1（2026-08-28，二手代理）。
> 信源等级：官网/官方公告 > 参赛者一手（HF 仓库、渲染全文的 writeup）> 二手（arXiv 代理、第三方 Space、搜索片段）——涉及二手的结论逐条标注，未核细节不写入正文事实层。

## 一、评审偏好（赛制特殊性：纯客观指标制 + 合规验证门槛，无主观评审环节）

- **名次奖纯客观计分**：按私榜解题数（110 道 National Olympiad→IMO 难度原创题，AIME 风格非负整数答案，五位数答案"making guessing essentially impossible"）排序发 1st–5th Place 奖金（$262,144 逐级减半至 $16,384；总池 $2,207,152）。不存在评委打分/答辩/文书评审环节（meta.md 概况与 award_levels，[K-site][公]）。
- **评审标准的实质形态**（winners/2026.md 深构节引言原话）："私榜解题数 + 合规（单卡 H100、5 小时 wall-clock、无外部 API、开源权重模型、获胜方案公开共享）"——合规是硬性入围条件而非加分项。
- **算力与提交形态强约束**："H100 are only available for notebooks attached to this competition"（[K-site]，官方快照口径）；获奖方案实测约束 "runs entirely on a single H100 80 GB within Kaggle's 5-hour wall-clock limit. No external APIs, no multi-GPU setups, no pre-computed..."（[W1][arXiv]，**二手**——官方 Rules 全文 SPA 未直抓，meta 待核验清单已记）。
- **开源模型/工具限定**："competition entries may only use AI models and tools that are open source"（[FAQ] §7.2）；训练期不限、赛期 "time limit, compute limit, length of solutions"（[FAQ] §7.1）。
- **公开共享是获奖条件**："all winning solutions to be publicly shared"（launch 公告，经 meta.md）；本届获奖提交已全部发布 HuggingFace（[公]）。
- **合规验证本身影响名次**：验证周期较长归因于 "this year's stricter rules"（[公]）；私榜第 4 名（DrDobok，43.5/110）与第 6 名未进入五队获奖名单，官方未点名排除原因（[W4] 结果表 + [公]；**排除原因属未证实推断，见第三节**）。
- **大奖解锁制**：Overall Progress Prize Winner（≥$1,589,248）与 IMO 金牌级 $5mn Grand Prize 本届均未触发（[公] 无触发记录，meta 口径）——与 ARC Prize 同构的"解锁制从未解锁"格局（跨条目对照，供 K-02 复用）。
- 主观评审位仅存在于 Extra Prizes（Write-up/Math Corpus 等），得主公告 SPA 阻断未入库（winners/2026.md 数据缺口声明）——本节对其不作归纳。

## 二、方法论分布（五队方案模式表——2026 单届全样本）

**共享基线谱系（本表前提）**：五队共享同一公共 notebook 谱系——Parthenos 的 "44-50-let-me-over-cook" 与 Andreas Bisiadis 的 "aimo-3-gpt-oss-120b-with-tools"；#1 的选定 notebook 即 let-me-over-cook 系（[W4] 一手表格注明）。谱系标配 = vLLM 本地服务 gpt-oss-120b（FP8 权重+KV cache、ctx 65536）+ N=8 并行尝试（T=1.0）+ 每尝试挂持久 Jupyter 内核做 TIR（sympy/numpy/mpmath）+ 熵加权多数投票 + 4/8 早停 + 18000s 时间预算等分+安全边际（[W2][W4] 一手自述 + [arXiv] 交叉）。模型层 5/5 确认（[公]"多数队伍围绕 gpt-oss-120b 构建 harness 与提示策略"）；完整工程栈一手确认 3/5（#2/#3/#5），#1 为确认层+生态侧写、#7 仅官方口径+voting scheme 注记（材料等级不齐，如实分层）。

| 模式 | 出现频次（材料等级） | 代表条目与差异点 | 可迁移性 |
|---|---|---|---|
| gpt-oss-120b 纯推理（无微调）+ 8 路自洽 + 工具推理 | 5/5（模型层一手+官方；#1/#7 工程细节二手/缺口） | 全队共用；116.8B 总参/5.1B 激活 MoE 单卡 H100 80GB 可服务（gpu-memory-utilization 0.96、kv fp8_e4m3，同族配置实抓 [W1]） | 高：整栈开源（varianceofx repo + [arXiv] 附录 A–F + 公共 notebook），Kaggle notebook 级复用成本 |
| 熵加权/低熵优先聚合 | 3/5 一手（#2/#3 基线保留/#5）+ #1 二手线索 | #5：按每次尝试平均熵的倒数加权，无多数时选最低熵答案（[W4]） | 中高：聚合层与模型解耦，纯代码可移植 |
| 三级时间预算 + 最小共识早停 | 2/5 一手互证（#2/#5），同族标配口径另见 [arXiv] | #2：MAX_TIME=18000/单题 900/单尝试 300/MIN_CONSENSUS=4；#5：另留 540s 安全边际给模型加载（[W2][W4]） | 高：纯配置模板，任何时间盒评测 harness 通用 |
| 反过拟合离线验证闭环 | 2/5 一手（#3/#5） | #3：1120 条全文回答错误语料 + 50 题外部独立集 + "5/10/35" 问题三分假设，明确拒绝以公榜为唯一指标（[W3]）；#5：64×H100 场外分诊 + golden traces（[W4]） | 高：方法论标准作业流程，一次采集多次复用 |
| 错误驱动提示工程 | 1/5 一手深构（#3）+ 公告口径（多队"提示策略"）+ #7 标题方向（材料缺口） | #3：全文语料→强模型归类（喂 gpt-oss-120b 自己的正确范例防"过于高级的建议"）→可行域内三点对策（[W3]） | 中：天花板受基线钳制（[W3] 自评），需配合验证闭环 |
| 答案抽取鲁棒性工程 | 1/5 一手（#2） | 流式滚动窗口扫 \boxed{} + 截断恢复 + 大整数逗号处理 + [0,99999] 整数前置校验清单（[W2]） | 高：一切"生成可能撞时限"的 LLM 评测通用 |
| 离线-在线分离纪律（强模型仅场外） | 1/5 一手（#5） | GPT-5 high 仅用于离线题集分诊，"从不在计时提交内，提交完全自包含"（[W4]） | 高：合规示范做法，直接套用 |
| 动态早停数学化（最快答案优先） | 1/5 一手（#2） | "尾随答案在数学上不可能反超时即停"，省时回流难题（[W2]，writeup 标题双证） | 中高：聚合与调度层通用 |

> 频次声明：样本 = 4138 支参赛队（[W4] 一手口径）中获名次奖的全部 5 队——**非随机极小样本且仅单届（2026）**，频次不代表总体方法分布；五队同族意味着"共享模式"反映的是头部生态收敛而非因果优胜（差异化证据见第三节）。AIMO1（Numina）/AIMO2（NemoSkills）仅 meta 前史注记，无方法深构，跨届演进不作归纳。

## 三、往届差异化点（分差极小意味着什么 + 未获奖异常）

- **拿到最高奖的证据链（#1，46/110）**：① 确认层——"GPT-OSS-120B Based Inference" 纯推理方案（[W1] writeup meta + [公]）；② 专属线索层（**二手未核**，SPA 阻断）——memory optimization、prefix caching、KV fp8、entropy-weighted SC、verification-assisted（[W1]）。1 题优势胜出（45→46）。
- **分差极小的三层含义**（46/45/44/43.5/42，五队全距仅 4 题/110；分数表出自 [W4] 一手，非官方 leaderboard 直抽——等级如实标注）：
  1. **差异不在算法层**：五队同基线谱系（第二节），[公] 自述"榜单分数高度密集"；胜负落在工程鲁棒性（时限管理/抽取/时间分配）与验证闭环——即第二节表中各 1–2/5 的独占模式。
  2. **顶部差距在采样噪声内**：同族基线 13 次运行实测 μ=39.7/50（公榜）、min 37/max 44、σ≈1.7（[arXiv] §代理实测，二手）→ #1 对 #2 的 1 题领先在运行方差以内，winners 深构原话"运气成分无法排除"（[W1]）。
  3. **提交预算=彩票管理**：P(单次提交≥44)≈2.3%，13 次剩余提交内 max≥44 概率≈28%（[arXiv] §8，二手代理）；[arXiv] §11 策略原话 "use the largest model that fits, keep temperature high, and spend your submission budget on lottery tickets"。
- **总纲式结论（模式归纳线索经 winners 原文核实后的表述）**："模型能力碾压推理期技巧"在库内的证据形态 = ① [arXiv] 消融结论"模型能力差距碾压一切推理期优化，最优策略是反复提交未修改基线"（二手代理）；② [公] 队伍层面互证（全部围绕同一 120B 模型做 harness）；③ 两独立实测方（#5 一手 + [arXiv]）对推理期技巧清单一致给出负结果（第四节）。置信度：中（①为代理材料）。
- **未获奖异常（rank #4/#6）**：DrDobok（43.5，与 #5 同分）与第 6 名未进五队名单；官方仅以 "stricter rules" 解释验证耗时更长，未说明排除原因（[公][W4]）。可证的只有：**同分之下获奖与否由名次外的验证/合规维度决定**（[W4] 亮点原话"合规稳健性本身成为名次的一部分"）；具体归因（合规排除/弃权/其他）未证实，不写为事实。
- **单团队可及性证据**：#3 为单人参赛、自述"以学习为目的"（[W3] 开篇），44/110 拿 3rd——在共享开源基线生态下，无大团队/大算力亦可进入头部（对本框架定位关键，见第六节）。
- 前史注记：AIMO1=Project Numina（2024-07 获奖）、AIMO2=NVIDIA NemoSkills（2025-04）（meta participate 页口径）——未深构，仅说明该系列逐年增奖金/提难度/加算力。

## 四、反面观察（被证伪的技术路线与合规红线）

**被两独立来源交叉证伪的推理期技巧**（#5 "what didn't work" 一手清单 + [arXiv] 同族消融，winners 原话"两个独立来源得出同族结论，模式可信度高"；注意 [arXiv] 为代理材料，独立性按方案族划分）：

- **提示多样性（prompt diversity）无增益**——注：任务包线索所称 "Diverse Prompt Mixer 全败" 术语在库内原件无对应文本，按纪律采用库内实抓措辞"提示多样性无增益"（[W4][arXiv]）。
- **提示压缩（prompt compression）反而伤分数**（[W4][arXiv]）。
- **扩大工具菜单无效**——模型不使用新增工具（[W4][arXiv]）。
- **attempt 级反思（reflection）浪费 token**（[W4][arXiv]）。

**#3 writeup 一手负结果清单**（[W3] §2.2，负结果如实公开本身是其亮点）：日文推理、两步自纠、complexity-based consistency、8→16 扩池（提前完成的答案精度反而降）。

**失败模式（方案层）**：

- **离线增益不迁移**：#5 自认 64×H100 场外分诊"大部分收益未迁移到比赛环境"（[W4] §3 原文）——离线提示增益在真实算力/时限约束下蒸发，该队未解决迁移问题。
- **纯提示层天花板受基线钳制**：无服务层/聚合层工程的方案上限被共享基线锁死（[W3] 不足节自评）。
- **依赖外部 API 的方案结构性不可行**：评测期无外部 API（[W1][arXiv] 实测约束，二手；[K-site] 挂赛 H100 限制为官方口径）。

**合规红线（条款 + 可观察的执行后果）**：

- 仅开源模型与工具（[FAQ] §7.2）；开源日期截止与许可类型的 Rules 原文未直抓（meta 待核验）。
- 训练数据/脚本/模型权重须公开可复现（[FAQ] §8.2）；获奖方案已全部 HF 公开（[公]）。
- "stricter rules" 验证下同分未获奖的 #4/#6 案例（第三节）——**归因未官宣**，作为"合规稳健性需自检"的观察证据而非定论。
- 本节无评委讲评类材料（本赛无主观评审），全部为参赛者自报负结果 + 条款原文 + 排除异常，等级已逐条标注。

## 五、赛点检查表（Kaggle 型算法赛检查项 → 快循环验收清单派生源）

- [ ] **开源合规自检**：提交内模型/工具全部开源可用（公开权重+许可清单逐项核对），无闭源 API 调用残留；开源日期截止条款查 Rules 原文确认——依据：[FAQ] §7.2 + [W1][arXiv] 实测约束（时限/许可原文未直抓，运行前必须补核）
- [ ] **算力预算内端到端自测**：在挂赛 Kaggle notebook（单卡 H100 80GB）实测端到端 < 5h wall-clock，含模型加载与基础设施开销的安全边际（对标：#2 约 4.5h 跑完、#5 预留 540s 边际）——依据：[W2][W4] 一手 + [arXiv]（约束原文二手）
- [ ] **三级时间预算落地**：全局/单题/单尝试超时三级硬上限 + 最小共识早停（含"尾随不可反超即停"式动态早停）写入 harness——依据：[W2][W4] 双源一手互证
- [ ] **答案抽取鲁棒性**：流式 \boxed{} 扫描/截断恢复/答案格式前置校验（整数/范围/逗号）有专门测试用例——依据：[W2] README
- [ ] **私榜过拟合防控**：不以公榜为唯一改进指标；建立外部独立验证题集 + 全文错误语料与归类闭环（对标 #3：1120 条语料 + 50 外部题 + 问题难度分层假设）——依据：[W3] §1.2–2.1 一手
- [ ] **离线增益在线复验**：任何离线调出的提示/参数增益，须在比赛同构环境（同模型同预算）复验通过后才计入决策（#5 教训：64×H100 分诊大部分收益未迁移）——依据：[W4] §3 原文
- [ ] **提交预算"彩票"管理**：保留多次未修改基线提交（同族 σ≈1.7 下 13 次提交 max≥44 概率≈28% vs 单次 2.3%），不把全部预算押在"改进版"上——依据：[arXiv] §8（二手代理，量级参考而非精确规划数）
- [ ] **默认排除清单**：提示多样性/提示压缩/工具菜单扩张/attempt 级反思不作为首轮投入方向（两独立来源证伪）——依据：[W4] what didn't work + [arXiv]
- [ ] **提交自包含**：计时提交零外部依赖（强模型仅限场外分诊且分诊产物不依赖专有题集可复现）——依据：[W4]（其对 GPT-5 场外过滤的可复现性批评亦一并吸收）
- [ ] **公开共享包**：writeup + HF 仓库在获奖核验前就绪（训练数据/脚本/权重可复现口径对齐 [FAQ] §8.2），并保留人机分工记录（本仓库 AGENTS 合规底线）——依据：[公] + [FAQ]

## 六、对本框架的启示（4070 laptop 单卡画像的如实评估 + Kaggle-竞赛 track 现实定位）

- **本地硬件不构成参赛硬门槛，构成迭代方式约束**：评测算力由 Kaggle 挂赛 H100 承担（[K-site] "H100 only for notebooks attached to this competition"）；本地 4070 laptop 无法本地服务 gpt-oss-120b 级模型（同族服务配置需单卡 80GB 级显存，[W1] 实抓配置），本地角色 = 工程件开发 + 小模型代理迭代，真实约束验证在 Kaggle 环境完成。
- **工程侧创新恰好落在胜负层**：五队模型同族、算法层无代差，名次由工程鲁棒性（时间预算/抽取/聚合/调度）与验证闭环决定（第三节）——这些组件模型无关、可在本地完整开发测试，是本画像下少数可全流程自主交付的创新位。
- **必须内化的反外推纪律**：[arXiv] "模型能力碾压推理期优化"（二手代理）+ #5 离线增益未迁移（一手）双重证据 ⇒ 本地小模型代理实验得出的"推理期技巧"结论不可直接外推；本框架若走此 track，验收清单必须含"Kaggle 同构环境复验"项（第五节已派生）。
- **Kaggle-竞赛 track 的现实定位**：① 可及性证据——#3 单人参赛以学习为目的拿 3rd（[W3]），头部生态开源可复现（整栈公共 notebook + HF 仓库）；② 风险证据——同族 σ≈1.7 下顶部 1 题差距在噪声内（[arXiv]）⇒ 名次结果含不可控方差，框架不承诺名次目标，交付物定位为"稳健完成 + 可复现工程贡献 + 合规 writeup"（对齐 AGENTS 边界备忘"不承诺自动解题获奖"的同一诚实标准）；③ 参赛策略默认继承 [arXiv] §11 口径（最大可用开源模型 + 高温自洽 + 提交预算分散），作为基线而非创新声明。
- **合规栈**：开源模型/工具 + 自包含提交 + 公开共享（writeup/HF）+ 人机分工记录——与本仓库"AI 辅助原创"底线和开源栈天然兼容；Rules 全文（许可类型/开源截止/时限原文）直抓前，相关检查项保持"待补核"状态。
- **刷新点**：#1/#7 writeup 正文经 Browser Use 预抓后，刷新第二节（#1 专属工程件升级为一手、#7 补深构）与第三节（差异化证据链）；Extra Prizes 得主与 Proof Pilot 结果入库后补充评审偏好节；AIMO 4 若开赛，以同版式新建条目检验本模式库跨届稳健性。

## 数据缺口与待刷新（超出模板六节，如实记录）

1. **#1/#7 writeup 正文未取得**（SPA 壳，快照在 `kb/raw/<id>/winners/`）：#1 的 prefix caching/verification-assisted 等专属细节、#7 全部方案细节为二手/不可核——待主会话 Browser Use 预抓后刷新第二、三节相应行。
2. **私榜分数表非官方直抓**：46/45/44/43.5/42 出自 #5 TAMU-TACO HF writeup.md（参赛者一手），Kaggle leaderboard 原件未取得；若官方分数口径不同，第三节数字须订正。
3. **[arXiv] 代理定位**：与五队身份映射未确认（v1 完整/v2 截断），其消融与统计只作同族生态证据，不归属任何获奖队；含它的结论置信度均按"中"处理。
4. **单届局限**：仅 2026 届深构；AIMO1/2 获奖方法未入库，"共享基线+工程决胜"是否跨届成立未知——K-02 消费时按单届模式引用。
5. **Kaggle Rules 全文**（开源许可类型/模型可用日期截止/运行时限原文）与 Extra Prizes 得主：SPA 阻断未直抓，第五节相关检查项依赖补核。
