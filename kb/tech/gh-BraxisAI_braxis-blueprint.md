---
id: gh-BraxisAI_braxis-blueprint
name: "braxis-blueprint: 零预算免费 LLM 通道路由与自动化运维的实战脚本集"
field: [LLM agents]
directions: [黑客松与数据竞赛]
published: "2026-08-23"
maturity: demo
signal:
  venue: GitHub
  stars: 83
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "零预算学生队的多 LLM 流水线保活组件：llm_router.py 在 20+ 免费通道（Groq/NVIDIA NIM/Gemini/Mistral/Zhipu/OpenRouter :free/本地 Ollama）上做任务链式回退+冷却+死模型追踪+免费额度强制，赛期免费额度被打爆时流水线不断供；cronwrap.sh 的 flock 单实例+超时击杀模式直接套在无人值守数据管道上；七条生产故障类复盘可当 agent 管线可靠性检查表"
    reuse_cost: "低"
    open_source: "https://github.com/BraxisAI/braxis-blueprint（MIT）"
sources:
  - url: https://github.com/BraxisAI/braxis-blueprint
    title: "BraxisAI/braxis-blueprint: The $0 AI Empire Playbook"
    accessed: "2026-08-28"
  - url: https://raw.githubusercontent.com/BraxisAI/braxis-blueprint/main/README.md
    title: "README 全文（组件表/架构/七条故障类/作者自述局限）"
    accessed: "2026-08-28"
---

# braxis-blueprint：零预算免费 LLM 通道路由与自动化运维的实战脚本集

## 是什么

BraxisAI 于 2026-08-23 开源的"零预算 AI 自动化"实战脚本集（83 star/13 fork，API 实查 2026-08-28；MIT，作者称全部脚本当日仍在生产运行）：单创始人一年全用免费额度/开放权重搭起 140+ 自主 agent、20+ 免费 LLM 通道、1800+ 首歌曲、5 平台日更内容与 3D 世界（README 实抓 2026-08-28）。对赛队有直接复用价值的核心文件：llm_router.py（任务链式回退、冷却、死模型追踪、自优化模型调参、免费-only 强制）、cronwrap.sh（flock 单实例守卫 + 超时击杀，治"重复进程级联"故障类）、backup.sh + backup_upload.py（本地轮转 + 对象存储异地 + 已验证恢复的三副本），以及七条生产故障类复盘。基建为 Oracle ARM 免费层 24GB VM + SQLite WAL（单写者 flock 守卫）+ 约 107 个 cron 作业，附 live demo（3D 世界/虚拟市长/内容机）可点验。

## 解决什么问题

没有预算时的多 LLM 流水线可靠性：免费通道天然高波动（作者实录 SambaNova 免费层一夜变付费、Groq 退役 llama-70b），单通道依赖会让流水线静默死亡；无人值守 agent 常驻场景又把定时任务的经典故障（重复进程、僵尸循环、静默失败）放大。

## 相比前方法优势

- 相比单提供商接入：通道级回退 + 死模型追踪 + 自优化调参把"供应商退役模型"从事故变成自动降级；
- 相比框架类教程：这是带故障复盘的生产脚本——每条故障类都有"怎么死的、怎么修死的"（如：质量门必须检查"包裹"而非"文风"，4 天零点击后改为"无链接不发送"；auto-reply 不算线索，一个 stop 永久拉黑；本地时钟对比 UTC 窗口导致发送端自我静音）；
- 相比一般 playbook 的 PPT 化：脚本 + live demo + 失败清单三层都有实证物。

## 局限（如实标注）

- 商业侧未验证：作者自认"还没赚到第一笔 19 美元"，营收自动化组件（冷邮件/Stripe/TikTok 通道）只有工程没有成效证据；
- "140+ agents" 为作者自述口径，README 层面无法逐一点验，叙事带明显营销味（"$0 AI Empire"）；
- 与作者个人业务深度耦合，可干净抽用的核心是 llm_router.py / cronwrap.sh / backup 三件，其余（求职机/虚拟市长/内容机）需按需拆解；
- 单人项目、无测试体系说明，脚本质量未经第三方检验；免费通道的合规与稳定性风险由使用者自担（其自述免费层随时变脸）。

## 如何用于比赛

1. **黑客松/数据竞赛的零预算基建（主用）**：赛期把 llm_router.py 抽出来做全部 LLM 调用的统一入口——免费额度冷却时自动切换通道，避免"跑到一半没 token"的赛场事故；cronwrap.sh 模式套在任何无人值守数据管道上防重复进程。reuse_cost 低：文件独立、MIT，读一遍故障类清单即可上手。
2. **agent 可靠性自检表**：七条故障类（静默 import 杀通道、时区钟、假回复计数、数据中心 IP 被社交站 403 需住宅 IP 通道等）直接作为带 agent 环节参赛作品的自检清单，逐条过一遍再交作品。
