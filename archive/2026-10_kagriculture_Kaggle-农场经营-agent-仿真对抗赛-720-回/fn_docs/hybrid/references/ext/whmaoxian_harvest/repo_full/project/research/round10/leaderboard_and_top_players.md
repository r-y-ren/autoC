# Round 10：榜单与前列选手的公开决策证据

**采集时间：2026-09-23 13:46:17 UTC（北京时间 21:46:17）。** 榜单会持续变化；本页数字只代表该时刻。[赛事榜单](https://www.kaggle.com/competitions/kaggriculture/leaderboard)通过公开的 `LeaderboardService/GetLeaderboard` 接口采集，原始的前 20 名字段保存在 [leaderboard_snapshot.json](leaderboard_snapshot.json)。上一轮本地快照 `research/round9/leaderboard.json` 的文件修改时间为 09:59:06 UTC；它不一定等于接口原始采集时刻。

| 当前名次 | 队伍 | 上榜提交 ID | 分数 | 对上一快照的变化 |
|---:|---|---:|---:|---:|
| 1 | DSM | 56468867 | 3163.2 | +5.9 |
| 2 | Boey | 56484772 | 3082.0 | +122.9；此前第 11 名，同一提交 ID |
| 3 | M & M & P & Q | 56464621 | 3074.7 | +9.4 |
| 4 | Unknown Mother-Goose | 56478145 | 3064.9 | +3.4 |
| 5 | Vadim Vasilenko | 56474685 | 3029.2 | −12.4，同一提交 ID |
| 6 | Kaggledew Valley 🏆 | 56478402 | 3011.2 | −3.4 |
| 7 | 吃白饭的大肥鱼 | 56483899 | 3010.3 | +4.4 |
| 8 | DECEM | 56482350 | 3004.8 | +2.8 |

**我方 V9 尚无法从公开榜单确认。** 13:52:58 UTC 查询队伍 MauoXX（teamId `16899200`，用户 `mclster`）时，榜单仍指向已知 V8 提交 ID `56481789`，显示 2215.1 分、当时第 1251 名。`lastSubmissionDate` 为 12:57:02 UTC，但接口没有给出能够归属 V9 的提交 ID 或成绩，不能将 V8 分数写成 V9 分数。证据见 [user_team_public_status.json](user_team_public_status.json)。

## 采样与可比性

按榜单采集时前五名各自公开列表中**最新的 4 局已完成、非自战对局**选样，先固定 episode ID，再下载回放。20 个队伍视角对应 17 个去重回放。选样规则、对手及结果见 [recent_episode_selection.json](recent_episode_selection.json)；回放 SHA-256 和随机种子见 [replay_provenance.json](replay_provenance.json)；动作请求、每天银行余额、农场地块和仓库存量见 [recent_replay_actions.json](recent_replay_actions.json)。下载器 [collect_leaderboard.py](collect_leaderboard.py)，分析器 [analyze_public_replays.py](analyze_public_replays.py)。它们只读取公开资料，不接触选手私有代码。回放可直接核查，例如 [DSM 对 Boey 的 112446065 局](https://www.kaggle.com/competitions/episodes/112446065/replay.json)。

另把每队最新 50 局公开非自战比赛作**背景统计**：DSM 44 胜 6 负、对手赛前分中位数 3051；Boey 49 胜 1 负、对手中位数 2946；M & M & P & Q 35 胜 15 负、中位数 3040；Unknown Mother-Goose 42 胜 8 负、中位数 2995；Vadim 25 胜 25 负、中位数 3025。[精确值](latest50_public_episode_summary.json)。这是不同对手、不同配对时间的观察，不能直接按胜率宣称 Boey 强于 DSM，也不能把近期 4 局当胜率估计。

## 从状态变化看决策

**1. DSM 与 Vadim 的早期动作相同，随后按状态分化。** 在两队各 4 局形成的 16 个跨队组合里，第 0 天 24 个小时的完整动作完全相同；首次不同发生在第 26–29 步。两队四局各自在第 5 天拥有约 10 块草莓、10 块甜瓜、2 头牛、3 只羊和 6 名雇工。这只能证明公开动作模式相同，**不能证明代码相同或谁借鉴谁**。第 3 天后商店组合不同，后期配置明显分化。逐日精确匹配率见 [opening_similarity.json](opening_similarity.json)。Boey 与两队的所有 16 个跨队组合则从第 1 步就不同。

**2. Boey 的近期对局展示了另一种资金周转路径。** 其 4 局第 5 天结束时账上只有 2–22，第 10 天升至 5,425–9,866；第 10 天均解锁 3 块地。DSM 的相应范围是 788–836、717–2,697，并在第 10 天均解锁 4 块地。这不是跨局收益的公平比较；更有用的是双方同场的 [112446065](https://www.kaggle.com/competitions/episodes/112446065/replay.json)：第 5 天 Boey 31 现金、地上 7 头牛，DSM 788 现金、2 头牛；第 10 天 Boey 6,793 现金和 3 块地，DSM 2,697 现金和 4 块地；第 15 天 41,801 对 30,025；第 20 天 83,705 对 70,320；终局 136,906 对 127,039。它支持一个值得测试的假说：**在劳动力、喂养、照料、收获能够跟上的条件下，较早投向可周转生产资产，有时优于提前买满土地。** 单局不能识别净因果效应，也不能照搬“7 牛、3 块地”。同场另一视角摘要见 [boey_dsm_headtohead_actions.json](boey_dsm_headtohead_actions.json)。

**3. 看商店需求后的生产配置，而不是固定的作物答案。** 官方引擎中，PET_CAFE 消耗胡萝卜，YARN_STORE 消耗羊毛，PIZZA_SHOP 消耗牛奶、番茄和小麦，ICE_CREAM_SHOP 消耗草莓、牛奶和小麦；商店每 4 小时消耗，可能重复开同种店。[引擎的商店映射及消耗规则](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.py)。DSM 在 112462531（先开农夫市场、面包店）第 20 天地上有 26 块胡萝卜、10 只鹅；在 112446065（先开披萨店、冰淇淋店）有 18 头牛、26 块小麦、27 块草莓。Boey 在 PET_CAFE、YARN_STORE 早开的一局（112454257）第 20 天有 11 只羊、16 块胡萝卜；在 BRUNCH_SPOT、SMOOTHIE_SHOP、PIZZA_SHOP 早开的一局（112454264）有 10 头牛、32 块草莓。此处是**配置与需求相符的观察**，不能仅凭回放断言私有程序使用了何种预测算法；也不能忽略随机种子、对手行为和两人共同影响的市场。

**4. 终局现金兑现必须看实际剩余。** Boey 和 Vadim 所抽 4 局的最终仓库全部为空；DSM 4 局中 1 局为空，另 3 局残留少量产品，其中 112446065 仍有 18 草莓。由此值得检查 V9 的产品是否卡在手中、销售是否过早压价，以及最后几天种植是否来得及回本。这是独立可测的资源回收问题，不能只看收益曲线的中段。

**5. 大额订单是请求，不是实际成交。** 某些公开动作每小时报 `SELL 10000`，另有累计数百单位的 `BUY_ANIMAL` 请求；不能据此写“卖出万件”或“买入数百头”。[官方市场处理](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.py)逐单位执行，库存、现金、仓库容量不足就停止该订单；每小时订单队列还有 10 项上限。两位选手逐单位按执行前的共同库存报价，因此生产与出售会改变双方的后续价格。对抗目标应记录**真实入账、真实持仓、双方终局现金差**，而非表面订单数。机器摘要明确将这些字段命名为 `requested_*`。

## 给下一轮“战之野”的可检验课题

1. **早期资产回收试验。** 以 V9 为基线，分开改变土地购买时机、畜牧投入时机和预留现金；动物分支必须同时验证喂食、照料、收获、仓库与雇工工时的完整链条。记录第 5、10、15 天双方现金差、成熟产能、待售库存和最终胜负。用新随机种子、交换先后手，分别对 DSM 旧公开代理、Boey 等多种对手测试；任何单个回放只用于提出假说。
2. **需求切换试验。** 在可控的早开商店组合、重复商店、晚开商店以及对手向同一产品倾销的情形下，比较状态驱动的产能分配。衡量的是需求出现后的边际产量、价格和执行成功率；避免把 episode ID 或某段固定路线写进正式策略。
3. **终局兑现试验。** 对最后若干天计算新增资产能否在第 29 天前完成回本，检查仓库剩余、地上未收作物、卖出时对手价格的影响。只在多对手留出集对胜率及现金差均有帮助时合并。

报告的身份边界：这是公开榜单与公开视频对应 JSON 回放的**行为分析**，并非 DSM、Boey 或 Vadim 私有程序源码；样本小，榜单分数动态，不能由此推定线上 3000 分。任何候选仍应按预先冻结的独立赛程验证。
