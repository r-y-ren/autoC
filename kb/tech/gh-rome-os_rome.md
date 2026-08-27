---
id: gh-rome-os_rome
name: "Rome: 面向人机协作的 Agentic OS 与可安装 App 模型"
field: [LLM agents, agent 工程化]
directions: [黑客松与数据竞赛]
published: "2026-08-23"
maturity: product
signal:
  venue: GitHub
  stars: 370
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "需要 24-48h 交付'一个带 UI、持久数据、定时任务的 AI 助手产品'的黑客松：Rome App 模型（app.yaml 清单 + 类型化 actions + app 私有 agents/skills/hooks + 持久数据库 + 专用 Web UI）把常见'聊天 demo'升级成'装得住的应用'，且产物是 git 跟踪的普通源码而非隐藏模型状态——答辩可讲'agent 自举扩展自身环境、能力复利'的叙事，这是拼 Next.js+agent+DB 手工作坊拿不到的差异化"
    reuse_cost: "中"
    open_source: "https://github.com/rome-os/rome（MIT，Docker quickstart + App Store + 云服务 preview）"
sources:
  - url: https://github.com/rome-os/rome
    title: "rome-os/rome: The agentic OS for humans and agents"
    accessed: "2026-08-28"
  - url: https://romeos.cc/docs/building-apps
    title: "Rome 官方文档：Building Rome Apps"
    accessed: "2026-08-28"
---

# Rome：把 agent 环境做成操作系统的"App/能力"模型

## 是什么

rome-os 组织（配 X 账号 RomeAILab、Discord、官网 romeos.cc）2026-08-23 开源的 TypeScript pnpm monorepo（MIT，实测 16 个包：core/web/desktop/mobile/app-runtime-sdk/app-web-sdk 等，2026-08-28 实抓 contents API）。定位"agentic OS"：一个护栏化环境，人类与 agent 协作且协作可复利——agent 自建 harness、自设计 SOP、编排工作流，"被验证的能力"沉淀复用。核心抽象是 **Rome App**：以 app.yaml 清单打包类型化 actions、app 私有 agents/skills/hooks、专用 Web UI、持久数据库与文件，成为可从 App Store 安装分享的产品；"工作流是动词，App 是名词"。用自然语言描述需求，Rome 生成规格、脚手架并在同一会话持续迭代，产物是 git 跟踪的源码。两个公共 SDK（@rome-os/app-runtime、app-web-sdk）支撑第三方开发（来源：https://github.com/rome-os/rome README 实抓 2026-08-28）。

## 解决什么问题

chat 界面只适合一次性请求：重复性工作（代码评审循环、邮件分诊、价格监控、晨报）需要有自己的"住所"——可记忆的收件箱、可检查的循环、持久数据与定时任务；现有 agent 产品把能力锁在隐藏模型状态里，无法积累、审计与分享。

## 相比前方法优势

- 相比 chat 套壳：App = 专用界面 + agent 推理 + 可复用工作流 + 持久数据四合一，"对话结束后依然有用"；
- 相比自拼 agent 栈：能力以 git 源码形式沉淀（可审计、可私有演化、可发布），而非平台私有状态；
- 相比单发 workflow 工具：capability 作为可被发现复用的单元，后续工作自动组合既有能力，形成自演化环。

## 局限（如实标注）

- **平台极年轻**：仓库 2026-08-23 创建（5 天龄 370 star，组织化推广明显：官网/云服务/App Store/Discord 全套），13 个 open issue；云服务仅 preview，自托管走 Docker（实测 README 有 quickstart 脚本，绑定 loopback、状态存 named volume）；
- 开发环境要求 Node 24+ / pnpm 11.6 / Docker，且默认连接 romeos.cc 云端（需设 ROME_DEV_PANTHEON_ORIGIN 指向别处）；
- 黑客松评审可能追问"底座平台挂了怎么办"——作为比赛底座存在平台成熟度风险，maturity 标 product 仅因云服务+分发渠道已上线（preview），不代表稳定；
- MIT 许可允许比赛使用，但 App Store 分发生态属官方云，赛场演示优先 Docker 自托管。

## 如何用于比赛

1. **AI 助手类黑客松（主用）**：赛题要求交付"可持续运行的 AI 产品"而非一次性 demo 时，用 Rome App 模型省掉 UI+持久化+调度三件套的胶水工作：把精力押在领域 agent 逻辑与数据源上。差异化叙事 = "agent 自己把缺的 App 建出来"（README 自演化环，抓取 2026-08-28）。reuse_cost 中：Docker 一键起，但需预拉镜像与验证断网可用性。
2. **架构借鉴（不依赖平台）**：即使不用 Rome 本体，其 app.yaml 清单设计（actions/agents/skills/hooks/持久态作为一等公民）可直接搬作自研 agent 项目的模块规格——评审看得见工程结构而非 prompt 堆砌。
