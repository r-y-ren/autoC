---
id: gh-joe960913_Jixu
name: "Jixu：TypeScript 持久化单 Agent Harness（事件溯源 Thread，可恢复/重放/分叉）"
field: [LLM agents]
directions: [黑客松与数据竞赛]
published: "2026-08-18"
maturity: demo
signal:
  venue: GitHub
  stars: 117
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agentic 黑客松作品最怕评委一问'agent 跑一半崩了/断网了怎么办'——Jixu 把崩溃恢复、断点续跑、确定性重放、从任意事件分叉做成 SDK 内建能力（durable Event → 纯 Reducer → 显式 Effect → Driver 单一执行路径，事件溯源存储），npm 装 jixu-core + jixu-store-sqlite 即嵌入，省掉自研 checkpoint/审计工程一整个模块；Context Manifest（记录每次模型请求选了什么上下文、为什么）与不可改写事件史可直接当'可审计 agent'的演示亮点，对比对手的手写 while 循环 agent 是可靠性维度的代差"
    reuse_cost: "中"
    open_source: "https://github.com/joe960913/Jixu（MIT，npm jixu-core 0.4.1 / jixu-ai，实查 registry 2026-08-28）"
sources:
  - url: https://github.com/joe960913/Jixu
    title: "joe960913/Jixu: Durable single-Agent Harness for TypeScript"
    accessed: "2026-08-28"
  - url: https://registry.npmjs.org/jixu-core/latest
    title: "npm jixu-core 0.4.1（runnable 实核）"
    accessed: "2026-08-28"
---

# Jixu：把"崩溃后继续"做成一等公民的单 Agent Harness

## 是什么

joe960913 2026-08-18 开源的 TypeScript 单 Agent 框架（MIT，pnpm monorepo：packages/、evals/、SPEC.md、ARCHITECTURE.md 实抓确认 2026-08-28；npm `jixu-core` 0.4.1 已发布）。核心 API 只有三个：`createHarness` / `createThread` / `thread.send`，但 Thread 之下的执行被记录为**有序不可变事件**：状态是事件的纯归约投影，外部副作用（模型调用、工具调用）先记录后派发。由此 Thread 支持 `pause/continue/interrupt/clear/replay/fork` 全套连续性操作——`replay()` 零真实 Driver 调用从事件重建状态，`fork({at, input})` 从任意事件的确切状态分叉子线程。配套：jixu-llm（OpenAI Chat Completions / Anthropic Messages 双 Driver）、jixu-store-jsonl / jixu-store-sqlite 两种事件存储、jixu-tools-node（文件+本地 shell）、jixu-tools-jina（联网搜索/读页）、jixu-testkit（确定性测试夹具）、可安装的参考 TUI（npm `jixu-ai`）。仓库自带 evals/ 目录与 skills-lock.json（技能机制）。

## 解决什么问题

agent 循环易启动、难安全恢复：工具调用可能 in-flight、进程可能写在半路停掉、模型上下文可能耗尽——而这些恰是"agent 干长活"（数小时自主跑批、无人值守任务）的死穴。Jixu 用事件溯源把"恢复"变成确定性操作：外部工作先记录再派发，未知非幂等结果进入 `waiting` 而非被静默重试；工具审批（allow/ask/deny）是对单个 pending Effect 的持久化决定。上下文工程侧：请求前解析模型的上下文窗口/输出上限（未知即停止而非猜测），压缩时写源链接的 Continuity Handoff 且不改写底层事件；每次请求附 Context Manifest 记录"选了什么、为什么"。

## 相比前方法优势

- **对比手写 agent 循环**：恢复/重放/审计不用自研——事件溯源 + 纯 Reducer 保证 replay 是确定性的，崩溃后 `continue()` 从安全边界续跑；
- **对比多 Agent 编排框架**：明确不做 workflow 图/supervisor/第二执行引擎（README "What Jixu is not" 一节），单一权威执行路径换来可推理性：逻辑模型调用与派发尝试分离、token 用量缺失值不渲染为 0、密钥永不进事件/状态/错误；
- **诚实的边界声明**：不宣称通用 exactly-once（需下游幂等契约），确定性工具失败记录后作为失败结果交还 agent 同轮自愈——这类如实标注在框架类项目里少见。

## 局限（如实标注）

- **pre-1.0**（官方明示 public API 可能变动，npm 0.4.1）；
- **Bash 工具无 OS 级沙箱**（官方 WARNING：以 Jixu 进程权限运行，权限控制批的是工具调用而非单条 shell 操作，建议保持 ASK + 一次性工作区）；
- **参考 TUI 仅支持 macOS arm64 与 Linux x64 (glibc)**，Windows 无原生 TUI，Intel Mac 不支持；Node ≥ 22.19；
- 单 Agent 模型：无多 Agent 编排/调度/队列，需要 supervisor 结构的项目不适配；
- 项目极年轻（创建于 2026-08-18，抓取时 117 stars / 7 forks），无第三方生产验证。

## 如何用于比赛

1. **agentic 黑客松的可靠性底座（主用）**：凡作品含"agent 自主多步干活"（自动调研 bot、自动数据清洗/特征工程管线、无人值守运维 agent），用 Jixu 做骨架，演示时**故意 kill 进程再 `continue()`**——评委直观看到对手方案做不到的恢复能力；事件史+Context Manifest 天然回答"你怎么证明 agent 没乱来"。reuse_cost 中：SDK 嵌入需按其 Thread API 写 agent 逻辑（非一行接入），但省下的 checkpoint/审计自研工程远超此成本。
2. **fork 做 A/B 策略对比**：从同一事件分叉两条 Thread 跑不同 prompt/策略，确定性重放保证对比公平——评审/答辩环节的现成方法论。
3. **环境注意**：参考 TUI 不支持 Windows，赛队演示环境选 Linux/macOS，或只用 jixu-core SDK 自建 UI（TUI 与应用共用同一套公开 API）。
