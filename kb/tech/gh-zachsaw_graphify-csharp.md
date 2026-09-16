---
id: gh-zachsaw_graphify-csharp
name: "graphify-csharp：给 LLM 编码 agent 的编译器级 C# 语义导航（Rider 语义切片的无头导出）"
field: [LLM agents, 代码智能, 开发者工具]
directions: [黑客松与数据竞赛]
published: "2026-09-08"
maturity: demo
signal:
  venue: "GitHub"
  stars: 64
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 主力写码的黑客松工程流（C#/.NET 技术栈赛题：微软系/企业赛道）：dotnet tool 一装 + 官方 SKILL.md 一下，当日让 Claude Code/Codex 对陌生大代码库回答『谁调用了这个重载/这接口谁实现/哪些方法只有测试在用（死代码）』且答案是编译器级证据而非文本匹配猜测——legacy 重构类赛题这是硬能力差；附带可迁移元模式：『领域工具语义证据导出成 JSON 给 agent 查 + skill 文件分发用法』，Python 队工具链可直接套用"
    reuse_cost: 低
    open_source: "https://github.com/zachsaw/graphify-csharp"
sources:
  - url: https://github.com/zachsaw/graphify-csharp
    title: "仓库主页 + README（gh api 实抓：创建 2026-09-08，最后 push 2026-09-15，64★/1 fork，MIT，语言 C#，release 迭代至 v0.1.10，CI 在库）"
    accessed: "2026-09-16"
---

# graphify-csharp：把 Rider 级 C# 语义导航导出成 LLM agent 可查的编译器级证据图

> 来源：https://github.com/zachsaw/graphify-csharp （GitHub API 仓库元数据 + README 全文实抓，抓取日期 2026-09-16；以下引述均出自本次抓取）

## 是什么

一个**无头（headless）Roslyn/MSBuild 索引器**：把 C# 源码变成确定性的、可查询的语义证据 JSON（README 口径，2026-09-16 实抓）——

- 产出单文件 JSON（`nodes`/`edges`/`hyperedges`），内容是**编译器解析**的调用方、引用、接口实现、继承、重写关系，跨重载、泛型、项目仍能对准符号；
- 自我定位："Rider/ReSharper 的语义导航切片，导出给 Codex、Claude Code 等编码 agent"（README：*the semantic-navigation slice of Rider/ReSharper, exported for Codex, Claude Code, and other coding agents*）；
- 交付形态：`dotnet tool install --global Graphify.CSharp`（NuGet 包，target net10.0），一条命令对 `.sln`/`.csproj`/SDK 风格单文件索引；
- **agent 原生分发**：官方自带两份 SKILL.md（Codex 走 `.agents/skills/`、Claude Code 走 `.claude/skills/`），curl 下载即把"何时刷新索引、如何沿语义边走、静态分析的边界"教给 agent；
- 工程质量：CI workflow 在库，release 已迭代至 v0.1.10（2026-09-16 tags 实核），MIT、无数据库、无 IDE 依赖。

## 解决什么问题

文本搜索回答不了"哪个重载被绑定、调用方属于哪个项目、接口的哪个实现才是这个符号"。README 对照表：无语义索引时"同名即用法、重载/泛型含混、test-only 用法靠人工逐个看、类型关系从文本重构"；有语义索引时每条调用携带编译器解析的声明、项目/TFM 身份与源码位置，`inherits`/`implements`/`overrides` 是显式边。README 示例：仓库内部一个 `ForTesting(...)` 方法在图中只有一条编译器解析的入边，调用方精确到测试类与行号——让 agent 从"猜"变成"查证据"。

## 相比前方法优势

- **vs 文本 grep**：编译器解析语义，重载/泛型/跨项目消歧，"找出所有调用方"从字符串匹配变为符号级事实；
- **vs IDE 工具链（Rider/ReSharper）**：无 IDE、无许可证、无需编译出项目 DLL、无数据库（README 明列 *MIT · No IDE · No compiled project DLL required · No database*），可在 CI/无头环境跑；
- **vs 通用代码图工具**：产物是 agent 可直接读/jq 查的 JSON，且"工具 + SKILL.md 用法说明"一体化分发——把使用方法本身做成 agent 可安装的知识，是少见的 agent 原生包装模式。

## 局限

- **C#/.NET 专属**（工具本身 target net10.0）：对 Python/MATLAB 主流的数模、Kaggle、ACM 工作流零直接复用；
- 索引前提是**本地可还原的 MSBuild 工程**（README："The repository's SDKs, packages, and MSBuild inputs must be available locally"）——零散代码片段无法索引；
- **静态证据不等于运行时事实**：README 自我告诫"zero inbound edges 是观测到的静态证据，不是运行时不可达的证明"（反射/动态调用不在图内）；
- 成熟度早期：v0.1.x、创建仅 8 天、1 fork、无第三方采用记录（2026-09-16 gh api 实核），API 与产物格式可能仍变动。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松数据与算法中**技术栈为 C#/.NET 的工程题**（微软系/企业赛道黑客松、legacy 系统重构题），以及一切"用 Claude Code/Codex 主力交付软件"的黑客松工程流。
- **打法**：
  (a) C# 赛题开题第一件事装工具 + 下 skill（两条命令），让 agent 全程对代码库做符号级问答与死代码/测试专用方法排查——评审演示"agent 维护陌生大代码库"时是实打实的能力差；
  (b) **元模式迁移**（对所有技术栈成立）：把领域工具的编译/语义证据导出成结构化 JSON 给 agent 查询 + 用 skill 文件分发用法——本框架的 scripts/kb 工程流可直接复刻这一分发形态；
  (c) legacy/重构类赛题中"找死代码、找仅测试引用的方法、列接口实现清单"常是隐含评分点，语义图的一等查询恰好就是这三件事。
- **成本**：reuse_cost=低——全局 dotnet 工具一条命令、无库无服务、索引产物为单 JSON；主要前置是工程能本地还原。
