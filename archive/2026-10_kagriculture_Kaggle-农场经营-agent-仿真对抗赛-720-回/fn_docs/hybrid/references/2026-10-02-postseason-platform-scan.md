# 2026-10-02 赛后平台侧增量扫描（postseason-platform-scan）

> 抓取时点 **2026-10-02 10:39–10:58 UTC**；通道：kaggle CLI 2.2.4（competitions topics/submissions/leaderboard/episodes、kernels list、datasets list）+ GitHub REST + 竞赛页 curl。基线=`2026-10-01-closing-sprint-scan.md`（止于 2026-09-30 23:38 UTC）。纪律：逐条带来源+抓取时间戳；自报数字标"自报"；查不到写"未找到更新"。原始拉取物见 `ext/postseason-platform/`（provenance.md+SHA256SUMS.txt）。
> **重要环境注记 1**：竞赛 slug 为 `kaggriculture`（双 g，k-a-g-g-r-i-c-u-l-t-u-r-e）。拼错 slug 时 kaggle API 返回 404/Not found（本轮曾误触发 leaderboard/topics/kernels/datasets 四类假 404，字节精确 slug 后全部恢复）——**勿把这类 404 误判为平台下线**。
> **重要环境注记 2**：CLI 2.2.4 **无** `competitions describe`（任务书假设有）；`competitions hosts` 403；`datasets metadata/files` 对本赛数据集仍 403（版本判定沿用 `datasets list` 的 lastUpdated）；竞赛页/overview 为 JS 壳（5,903 B）无正文可提。**上轮"评论正文不可得"的限制本轮解除**：`kaggle competitions topics show <slug> <id>` 可取全文评论树，`topic-messages`（==SUPPRESS== 命令）可取带 URL 的原文。

## 一、判据判定表（五块"增量有/无"）

| 块 | 判定 | 依据（实抓） |
|---|---|---|
| 1. 比赛状态与终评 | **有增量**（终评期口径落定+榜面漂移；无获奖公告） | `competitions list --group entered`（10:40/10:57）deadline=2026-10-14 23:59；官方口径帖 731587 新增 4 条截止后评论（10-01~10-02）；host 侧新口径回复（745074 内 Krzysztof Gonia 10-02 06:31）；榜 CSV 10:45:33 快照 vs 09-30 23:33 全面漂移；**无 final results/获奖/官方新帖**（20 新帖逐一验作者，无 host） |
| 2. 讨论区 | **有增量，大**（新帖 20 篇；评论级全可查） | `topics list` 5 页全量（10:43-44）：744788→745119 共 20 篇 09-30 23:38 后新帖；743993/742571/744614 commentCount 均**未变**（6/1/1，`topics show` 10:46 复核，末条评论分别为 09-28 18:44 / 09-22 15:54 / 09-30 15:31） |
| 3. 新公开 kernel | **有增量但仅老件重跑**（新 run 2 件；新建 0 件；榜顶成员开源=0 kernel） | `kernels list --competition --sort-by dateRun`（10:43）：10-01 22:57 destbreso x-ray、10-01 22:07 georgymarin 2600+ farms 两个新 run；`--sort-by dateCreated`（10:51）最新创建件仍 abhinav0370/cha22-agent（09-24）；22 作者逐人扫描（10:52-53）榜顶成员账号全部无本赛公开件 |
| 4. 数据集 | **有增量** | `datasets list`（10:51）：georgymarin/kagriculture-episodes lastUpdated **2026-10-02 01:16:55**（v79 冻结戳 09-30 00:43 之后→**v80+ 确有**）；官方日更 09-30 期（10-01 00:44:33 出包）、10-01 期（10-02 00:03:28 出包）均已出，10-02 期截至 10:51 未出 |
| 5. 我方读数 | **有增量且需更正**（计分对更正；仍在收敛） | `submissions --csv`+`episodes`（10:40-10:51）：**当前活跃计分对={56721419, 56721643}**（非任务基线所写 C_final/S8）；两活跃件 10:29-10:33 UTC 仍在打局，读数未冻结 |

## 二、块 1：比赛状态与终评

**状态**：比赛提交窗已关（09-30 23:59 UTC），处官方"两周收敛/终评"期第 2 天。`kaggle competitions list --group entered`（10:40，ext/comp_list_entered.txt）：`deadline=2026-10-14 23:59:00`、`reward=50,000 Usd`、`teamCount=10246`、`userRank=1256`。**evaluation 未完成，无 final results、无获奖公告、无官方新帖**（20 篇新帖作者逐一核验，无 María Cruz/Will Cukierski/Addison Howard 等 host 发帖）。

**终评口径三条实抓锚（存在张力，需留意）**：

1. **官方帖 731587**（María Cruz，2026-07-31，`topics show` 10:46 抓）："At the submission deadline, we will continue allowing submissions to run episodes for two weeks. At the end of those two weeks, we will be running a single Bradley-Terry Tournament, which will determine the final leaderboard rankings."（两周打局窗 + 单次 BT 定终榜；Evaluation 页同口径）。该帖**截止后新增 4 条评论**（Andrei Dzis 10-01 12:00、CemBas 10-02 00:27、Densike 10-02 00:45、Jason xu sk 10-02 08:16）追问"排位是否由两周 episodes 决定/是否 reset/截止后上传件有无补救"，**截至 10:46 均未获官方回复**。
2. **742571 内官方回复**（Addison Howard，2026-09-22，未变）："It will run over all episodes ever played between submissions that are still active..."（BT 拟合覆盖**活跃提交对**曾打过的**全部** episodes——即截止后两周内打的局计入终评）。
3. **745074 内 Krzysztof Gonia 回复**（2026-10-02 06:31/06:32，**身份未核实**，口吻似主办方）："Final rank is results of the Bradley tournament we are in right now. There is no second tournament."、"3 games during an hour can give you 1008 games in 14 days. It's enough for ranking to converge."——与 731587"期末另跑一次 BT"的字面有出入（回帖 Sheeesh--- 已贴 731587 链接反驳"Say otherwise"）。实操口径按 2+3 并读：**终榜=活跃对全程 episodes 的 BT 拟合，收敛窗至 10-14**。

**榜面漂移（10:45:33 快照 vs 09-30 23:33 收官快照，ext/lb_20261002/）**：Top1 M&M&P&Q 3073.5→**3066.9**；#2 出现 **"1x5090 potato run"（vmerckle 单人）3027.8**（09-30 榜 #2 "6x8 B200 Galaxy Run" 2948.6——改名或换位，未能确认）；DSM 2916.5→2942.2（#3）；Farmcore 2860.4→2893.4（#4，其 writeup 自称"5th Place (currently)"，与 10:45 榜 #4 有 1-2 位漂移差）；DECEM 2933.8→2890.9（#3→#5）；Majkel1337 2809.0→2775.8（#13→#15）；**Russell Kirk 队"有辣条有权"（russcore）2877.8 #6**。Top20 大量换位、分数普遍下移=BT 收敛进行中。队数 10,246 不变。

## 三、块 2：讨论区增量（20 新帖 + 关键旧帖评论级复核）

**新帖全量（postDate > 09-30 23:38 UTC，共 20 篇；来源 `topics list` 5 页 10:43-44 + `topics show` 10:45-46）**：

| postDate (UTC) | id | 标题 | 评论/票 | 性质 |
|---|---|---|---|---|
| 10-02 10:31 | 745119 | [5th Place (currently)] Farmcore: a one-pass transformer trained on executed engine events | 0/2 | **榜顶 writeup**（详见下） |
| 10-02 06:57 | 745087 | Economy was actually easy to solve, execution was much harder. | 0/0 | 经验帖 |
| 10-02 04:15 | 745074 | Games are played too rarely | 5/-1 | **含 host 侧口径回复**（详见下） |
| 10-02 03:38 | 745073 | [1st Place (currently)] A preview of our solution: BC, Self-Play PPO, and Heuristics — M & M & P & Q | 9/50 | **榜首 solution 预告**（详见下） |
| 10-01 21:19 | 745036 | It's SFT all the way down（Russell Kirk，队"有辣条有权"=LB #6） | 2/26 | **榜顶 writeup**：纯 SFT 微观动作序列、B-even/N-flow 双模型、"top3 队 09-30 胜局 404 席位作数据"（自报）、"provisionally top 10；thread 将在 writeup 出现时删除，正式文约两周后"（自报） |
| 10-01 19:04 | 744999 | Our Kaggriculture Journey: RL Experiments, Final Agents（队 "RL is all you need"） | 0/1 | writeup+GitHub（jwj1342/Kagriculture） |
| 10-01 18:20 | 744988 | ES-trained planner, residual RL head, ~190 experiments that did not ship（Roman Svet） | 0/1 | writeup+GitHub（romansvet/kagriculture，JAX 精确模拟器） |
| 10-01 14:20 | 744939 | Question for the top teams: How do you approach simulation competitions? | 6/7 | 方法论问答（Syed Asad Ali：精确快速模拟器优先；MarvinTMB：<1M 参数 BC+PPO 自对弈、10h RTX 5090，自报） |
| 10-01 07:42 | 744858 | My Solution（Eesh saxena，shepFOB4/3n） | 0/1 | writeup：Shepherd's Ledger 底盘+分层改件；"final rank=截止后 BT 拟合"（自报） |
| 10-01 04:41 | 744823 | Suggestions: compute transparency and ladder slots | 0/10 | 制度建议（"仅最新两件活跃、换件即弃历史"确认活跃池语义） |
| 10-01 04:00 | 744820 | Dominated by public kernels | 0/4 | 自报聚类 78% 对局归并到 D6 同态（自报，未复核） |
| 10-01 03:36 | 744819 | Kaggriculture research archive（Freakz2z） | 0/1 | GitHub（Freakz2z/Kagriculture，Apache-2.0） |
| 10-01 02:52 | 744814 | 🪰 FlyFarmer Solution（Takamichi Toda） | 2/9 | writeup（规则型 connectome agent，自报 777/10,246） |
| 10-01 02:13 | 744811 | Last accepted submission...missing from the active pool | 0/3 | **平台态报告**：验证完成的提交未进活跃池（疑冻结竞态），并称界面显示 100 提交配额（10-01）——**官方未回复** |
| 10-01 02:01 | 744808 | Notes and reflections on agent capabilities | 0/5 | 全托管 agent 实验失败自述 |
| 10-01 01:49 | 744786 | GiGPO: A Thought Experiment | 0/1 | 架构笔记 |
| 10-01 00:30 | 744791 | LLM provider 推广账号质疑 | 1/2 | 杂谈 |
| 10-01 00:28 | 744790 | Ported Kaggriculture to HTML Javascript | 0/0 | 外链 |
| 10-01 00:19 | 744789 | This was fun | 9/9 | 杂谈 |
| 10-01 00:19 | 744788 | Won a game right at the deadline but rating didn't update ("-NaN") | 3/0 | **平台态报告**：23:59 前完局的 rating 未更新、replay 显 -NaN；回帖 Zakaria Aala 称"all ranks are currently frozen since this counts as the final public leaderboard...they will be running a pri[vate]..."（**自报，与 745074 host 回复'现在仍在打 BT'相悖，以 host 口径+episodes 实证为准**） |

**榜顶 writeup 要点**：
- **745073（M&M&P&Q，作者 msd0110，10-02 03:38，50 票）**：BC↔自对弈 PPO 交替训练（公开回放+启发式规划器示范）；最终选 **10M 参数模型 + 推理期规则动作补丁（Final A）**（20M 线与 rule-aware PPO 变体 Final B 未采用）；自报训练血统约 **829 万局自对弈**；分工（自报）morim3=10M 线/msd0110=20M 线/piiiiiiii=启发式规划器/qistripute=规则补丁与回放分析；算力（自报，评论区）：10M PPO 峰值 17×A100+29×A30、20M 峰值 26×A100；"ratings 收敛并确认终榜后发详细 writeup"（自报）。**代码链接=https://github.com/msdsm/kagriculture-solution**（topic-messages 原文抽取）——**该仓 10:53 搜索快照可见（created 2026-10-02 03:17Z、5 stars），10:55-10:58 复查 API/网页/search 三路均 404/查无（疑转私或撤仓），公开面当前不可得**。
- **745119（Farmcore，作者 Yaroslav Pudovkin，10-02 10:31）**：**纯 BC 无 RL 无搜索**；关键三招（自报）：(1) 模仿目标改"引擎实际成交的 state change"而非玩家请求动作（15 个榜顶玩家回放显示挂单常被引擎静默截断，某教师 87% 采购请求未成交）；(2) 多强队预训练→单队微调→两微调权重平均（soup +$3.3k/46-48，自报）；(3) checkpoint 只按同种子金钱选（验证精度与实战负相关 −0.86，自报）。架构：21.5M 参数（约 16M 参与推理）单前传 draft + 6 层 corrector，移动用最短路规则；corrector 改写 25% 单位目标/74% 回合市场单（自报）；PPO 只带来几千刀/局，最终两件提交均为纯模仿（自报）。算力 2×A100+免费云 notebook（自报）。

**关键旧帖复核（10:46，`topics show`）**：
- **743993 开源帖：commentCount 6→6，未变**（末条 Hak 09-28 12:05、Syed Asad Ali 18:44:57），**无新增评论**；本轮已能取全评论树（上轮手段限制解除），未见官方答复。
- 742571（终评口径）：commentCount 1→1，未变（唯一回复=Addison Howard 09-22 15:54，见块 1 引文）。
- 744614（重激活问询）：commentCount 1→1，未变（千早愛音 09-30 15:31）。
- 743384（"Question for M & M & P & Q and Boey"）：commentCount 6，榜顶**仍未直接答**；但 745073 实际上就是 M&M&P&Q 的公开作答。

## 四、块 3：新公开 kernel（截止后 run/新建全量）

**基线后新 run 全量（dateRun > 09-30 23:38，2 件；来源 kernels_daterun_p1.json @10:43）**：

| lastRunTime (UTC) | ref | 作者 | 票 | 自报描述/许可 | 备注 |
|---|---|---|---|---|---|
| 2026-10-01 22:57:56 | destbreso/x-ray-your-agent | destbreso | 52 | 标题即自报（agent 拆解/诊断向）；许可未拉取 | 09-30 23:01 后**再次重跑**；内容开挖归并行子代理 |
| 2026-10-01 22:07:56 | georgymarin/kagriculture-what-2600-farms-do-differently | Georgy Mamarin | 55 | 标题即自报（2600+ 农场行为分析）；许可未拉取 | 09-30 22:06 后**再次重跑**；同上 |

- **截止后新建 kernel：0 件**。`--sort-by dateCreated`（10:51）最新创建件仍停在 **09-24**（abhinav0370/cha22-agent）——与上轮结论一致，全站本赛公开面零新发布。
- **补录基线漏网 1 件（截止前）**：farhanabidtech786/kagriculture-beginner-friendly（Farhan Abid，lastRun **09-30 18:10:49**，9 票）——落在上轮 final-hours（18:10 两轮比对）与 closing-sprint（只看 19:00 后）的缝隙，本轮 dateRun 全量比对补见。
- **在册 22 作者+榜顶成员逐人扫描（10:52-53，authors/）**：majkel1337、morimo、msd0110、piiiiiiii、qistripute、tetsu2131（账号实为 tetsutani）、tarosqrd2、georgymarin（账号 georgymarin）=**Not found（无任何公开 kernel）**；zy1343930734（DECEM）5 件最晚 2026-02、alperen5252525 最晚 09-19、haodou092 最晚 09-30 15:56、shiiin9 最晚 09-29、leoprovorov 最晚 09-30 23:15、ashok205/statma/prvsiyan/vmerckle/russcore 均 0 个基线后新 run。**榜顶 22 作者开源兑现（kernel 侧）仍=0**。
- 非本赛噪声（供排除）：anhadmahajan06/s6e10-are-you-satisfied（10-01 20:14，S6 外赛）、haideptry CASMI/Gemma 系 6 run（10-01~10-02）、guruprasaathas111/arc-agi-2（10-01 15:38）。
- 票数漂移（10:43 vs 09-30 23:31 基线）：leoprovorov ice-fire 103→109、georgymarin 2600 54→55、anhadmahajan06 V8 23→26、flexonafft 123→125、lynnsakurai wheat 41→43、tetsutani 138、evgendvorkin 73→72（微动）。
- **"final submission/solution"自名件**：本赛 kernel 面仅 leoprovorov/a-song-of-ice-and-fire-final-update（09-30 23:15，基线已录）；截止后自名 solution 均出现在**讨论区**（745073/745119/745036/744858/744814/744999），不在 kernel 面。

## 五、块 4：数据集

来源：`kaggle datasets list` 三组查询（10:41/10:51，ext/datasets_list_2026-10-02.json）。

- **georgymarin/kagriculture-episodes：v80+ 确有**。lastUpdated=**2026-10-02 01:16:55**（上轮冻结 v79 @09-30 00:43 → 此后至少一次新版）。**版本号本身不可得**（metadata/files 403），故只能判"≥v80、10-02 01:16 为最新版戳"；09-30 00:43→10-02 01:16 之间有无中间版未知。
- **官方日更 episodes**：`kaggle/kagriculture-episodes-2026-09-30` **已出包**（lastUpdated 2026-10-01 00:44:33；上轮 18:02 时还没有）；`kaggle/kagriculture-episodes-2026-10-01` **已出包**（2026-10-02 00:03:28）；`-2026-10-02` 期**未出**（截至 10:51；按惯例次日 00:0x 发）。`kaggle/kagriculture-episodes-index` 同步更新于 2026-10-02 00:03:29。→ **官方日更管线进入终评期未停**。
- 第三方新件：farukece/kagriculture-episodes（"1,402 Replayable Games"，10-01 09:13）、dariushafshar/kaggle-competition-leaderboard-intelligence（10-02 06:47）——新出现，用途未核。
- 异常：`datasets list --user georgymarin` 返回空（`-s` 搜索可见该件）——CLI user 过滤异常，非数据集消失。

## 六、块 5：我方读数（含基线更正）

**更正：当前计分对={56721419, 56721643}，不是 {C_final 56697824, S8 56708866}**。任务基线"计分对 {C_final,S8} 已定格"实为 09-30 17:42（lb-sweep6）时刻的活跃对；其后我方 19:05/23:26/23:36 三次提交依次顶掉旧件（每上传一件退役最旧活跃件，744823 语义），至截止活跃对已换为末两件。证据链（10:45-10:51 实抓）：

| 提交 ref | 提交时刻 (UTC) | publicScore（10:40 读） | episodes 数 | 末局 createTime | 活跃? |
|---|---|---|---|---|---|
| 56697824 C_final | 09-30 05:06 | **1783.1**（09-30 17:42 曾读 1796.2，−13.1 后冻结） | 120 | 09-30 18:36 | 否（19:05 被顶） |
| 56708866 S8 | 09-30 13:36 | **1476.8**（17:42 曾读 1490.5，−13.7 后冻结） | 75 | 09-30 23:13 | 否（23:26 被顶） |
| 56716525 H1X | 09-30 19:05 | 1642.1 | 68 | 09-30 23:35 | 否（23:36 被顶） |
| **56721419 composite** | 09-30 23:26 | **1699.3** | 119 | **2026-10-02 10:33** | **是** |
| **56721643 H1X-a** | 09-30 23:36 | **1743.8** | 133 | **2026-10-02 10:29** | **是** |

- **队分（官方榜 CSV 10:45:33）：rank 1257 / renyxin / 1743.8 / LastSubmission 09-30 23:36:00 / SubmissionCount=2**——队分=活跃对较高者（56721643 1743.8），与 SubmissionCount=2、末次提交时刻三点互证。
- **仍在收敛，未冻结**：两活跃件 10:29/10:33 UTC 仍在出新局（距抓取仅 10 余分钟）；745074（10-02 04:15）多人自报 rating 持续变动、Gonia 口径"14 天收敛窗"。队分轨迹：1796.2（09-30 17:42）→1646.1（09-30 23:33）→**1743.8（10-02 10:45）**，名次 #1198→#1715→**#1257**，双向漂移=换件+BT 重拟合叠加。
- 按 Addison Howard 口径（BT 覆盖活跃对全部 episodes），**我方终评输入即为 56721419+56721643 的全程对局**，C_final/S8 已不在终评语义内（其 09-30 晚间读数仅作历史记录）。

## 七、附：站外 GitHub 快照（745073 开源线索为主，10:53-10:57 实抓）

- `q=kagriculture pushed:>2026-10-01` → 35 仓；`q=kagriculture created:>2026-09-30T23:38` → 15 仓。**开源潮在赛后爆发**（对比截止前 393 仓中榜顶 0 仓）。
- **榜首 M&M&P&Q**：745073 自报代码仓=github.com/**msdsm**/kagriculture-solution（msdsm 账号名 "MSD"，与成员 msd0110 对应；created 2026-10-02 03:17Z、5 stars@10:53 搜索快照）——**10:55 后复核 404/搜索查无，当前不可公开访问**（转私或撤仓；保留快照待复查）。
- **榜顶成员新仓**：atsushi11o7/kagriculture（LB #21 成员，10-01 11:55Z）、PavelSavchenkov/kagriculture（LB #25 队"My second life"成员，10-01 07:59Z）——中段榜成员率先放码；**#1-#15 主力（majkel1337/DECEM/DSM/Farmcore/MarvinTMB 等）除 M&M&P&Q 外未找到新仓**。
- 自名解决方案仓（自报，未核内容）：sunyuxiang136/kagriculture-silver-agent（"Silver Medal Solution"）、egoring/Kagriculture（自报峰值 14 位 2819/收官 117 位 2505.9）、CarsonBurke/kagriculture（"A top model"）、msdsm 见上；writeup 对应仓：jwj1342、romansvet、eeshsaxena、Freakz2z、debmalyaroy、sweeden-ttu/kagriculture_1_37_muzero、graceyunliu（10-02 10:38 仍在推，自进化循环延续）。

## 八、异常与限界

1. slug 假 404（见环境注记 1）；2. `competitions describe` 不存在（改用 list --group entered/榜单/topics 三源拼状态）；3. datasets metadata/files 403 → 版本号不可得，georgymarin 只能判"≥v80"；`datasets list --user georgymarin` 空返回异常；4. `competitions hosts` 403 → Krzysztof Gonia 身份未核实（口径按"疑似 host"降权使用）；5. 竞赛页 JS 壳，无"evaluation 是否完成"的官方页面级证据，状态判定靠 deadline 字段+评论区口径+episodes 活动实证；6. 745073/745119 正文图片（结构图/曲线）为 GCS 附件，未下载；7. kernel 许可字段需 pull 元数据，为避让并行开挖子代理未拉取（2 件新 run 件许可=未获取）；8. GitHub 搜索按仓名/描述含 kagriculture 召回，改名仓可能漏；9. "1x5090 potato run"（#2）与旧 #2"6x8 B200 Galaxy Run"的关系（改名/异队）未核实；10. 744788 回帖"ranks currently frozen"与实测仍在打局矛盾，已按实测采信。

## 九、建议（分级）

- **P0**：我方计分对更正入库（C_final/S8→56721419/56721643），metrics/复盘一律以新对为终评输入；对 C_final/S8 的一切"终评期望"作废。
- **P0**：盯 msdsm/kagriculture-solution 是否重新公开（10:55 404，可能是短暂转私）——榜首代码是全战役最高价值战利品；建议 24h 内复探 + 尝试 web.archive/搜索缓存。
- **P1**：10-14 23:59 终评窗结束前安排 1-2 次平台扫（episodes 是否停、榜终态快照、731587 追问是否获官方答、745073 承诺的"详细 writeup"是否落地）。
- **P1**：对 745119（Farmcore）"按引擎成交重标注"与 745073（M&M&P&Q）"10M+规则补丁/829 万自对弈"做技术拆解（若归复盘轨）；二者+745036 是终评期三篇最有含量的 writeup。
- **P2**：georgymarin/kagriculture-episodes 新版（10-02 01:16）内容量核对（是否覆盖 09-30/10-01 期 episodes）；官方 10-02 日更出包后核量。
- **P2**：将"评论正文可取（competitions topics show / topic-messages）"写进扫描技能备注，解除旧限界。

## 十、来源清单

- kaggle CLI 2.2.4（全部10:39-10:58 UTC）：`competitions list --group entered -v`；`competitions submissions -c kagriculture --csv`；`competitions leaderboard kagriculture -d`（zip→lb_20261002/，快照戳 2026-10-02T10:45:33）；`competitions topics list kagriculture -p 1..5 --format json`；`competitions topics show kagriculture <745119|745087|745074|745073|745036|744999|744988|744939|744858|744823|744820|744819|744814|744811|744808|744786|744791|744790|744789|744788|743993|742571|744614|731587>`；`competitions topic-messages kagriculture 745073 --format json`；`competitions episodes <56697824|56708866|56716525|56721419|56721643> --format json`；`kernels list --competition kagriculture --sort-by dateRun|dateCreated --format json`；`kernels list --user <22 账号>`；`datasets list --user georgymarin / -s kagriculture / -s kagriculture-episodes --sort-by updated`。
- 官方页：https://www.kaggle.com/competitions/kaggriculture/overview （JS 壳，10:57 curl，无正文）；https://www.kaggle.com/competitions/kaggriculture/leaderboard （CSV 见 ext/lb_20261002/）；讨论区各帖 URL 形态 https://www.kaggle.com/competitions/kaggriculture/discussion/<id> 。
- GitHub REST（10:53-10:57）：api.github.com/search/repositories（q=kagriculture pushed:>2026-10-01 / created:>2026-09-30T23:38 / user:msdsm）、/repos/msdsm/kagriculture-solution（404 记录）、/users/msdsm。
- [前次] `2026-10-01-closing-sprint-scan.md`（基线止点 2026-09-30 23:38）、`2026-10-01-lb-sweep6.md`（我方 17:42 读数）、`2026-10-01-final-hours-scan.md`（环境 403 注记、09-30 18:10 比对）。
