# 2026-10-01 终点前扫描（final-hours 四通道）——截止前 ~6h 增量

> 抓取时点 **2026-09-30 17:40–18:15 UTC**（=CST 10-01 01:40–02:02）；通道：kaggle CLI 2.2.4 + GitHub API + URL 探测 + WebSearch。基线：上轮双通道扫描（`2026-10-01-final-window-sweep.md`，截至 16:35 UTC）。纪律：逐条带来源 URL+抓取时间；自报数字标"自报"；查不到写"未找到更新"。截止=09-30 23:59 UTC。
> 环境注记：本机 CLI 的 `datasets metadata/files` 端点对本赛数据集（含官方 kaggle/* 件）一律 403，版本判定改用 `datasets list` 的 lastUpdated 字段；竞赛论坛无法用 `forums topics list` 列出（403，slug 命名空间仅覆盖全局论坛），新帖发现改用竞赛域 URL 探测法（详见 ext/final-hours/discussion_probe_2026-09-30.txt）。

## 一、新公开件清单（通道1，kaggle kernels list --sort-by dateRun，17:42 首扫 + 18:10 复扫）

相对 16:35 基线（haodou V94@15:56 / leoprovorov 两件@15:48,15:31 / evgendvorkin@15:46 / lynnsakurai@13:05 / flexonafft@11:40 / anhadmahajan06@09:43）：

| # | 件（lastRun UTC） | 版本/增量 | 许可 | 榜顶作者? |
|---|---|---|---|---|
| 1 | **lynnsakurai/farmer-john-and-the-wheat-seller @17:19:36**（41 票） | **重写验收准则的延售释放控制器**：r_g=min{8,q_g,d_g,H} 释放量公式；接受条件改为价差 p_g(I−d_g)−p_g(I)≥3 **且** 释放收益 r_g·Δp≥10；新增"Guarded changes"护栏（到期量不得二次延后、容量按售后库存计、10 市场槽满则挂账不删单、部分成交部分重试、未知 schema 直通父策略）。**旧 13:05 版的"margin>0.5 接受准则"语言已全文消失**（自报，源码级核验；CLI 不暴露版本号，版本间差异未逐字 diff） | 未声明 | 否（Arlene，社区拆解系） |
| 2 | **flexonafft/kaggriculture-multi-route-farming-agent @16:57:34**（123 票） | **打包对象切换**：由 god-s-mode v7（上轮已测 WEAK，证据 ext/godv7/）→ **ahmedberatozer V43 "Recovering Lost Harvests"**。头部自述"preserves the public agent… The published score is historical and may not repeat"（自报）；build_manifest（自报）：version=v43, classification=evaluated_upgrade, EXP277 定向仓库/EXP278-279 动作等价改写，exp279 isolated runtime+linux replay passed，EXP277/278 runtime failed，live_rating_guarantee=None；main_sha256=919fc1d6…，archive_sha256=f76baf85…。源件 ahmedberatozer/kaggriculture-v43-recovering-lost-harvests **仍公开**（09-20 前老件，id_no=134403057，competition_sources=kaggriculture） | 上游 Apache-2.0（ahmedberatozer 系） | 否（Igor Zharov，存档转制人） |
| 3 | **anhadmahajan06/kaggriculture-autonomous-ai-farming-agent @17:53:27**（21 票；18:12 UTC 复扫新抓，17:42 首扫时仍为 09:43 旧 run） | 自报头部"Grandmaster Agent (Version 8)"：V56 底座（EarlyCycle 直种 5 麦开局消 12 币摩擦）+ E402 后期封种（T612-648 停买胡萝卜/麦种）+ E410 施肥保守（T600-718 自报省 ~1000 肥料单位、清算 +2000~3000 币）+ Layer D 订单簿锁步结算（自报 +180 币净边际）；自报确定性胜率 100%（seed 42/100 双席位）、源件 1,067,635 字节 sha256=9e460f53…。与 09:43 版内容差异未核验（旧版无存档可 diff） | 未声明 | 否（Anhad Mahajan，综合转制系；V56=ahmedberatozer 血缘） |

- **haodou092/kaggriculture-harvest-ledger：未找到 V95+**。lastRun 仍 15:56:57；17:42 重拉最新版头部仍为"Kaggressulture V94 — Verified Spatial Mirror Gate"（正文中的 V97/V98 字样经核验为内嵌压缩归档的随机字符串，非版本号）。
- **leoprovorov 两件：未找到更新**（god-s-mode lastRun 15:48 / ice-and-fire 15:31 均未变；god-s-mode 源件内 engine_version=1.32.7，无 v8 迹象）。
- 其余在册件（haideptry×2 / shiiin9 / guru×2 / tetsutani / lynnsakurai idle-seller / destbreso x-ray / georgymarin×2 / evgendvorkin / ashok205）：**未找到更新**（dateRun 前 50 于 17:42 与 18:10 两轮全量比对）。
- **榜顶队伍成员新公开件：未找到**。dateRun 前 50 无 M&M&P&Q（morimo/msd0110/piiiiiiiii/qistripute）、DECEM（zy1343930734）、vmerckle、DSM、Majkel1337 等任何件；dateCreated 排序显示最新创建件仍停在 09-24（近期全部是老件重跑，无新发布）。

## 二、讨论区（通道2，17:47–17:58 UTC）

- **本赛论坛零新帖**：对 744615-744740 全量 URL 探测+逐帖内容核验（CLI `forums topics show`），本赛论坛最新帖仍是 744614（09-30 14:40，上轮已报）；探测命中的 20 个真实帖全部属外坛（ARC-AGI-3、音频 notebook、SWE-bench、memecoin 赛、课程论坛、WriteUp 垃圾）。**榜顶选手新发言：未找到**。原始证据：ext/final-hours/discussion_probe_2026-09-30.txt。
- **三关键帖后续回复：均无**。743993（开源问询）6 条回复全在 09-28；744614（重激活问询）仅千早愛音 15:31 一条；742571（终评口径）仅 Addison Howard 09-22 官方回复——**终评口径无新说法**（BT 全窗对局史、仅计仍活跃提交间对局）。
- **重要旁证——全站截止新规帖 744617**（Will Cukierski，Kaggle 竞赛负责人，09-30 14:48:35，`forums topics show` 抓取）：代码赛/文件赛改为"须在截止前完成评分"，**Simulations Competitions (Agent-based)：No change（仍为截止前完成上传即可）**；目的为"截止时即刻放出（初步）正确榜"。对本赛含义：23:59 UTC 前完成上传即有效，无需等待验证局打完；但官方鼓励勿压哨（评分排队 p90=18.2s 为全站历史数据）。来源 https://www.kaggle.com/discussions/744617 之类规范路径不可得（全站帖），以 CLI 抓取文本为准。
- 分享锁 bug（741281 相关观察）：本窗未再复查；上轮结论（09-30 仍有新件发布=未修）无反证。
- **doanthuan/kaggriculture kernel：仍 403**（`kernels status`/`kernels pull` 均 Permission denied，17:43 UTC）——与上轮一致，非临时故障。

## 三、数据集（通道3，17:44-17:58 UTC）

- **georgymarin/kaggriculture-episodes：未找到 v80+**。`datasets list -s kaggriculture --sort-by updated` 显示 lastUpdated 仍为 **2026-09-30 00:43:36.270**（=v79 推送戳，与上轮一致）；29.94GB/33885 下载/67 票无变化。metadata/files 端点 403（端点级，官方件同 403，见环境注记）。
- **官方日更：09-30 期未出包**。列表中最新为 `kaggle/kaggriculture-episodes-2026-09-29`（lastUpdated 09-30 00:05:29，size 显示 0——09-26 期同样显示 0，疑为列表 size 字段未回填的显示异常，文件级核验因 403 无法完成）；`-2026-09-30` slug 检索无结果。索引件 `kaggle/kaggriculture-episodes-index` lastUpdated 09-30 00:05:31。按出包节律（每日 ~00:05 UTC），09-30 期约在 10-01 00:05 UTC 出——**截止后**。
- 其余（ashok205 top10-replay-archive 09-26、xishengfeng replay-db 09-26、billll BC sweep 09-26 等）：未找到更新。

## 四、GitHub（通道4，17:45-17:57 UTC）

- **仓库总数 393，零新仓**（`q=kaggriculture` total_count=393，与上轮持平；created:>09-29T16:00Z 仅 3 仓，全部在上轮已入册：Manav20032008 09-29 18:46、daulettoibazar 09-30 09:27、elrensmin 09-30 09:21）。
- **pushed:>2026-09-30T16:00Z 唯一 1 仓**：`the-genius-man/kaggriculture-agent`（无许可，0 star，09-18 建）。今日两笔自动提交：dbfd4c0 @13:27Z、4411429 @17:06Z，message 为"feedback <时间戳>"，变更仅 analysis/feedback/*（episodes.json/leaderboard.txt 快照/submissions.csv/kaggriculture.zip/docs/index.html）——**自反馈流水线仓，无策略代码增量**；其 leaderboard.txt 快照（17:06 世代）顺带留下冲刺痕迹：Majkel1337 #11 2822.2（末次提交 04:52）、Anton Tikhonov 末次提交 16:52、KawattaTaido 14:59、Luca 15:06。来源 api.github.com/repos/the-genius-man/kaggriculture-agent/commits。
- **doanthuan/kaggriculture：未找到新 commit**（since b325122@00:41:35Z 仅其自身，Apache-2.0，终态结论维持）。
- HN Algolia `kaggriculture`：0 命中；Bing `site:github.com kaggriculture`：无新索引（仅一条过期 profile 提及）。赛后拆解/复盘：未找到（截止前 6h，常态）。

## 五、榜面快照（旁证，ext/lb-20261001/ CSV，2026-09-30T17:41:44Z，10216 队）

| # | 队 | 分 | vs 16:11 快照 | 末次提交(UTC) |
|---|---|---|---|---|
| 1 | M & M & P & Q | 3047.3 | +8.5 | 15:21 |
| 2 | DECEM | 2965.4 | +7.3 | 10:46 |
| 3 | Victor @ Tufa Labs | 2954.1 | −3.4 | 14:25 |
| 4 | DSM | 2928.8 | （16:11 表外） | 14:09 |
| 5 | CDE | 2896.1 | +16.5 | 07:36 |
| 9 | Gemini IS ALL YOU NEED | 2852.9 | +2.7 | 13:31 |

- 我方 renyxin **#1198 / 1796.2**（16:11 为 #1160/1813.9；−17.7 波动，末次提交 13:36:40 不变=2 槽换交暂态 BT 读数漂移，非我方动作）。换交窗口噪声持续，榜面读数在 10-01+ 两周收敛期前无终评意义。

## 六、对同门带（haodou 系）相关的增量小结

- haodou092 停更于 V94（镜像门定稿件，上轮已池测 COMPETITIVE 但低于我方现件）；V95+ 未出现，**"仅同血脉触发"自报口径与 78.5% 触发仍输 V82/H1 的实测矛盾维持原判**。
- 同门带外围：flexonafft 从打包 god-s-mode v7 转向 ahmedberatozer V43（同门"存档转制"生态位持续活跃，但转制对象分与策略血缘无关）；lynnsakurai wheat 件重写准则（启发式延售族，上轮已证负区，新阈值版未池测——如需可按 godv7_lab 惯例补测，但属已证负区家族的参数化微调，优先级低）。

## 七、来源清单（均 2026-09-30 17:40-18:15 UTC=CST 10-01 01:40-02:15 抓取）

| # | 来源 | 通道 | 戳 |
|---|---|---|---|
| S1 | https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-wheat-seller | kernels pull | lastRun 09-30 17:19:36 |
| S2 | https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent | kernels pull | lastRun 09-30 16:57:34 |
| S3 | https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger | kernels pull | 版本头 V94；lastRun 15:56:57 |
| S4 | https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v43-recovering-lost-harvests | kernels pull -m | id_no 134403057 |
| S5 | https://www.kaggle.com/code/leoprovorov/god-s-mode-hacked-stores | kernels pull | lastRun 15:48:15 未变 |
| S5b | https://www.kaggle.com/code/anhadmahajan06/kaggriculture-autonomous-ai-farming-agent | kernels pull | lastRun 09-30 17:53:27 |
| S6 | 743993/744614/742571/744617 等 | kaggle forums topics show | 17:47-17:58 |
| S7 | georgymarin/kaggriculture-episodes、kaggle/kaggriculture-episodes-* | datasets list | 17:44 |
| S8 | api.github.com search/repos（q=kaggriculture、pushed/created 过滤）、repos/*/commits | REST | 17:45-17:57 |
| S9 | https://www.kaggle.com/competitions/kaggriculture/leaderboard（ext/lb-20261001/ 共享快照） | CSV | 2026-09-30T17:41:44Z |
| S10 | hn.algolia.com、Bing site: 检索 | web | 17:56-18:01 |
