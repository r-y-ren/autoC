---
id: gh-wolfiesch_omp-best-of
name: "omp-best-of: Best-of-N 候选 + LLM-as-a-Verifier 择优的编码 agent 编排插件"
field: [LLM agents]
directions: [黑客松与数据竞赛]
published: "2026-08-18"
maturity: demo
signal:
  venue: GitHub
  stars: 60
  runnable: true
competition_fit:
  - track: "Kaggle-竞赛"
    edge: "agent 辅助解题时把『单发提交』升级为『N 候选隔离生成 + 轨迹级验证器择优 + 仅应用赢家补丁』，降死线前坏提交率；MIT 参考实现给出完整工程骨架（脏树拒跑、COW 隔离、基线感知二进制安全补丁捕获、HEAD 守卫回写、CI 可用的 JSON 摘要），验证器核心在上游 llm-verifier（独立 Python 包）可脱离本插件直接复用——移植编排层即可接到任意 headless coding agent"
    reuse_cost: "中"
    open_source: "https://github.com/wolfiesch/omp-best-of（MIT）；验证器算法 https://github.com/llm-as-a-verifier/llm-as-a-verifier"
sources:
  - url: https://github.com/wolfiesch/omp-best-of
    title: "wolfiesch/omp-best-of: Best-of-N coding agents with LLM-as-a-Verifier selection"
    accessed: "2026-08-28"
  - url: https://raw.githubusercontent.com/wolfiesch/omp-best-of/main/README.md
    title: "README 全文（七步流程/双验证后端/选项表/作者自述可靠性边界）"
    accessed: "2026-08-28"
---

# omp-best-of：Best-of-N 候选 + 验证器择优的编码 agent 编排

## 是什么

wolfiesch 于 2026-08-18 开源的 Oh My Pi（OMP）编码 agent 插件（60 star/5 fork，API 实查 2026-08-28；MIT，CI 绿）：`/best-of --n 2-8` 一条命令在同一任务上并行跑 N 个候选 agent 会话（README 实抓 2026-08-28）。七步流程：preflight（脏树拒绝、记录 HEAD）→ 按 COW 后端（必要时回退 git worktree）开 N 个隔离工作区 → 每区跑一个 headless OMP 会话（JSON 事件模式）→ 基线感知 delta 捕获产出二进制安全补丁 → 排序（默认 logprob 后端：经上游 llm-verifier==0.2.0 的 Kwok et al. 锦标赛算法，从 score-token 分布算连续期望分，默认评分端点 deepseek/deepseek-v4-flash；备选 sampled 后端：走 OMP 订阅模型的成对评审，不烧 API 点数）→ 仅当 --apply 且父仓 HEAD/status 未变才应用赢家补丁 → 无论成败清空隔离区、工件永久保留。非零退出/无法捕获补丁的候选在排序前剔除；另有独立 CLI 形态（stderr 进度 + stdout JSON 摘要）供脚本与 CI 调用。

## 解决什么问题

采样多个解提高"至少一个对"的概率，但"选出那个对的"是另一个独立问题。本插件把选择做成可插拔验证器（连续 logprob 锦标赛或采样成对评审），并用工程护栏（隔离、HEAD 守卫、失败候选剔除、工件留存）保证择优过程可控可审计。

## 相比前方法优势

- 相比 best-of-N 后靠人眼看 diff：验证器按评分端点/订阅模型自动排序，评测可重复（--evaluations、--pivots、--seed 全部暴露为 CLI 参数）；
- 相比直接在主 checkout 里跑 N 个 agent：COW 隔离 + 脏树拒绝 + 仅 HEAD 未变时回写，杜绝候选互相污染与"择优期间仓库又动了"的竞态；
- 自检链路完整：sampled 模式按"最便宜的先失败"排序（仓库检查 → 本地沙箱预检 → 一次付费能力探针），预检失败不启动任何候选子进程、不产生任何模型调用。

## 局限（如实标注）

- 绑定 Oh My Pi 生态：需 omp 17+、Bun 1.3+、uv、score-capable 端点（logprob 后端要求端点通过 constrained-prefill 能力探针，兼容自托管 vLLM/SGLang）——换 Claude Code/Codex 等其他 agent CLI 需移植编排层（验证器核心 llm-verifier 是独立 Python 包，可直接用）；
- 作者自述"未建立与上游论文等同的可靠性"：benchmark 结论属上游作者；sampled 后端明确"不是论文连续评分法的复现"，只是常规成对评审；
- 验证器只做选择不保证正确：selection quality 取决于候选质量、评审标准、验证器模型与端点（作者自述）；
- 社区小且有停更迹象：60 star/5 fork、5 个 open issue、08-20 后无推送（API 实查 2026-08-28）。

## 如何用于比赛

1. **Kaggle 等算法竞赛的 agent 辅助解题（主用）**：赛期用 coding agent 批量产提交脚本时，以本插件为参考搭"N 候选 + 验证器择优"环——验证器可直接用上游 llm-verifier 按自定 rubric 给候选解打分，winner-only 回写避免坏提交覆盖好提交；有 OMP 栈的队当天可用，其他栈按其七步流程移植（隔离/补丁捕获/守卫逻辑均有现成实现可抄）。reuse_cost 中。
2. **比赛工程化模板**："preflight 拒脏树 → 隔离 → 产物留存 → 条件回写"的护栏编排，可迁移到任何"多个自动化产出择优入库"的赛题环节（多版本 solution 择优、多版报告择优、多参数配置择优）。
