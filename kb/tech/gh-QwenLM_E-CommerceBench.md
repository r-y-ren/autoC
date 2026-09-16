---
id: gh-QwenLM_E-CommerceBench
name: "E-CommerceBench：18 个 LLM Agent 各持 ¥10 万经营 365 天模拟网店的长程评测环境"
field: [LLM agents]
directions: [黑客松与数据竞赛]
published: "2026-08-26"
maturity: demo
signal:
  venue: GitHub
  stars: 82
  runnable: true
competition_fit:
  - track: "黑客松-数据与算法"
    edge: "长程 Agent 作品的『抗注水评分环境』：主分数是资产乘数（年末总资产/期初 ¥100,000），配 CSE+、BadSpend%、回撤、每工具调用产出（¥/tool call）、破产次数等诊断维——团队自夸『我们的 agent 很强』时，直接在此环境跑 5 个独立 episode 给出可复核数字，比 demo 视频可信一个量级；真实市场数据驱动的供需，防背题；QwenLM 官方出品 + arXiv 论文（2608.30730）+ 榜单，引用有出处"
    reuse_cost: "中"
    open_source: "https://github.com/QwenLM/E-CommerceBench（Apache-2.0；Python 3.10+）"
  - track: "数模-数据分析与决策"
    edge: "现成的零售运营决策沙盘：供应商谈判、定价、库存、现金流断裂风险都被环境显式建模——数模选题若落在定价/库存/资金流优化，可当策略评估器（把优化策略接进环境跑 365 天对照），比自建仿真省一周且自带真实市场数据；注意它是为 LLM agent 设计的接口，接经典优化策略需自写适配层"
    reuse_cost: "中"
    open_source: "https://github.com/QwenLM/E-CommerceBench（Apache-2.0）"
sources:
  - url: https://github.com/QwenLM/E-CommerceBench
    title: "QwenLM/E-CommerceBench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation"
    accessed: "2026-09-09"
  - url: https://raw.githubusercontent.com/QwenLM/E-CommerceBench/main/README.md
    title: "README 全文（评分维度/18 模型榜单/破产案例）"
    accessed: "2026-09-09"
---

# E-CommerceBench：365 天模拟网店经营的长程 LLM Agent 评测环境

## 是什么

QwenLM（通义）2026-08-26 开源的长程 agent 基准（82 star，Python，Apache-2.0，API 实查 2026-09-09：推送至 2026-09-03；README 挂 arXiv 2608.30730 与主页 ecbench.github.io）。设定：agent 期初持有 ¥100,000，最多运营 4 家模拟网店共 365 个模拟日，动作覆盖与供应商谈判、定价、库存管理、现金流维持，供需由真实市场数据驱动。主分数为资产乘数（年末总资产/期初本金，每模型 5 个独立 episode 取均值）。诊断维度（README 榜单表实抓 2026-09-09）：CSE+、BadSpend%、回撤/峰值、每工具调用产出（¥/tool call）、可控回报 pp、AnchorRatio、工具调用数、轮数、破产次数。榜首格局（README 快照）：GPT-5.6 Sol (max) 平均年末资产 ¥1,431k 零破产、Fable5 (max) ¥805k（每工具调用产出最高 ¥479）、GPT-5.5 ¥702k 但 5 episode 破产 2 次——即便头部模型，长程经营稳定性差异也被环境显式暴露。

## 解决什么问题

LLM agent 评测的"短平快"偏差：主流基准是几步工具调用或单轮任务，测不出预算纪律、长期规划、失败恢复与现金流约束下的持续决策。本环境把"经营一家会倒闭的公司"作为压力测试——错误会在数百天内复利放大，破产就是破产，无法用话术掩盖。

## 相比前方法优势

- 相比 WebArena/AgentBench 类短任务基准：评估的是 365 天复利式长程表现，分数（资产乘数）天然抗 gaming——想拿高分必须真的会经营；
- 相比自建商业仿真：供需锚定真实市场数据，榜单有 18 模型 × 5 episode 的公开基线，新方法可直接对表；
- 诊断维度设计（每工具调用产出、可控回报、AnchorRatio）把"赚了钱"拆成"怎么赚的"，可区分稳健经营与运气单押。

## 局限（如实标注）

- 评测框架属性：它不提供方法，只提供考场——对"找打法"的队伍是环境而非答案；
- 模拟世界与现实电商仍有差距（真实市场数据驱动供需，但平台机制/竞对行为是仿真的），高分不等于真实商业能力；
- 365 天 × 5 episode 的评测运行成本可观（头部模型单 run 数千次工具调用、上千轮），队伍复跑全量榜单不现实，只能跑自己的 1-3 个 episode；
- 年轻仓库（2026-08-26 创建），榜单口径可能随版本漂移；README 榜单数字为作者自报，独立复核有限；
- 接口面向 LLM agent，接经典优化/OR 策略需自写适配层。

## 如何用于比赛

1. **黑客松 Agent 赛道（主用）**：作品若声称"长程自治决策能力"，在此环境跑 3-5 个 episode 出资产乘数与破产次数，作为答辩时的第三方可复核证据；其诊断维度（¥/tool call、BadSpend%）可直接搬进作品评测章节，展示成本意识与稳健性双视角。reuse_cost 中：Python 3.10+ 环境半天可通，但 LLM API 费用与运行时长需预算。
2. **数模决策类赛题（备用）**：定价/库存/现金流优化选题时，把它当现成零售沙盘做策略对照实验（优化策略 vs README 榜单基线），省去自建仿真的赛期成本；论文里注明环境出处与 episode 数即可满足可复现性要求。
