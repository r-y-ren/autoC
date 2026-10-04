# 2026-09-29 GitHub/Web 频道线上增量扫查册（09-28 晚 → 09-29 11:10Z）

> 任务：kaggriculture 战役线上增量扫查（GitHub/Web 频道），窗口=09-28 晚（基线轮 17:00-17:50 / 09:50Z）之后的站外新增量，判有无可改善我方策略的内容。
> 抓取日期统一 **2026-09-29**（11:00-11:20Z）。通道：GitHub REST API（search/commits/contents/raw）+ HF API + arXiv API + HN Algolia + dev.to/zenn/Qiita/掘金站内直查 + YouTube 结果页 + GitLab API。
> 纪律：逐条带来源 URL+抓取日期；自报数字标"自报"；查不到写"未找到"；候选改善项带证据等级（A=可验证实据 / B=自报+可核方法学 / C=自报未核 / D=宣传或自相矛盾）与分析37 §一禁区标注（禁区1 跨拍卖时移动；2 巨量晚抛；3 计划层抄作业+小幅 mix；4 路线表裸换线；5 镜像提前卖/启发式重排/持货等峰值；6 番茄门/PET 无门；7 公开件增量移植；8 剪毛错峰防御；9 学习式/神经网络=用户明令范围外）。工作件在 /tmp/scan_g/（未入仓）。

---

## 一、扫查面 1：GitHub 增量

**总量**：`q=kaggriculture` 388 仓（基线 387，净 +1；本轮新收 3 件 created≥09-28 11:24Z，推断约 2 件删除/改名/转私，未逐一定位）。**09-28T10:00Z 后有推送 16 仓**，其中默认分支有新提交 13 仓、纯分支/标签推送 3 仓（nagasora/BillXu21/phucthaiv02）。

### 重点深读 5 件

1. **mooman0222/Kaggriculture-opencode — e090 收官冻结**（https://github.com/mooman0222/Kaggriculture-opencode/commit/fed8d5d ，2026-09-29T04:43:35Z 抓取）：commit="最終2枠 E090 + E081再提出。hold層は打ち止め、帯50-110は自作系統のみ"。E090（ref 56662928，09-29 04:42 UTC）=公開 step1009 底盘+番茄阈值 7,500+**held-out 验证过的对镜像路由 12 对**；E081 再提交（ref 56662930，herd2700 系+自层，"実戦最高の系統"）。chassis.md/AGENTS.md 增量情报（自报）：①**公开系天花板 2,000-2,100（me4 公开作者本人同带），2,550-2,650 帯仅自作系、与公开 38 体 0 手一致**；②E085 分解：对旧 frontier 型（BUY20/SELL15）14-0 +1,606、BUY5 型 7-3 +48、同底盘（BUY8/SELL3）4-5 −149——停滞主因=同底盘流入+低带匹配（block20 均对手 1,789 vs E081 09-25 的 2,304）；③E081 09-27 后 97 局：85 局同农场 tape（开局 72 手哈希 4daa5387）、**品目单价亏 WOOL −2.3k/STRAW −0.8k/EGG −0.6k/FERT −0.6k**、对手高档品 SELL 位相散（mod1=36%）我方 mod1 集中 47%、大败（≥2k，28 局）多为羊鹅多的别路线；④hold 层（后知恵 oracle）：add 族上限 0；hold 族对 tape **+1,041±112/局（t=9.3），97/97 改善，胜 51→69**，对响应式 me4 镜像 +679±98（t=6.9）32/32（镜像战 0→全胜）；**但学习版（早晨公开特征）约束后仅 +19±21（阈 0.5）/−22±37（0.3），无约束版仓库溢出 −80k〜−117k**，作者结论"后知恵上限大、早晨可预测部分小疑い"；⑤路由扫引方法：Kaggle 5 核（rl/kaggle38）41 对×41 路由×3 seed×双席 vs pub_me4，采用门槛 均 +500 以上/6 局 5 胜/均值÷SE≥2，held-out（rl/kaggle39）后入 e090。e090 NOTICE（https://raw.githubusercontent.com/mooman0222/Kaggriculture-opencode/main/agents/e090/NOTICE.txt ）：step720-1009 底盘层取自 guru top-2-master-engine-v4（Apache-2.0），谱系 shiiin9→ahmed V55/56→Tschinkel→Hayashi→Gluzdov→Herd-Safe；**"Public Master Hybrid was evaluated as a competing base; its replacement was rejected"**。收官姿态："締切 09-30 23:59 UTC までに壊れていないことだけ確認する（新機構は出さない）"；09-28 02:00 快照 1 位 3034、50 位 2705（自报）。
2. **devasad67-lgtm/kaggriculture-agent — 新仓收官件（自报 rank 253）**（https://github.com/devasad67-lgtm/kaggriculture-agent ，created 2026-09-28T11:24Z；README+PROGRESS.md 09-29 抓取）：README 自报 "Best global rank 253/10,000+（rating 2471）"。内核=tetsutani demand-preserving-turn-sale-timing（Apache-2.0）+ edge 层：Lead-48 高档品提前卖（goods 入仓即卖、不超内 tape 计划、lead_steps 族 8/48/720）、崩价计量放货、Detour courier、羊毛优先挤奶队、**Rescue guard（day1 雇工失败→牲畜将逃→修复）**、镜像门胡萝卜反制、便宜开局。PROGRESS.md 关键数字（自报）：①`premium_first`（卖单挪 slot0）**30/30 负、约 −$34k，禁开**；②09-24：对 8 个公开强 bot 25/27；**对 DSM tape 回放 ~$45k/局、"adaptive play does not transfer" 判死**；顶层情报 "DSM、M&M&P&Q 5-5 互战，均为私有 adaptive planner，赢 $5-20k"；公开底板（ca25/pioneers-c2/shepherds/harvest-ledger/cha22）与 dp_L720a 成石头剪刀布，edge 叠新底板反而 37-43%；lead 扫描 dp_L8a 32-16(+420) vs 公开场而 L720 16-32、L720 对 L8 头对头 14-2（RPS）；③**day1 现金 ~$0→HIRE 失败→应喂牛的手不存在→day1 末牛逃逸→级联 −$10k..−$32k**（6/73 局=8 次大败中 6 次），修复=便宜开局 [BUY 10, SELL 10, BUY 5 WHEAT]（旧 [BUY 20/SELL 15] 在 step0 浪费 ~$22），dp_L8o 对 dp 族 35-0 +16k；④09-28 SALE-RACE 否证：镜像门（step24、≤1 格差）+MILK/WOOL/STRAW 每步全仓抛售，110 强局精确回放 43-67→41-69、翻 3 丢 5、净 −2、−211/局，**KILLED**，教训="对手价格优势不能靠更早更大抛售复制；抛自家库存只会拉低均价"；⑤09-28 结构普查：我方鹅 62%（1.5 只）vs **Yizhou 93%（5.9）** vs rank≤100 planner 100%（4.8），蛋卖单 14 vs 30/53；GOOSE forensic：首鹅 step156 中位（d6）、d29 累计蛋收 Yz 9,298/planner 6,686/us 3,203、每鹅日蛋 $74/$55/$68，**饱和农场修正净利 ≈ −$50..−$20/鹅日（原 $100 口径漏劳动/购价/格子）**，结论="顶强鹅优势=其全劳动/土地计划供养的规模，不是可拆规则"。
3. **graceyunliu/kaggriculture — 09-29 新 tape**（https://github.com/graceyunliu/kaggriculture/commits/main ，4 commits 2026-09-29T10:01Z）：新增 `Opponents/tape_majkel1337_114061801.py`+`tape_thirdfarmclub_111923787.py`，更新 tapes.json/frontier.txt。tapes.json 实据：**Majkel1337 ep114061801 money 149,166**（开局指纹 "HIR×5 BUYCO1 BUYSH1 BUYWH10"）、THIRD FARM CLUB ep111923787 money 149,665；存量 feel the agi 183,522、Majkel 109144271 147,092、Vadim Vasilenko 131,015。另有 ladder_watcher 基建（10/20/30/50/100/200 局检查点触发研究环）。
4. **pranav-bot/kaggriculture — 评测/求解基建爆发**（https://github.com/pranav-bot/kaggriculture/commits/main ，09-28 16:36-19:12Z，12+ commits）：**Retrograde DP + MILP 终局清算求解器（day20-29）**、**Bayesian/HMM 城镇店铺排水率估计（用市场价差）**、Rank-1 开局书生成器、**Elo 循环赛 runner + McNemar A/B + 延迟剖析门**、梯子评级追踪、Kaggle 提交监视、ladder ghost 对手注入+Optuna 反制求解、IQL 连续训练（=禁区9 线）。README（09-29 抓取）：集成 debmalyaroy 的字节级 Rust 仿真器（293 局/s、~0.30s/720 步）、MarketForecaster 因果 GRU（48h 特征窗→6 步库存增量均值+对数方差）、逐单位清算助手（$1 地板/边际报价 vs 保留价）；`docs/creating-agents.md`=机制→进阶 agent 教程。
5. **raju-sah/Kaggriculture — 09-29 转公开的 V135 合成件**（https://github.com/raju-sah/Kaggriculture ，created 2026-09-29T10:26Z、git 历史自 09-28T11:56Z；README/docs/RESEARCH_LOG.md 09-29 抓取）：提交序列 V115（动态 yarn 转向+step-717 终局冲刺）→V120（RACE sell-forward+terminal overlay）→V125（**God's Mode 店铺需求套利**：shop_predictor.py+shop_overlay.py）→V127（God's Mode archive bundle）→**V135（"hybrid sovereign: Farmer John + God's Mode overlay"**，ref 56668737）。自查榜位 rank 3,475/10,059、1,184.3 分（09-27 下载快照，自报）。RESEARCH_LOG=逐局门禁纪律（种子/席位/精确重放哈希、V77 拒绝案），钉 kaggle-environments==1.32.7。

### 其余 11 仓 triage

| 仓 | 推送 | 内容 | 相关面 |
|---|---|---|---|
| ShashankJangid/kaggriculture-agent | 09-29 06:30Z | "v4200 Apex Sovereign…Zero-Latency Fluid Liquidation（10-seed 均 $121,316、85% H2H vs v4100）"（自报）vs 自家 README 均 23,137.6/峰 28,397——**自相矛盾，D 级** | 无 |
| yen-ghub/kaggriculture-agent | 09-28 12:30-15:00Z | 终局微操系列（自报 perf）：d25-29 无回报的喂/护理跳过、终局日不喂不买饲料、蛋/番茄雇齐班再卖、**持羊毛等班被否证（order-sensitive price）**、晚甜瓜 4 颗 d19 种末日卖 | 收尾执行微面 |
| lvanegast/Kaggriculture | 09-29 01:39Z | "restore exact v16 champion（1118 Elo）"+v26/v27 草稿；低带 | 无 |
| smarino76/Kaggriculture | 09-29 08:54Z | "semantic matrix documentation"；skim 级 | 无 |
| sweeden-ttu/kaggriculture_1_37_muzero | 09-28 18:59-20:29Z（claude/* 分支） | RL 线文档："tuned candidate +$105 vs champion 10W-6L（自报）"、逐旋钮消融；另一分支渲染短片"Everyone Wins"（2:08 1080p30）=视频件 | 禁区9，仅记录 |
| Aayush033/Kaggriculture | 09-29 08:03Z | "AgriMind AI"（HyperBloom Hacks 黑客松件，营销化 README） | 无 |
| OpenKaggle/kaggriculture-research | 09-28 10:53-10:57Z | 引用面文档 3 commits | 无 |
| divyanshkumar333/Kaggriculture | 09-28 11:34Z | "update" | 无 |
| nagasora/kaggriculture | 09-29 07:57Z（分支级） | 日文成绩同步/回放分析工具（HEAD 09-10）；分支含 hierarchical-expert-transformer（禁区9） | 评测工具存量 |
| BillXu21/Kaggriculture | 09-29 05:41Z（分支级） | RL 中心规划笔记（1.32.6/1.32.7 平衡注记与我方一致） | 禁区9 |
| phucthaiv02/kaggriculture | 09-28 10:15Z（分支级） | 结构化 agent 仓 RULES.md（HEAD 09-24） | 无 |

**在册仓核对（全部无新推送）**：doanthuan/kaggriculture（09-27T02:07Z）、frapercan/kagsym（09-25T12:27Z）、wmar-dev/kaggriculture（09-28T04:19Z，**v20+ 未出现**）、alvaromendizabal（09-28T07:19Z）、alpertaskiran（09-28T07:40Z）、debmalyaroy/kaggriculture-simulation（09-24T10:43Z）、destbreso/kaggriculture-cppsim（09-14）。均 2026-09-29 核。

## 二、扫查面 2：顶强名字二次检索

GitHub repos 检索（q=kaggriculture+名字）与 users 检索（2026-09-29 抓取）：

| 名字 | 开仓/发帖/开源动作 |
|---|---|
| Majkel1337 | **未找到**（无 GitHub 账号、无仓；仅有 graceyunliu 回放 tape 两枚=数据非开源） |
| DSM | **未找到**（仅 devasad67 转述梯子情报，自报） |
| Tufa / SpTaro(spataro) / DECEM(Decem) / 4th | **未找到**（同名账号 0-1 仓、无 kaggriculture 件） |
| UMG=UnknownMotherGoose | **未找到**（账号存在、0 公开仓） |
| Rudra-r34l | **未找到**（无账号） |
| feel-the-agi | **未找到**（Feel-The-AGI 账号存在、44 仓但无 kaggriculture 件） |

**官方开源承诺兑现？未找到任何顶强开源落地**；终榜截止 09-30 23:59 UTC 未到，兑现窗口可能在截止后——截止后需再扫一轮。**名录新情报（自报，勿入结论）**：M&M&P&Q（与 DSM 5-5 私有 adaptive 族）、Yizhou（鹅重 93%/5.9、首鹅 d6）、"THIRD FARM CLUB"、Vadim Vasilenko。

## 三、扫查面 3：资料增量（博客/视频/HF）

- arXiv：**未找到**（all:kaggriculture 0 命中，09-29 查）。
- HN：**未找到**（20 命中全为 "agriculture" 模糊噪声，字面命中 0）。
- dev.to：**未找到**（服务端 HTML 无结果卡）。
- zenn：**未找到**（0 篇）。Qiita：**未找到新文**（1 篇 08-07 旧文顺带提及）。掘金：**未找到**（API 0）。
- YouTube：**未找到新增量**（最新 kaggriculture 件=Ekonomatica "Concept Demo" 3 周前 111 views；Just_a_dead_acct 模仿训练/一致性套件等均为存量，即基线"YouTube 5 条"同源）。
- HF：**未找到新增量**（4 数据集全部 lastModified≤09-17：ThanThoai9x rsp-decisions/KiroSamurai il/Mlboy23 replay/sweeden-ttu season-training）。
- GitLab：1 旧项目（phamhuubaochung，08-19）=无增量。X/推特+nitter：**反爬不可用**（307/连接失败）。
- 收官文/教程/评测（截止前）：**仅 GitHub 仓内文档**——devasad67 README+PROGRESS（收官复盘，自报）、pranav-bot `docs/creating-agents.md`（教程）+`docs/kaggriculture_simulation_guide.md`（仿真器评测指南）、mooman e090（收官冻结宣言）；站外博客未找到。

## 四、扫查面 4：对战/评测资料

1. **devasad67 real-ladder replay test**（`rnd/replaytest.py`/`rtbatch.py`，README 09-29 抓取）：**同种子重放对手录制动作**，卖单/时序改动逐局对照（wins flipped vs wins lost），替代噪声大的本地循环赛——与我方 frozen-rival paired 协议同构的可复用 harness 口径；辅以 per-item 钱账本重建、day1 镜像指纹、逐店布局胜率、top-10 生产结构对照。
2. **pranav-bot 评测基建**：Elo 循环赛 runner+McNemar A/B+延迟剖析门、梯子评级追踪+平台期告警、autopsy 脚本（败局宏观里程碑抽取+交叉分析）。
3. **模拟器**：debmalyaroy/kaggriculture-simulation（Rust 字节级、并行锦标赛）09-24 后无更新；pranav-bot 集成报 293 局/s 为新用法自报；cppsim/Ashee harness 无更新；**未找到新模拟器**。
4. graceyunliu ladder_watcher（检查点触发研究环）；nagasora 成绩同步工具（09-10 存量）。

## 五、候选改善项（证据等级+禁区标注）

1. **同种子录制动作精确回放对照尺**（devasad67 口径）→ P4 评测尺升级素材，合法（开放面 A3），证据 B。
2. **全仓抛售/提前大抛否证复证**（−211/局 KILLED；slot0 卖单 30/30 负 −$34k）→ 复证禁区2/5，证据 B+，无行动（归档）。
3. **day1 现金→HIRE 失败→牲畜逃逸级联根因+Rescue guard** → 防御卫兵属 A2 内生织入合法形态；改开局数字近禁区3，只取"卫兵"不取"开局表"，证据 B。
4. **hold/持货可学性坍缩**（后知恵 +1,041/局 vs 早晨特征 +19±21 不显著）→ 复证禁区5 预测面小，证据 B+，无行动。
5. **对手条件路由**（mooman 对镜像 12 对、held-out 验证、41×41×3×2 扫引协议）→ A1 对手条件策略合法形态（带对手画像门的路由选择）；**裸换表=禁区4**，证据 B。
6. **单价亏损清单（WOOL −2.3k 等）+SELL 位相集中（mod1 47% vs 对手 36%）** → A1 对手画像/B5 摆法回放择优（重排族禁区5 之下唯一合法形态），证据 B。
7. **鹅规模=全劳动/土地计划耦合、不可拆规则**（饱和场净 −$50..−$20/鹅日）→ B4 全局建模合流输入；裸加鹅=禁区3，证据 B。
8. **MILP/DP 终局清算+HMM 城镇排水估计**（pranav-bot）→ B4/对手-城镇建模候选；证据 C（新仓未核），RL 部分=禁区9 不采。
9. **顶强新 tape**（Majkel1337 149k/THIRD FARM CLUB 149.7k，graceyunliu）→ C7 gengame 挖掘/A1 数据燃料，证据 A。
10. raju-sah God's Mode 店铺需求套利移植件、yen-ghub 终局微操系列、devasad67 Lead-48 裸提前 edge → **禁区7（公开件增量移植）已关、devasad67 提前卖近禁区1**，仅作家族证据张力记录，不移植。

## 六、限制与未复核清单

① 全部强度数字为自报（devasad67 rank 253 无第三方凭据；ShashankJangid 数字自相矛盾已降 D）；② GitHub code search/gist 未扫（未认证 API 限制），X/推特反爬不可用；③ 388 vs 387 净 +1 但新收 3 件→约 2 件消失未定位；④ 榜单快照（1 位 3034/50 位 2705/DSM 3068）均为他方自报，非我方拉取；⑤ raju-sah created_at=09-29 但 git 历史自 09-28，疑似转公开，首次公开时刻不确定；⑥ mooman/devasad67 对镜像/对同族数字均未我方复核（其"同种子精确回放"条件我方 P4 落地后可重校）。
