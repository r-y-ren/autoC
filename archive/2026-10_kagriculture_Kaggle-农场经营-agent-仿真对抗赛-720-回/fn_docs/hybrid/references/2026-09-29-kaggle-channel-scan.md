# 2026-09-29 Kaggle 频道增量扫查（Kaggle 频道线上扫查轮）——09-28 晚之后的新 run/新件/新帖/数据集/榜面

> 任务：扫查 09-28 晚（基线=2026-09-28-family-update-scan.md 午后轮 + 2026-09-28-family-topband-deepcut-scan.md 17:50 截稿）之后 Kaggle 频道新增量，判断有无可改善我方策略的内容。
> 抓取日期统一 **2026-09-29**（榜面快照 11:15 UTC）。通道：kaggle CLI 2.2.4（kernels list 全量翻页/kernels pull/API v1 kernels/pull currentVersionNumber/topics list+show/leaderboard download/datasets list）。
> 纪律：逐条带来源 URL；自报数字标"自报"；我方解包/重算标"重算"；查不到写"未找到"；工作件在 /tmp/scan_k/（未入仓）。候选项对照分析37 §一"已关门面"标注禁区关系。

---

## 〇、增量 vs 基线对照表（kernels，09-28 18:00 后有新 run 者全量）

| 件 | 基线状态 | 现行（CLI dateRun / API 版本） | 增量判定 |
|---|---|---|---|
| haodou092/kaggriculture-harvest-ledger | V85（V82 后未测） | 09-29 08:26 / 保存版次 88，笔记本标签 **V89** | **有内容增量**（V82→V85、V85→V89 两级 diff，见一-1） |
| leoprovorov/a-song-of-ice-and-fire-fixed-flexible | v22（09-28 07:11） | 09-29 09:12 / v24 | 无内容增量（与 v22 缓存单元格源逐字节一致，纯重跑） |
| leoprovorov/god-s-mode-hacked-stores | v23（09-28 03:04） | 09-29 09:12 / v26 | 无新机制（结构普查同 v23 主题；新增 SUBMISSION/ARTICLE 双渲染模式包装） |
| flexonafft/kaggriculture-multi-route-farming-agent | 基线外（mooman 战报知 multiroute_v70） | 09-29 10:09 / v106 | **有内容增量**（改打 MarketShock-M1-WR1K 提交适配，见一-4） |
| haideptry/the-shepherds-ledger-herd-safe-sovereign | 09-25/27 在册（T4 镜像抢先壳） | 09-29 00:45 / v12 | **有内容增量**（整件换装 MarketShock-M1-WR1K 引擎，见一-5） |
| guruprasaathas111/game-theoretic-master-discrete-optimization | 基线外新件 | 09-29 04:50 / v3 | **新登记**（零 blob 明文 V49 源，见一-6） |
| evgendvorkin/kaggriculture-version-31-26-09-bronze-going-up | 基线外新件（在册仅其旧件 kaggriculture） | 09-28 20:33 / v32 | 新登记（公开件学习收割笔记，无机制增量） |
| destbreso/x-ray-your-agent | 09-27 23:00 版已收 | 09-28 23:03 / v91 | 例行日更重跑，未找到新指标 |
| ashok205/top10-replay-dataset-archive（kernel） | 09-28 已收 | 09-28 22:43 / v43 | 例行归档维护器重跑 |
| georgymarin/kaggriculture-what-2600-farms-do-differently | 09-27 22:10，pull 403 | 09-28 22:13 / — | 有新 run；**pull 仍 403**，内容未获取 |
| tetsutani/demand-preserving-turn-sale-timing | step1009（09-27 02:50） | 09-28 17:41 / v16 | 无内容增量（与 09-28 深挖缓存逐字节一致，重跑） |
| haideptry/the-2965-master-hybrid-engine、guru V5（v3）、guru top-2-master-engine-v4（v11）、lynnsakurai/farmer-john（v4）、statma ca25（v1）、prvsiyan（v1）、shiiin9（v2）、uninhibitedscholar（v1）、alperen 五件 | 在册 | 无新 run | **未找到更新** |

顶强开号核查（重点②）：Majkel1337/majkel1337、SpaTaro/tarosqrd2、Boey、akimaru、masspeaks 名下均 "Not found"（无公开 kernel）；denden12/shimishige/zy1343930734（DECEM）/linkinpony/kurupical 仅有他赛题旧件。**未找到顶强开号发件**（与 GitHub 频道 09-29 扫查"开源承诺兑现窗口在截止后"互证）。

---

## 一、kernels 增量细账

### 1. haodou V82→V85→V89 行级 diff（重算：本地缓存 V82/V85 main.py × 现行 V89 解包，SHA 校验通过 01ee3976…）

- **V82→V85**（唯一 hunk，尾壳 10139-10156 行）：**摘除** V82 的 PET_CAFE 需求倾斜壳（d10-23 且 PET_CAFE 解锁 → `_CA_MARGIN=-22`，用后还原）→ **换装 fail-closed 接口守卫** `v85_fail_closed_interface_agent`：父动作 dict（farmer/hands/market）结构合法即恒等直返；异常或畸形顶层动作按手牌数回退合法 PASS，防单次异常态终局。即 **V85 = V82 正文 −PET 倾斜 +接口防崩壳**。
- **V85→V88**：正文无变化（V85→V89 diff 仅尾壳一个 hunk，证明 V86-V88 为标签空转/回滚，正文与 V85 同构）。
- **V85→V89**（唯一 hunk）：fail-closed 壳撤除，换装 **G793 镜像家族门**：`_g793_shape(farm)`=(unlocked_quadrants, tiles 的 kind/crop/animal 计数) 结构指纹；step 96-120（d4-5）比对双方农场，**结构镜像且 |money 差|≥20 → 判"cha22 家族"→ 本局永久旁路 `_s793_reorder` 固定卖单置换优化器（保留父顺序）**；对精确 V76 镜像保留优化器；异常回退原优化器。
- V89 自报：12 个最新在线种子对 cha22 家族 10 胜、均 **+675 币/局**；5 个未见种子双席 8/10 胜 cha22；对 V76 策略 10/10 逐字节打平（门=零副作用）——**全部自报未复核**。

### 2. icefire v22→v24（重算 diff）：23 单元格源与 09-28 缓存**逐字节一致**，v23/v24=纯重跑无内容增量。

### 3. god-s-mode v23→v26：无 v23 缓存只能结构普查——章节与在册 v23 口径同构（DIG→RNG 撬动/杂草 Bernoulli 传感/31-bit 种子签名/五门生产控制器/64 world 仪表盘）；c2 新增 "One notebook, two execution modes"（SUBMISSION 跳渲染 / ARTICLE 全渲染，无外部 Dataset）。**未找到新机制结论**。

### 4. flexonafft v106（115 票，09-29 "Comment-only submission adaptation"）：内嵌 leoprovorov **MarketShock-M1-WR1K** 运行时（base85+lzma，SHA256 钉死，上游 hash 校验后加回调），入口显式 `kaggle_submission_agent` + `get_last_callable` 自检 + kaggle-environments==1.32.7 钉版双席 smoke；明言"两适配件共享同一 agent，双提交=同策略测试"。mooman 战报中的强件 multiroute_v70 作者公开转向 leoprovorov 开源运行时=对手群体收敛信号。

### 5. haideptry shepherds-ledger v12（35 票）：整件重挂 **MarketShock-M1-WR1K 引擎**（gzip+base64 内嵌 main.py 897,884B，SHA-256 1eb0938d…，stdlib-only AST 断言）+"Water Repair Local Patch"（自述 turn 506-527）+ 引 top-50 玩家 Syed Asad Ali 价格信号论（与二-743993 同源）。自报战报矩阵：对 Herd-Safe 基线 100% +$1,280/局、对纯回放克隆 28-0、对 "Legacy 2950" +$910/局（均自报未复核）。

### 6. guru game-theoretic-master-discrete-optimization v3（新登记）："Pure Uncompressed Master Agent (Zero Blobs | 200k+ Score)"（"200k+"为自报银行额口径非榜分，勿引）；正文=扩展式博弈数学式（T=720/30 日）+ **449KB 明文源码**（零 blob，SHA 钉死 ed89be8c…，产出 submission_competitive_v2.tar.gz）；源码头为 EXP157/167/173/257/260 系列+Ahmed Berat Ozer v31 谱系+多上游 Apache-2.0 署名。价值=第二件可读全文产线存档（与 tetsutani step1009 并列，供 B4 对照读）。

### 7. evgendvorkin version-31-26-09 v32（新登记）：自述"按速度排序公开 notebook、从最弱跑到最强逐个学习"的收割型学习笔记（自述 DEEPSEEK 三对话学习法），无机制增量。

## 二、讨论区增量（vs 基线：743993 0 回复、742856 在册）

**新帖 6 件（全部 09-29 凌晨-上午，主题=提交队列/服务器过载）**：
1. 744277 "[RESOLVED] Servers Overloaded -> Queue times"（https://www.kaggle.com/competitions/kaggriculture/discussion/744277 ，**官方** Bovard Doerschuk-Tiberi，09-29 07:55，10 票）："Your queued submissions should be running their validation matches now! No need to re-submit."
2. 744219 "Unusual long pending time"（10 回复）：pending 1-3h 实录；一用户"resubmitted…but it cost me 1 sub as it was pending forever"（重交烧配额实录）。
3. 744218 "Is Kaggle lagging?…14 matches queued"（11 回复）/ 744261 "Pending + in process"（9）/ 744255 "why is submission taking too long"（3）/ 744287 "Submission sent!"（0）。

**743993 后续（0→6 回复）**——Syed Asad Ali（自报 top-50）终局方法论（自报）：①赛后大概率开源 writeup、未必开源权重；②头部=IL+RL 学习模型+确定性守卫规则+关键时刻 look-ahead/search 的复合体，"It's not just RL"；③**"top agents react to the market, not the opponent"**——对手影响主要经共享价格传导，价格信号已携带大部分对手信息，直读对手农场"只在少数特定情形有用"；更大杠杆=建造顺序/按解锁商店生产/卖时；④给定 seed 全局确定性，回放是好教材。

**742856（评估方法论帖）：未找到新回复**（仍 0 回复）；其余在册帖无官方新回复。

## 三、对战数据增量

1. **georgymarin/kaggriculture-episodes**：09-29 00:10 **新版本**（日更确认）；但 datasets.get/files/download 现均 403/denied（作者收紧，09-28 00:25 版曾可下载）——**该取数入口失效**，回放取数改走官方日包。
2. **leoprovorov/a-song-of-ice-and-fire-interactive-dashboards**：**仍 v1（09-20 19:18），未找到新版**。
3. **ashok205/top10-replay-dataset-archive（数据集）**：**重试仍 403**；同源公开集 ashok205/kaggriculture-top10-replay-archive v41/3.95GB 末更 09-26 22:51（晚于其维护器 09-28 22:43 的 run——疑归档写入滞后/受限）。
4. 官方日包：**kaggle/kaggriculture-episodes-2026-09-28**（719MB，09-29 00:03）+ kaggle/kaggriculture-episodes-index **v61**（09-29 00:03）。
5. 基线外新见数据集（非本窗口新增，登记备胎）：xishengfeng/kaggriculture-replay-db（2.0GB，09-26）、kksky9k/kaggriculture-r88-rivals（09-25）、billll/stage25-bc-capacity-sweep（BC 容量扫描，09-26）、chaitanyagullapalli/kaggriculture-cpp（09-27）。

## 四、榜面读数（2026-09-29 11:15 UTC 快照 vs 昨日）

- **我方**：renyxin（TeamId 16784420）rank 813，榜面 **2069.5**；计分对=H1 56650881 **2069.5**（昨 2074.0，−4.5 平稳）+ oc_c3 56672720 **976.7**（09-29 10:51 新交，收敛中——正合 742856 在册"新提交 40-70 局才收敛、峰落 1233→950"模式，勿读作劣化）。
- **同门带下沉**：Georgy 2345.4→**2180.7**（−165，今 06:19 新交）；tetsu2131 2307.3→**2073.0**（−234，无新交=纯漂移）；Lynxx 2210.6→**2028.3**（−182，无新交）；haodou 2215.6→**1594.3**（今 08:27 交 V89，显示未收敛值）；Alperen Aydın 2187.5→**1932.5**（今 01:11 新交）；带底 statma 1795.9/prvsiyan 1781.6 持平（昨带底 ~1772）。判读：终局换血期同门顶段被新交+收敛噪声拉低，**我方 H1 是带内最稳**。
- **前 20（谁在动）**：**#1 易主信号——M&M&P&Q 3058.6**（01:41 新交）压过 Majkel1337 2908.4（#6，05:09 仍在交，与分析38"榜一 Majkel"口径相比已易位）；DSM 3010.6 #2、DECEM 2998.4 #3、**Victor @ Tufa Labs 2945.9 #4（新面孔强冲）**、Boey 2941.6 #5；Unknown Mother-Goose 2892.2（10:01 仍在交）；前 20 全员 09-28 12:00 后有提交=全线终局换血中。

## 五、候选改善项（对照分析37 §一已证负清单）

1. **[B 级] G793 对手家族条件门（haodou V89）**：公开农场结构指纹+现金差 ≥20（step 96-120）判 cha22 家族 → 本局旁路自家投机置换优化器。=A1"三维条件策略"（开放面）在中段同门的独立收敛证据，与我方 oc_c3 画像器（476/476）同构不同实现（结构计数指纹 vs 开局窗逐拍身份；其门键=shape+money，我方=world×face）。禁区核查：非"镜像提前卖"（是关自家优化器而非提前卖）、非"启发式重排"（条件旁路而非重排）、非"公开件移植"（作 A1 口径参考，采纳仍须判决流程）——**无正面冲突**。证据=B 级（自报 +675/局 10/12；机制经我方 diff 核实；且 V82→V85→V89 尾壳三连换=作者自家亦在快速试错，其在线判定未收敛）。
2. **[C 级] Syed Asad Ali（top-50）价格信号论**："头部卖单纯反应式+价格信号即对手信号、直读对手农场只在少数情形有用"——支持 A1 采**窄触发门**形态而非全程对手反应（与冰火件"卖单 1% 冰"、haodou G793 窄门互证）。证据=C 级（公开讨论自述，仅方向印证）。
3. **[禁区冲突·仅登记不移植] MarketShock-M1-WR1K 采用潮**（flexonafft v106+haideptry v12 双双打包提交）：撞"公开件增量移植"已关门（横测 0/6）与"巨量晚抛/MarketShock 大败"复证面。登记两点：①对手群体向该运行时收敛→gengame 语料/kinship 谱系预期变化；②其工程卫生口径（hash 钉死+get_last_callable 入口自检+stdlib AST 断言+1.32.7 钉版）与我方外壳硬断言清单同族，可零风险补录清单条目。
4. **[C 级] 截止前队列运维事实**（744277/744219）：pending 1-3h、重交烧配额（有实录烧 1 sub）——若需补交应预留排队窗、绝不因 pending 重交；oc_c3 读数 976.7 为收敛噪声非劣化，读数以 40-70 局后为准。
5. **[存档] guru 零 blob 明文 V49 源**=第二件可读全文产线（并列 tetsutani step1009），供 B4 产线大变体合流对照读物，不移植。

## 六、来源清单（均 2026-09-29 抓取）

| 来源 URL | 通道 | 版本/读数 |
|---|---|---|
| https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger | kernels pull（base85 解包+本地 diff） | 保存版次 88/标签 V89 |
| https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible 、/god-s-mode-hacked-stores | kernels pull（与 09-28 缓存 diff/结构普查） | v24 / v26 |
| https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent 、https://www.kaggle.com/code/haideptry/the-shepherds-ledger-herd-safe-sovereign 、https://www.kaggle.com/code/guruprasaathas111/game-theoretic-master-discrete-optimization 、https://www.kaggle.com/code/evgendvorkin/kaggriculture-version-31-26-09-bronze-going-up | kernels pull（全文） | v106 / v12 / v3 / v32 |
| https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing 、/destbreso/x-ray-your-agent 、/ashok205/top10-replay-dataset-archive 、https://www.kaggle.com/code/georgymarin/kaggriculture-what-2600-farms-do-differently | kernels pull/diff（georgymarin 403） | v16 / v91 / v43 / 403 |
| 在册 8 件版本核查 | kernels list 全量翻页 + API v1 kernels/pull currentVersionNumber | 见〇表 |
| 顶强开号核查（Majkel/SpaTaro/Boey/DSM 三子/DECEM 等） | kernels list --user | 未找到 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/744277 、/744219 、/744218 、/744261 、/744255 、/744287 、/743993 、/742856 | competitions topics list/show | 见二 |
| https://www.kaggle.com/datasets/georgymarin/kaggriculture-episodes 、https://www.kaggle.com/datasets/ashok205/top10-replay-dataset-archive 、https://www.kaggle.com/datasets/ashok205/kaggriculture-top10-replay-archive 、https://www.kaggle.com/datasets/leoprovorov/a-song-of-ice-and-fire-interactive-dashboards 、https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-index 、/kaggriculture-episodes-2026-09-28 | datasets list/API view/files（两个 403 重试） | 见三 |
| https://www.kaggle.com/competitions/kaggriculture/leaderboard | leaderboard download（快照 2026-09-29T11:15:09） | 见四 |
| [前次] 2026-09-28-family-update-scan.md、2026-09-28-family-topband-deepcut-scan.md、../analyses/37（已关门面） | 见各篇 | 基线与禁区对照 |

## 七、限制

① georgymarin kernel pull 与两个数据集 files/download 403 持续，其 09-28 22:13 新 run 内容与 episodes 新版本内容均未获取；② god-s-mode v23 无缓存，v23→v26 仅结构级普查非逐行 diff；③ V86-V88 中间版本正文无法钉版拉取（API versionNumber 钉版 403/400 在案），"V86-V88 无正文变化"由 V85→V89 单 hunk diff 反证；④ 各家强度数字（V89 +675、haideptry 矩阵、guru 200k+）全部自报未复核；⑤ 榜面 11:15 快照对 10:51 后提交（oc_c3 等）读数不收敛，判读按 40-70 局口径；⑥ API lastRunTime 字段疑缓存失真，时间一律以 CLI dateRun 为准（与前次口径一致）。
