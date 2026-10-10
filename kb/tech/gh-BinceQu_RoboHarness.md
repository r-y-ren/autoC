---
id: gh-BinceQu_RoboHarness
name: "RoboHarness: 免训练的 LLM 具身控制面板——视觉关键点+几何约束闭环超越 VLA"
field: [LLM agents, 具身智能, 机器人操作]
directions: [创新创业大赛, 黑客松与数据竞赛]
published: "2026-10-07"
maturity: demo
venue_tier: other
reproducibility_level: high
signal:
  venue: "GitHub"
  stars: 224
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "具身/机器人 agent 赛题的免训练差异化：『LLM 只做语义决策、几何执行交给视觉关键点+深度反投影+约束闭环』的架构可直接 fork 成现场演示，README 级复现契约齐全（每任务 5 实例、2× 人类演示步数预算、Mean Q-score 四位小数对参考 1e-6 容差校验），eval 管线与 reproduce_task.sh 可直接当赛题评测框架；在全员端到端 VLA 叙事的赛场上，『不训练任何模型也能超越 VLA/世界动作模型』是稀缺反直觉卖点"
    reuse_cost: 中
    open_source: "https://github.com/BinceQu/RoboHarness（MIT，代码开放；BEHAVIOR 数据/Isaac Sim/模型权重独立授权）"
  - track: "双创-文书与申报"
    edge: "具身智能产品的可申报分层架构：『语义层 LLM + 几何层控制面板』比端到端 VLA 更可解释可审计（关键点轨迹与约束验证全程留痕，闭环『跟踪→约束→执行→验证』天然是安全论证素材），可引用其在 BEHAVIOR 基准超越 VLA/wAM 的结果作为免训练路线可行性论据；对仓储/巡检/家庭机器人方向的申报书是现成的技术方案骨架"
    reuse_cost: 中
    open_source: "https://bincequ.github.io/RoboHarness/（项目页）"
sources:
  - url: https://github.com/BinceQu/RoboHarness
    title: "BinceQu/RoboHarness — README 与仓库结构实抓（224 stars/18 forks，MIT，2026-10-10 快照）"
    accessed: "2026-10-10"
  - url: https://bincequ.github.io/RoboHarness/
    title: "RoboHarness 项目页（README 所附链接，2026-10-10 抓取）"
    accessed: "2026-10-10"
---

# RoboHarness：免训练的 LLM 具身控制面板——视觉关键点 + 几何约束闭环超越 VLA

> 来源：https://github.com/BinceQu/RoboHarness （README 与仓库结构，224 stars/18 forks，2026-10-10 实抓快照）；项目页 https://bincequ.github.io/RoboHarness/ 。本卡内容全部出自本次抓取的 README/项目页，未读独立论文全文（仓库未附正式论文链接，仅项目页）。

## 是什么

RoboHarness（2026-10-07 发布，MIT，224 stars/18 forks，2026-10-10 快照）给 LLM agent 一个**视觉-几何控制面板**，使其无需训练任何模型即可直接理解并执行具身任务。工作方式：LLM 在 2D 图像上标注兴趣点（keypoint），系统经**光学流跟踪 + 深度反投影**持续回传这些点的 3D 位置，把关键点转成几何约束，再由 LLM 组合原语动作（primitive actions）完成复杂操作——README 概述为"关键点被持续跟踪、转成几何约束、执行并在闭环中验证"。仓库声称的核心结果："A Simple Harness Outperforms VLA and World Action Models"（在 BEHAVIOR 基准上，验证环境为 Claude Code 2.1.259 + Qwen3.8-Flash-Next-FP8 + R1 Pro 机器人）。

仓库结构即完整管线：`BEHAVIOR/`（StanfordVL/BEHAVIOR-1K v3.9.1 子模块：模拟器+评测器）、`interface/`（RGB-D 观测、机器人控制、交互界面 http://127.0.0.1:15071）、`harness/claude_code/` 与 `harness/codex/`（两套 agent harness）、`tasks/`、`roboharness/`（任务运行器+评测管线）、`reference_results/` 与 `validation_results/`。复现契约明确：任务级人工 prompt 跨实例共享，每任务 5 实例（seed 20260911），步数预算为人类演示均长 2×，Mean Q-score 五次 rollout 取均值至四位小数、与参考结果按 1e-6 容差经 `report_validation.py --require-match` 校验。

## 解决什么问题

具身任务走 LLM 有两条现成路，各有硬伤：端到端 VLA/世界动作模型需要大量训练且跨任务泛化差；直接让 LLM 输出低层动作又缺乏几何精度。RoboHarness 在两者之间插一层免训练中间件——LLM 保留语义规划角色，几何执行交给关键点跟踪与约束系统，使"调用具身任务"变成 LLM 可直接操作的面板而非需要训练的能力。

## 相比前方法优势

- **免训练**：不改任何模型权重，靠"视觉点击 + 关键点跟踪 + 几何约束"三件套组装，规避 VLA 的训练成本与数据依赖；
- **闭环验证内建**：跟踪→约束→执行→验证的闭环使动作有几何依据，不是开环盲目执行；
- **声称超越 VLA/世界动作模型**（BEHAVIOR 基准，作者口径），若成立则"轻量 harness > 重训练模型"对该领域是路线级挑战；
- **复现工程完整**：setup/reproduce/report 三段脚本 + 参考结果 + 容差校验，在同类具身开源中少见地给出了可机检的复现契约；
- 双 harness（claude_code/codex）+ OpenAI Chat Completions 桥接配置，模型端可替换。

## 局限（如实标注）

- 无正式论文：结果仅项目页与 README 自报，"超越 VLA/wAM"无同行评审背书，独立复现尚未见；
- 重资产门槛：Linux x86-64 + NVIDIA RTX GPU（验证机 48 GB VRAM）+ Python 3.11 + CUDA 12.4 + BEHAVIOR 授权数据 + Isaac Sim 条款 + Anthropic 兼容 `/v1/messages` 端点（需图像输入/工具调用/流式），笔记本级环境跑不动；
- 贡献者为 BinceQu 与 Codex（AI 编码 agent），119 commits 单人+AI 协作，工程成熟度未经第三方检验；224 stars 生态刚起步（2026-10-10 快照）；
- 任务域绑定 BEHAVIOR 家庭任务套件，向其他机器人平台/仿真器迁移的适配成本未量化。

## 如何用于比赛（比赛映射展开）

1. **黑客松-数据与算法（具身/机器人 agent 赛题）**：fork 仓库把"LLM+控制面板"跑成现场演示——评委看到的是 LLM 在图像上点关键点、系统实时跟踪并完成 manipulation，而非黑盒策略回放；`scripts/reproduce_task.sh --dry-run` 流程可直接改造为赛题评测脚本（五实例均值 + 参考容差校验是现成的公平评测设计）。reuse_cost 中：代码 MIT 全开放，但需 RTX GPU 环境 + 模型端点 + BEHAVIOR 数据授权，赛期建议先跑通单任务再扩展。
2. **双创-文书与申报（具身智能产品方向）**：申报书技术方案可直接采用"语义层 LLM + 几何层控制面板"分层架构，主打两个论证点：可解释可审计（关键点轨迹与约束验证全程留痕，区别于端到端黑盒策略）与免训练低成本（不依赖 VLA 训练管线与数据采集）；引用 BEHAVIOR 超越 VLA/wAM 结果时注明作者自报口径（reuse_cost 中：架构思路可直接写进方案，实证数字引用需带出处与自报标注）。
