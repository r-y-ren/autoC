---
id: arxiv-2608.23918
name: "MARS: Multi-Specialist LLM Relay System for Competitive Programming"
field: [代码生成, 多智能体系统, 竞赛编程]
directions: [黑客松与数据竞赛]
published: "2026-08-24"
maturity: paper
signal:
  venue: "EMNLP 2026（arXiv:2608.23918）"
  runnable: true
competition_fit:
  - track: "ACM-训练体系"
    edge: "『专题专家接力 + 沙盒样例验证』回路可直接改造成队内训练体系组件：训练复盘器（对队员提交给出专题专家修复轨迹）、按 cf_tag 检索算法理论语料的出题-批改 harness；repo 的 ExecEval 执行评分链可复用作队内 OJ 判题服务。注意合规边界——仅作训练/复盘工具，不用于赛场自动提交"
    reuse_cost: "中"
    open_source: "https://github.com/fckand/mars"
  - track: "黑客松-数据与算法"
    edge: "coding-agent 类赛题的即插架构：按题检索选专家 → 起手解 → 沙盒跑公开样例 → 保留/修复/结构化交接。prompt-only 无需微调，官方工件支持任意 OpenAI 兼容 API（含 --no-rag 冒烟路径），短周期可组装出 demo"
    reuse_cost: "中"
    open_source: "https://github.com/fckand/mars"
sources:
  - url: https://arxiv.org/abs/2608.23918
    title: "MARS: Multi-Specialist LLM Relay System for Competitive Programming (arXiv:2608.23918)"
    accessed: "2026-08-28"
  - url: https://github.com/fckand/mars
    title: "fckand/MARS — EMNLP 2026 code artifact（MIT）"
    accessed: "2026-08-28"
---

# MARS：多专家 LLM 接力竞赛编程系统

## 是什么

MARS（Mikhailov, Burtsev, Sagirova，2026-08-24 提交 arXiv，cs.AI/cs.MA/cs.PL，Comments 标注 EMNLP 2026 录用）是一个 **prompt-only** 的多智能体接力框架：每个 agent 是一个算法专题专家（动态规划、图论、字符串、几何等），由 RAG 检索算法理论语料（官方实现用 cp-algorithms 文档 + Qdrant 向量库）先选出 ≤3 名相关专家组成小队；起手 agent 写初始 C++17（或 Python3）解，随后每轮在沙盒（ExecEval）对公开样例运行候选解，当前专家可保留、修复或交接草稿（以结构化交接包 forward），末尾由 infra-fixer 归一化样板代码。CodeContests 测试集 + Gemma 4（31B）上达到 0.624±0.006 通过率（较直接提示 +14.4 个百分点），平均每题仅 2.3 个流水线阶段；与 CodeSIM（0.731）的差距以 3.3 倍更低的 wall-clock 成本收窄，且单题 token 开销方差显著更低。

## 解决什么问题

现有多智能体代码生成流水线用通用 planner/coder/debugger 角色分工，把"选哪种算法技术"完全留给 backbone 单模型，导致专题类题目不稳定。MARS 用"专题专家化 + 检索选队 + 沙盒验证接力"替代通用角色分工，全程不训练、只改 prompt。

## 相比前方法优势

- **免训练**：prompt-only，任何 OpenAI 兼容 API 即可运行（官方 README 明确支持 hosted API 替代本地 31B vLLM）；
- **成本效率**：接近 CodeSIM 精度的同时 wall-clock 成本低 3.3 倍，token 开销方差更低（预算可控性好）；
- **工件完整**：MIT 协议官方仓库含 relay 主循环、RAG 索引构建脚本、ExecEval 评分链与语言 profile，不是论文挂名空仓。

## 局限（如实标注）

- 论文配置 backbone 为 gemma-4-31B-it 双卡 vLLM 本地服务；更小模型上的收益未在论文验证（README 自述所报数字为论文配置均值，非 bit-for-bit 复现）；
- 0.624 仍低于 CodeSIM 的 0.731——接力是"效率-精度"折中而非 SOTA 声明；
- 官方工件剔除了全部 baseline 入口（direct prompting / 单 RAG / planner-coder-debugger），对比实验需自建；
- ExecEval 沙盒需 Docker 构建；RAG 索引需从 cp-algorithms 现场重建（原索引不分发），严格复现有偏差；
- maturity: paper（会议录用 + 官方代码工件，非产品）。

## 如何用于比赛

1. **ACM-训练体系（主用，注意合规）**：按 AGENTS.md 边界，ACM 方向不承诺自动解题获奖，MARS **不作赛场自动提交工具**（违反赛事规则的提交策略禁止生成），而是作训练体系组件：a) 训练复盘器——队员提交后由专题专家接力产出修复轨迹，与人类补丁对照学习；b) 出题-批改 harness——检索算法理论语料按专题生成变式训练题，沙盒样例即批改器；c) 复用 ExecEval 评分链做队内 OJ 的执行判题服务。复现成本中（需 Docker + 索引重建）。
2. **黑客松-数据与算法**：coding-agent 类赛题（自动修 bug、算法 copilot）直接套"检索选专家 + 沙盒验证 + 结构化交接"架构；prompt-only 意味着调 API 即可组装 demo（repo 提供 --no-rag 冒烟命令先跑通再补检索）。
3. 风险控制：小 backbone 上先验证单专家 + 沙盒回路有效，再扩展多专家接力；沙盒判题覆盖面依赖公开样例数量，弱样例题目上反馈信号噪声大。
