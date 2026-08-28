---
generated_at: 2026-08-28
direction: 黑客松与数据竞赛
profile_ref: config/profile.yaml
kb_snapshot: ac8f6c1
---

> 决策变更记录：2026-08-28 用户在人工闸门改向——"报名门槛高的先不考虑"（CUMCM 须学校教务报名），指定 **kaggle-kaggriculture** 为主攻。前版 CUMCM prep 攻略归档于 git ac8f6c1，赛窗（09-10~13）前均可复活。

## 一、赛事情报摘要

- **kaggle-kaggriculture**（主攻）：Google 自办 Simulation Competition——自主 agent 在 720 回合（30 日×24 回合）农场经营博弈中对抗，赛季末银行存款多者胜；Elo 天梯 + 终交后 Bradley-Terry 锦标赛定榜，无 Private LB。07-29 已开赛 → **09-30 终交**（verified）→ 约 10-15 定榜；⚠ entry_deadline 官方数值缺失（Timeline 模板变量未解析），当前确认可提交。奖金 **$50K 官方双证**（10×$5K；$60K 口径待核）。AI 政策全库最宽松：LLM 按费用合理性放行（Gemini Advanced 级订阅可接受）、外部数据/模型默认允许、数据 Apache 2.0、获奖 CC-BY 4.0；单账号、队上限 5 人。每日 ≤5 提交、仅最近 2 次计入评估。
- **kaggle-rsna-knee**（备选）：多模态医学影像（MRI+放射报告），12 类异常 macro-AUC，Code Competition（9h/断网）；10-15 报名截止、10-22 终交（全 verified）；$77K 双轨（主榜 $59K + Efficiency $18K）；预训练模型放行、获奖 CC-BY-NC。
- **tianchi-qoder-thursday**（支线）：系列至 2027-07，AI 鼓励，agent 栈练兵场。
- **mcm-icm**（远期锚点）：2027-01-28 开赛；CUMCM/MCM 线整体后置待用户重启。

## 二、赛道对比矩阵（六维，主攻视角）

| 赛事 | 时间窗 | 技术契合 | 通吃度 | 画像匹配 | 竞争密度 | 合规风险 |
|---|---|---|---|---|---|---|
| **kaggle-kaggriculture** | ★强：33 天至终交，2-10 周最优区【kaggle-kaggriculture】 | ★强：agent 仿真 × KB-2 LLM-agent 卡 40+【KB-2】 | ★中：agent 栈可复用 Qoder/lablab.ai | ★中：全栈编码对口，RL 实绩未证实（如实降权） | ★中：2k+ 队（二手口径），新赛种早期红利 | 低：apply，LLM/外部模型明文放行 |
| kaggle-rsna-knee | ★强：8 周，且 09-30 后可无缝接力 | ★中：监督学习管线对口但医学领域新 | ★弱：栈独立 | ★中偏高：ML+可视化直配 | ★高：医学旗舰 | 低：apply |
| tianchi-qoder-thursday | ★强：长窗口 | ★强 | ★中 | ★强：全栈 web | ⚠低证据（降权告知） | 低 |
| cumcm | 已后置：学校报名门槛（用户裁决 2026-08-28） | ★强 | ★强 | ★强 | ★中 | prep |
| mcm-icm | ★远：2027-01 | ★强 | —锚点 | ★强 | ★中 | prep |

## 三、大显身手信号（近 90 天 KB-2 新卡 × patterns 命中）

- **kaggle-kaggriculture**：`arxiv-2608.27456`（UrbanGround 城市 agent 沙盒：runnable demo、评测方法论与失败模式清单——直接迁移为本地自博弈评估基建）+ `arxiv-2608.25500`（CaSKG 技能检索——策略库组件）+ `arxiv-2608.25992`（ProgRouter 质量-成本路由——LLM 调用的回合预算控制）+ `arxiv-2608.24087`（Bayesian Self-Escalation——求助升级机制）。⚠ 无 patterns（首届未放榜）——方法论分布维度证据缺失，如实降权。
- **kaggle-rsna-knee**：`arxiv-2608.22108`（edge 医疗 demo）弱命中。
- 其余入围赛信号见前版（git ac8f6c1），本轮不重复。

## 四、一鱼多吃路线

**主线（agent 线）**：Kaggriculture bot 战役（09-30 收官）→ **kaggle-rsna-knee**（10-22 终交，改造**中**：切换监督学习管线，EDA/实验管理基建复用）→ tianchi-qoder 系列（改造**低**：agent 应用单题单投）。
**后置线（数模线）**：CUMCM prep 方案归档待复活（09-07 报名截止前须用户决策）；MCM/ICM 2027-01 锚点不变。

## 五、合规与风险

**模式判定**：kaggle-kaggriculture = **apply**。依据 meta.ai_policy 原文摘引：
> "The use of external data and models is acceptable unless specifically prohibited by the Host."（外部数据/模型默认允许）
> "a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard"（LLM 放行）
> "Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license"（AMLT 放行）

→ 本赛目标即 agentic AI（官方 abstract "design, build, and deploy an autonomous AI agent"），作品在政策允许范围内构建、人主导迭代，apply 成立。Winner License CC-BY 4.0 / 数据 Apache 2.0，合规负担最轻。

风险清单：
1. **entry_deadline 缺失**：官方数值未解析——战役第 0 天人工核对赛站页面并尽早完成 Kaggle 报名（列入 manual 验收项）。
2. **奖金双口径**：$50K 采信 / $60K 待核——不影响模式判定，呈报如实并存。
3. **RL/博弈新领域**：队内无实绩（画像维度已降权）——缓解：启发式基线先行 + 本地评估基建量化迭代 + 卡片方法论迁移。
4. **提交纪律**：每日 ≤5 次、仅最近 2 次计入——SOP 内嵌提交检查单，防临近终交误提交。
5. **仿真环境限额**：agent 运行环境 HDD/RAM/vCPU 为模板变量未解析——bot 资源占用留裕量（FAQ 待核项）。

## 六、推荐结论

**推荐第一名：Kaggriculture 农场博弈 Agent 战役（kaggle-kaggriculture，apply 模式，用户指定）**

理由：① 用户闸门指定 + 报名零门槛（Kaggle 直投）；② 时间窗 33 天处最优区，且收官后可无缝接力 RSNA（一鱼多吃主线成立）；③ AI 政策全库最宽松，apply 模式可正式启动作品构建；④ KB-2 agent 卡群提供评估基建/技能检索/成本路由三线组件支撑——但无 patterns、RL 无实绩两项如实降权，夺奖面为前十 ×$5K 单轨，属高方差高学习价值选择。

**备选：kaggle-rsna-knee**（apply）——技能更对口、8 周从容、双轨夺奖面；若 Kaggriculture 首周评估（m1-m3 里程碑后）投入产出比不佳，09-15 前可切换主攻且互不浪费（评估基建通用）。

**支线**：tianchi-qoder 系列（agent 应用练兵，改造低）。
