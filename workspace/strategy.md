---
generated_at: 2026-08-28
direction: 黑客松与数据竞赛
profile_ref: config/profile.yaml
kb_snapshot: 0df2fc6
---

> **决策变更记录**：2026-08-28 用户闸门曾指定 kaggle-kaggriculture 为主攻（前版攻略随第一场战役归档）。同日第一场战役闭环归档（`archive/2026-08_Kaggriculture-农场博弈-Agent-战役_720-回合供应链博弈-bot（agentic-RL-风向标赛，09-30-终交/`，软件树 42 文件）。用户现重开 `/attack Kaggriculture`——**第二场战役**，使命从"框架闭环验证"升级为"参赛级迭代至 09-30 终交"。
>
> K-01 前置说明：今日 14:46 已完成 /attack 预刷新（git 31ea4e1：tech+1 UrbanGround、comp 增量全噪弃置），KB 新鲜度满足，本轮不重复跑批。

## 一、赛事情报摘要

- **kaggle-kaggriculture（主攻，用户指定）**：Google 自办 Simulation Competition——自主 agent 在 720 回合（30 日×24 回合）农场经营博弈中对抗，赛季末银行存款多者胜；Elo 天梯 + 终交后 Bradley-Terry 锦标赛定榜，无 Private LB。07-29 开赛 → **09-30 终交**（verified）→ 约 10-15 定榜；⚠ entry_deadline 官方数值缺失（Timeline 模板变量未解析）。奖金 $50K 官方双证（10×$5K；$60K 口径待核）。AI 政策全库最宽松：外部数据/模型默认允许、LLM 按 Reasonableness Standard 放行、数据 Apache 2.0、获奖 CC-BY 4.0；单账号、队上限 5 人、每日 ≤5 提交且仅最近 2 次计入。
- **第一轮战役资产（归档实测，2026-08-28）**：可提交 bot（"鹅引擎+瓜波段"，stdlib-only）本地 40 局实测 24/24 胜、平均终局资金 30548.5、A/B 对基线 2.56×、本地 Elo 1460.9；评估基建 kgenv（官方引擎 vendored 复刻/收益模型/红线检查/Elo/复盘日志）+ 45 项测试全绿。**遗留边界**：Kaggle 报名与线上提交均未发生（人工项）；对手池偏弱（最强 greedy_carrot Elo 1162），天梯真实对手分布未标定。
- **kaggle-rsna-knee（备选）**：多模态医学影像（MRI+放射报告），12 类异常 macro-AUC，Code Competition（9h/断网）；10-15 报名截止、10-22 终交（全 verified）；$77K 双轨（主榜 $59K + Efficiency $18K）；预训练模型放行、获奖 CC-BY-NC。
- **tianchi-qoder-thursday（支线）**：系列至 2027-07，AI 鼓励，agent 栈练兵场。
- **mcm-icm（远期锚点）**：2027-01-28 开赛；CUMCM/MCM 线整体后置待用户重启。

## 二、赛道对比矩阵（六维，主攻视角）

| 赛事 | 时间窗 | 技术契合 | 通吃度 | 画像匹配 | 竞争密度 | 合规风险 |
|---|---|---|---|---|---|---|
| **kaggle-kaggriculture** | ★强：至终交 33 天，2-10 周最优区【kaggle-kaggriculture】 | ★强（**已升级**）：第一轮本地实测 24/24 胜+Elo 1460（归档 metrics.json，证据强）；KB-2 agent 卡 40+ 支撑 | ★中：评估基建可复投 RSNA 实验管理与 Qoder agent 题（归档 report 第六节） | ★中→强：全栈对口；RL 实绩已由第一轮启发式路线本地验证（学习类策略仍无实绩，如实降权） | ★中：2k+ 队为二手口径（Reddit，未直抓）——**低证据，如实降权**；新赛种早期红利判断不变 | 低：apply，LLM/外部模型明文放行【meta.ai_policy】 |
| kaggle-rsna-knee | ★强：8 周，且 09-30 后无缝接力 | ★中：监督学习管线对口，医学领域新（无实测） | ★弱：栈独立（EDA/实验管理可复用） | ★中偏高：ML+可视化直配（蓝桥杯国三实证） | ★高：医学旗舰（无量化数据，定性判断） | 低：apply |
| tianchi-qoder-thursday | ★强：长窗口（至 2027-07） | ★强：agent 应用栈 | ★中：单题单投 | ★强：全栈 web | ⚠低证据（**该维度基于有限数据，如实降权告知**） | 低：AI 明文鼓励 |
| cumcm / mcm-icm | 已后置 / 2027-01 远窗 | ★强 | ★强（数模线内部） | ★强（美赛 M 实证） | ★中 | prep（竞期限外部交流类默认） |

## 三、大显身手信号（近 90 天 KB-2 新卡 × patterns 命中）

- **kaggle-kaggriculture**：
  - `arxiv-2608.27456`（UrbanGround 城市 agent 沙盒：runnable 评测方法论与失败模式清单——第一轮已迁移为本地评估基建，第二轮继续驱动迭代）；
  - `arxiv-2608.26753`（ABE-Ralph 实验保真审计——**本轮新增命中**：直接对症"对手池偏弱"自欺风险，评估审计清单化）；
  - `arxiv-2608.15291`（ReasonCast 选择性语义推理——**本轮新增命中**："何时不干预"门控方法论迁移到动态市场出货决策：价格随自身出货反应，稳定期不卖、事件窗倾销）；
  - `arxiv-2608.25992`（ProgRouter 质量-成本路由）+ `arxiv-2608.24087`（Bayesian Self-Escalation）——LLM 模块预算闸已落地接口，本轮做真实 A/B 实测；
  - `arxiv-2608.25500`（CaSKG 技能检索——策略库分段组织，方法论级）。
  - ⚠ 该赛 **patterns 方法论分布无数据**（首届未放榜，定榜约 10-15）——"恰有最新科技成果"仅官方机制一手依据 + 本地实测，无获奖样本佐证，**该维度如实降权**。
- **kaggle-rsna-knee**：`arxiv-2608.22108`（edge 医疗 demo）弱命中。
- 其余入围赛无 90 天内新卡强命中，不硬凑。

## 四、一鱼多吃路线

**主线（agent 线）**：Kaggriculture 第二轮战役（09-30 收官）→ **kaggle-rsna-knee**（10-15 报名截止、10-22 终交；改造**中**：切换监督学习管线，EDA/实验管理/报告基建复用）→ tianchi-qoder 系列（改造**低**：agent 应用单题单投）。
**复用资产**（归档 report 第六节"可复用资产清单"）：官方引擎 vendored 复刻路线（同族 Kaggle 仿真赛直用）、评估基建骨架（对手池/Elo 六榜/复盘日志、40 局评估协议）、提交 SOP 19 项检查单。第二轮战役本身 = 归档资产"复活-迭代-再归档"，改造量**低**（工程 42 文件整体复活，回归线已冻结）。
**后置线（数模线）**：CUMCM prep 方案在 git 历史可复活；MCM/ICM 2027-01 锚点不变。

## 五、合规与风险

**模式判定**：kaggle-kaggriculture = **apply**。依据 meta.ai_policy 原文摘引（2026-08-28 Kaggle ListPages API 直抓）：

> "The use of external data and models is acceptable unless specifically prohibited by the Host."
> "a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard"
> "Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license"

→ 本赛目标即 agentic AI（官方 abstract "design, build, and deploy an autonomous AI agent"），作品在政策允许范围内构建、人主导迭代，apply 成立。Winner License CC-BY 4.0 / 数据 Apache 2.0，合规负担最轻。人机分工延续第一轮模式（AI 全部实现与本地验证，人工报名/提交/裁量）。

风险清单：
1. **entry_deadline 缺失**（第一轮遗留未决）：第 0 天人工核对赛站并完成 Kaggle 报名（manual 验收置顶）——唯一硬时点风险。
2. **线上天梯未标定**：本地对手池 Elo 1162 封顶，真实对手分布未知——m1 对手池强化 + 首轮线上提交尽早拿反馈回填，09-15 前保留 RSNA 切换决策点。
3. **提交纪律**：每日 ≤5 次、仅最近 2 次计入——SOP v2 检查单 + 终交前锁定检查（manual）。
4. **容器限额与网络政策未解析**（FAQ 模板变量）：提交形态保持 stdlib-only、不依赖外部网络模型；LLM 模块仅本地 A/B 且默认关闭，不臆测线上能力。
5. **奖金双口径**（$50K 采信/$60K 待核）：不影响模式判定，如实并存。
6. **数字纪律**：报告一切对局指标只能来自 workspace/metrics.json 实测；线上指标未发生时如实为 null。

## 六、推荐结论

**推荐第一名：Kaggriculture 农场博弈 Agent 战役 II（kaggle-kaggriculture，apply 模式，用户指定）**

理由：① 用户指定 + 报名零门槛（Kaggle 直投），且第一轮已把工程从零做到本地实测 24/24 胜——第二轮复活成本全场最低（改造量低），边际投入全部落在"线上标定 + 策略增强"这两个真正的夺奖变量上；② 时间窗 33 天处最优区，收官（09-30）后 RSNA（10-22 终交）可无缝接力，一鱼多吃主线成立；③ AI 政策全库最宽松，apply 成立无合规摩擦；④ KB-2 新增两张对症卡（ABE-Ralph 评估保真、ReasonCast 门控）+ 既有四卡组件支撑。**如实降权项**：无 patterns（首届未放榜）、2k+ 队二手口径、学习类策略无实绩——夺奖面为前十 ×$5K 单轨，属高方差高学习价值选择，禁止 promising 名次。

**备选：kaggle-rsna-knee**（apply）——技能更对口（蓝桥杯国三+美赛 M 实证）、8 周从容、双轨夺奖面；若第二轮线上反馈（m1-m2 后）显示投入产出比不佳，09-15 前可切换主攻且评估基建通用。

**支线**：tianchi-qoder 系列（agent 应用练兵，改造低）。
