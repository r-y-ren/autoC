---
generated_at: 2026-08-28
direction: 黑客松与数据竞赛
profile_ref: config/profile.yaml
kb_snapshot: dec4d97
---

> **决策变更记录**：Kaggriculture 战役 II 的 m0/m1 已完成，m2/m3 曾以固定 p0、重复开发种子和顺序敏感 Elo 形成交付稿。2026-08-28 交付审计确认这些结果只能作为开发集描述性基线，并发现评估门可绕过、异常局计平、正式产物可被失败运行覆盖等缺陷。本攻略据此重开 m2/m3；旧 `1500.8 / 36-0` 不再作为确认性结论。
>
> K-01 前置：本轮增量同步提交 `dec4d97`；赛事新增 1 个待深核候选、技术卡新增 0，未出现改变 Kaggriculture 主攻判断的新证据。

## 一、赛事情报摘要

- **kaggle-kaggriculture（重开主攻）**：官方任务是提交部署在 `/kaggle_simulations/agent/` 的自主 Python bot，在 30 日、720 回合农场经营仿真中对抗；持续天梯只按胜负平计分，终交后以 Bradley-Terry 锦标赛定榜。2026-09-30 23:59 UTC 终交，奖金采用官方 Rules/Prizes 双证支持的 **$50,000（前 10 名各 $5,000）**【kaggle-kaggriculture】。提交每日最多 5 次，仅最近 2 次被跟踪；团队上限 5 人【kaggle-kaggriculture】。
- **报名状态**：KB 未取得通用 `entry_deadline` 官方数值，但本项目已用 Kaggle CLI 实抓 `userHasEntered=True`，因此本队报名风险已闭环；不得把该项目状态外推成新用户仍可报名【kaggle-kaggriculture；workspace/JOURNAL.md】。
- **现有资产**：m0/m1 已交付官方引擎、本地评估包、强启发式对手池、回归门和 101 项软件测试。m2 版本在固定 p0 与开发种子上表现强，但审计证明其结果受座位、种子复用和在线 Elo 顺序影响，只能作为开发基线，不支持天梯实力或获奖概率判断【workspace/metrics.json】。
- **证据边界**：`patterns.md` 存在但 confidence=低，可靠部分是游戏机制、720 回合完成性、浇水/喂养红线、终局回收期与提交管理；winner-derived patterns 为零，RL/PPO/做市等仍只是待验证分析轴【kaggle-kaggriculture】。
- **备选**：`kaggle-rsna-knee-abnormality-detection` 仍是 09-30 后可接力的监督学习赛；`tianchi-qoder-thursday` 是低改造 agent 工程支线【kaggle-rsna-knee-abnormality-detection；tianchi-qoder-thursday】。

## 二、赛道对比矩阵（六维）

| 赛事 | 时间窗 | 技术契合 | 通吃度 | 画像匹配 | 竞争密度 | 合规风险 |
|---|---|---|---|---|---|---|
| **kaggle-kaggriculture** | **强证据**：终交 09-30，当前仍有迭代窗口【kaggle-kaggriculture】 | **强工程证据/弱泛化证据**：已有可运行 bot 与强池，但确认性评估尚未成立【workspace/metrics.json】 | **中强**：双座位评估、holdout、原子证据链可复投其他仿真赛与模型评测 | **强**：Python/数据分析/全栈画像直接匹配，且已有同赛资产 | **中证据**：本项目 CLI 曾实抓 6723 队口径，但 KB 官方参赛规模字段仍未闭合；不据此推导名次概率 | **低**：apply；外部模型、合理费用 LLM、持证 AMLT 明文允许【kaggle-kaggriculture】 |
| kaggle-rsna-knee-abnormality-detection | **强证据**：10 月窗口，可在 Kaggriculture 后接力【kaggle-rsna-knee-abnormality-detection】 | **中**：监督学习和可视化匹配，医学域无实测 | **中弱**：实验治理可复用，模型栈需重建 | **中强**：ML 与建模履历匹配 | **有限证据**：医学旗舰赛竞争强但缺少本队实测 | **低**：apply【kaggle-rsna-knee-abnormality-detection】 |
| tianchi-qoder-thursday | **强证据**：长窗口至 2027-07【tianchi-qoder-thursday】 | **中强**：agent 工程栈匹配 | **中**：评估与工作流资产可迁移 | **强**：全栈画像匹配 | **低证据**：缺少可比参赛规模与 winner patterns | **低**：AI 编程工具明确鼓励【tianchi-qoder-thursday】 |
| mcm-icm | **强证据**：2027-01 远期窗口【mcm-icm】 | **强**：团队已有 M 奖 | **强**：数模线内部复用高 | **强**：历史成绩直接验证 | **中**：成熟赛事，竞争稳定 | **中**：竞赛期 AI 使用与披露需按届规执行，采用 prep【mcm-icm】 |

## 三、大显身手信号

- **Kaggriculture**：`arxiv-2608.26753`（ABE-Ralph）命中本轮核心问题：把实验保真从文档审计升级为可执行约束，包括候选身份、完整赛程、异常 fail-closed 与证据一致性。
- **Kaggriculture**：`arxiv-2608.27456`（UrbanGround）命中 runnable 沙盒与失败模式驱动迭代；本轮进一步把开发集与确认性 holdout 分离。
- **Kaggriculture**：`arxiv-2608.15291`（ReasonCast）继续支撑选择性市场干预，但策略收益必须经过双座位独立 holdout 后才能宣称。
- **Kaggriculture**：`arxiv-2608.25992` + `arxiv-2608.24087` 支撑 LLM 质量-成本路由和求助升级；真实 A/B 仍受 key 与逐局预算隔离条件约束，不作为本轮阻塞项。
- **证据降权**：该赛无 winner-derived patterns；上述命中是方法论迁移，不是获奖套路复现【kaggle-kaggriculture】。

## 四、一鱼多吃路线

1. **当前主线**：Kaggriculture 评估加固与策略修复。新增资产包括 AB/BA 双座位矩阵、候选哈希冻结、一次性随机 holdout、语义校验、异常局 fail-closed 和原子产物发布，改造量**中**。
2. **近期开枝**：Kaggriculture 收官后转 `kaggle-rsna-knee-abnormality-detection`，复用实验身份、holdout、原子指标与报告一致性工具；模型管线改造量**中高**。
3. **低成本复投**：把评估治理脚手架用于 `tianchi-qoder-thursday` 的 agent 题，改造量**低**。
4. **远期复用**：MCM/ICM 报告与实验审计复用，算法主体另建，改造量**中**。

## 五、合规与风险

**模式判定：apply。** Kaggle 官方 Rules（KB 抓取日期 2026-08-28）明确：

> “The use of external data and models is acceptable unless specifically prohibited by the Host.”
>
> “a small subscription charge to use additional elements of a large language model such as Gemini Advanced are acceptable if meeting the Reasonableness Standard”
>
> “Individual Participants and Teams may use automated machine learning tool(s) ('AMLT') ... provided that ... they have an appropriate license”

因此 AI 辅助设计、实现、测试和迭代与规则相容【kaggle-kaggriculture】。提交 bot 仍保持 stdlib-only、离线自主运行；规则允许 LLM 不等于线上容器允许外部网络调用，外部 API 不进入提交依赖。

风险与缓解：

1. **评估泄漏**：101-104、201-208 已用于调参，永久降格为开发种子；候选冻结后才用系统随机源生成新的 holdout，运行后公开种子清单，任何候选变更必须生成新 holdout。
2. **座位偏差**：每个 `(pair, seed)` 强制 AB/BA，两座位分别报告并汇总；固定 p0 的旧 `36-0` 不再作为确认性指标。
3. **异常伪平局**：任何非 DONE、contract 失败、超时或 INVALID 使整批失败，不得进入 Elo、胜率或门禁。
4. **证据污染**：quick/dev/失败运行写独立临时产物；只有完整语义校验和门禁通过后才原子替换正式 export。
5. **门禁绕过**：正式 verdict 必须验证全部 gate/guard 对手、预期局数、双座位和种子集合完整；自定义子集只能输出 exploratory，不得 PASS。
6. **统计误读**：顺序敏感 Elo 降为描述性附录；主结论采用逐对 W/L/T、座位分层、Wilson 区间及顺序无关 Bradley-Terry/配对汇总。
7. **线上未知**：本地 holdout 仍不能替代天梯；online metrics 未发生时保持 null，禁止外推名次或获奖概率。

## 六、推荐结论

**推荐第一名：继续 Kaggriculture，但以“评估可信度修复后再优化策略”为唯一允许路线。**

理由：现有 bot、官方引擎和对手池使重开成本低；审计已经给出可复现的高价值缺陷，修复末日资本支出、库存预留和门禁完整性具有明确工程收益；`arxiv-2608.26753`、`arxiv-2608.27456` 与 `arxiv-2608.15291` 分别覆盖实验保真、沙盒失败驱动和市场门控。推荐不再依赖旧 1500.8，而以独立 holdout 双座位结果决定最终表述。

**备选：kaggle-rsna-knee-abnormality-detection。** 若新 holdout 显示候选对强敌不能稳定达到非劣，或线上提交反馈持续不匹配本地池，则停止继续针对本地启发式过拟合，转向 RSNA；评估治理资产仍可复用。
