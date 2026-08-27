---
id: kaggle-ai-mathematical-olympiad-progress-prize-3
name: "AI Mathematical Olympiad – Progress Prize 3（AIMO 3）"
tier: 编程/黑客松
directions:
  - 黑客松与数据竞赛
status: ended
organizer: "XTX Markets（AIMO Prize 设立与资助方；总基金 $10mn、Grand Prize $5mn）；Kaggle 承办；奖项由 Advisory Committee 设计"
award_levels:
  - name: "Overall Progress Prize Winner"
    count_or_ratio: "≥ $1,589,248（若颁出；Kaggle 页快照口径，'if awarded'）"
    note: "达 IMO 金牌级才触发的系列 Grand Prize（$5mn）另计，不属本赛已发奖项"
  - name: "1st Place"
    count_or_ratio: "$262,144"
  - name: "2nd Place"
    count_or_ratio: "$131,072"
  - name: "3rd Place"
    count_or_ratio: "$65,536"
  - name: "4th Place"
    count_or_ratio: "$32,768"
  - name: "5th Place"
    count_or_ratio: "$16,384"
  - name: "Extra Prizes（Longest Leader Prize / Write-up Prizes / Math Corpus Prize / Hardest Problem Prize）"
    count_or_ratio: "金额未公布于本次所抓官方页；2026-06-24 公告确认本届追加了 best dataset（Math Corpus Prize）与 best write-ups 奖"
key_dates:
  launch:
    date: "2025-11-19"
    verified: false
    note: "launch 公告页原文 'has launched today on Kaggle'，官方 URL slug 为 2025-11-19；updates 索引页第二源仅月度 'November 2025'，日精度单源"
  entry_deadline:
    date: "2026-04-08"
    verified: false
    note: "单源：Kaggle 赛站搜索索引快照（SPA 未直抓）；另有 LinkedIn 二手同日，不并入官方双源"
  final_submission_deadline:
    date: "2026-04-15"
    verified: false
    note: "单源：Kaggle 赛站快照 'April 15, 2026 - Final Submission Deadline. All deadlines are at 11:59 PM UTC'"
  winners_announced:
    date: "2026-06-24"
    verified: false
    note: "官方公告 URL slug 2026-06-24 + updates 索引第二源仅月度 'June 2026' + Kaggle 官方 discussion #714435 同名单；无显式日期文本，日精度单源"
deliverables:
  - "Kaggle notebook 提交（H100 仅限挂靠本赛的 notebook：'H100 are only available for notebooks attached to this competition'；获奖方案实测约束为单卡 H100 80GB、Kaggle 5 小时 wall-clock、无外部 API——时限细节源自获奖 writeup 与 arXiv 论文二手，官方规则原文待核）"
  - "110 道 National Olympiad→IMO 难度原创数学题（AIME 风格、非负整数答案、答案五位数使猜测几乎不可能），公开榜 + 私榜评测"
  - "获胜方案公开共享：winners 公告确认提交已在 HuggingFace 发布；系列 FAQ 要求训练数据/训练脚本/模型架构与权重公开、第三方可复现"
ai_policy:
  summary: >-
    三层实抓：①系列 FAQ（2023-12-19，官方，"for the first progress prizes" 口径）——"competition
    entries may only use AI models and tools that are open source"（仅可用开源 AI
    模型与工具，如 Llama/Gemma 公开权重；设可用日期截止），"There will be no restrictions on AI
    models during training"（训练期不限），比赛期则 "may be some restrictions on AI models
    during competitions (e.g. time limit, compute limit, length of solutions)"；②AIMO
    3 Kaggle 赛站（快照口径）——载有 "rules for using open-source LLMs" 专节；"H100 are only
    available for notebooks attached to this competition"（算力与挂赛绑定）；③launch 公告——获胜方案必须公开共享（"all
    winning solutions to be publicly shared"），本届支持 GPT-OSS-120B、Qwen3-Next 等更大开源权重模型，胜作实测以
    gpt-oss-120b 为核心（winners 公告：多数队伍围绕该模型做 harness 与提示策略）。Kaggle Rules
    全文（开源许可类型、运行时限原文）为 SPA 未能直抓，如实标待核验；"单卡 H100 + 5 小时"口径来自获奖方案
    writeup/arXiv（二手，信源等级低于官网）。
  url: https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3
  checked: "2026-08-27"
credibility: 官网
last_verified: "2026-08-27"
sources:
  - url: https://aimoprize.com/updates/2025-11-19-third-progress-prize-launched
    title: "Third Progress Prize launched（$2.2mn 口径、Kaggle 链接、H100/128×H100 Fields Model Initiative 算力条款、Extra Prizes 名单、110 题五位数答案）"
    accessed: "2026-08-27"
  - url: https://aimoprize.com/updates/2026-06-24-aimo-3-winners-announced
    title: "AIMO 3 Winners Announced（五队名单与名次 #1/#2/#3/#5/#7、stricter rules、HuggingFace 公开、gpt-oss-120b 主导、Proof Pilot 启动）"
    accessed: "2026-08-27"
  - url: https://aimoprize.com/participate
    title: "Participate 页（AIMO3 增奖金/提难度/加算力；AIMO1=Numina、AIMO2=NemoSkills 前史；规则在 Kaggle）"
    accessed: "2026-08-27"
  - url: https://aimoprize.com/
    title: "AIMO Prize 首页（总基金 $10mn、Grand Prize $5mn 口径、第三届 2025-11 开放）"
    accessed: "2026-08-27"
  - url: https://aimoprize.com/updates
    title: "updates 索引页（winners 公告 June 2025→2026-06 月度佐证、launch November 2025 月度佐证）"
    accessed: "2026-08-27"
  - url: https://aimoprize.com/updates/2023-12-19-frequently-asked-questions
    title: "AIMO FAQ（§7.2 仅开源模型与工具、§7.1 训练不限/赛期时限算力限、§8.2 公开共享协议与可复现要求）"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3
    title: "Kaggle AIMO-3 赛站（SPA；总池 $2,207,152、1st–5th 名次奖金、entry 04-08/final 04-15 11:59 PM UTC、开源 LLM 规则节、H100 挂赛限制，均经搜索索引快照交叉）"
    accessed: "2026-08-27"
  - url: https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/714435
    title: "Kaggle 官方 winners 公示讨论（'We are pleased to announce the five winning teams of AIMO 3: Exalted Joseph, varianceofx, SKobayak, TAMU...'，快照口径）"
    accessed: "2026-08-27"
  - url: https://arxiv.org/html/2603.27844v1
    title: "Inference-Time Optimization Lessons from AIMO 3（获奖方案技术报告，二手：单 H100 80GB、5 小时 wall-clock、无外部 API 实测约束）"
    accessed: "2026-08-27"

---
# AI Mathematical Olympiad – Progress Prize 3（AIMO 3）— meta

## 概况（全部为 2026-08-27 实抓）

- XTX Markets 资助的 AIMO Prize 第三届 Progress Prize，Kaggle 承办，2025-11-19 launch，2026-04-15 最终提交截止，2026-06-24 公布获奖名单，**已结束**。
- 题面：110 道 National Olympiad→IMO 难度原创题（代数/组合/几何/数论），AIME 风格非负整数答案，五位数答案"making guessing essentially impossible"。
- 奖金：总池 **$2,207,152**（Kaggle 快照精确值；launch 公告 "$2.2 million" 官方第二源）。名次奖金 1st–5th 为 $262,144 / $131,072 / $65,536 / $32,768 / $16,384（2 的幂次递减）；Overall Progress Prize Winner（若颁出）≥ $1,589,248。
- 算力：Kaggle 提供 H100（"roughly double the compute power of AIMO2"），且仅限挂靠本赛的 notebook；遴选参与者可经 Fields Model Initiative 获至多 128 张 H100 微调算力（LLMC/NII 东京、Benchmarks+Baselines 维也纳），及 Thinking Machines 的 Tinker credits。
- 获奖五队（官方 2026-06-24 公告）：**Exalted Joseph（#1）、varianceofx（#2）、SKobayak（#3）、TAMU-TACO（#5）、yemao ye（#7）**——即公榜 #1/#2/#3/#5/#7；验证耗时较长因 "this year's stricter rules"，获奖提交已在 HuggingFace 公开。
- 技术面（公告口径）：榜单分数高度密集，多数队伍围绕 gpt-oss-120b（"exceptional, though hard-to-train"）构建 harness 与提示策略；社区产出约 100 万新数据点，"Several submissions matched the quality expected of peer-reviewed conference papers"。
- 后续：AIMO Proof Pilot（仅邀请，7 队 = 6 支 Extra Prize 获奖队 + Andreas Bisiadis），2026-06-26 上线、评分至 2026-07-05，测试开源 LLM 做完整数学证明并由人工评分；其获奖公告见 updates 索引 "AIMO Proof Pilot Winners Announced（July 2026）"。
- 前史（participate 页口径）：AIMO1 由 Project Numina 于 2024-07 获奖；AIMO2 由 NVIDIA NemoSkills 于 2025-04 获奖。

## 线索核对（对任务包线索，2026-08-27 复核）

- "2025-11-19 开赛"：成立（launch URL slug + 公告"今日开赛" + 索引月度佐证；日精度单源，已标 verified:false）。
- "获奖名单 2026-06-24 公布"：成立（官方 URL slug + Kaggle 官方 discussion 同名单；显式日期文本未见，已标 verified:false）。
- "总池约 $2.2M"：成立（$2.2mn launch 口径 + $2,207,152 Kaggle 精确值）。
- "五支获奖队 Exalted Joseph 等"：成立（官方公告原文名单）。
- "1st $262,144…"：成立（Kaggle 快照）。

## AI 政策原文（aimoprize.com，2026-08-27 抓取）

- "For the first progress prizes, competition entries may only use AI models and tools that are open source and were available before 23 February 2024."（FAQ §7.2，首届口径；AIMO 3 的对应日期截止以 Kaggle Rules 为准，未直抓）
- "There will be no restrictions on AI models during training. There may be some restrictions on AI models during competitions (e.g. time limit, compute limit, length of solutions)."（FAQ §7.1）
- "the training data, training script and final model (architecture and corresponding weights) should be made public"（FAQ §8.2，可复现要求）
- "H100 are only available for notebooks attached to this competition"（Kaggle 赛站快照）
- 获奖方案实测约束（二手，arXiv/writeup）："Our system runs entirely on a single H100 80 GB within Kaggle's 5-hour wall-clock limit. No external APIs, no multi-GPU setups, no pre-computed..."

## 信源与快照

- `kb/raw/kaggle-ai-mathematical-olympiad-progress-prize-3/2026-aimoprize-launch.html`
- `kb/raw/kaggle-ai-mathematical-olympiad-progress-prize-3/2026-aimoprize-winners.html`
- `kb/raw/kaggle-ai-mathematical-olympiad-progress-prize-3/2026-aimoprize-participate.html`
- Kaggle 赛站/规则页为 SPA，无有效静态快照；其事实经搜索索引快照与 aimoprize.com 官方页交叉后引用。

## 待核验清单

- [ ] Kaggle Rules 全文直抓（开源许可类型、开源 LLM 日期截止、运行时限/算力原文）——SPA 阻断，建议主会话 Browser Use 或 winners 深构分片时补。
- [ ] launch / entry / final / winners 四个日期的第二官方日精度源（Kaggle 赛站直抓后可升 verified:true）。
- [ ] 总池 $2,207,152 与名次奖金之和（$507,904）+ Overall（≥$1,589,248）的差额约 $110K 归属（疑为 Extra Prizes，未见官方拆分表）。
- [ ] Extra Prizes 各项金额与得主（Math Corpus Prize 得主 Yi-Chia Chen 为二手快照口径，未独立核实）。
- [ ] winners 深构分片入口：五队 HuggingFace 仓库 + Kaggle writeups（Entropy-Weighted Self-Consistency、Majority-First Tool-Augmented Reasoning 等）+ arXiv 2603.27844。
