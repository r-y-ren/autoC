---
id: arxiv-2609.20625
name: "Chronicle：agent 失败的 cut-point 回放回归测试（零模型调用进 CI）"
field: [LLM agent, 回归测试, record-replay]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-09-17"
maturity: demo
venue_tier: arXiv
reproducibility_level: high
signal:
  venue: "arXiv（Comments：摘要末尾自述 Chronicle 与 benchmark 公开于 github.com/theagentplane/chronicle）+ GitHub 实抓（22 stars，MIT，2026-09-20 API）"
  stars: 22
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "agent 作品『演示时好、评审复跑时崩』是黑客松高频翻车点：Chronicle 把一次失败运行在非确定性边界处录成 immutable envelope，cut-point replay 让『修过的 bug 不复发』变成 CI 里的回归测试——全回放零模型调用且 20 次重复比特稳定，录制开销每边界仅 23μs；mutation study 中 cut-point 测试捕获全部放行危险动作的变异体、而同等断言的 stub-everything 基线捕获为零；MIT 代码，赛期最后半天给作品补『可复跑』工程背书，答辩现场演示故障复现极有说服力"
    reuse_cost: 低
    open_source: "https://github.com/theagentplane/chronicle（MIT；仓库描述自述 record-and-replay for agent decision graphs）"
  - track: "双创-文书与申报"
    edge: "申报/路演的工程质量模块：产品 demo 附 CI 级 agent 回归测试是同类『AI+』项目几乎无人有的差异化亮点，直接回应评委对 LLM 产品不可测试、不可维护的惯性质疑"
    reuse_cost: 低
sources:
  - url: https://arxiv.org/abs/2609.20625
    title: "Chronicle: Cut-Point Replay for Regression Testing of LLM Agents（arXiv export API 实抓：2026-09-17；immutable envelope/cut-point replay/23μs 每边界/全回放零模型调用 20 次比特稳定/6 失败基准/mutation study 全捕获 vs stub 基线零捕获/开源链接均出自摘要原文）"
    accessed: "2026-09-20"
  - url: https://github.com/theagentplane/chronicle
    title: "theagentplane/chronicle 仓库实抓（GitHub API 2026-09-20：22 stars，MIT，描述『Record-and-replay for agent decision graphs: reproduce a prod agent failure as a committed regression test, and re-run your fix without live LLM calls』）"
    accessed: "2026-09-20"
---

# Chronicle：把 agent 的一次线上失败变成 CI 里零成本可复跑的回归测试

> 来源：https://arxiv.org/abs/2609.20625 （arXiv export API 实抓，抓取日期 2026-09-20；仓库元数据 GitHub API 同日实抓。以下分析基于本次抓取的摘要原文）

## 是什么

LLM agent 的回归测试工具（摘要口径）：模型响应非确定性 + 工具读变化状态 + 多步轨迹难复现，使 agent 故障几乎无法稳定重放；现有 record-and-replay 工具只用于追踪或打分，不能用来测代码改动。Chronicle 在 agent 运行的**非确定性边界**（模型调用等）处把运行录成不可变 envelope，回放时从记录取数。核心操作 **cut-point replay**：边界的一个子集从记录中供给、补集用新代码真实执行——于是"一次录得的线上事故"变成一个能在 CI 里跑的回归测试：被测逻辑走新代码、其余世界保持录制时的确定性。实测：录制每边界 23μs（占假设 300ms 模型调用的 0.008%）；全回放零模型调用、20 次重复比特稳定；6 个录制失败的基准上，cut-point 测试对故障代码失败、对带守卫与无害改动通过；变异测试中捕获全部"放行已录危险动作"的变异体，而逐边界 stub 的同断言基线一个都抓不到。代码与基准公开（MIT，theagentplane/chronicle，22 stars，2026-09-20 实抓）。

## 解决什么问题

"修好了"在非确定系统里不可断言：重跑一百次都对也不代表 bug 被修住。Chronicle 让 agent 修复获得与确定性软件同等的回归测试语义。

## 相比前方法优势

- **选择性回放**（部分边界真实执行）是与全录制全回放的本质区别——只有这样才能"测新代码"而非"重放旧世界"；
- **零模型调用**的 CI 成本：回归测试不烧推理费、不出抖动（比特稳定），可在每次 push 跑；
- **断言力可证**：mutation study 给出 stub 基线 0 捕获 vs cut-point 全捕获的对照，不是感觉上的"更稳"；
- 录制开销 23μs/边界，生产路径可常开。

## 局限

- 基准仅 6 个录制失败且模型边界为模拟（摘要口径）——规模小，真实生产轨迹上的召回未证；
- 22 stars 早期项目（2026-09-20 实抓），API 稳定性与文档深度未知；
- 前提是 agent 边界清晰可拦截（模型调用、工具调用处）——高度内联/黑盒 API 的 agent 需改造接入；
- 本卡止于摘要层。

## 如何用于比赛（比赛映射展开）

- **适用赛种**：黑客松-数据与算法（任何 agent 类作品）；双创-文书与申报（工程质量叙事）。
- **打法**：
  (a) **赛前录制护栏**：开发期把踩过的坑录成 envelope，提交前在 CI 跑 cut-point 测试——评审复跑环境即使断网/换模型，核心修复路径仍可证明；
  (b) **答辩演示**：现场"复现当时故障→展示修复→跑零模型调用回归测试通过"三连，是对"LLM 作品不可测"质疑的最硬回应；
  (c) **低成本接入**：录制开销可忽略，只需在模型/工具调用边界包一层 recorder。
- **成本**：reuse_cost=低——MIT 代码可得，接入点明确（非确定性边界）；主要工作量是把自家 agent 的调用边界暴露给 Chronicle。
