# 2026-10-02 X-ray 六判据并入 P4 判决尺（xray-p4-integration）——工具级实现 + 对手画像基线 + 样例报告

- 时点：2026-10-02；比赛 09-30 已截止；赛后五件并行任务之一（P3 判决尺升级）
- 材料：`2026-10-02-closing-kernels-mining.md`（六判据定义与出处）+ `ext/closing-kernels/destbreso-xray/x-ray-your-agent.ipynb`（13 节诊断 harness 全码，无许可证声明、作者明示 fork 自用）+ `ext/closing-kernels/leoprovorov-iaf-final/`（cell 16 ROWS p10/p25/p50 硬数据）
- 落点：`fn_work/legacy_software/kaggle_simulations/orderbook_p4up_lab/`（**新目录**；并发隔离：未动任何既有 judge/实验室文件——orderbook_*_lab 既有目录、`run_judgment.py` 一律未改）
- 纪律：不 commit、不在线提交、阈值随判声明、x-ray 自校准数字全标"自报"、本方实测数字带出处；duckdb（第三方）执行恒走 bwrap 沙箱

## 〇 交付总表

| 交付物 | 路径 | 状态 |
|---|---|---|
| 六判据模块 + 判据元数据 | `orderbook_p4up_lab/criteria.py`（CRITERIA_SPEC 六条：判据定义→输入数据→输出字段→阈值来源） | ✅ |
| 归一模型/双指纹/两入口 | `records.py`（canon=x-ray cell 10 / bundle=leoprovorov cell 11）+ `adapters.py`（回放 blob t+1 对齐入口 / feats-band day0 片段入口） | ✅ |
| 磁带长度刻度 | `divergence.py`（D(t)/K(t)/p10/p25/p50，cell 11/17 数学区） | ✅ |
| 对手画像基线 | `data/opponents_baseline.json` + `baseline.py`（tape_tier 分层 + profile_lookup） | ✅ |
| 样例报告（真数据） | `samples/cohort_tfc_20260923.jsonl`（TFC 09-23 cohort 24 局）+ `samples/xray_p4up_sample_report.json/.txt` | ✅ |
| 测试 | `test_*.py` 7 文件 **94 判例全绿**（`python3 -m pytest orderbook_p4up_lab/`） | ✅ |
| 集成说明书 | `orderbook_p4up_lab/INTEGRATION.md`（安全窗口接入 run_judgment + 49 P1 衔接点） | ✅ |
| 抽取管线 | `extract_replays.py`（parquet→compact records，duckdb 走 bwrap） | ✅ |

## 一、判据判定表（六判据 × 实现状态 × 阈值来源）

判定口径：**已实现可测**=代码完整+pytest 金值判例过；**部分**=实现完整但真数据实测面受限（注明缺什么）；**不可实现**=数据/语义缺（注明原因）。

| # | 判据 | 状态 | 判据定义→输入→输出（摘要） | 阈值来源 |
|---|---|---|---|---|
| ① | GLOBAL vs WITHIN-WORLD 判定差 | **已实现可测**（合成判例全过；真数据 within-world 面受限→样例落"无同世界重复局"如实报） | 双读数：全体互比 vs 按世界（前两店有序对）组内互比；类目 PURE_REPLAY/REPAIRING_SCRIPT/ADAPTIVE；差=诊断（全局狂适应+世界内全同=SHOP_ROUTER_SIGNATURE；世界内也分叉=WITHIN_WORLD_ADAPTIVE）→ 输入：逐拍流+world 键 → 输出：global/within_world 行/gap_diagnosis/router_hint | classify 截断 0.25/0.10 与 router 窗 [70,146]（x-ray cell 14 代码常量，**自报**）；t<48 盲区（cell 16） |
| ② | 血缘谱镜像线 + BARCODE 分叉日 | **已实现可测**（镜像/sibling/无关三分、fork_day、基因群连通分量判例全过；样例 24 对手实跑） | PLAN 一致（farmer+hands）认家族、WHOLE（+market）1.000=同录、BARCODE=每日 d1-4 重锚窗签名×30 天+首个不一致日；基因群=开局窗 plan≥0.98 连通分量 → 输入：对战双方流+margin → 输出：kin_rows/n_mirror/mirror_record/fork_day/genetic_groups | mirror=0.95、sibling=[0.5,0.95)（cell 17，**自报**）；基因群 0.98、PRE=144（cell 19，**自报**）；镜像战绩带 design effect 1+φ 置信修正（georgymarin 口径） |
| ③ | 收敛三件套（DRIFT/SIGN FLIPS/n） | **部分**：实现完整+合成轨迹金值判例过（WARMING UP/SETTLING/SETTLED/TOO_FEW 四态+阈值随判+配对速率不进判决全过）；**真实数据实测不可实现**——战役内无评分轨迹（episode 清单只有 id/state/时刻，无 updatedScore） | DRIFT=近 WIN=min(20,n−1) 局评分 delta 均值（单位 pts/episode）+非零 delta 变号数+n → 输入：按时间序 updatedScore 轨迹（可选 endTime 算配对速率）→ 输出：verdict/drift/flips/n/**threshold**/reread_eta | THRESH=1.0 pts/episode（cell 33 写死，**自报**，随判声明纪律"a verdict quoted without its threshold is not a verdict"）；n<4 不判 |
| ④ | 语言指纹 SCRIPT/BRANCHER/SCHEDULER 三分 | **已实现可测**（SCRIPT/BRANCHER/SCHEDULER/MIXED/INSUFFICIENT 五态金值判例过；样例真数据实跑） | 5 连非空拍=短语（丢移动/PASS/数量）；日带 6-11/12-19/20-29 跨局复现率中位+归一化熵 → 输入：≥8 局全流 → 输出：bands{repeat_rate,norm_entropy,distinct}+class | 类目截断 r0≥0.95&r1≥0.7 / r0≥0.5&r1<0.5 / r0<0.5（cell 37，**自报**）；地板 8 局；校准锚 tapes 1.00/0.91-1.00/0.74-0.91、カワシギ 0.89/0.15/0.00 等全**自报**（cell 36，含盲测 7/7 分叉点恢复） |
| ⑤ | crater 卖压判据 | **已实现可测**（dmg 金值=数量×价差、双方向、窗口边界判例过；样例真数据实跑） | 一方大卖砸价后 window 拍内对侧同品卖出=crater；一阶伤害=Σ victim 数量×吃掉价差，读作坑的大小非因果转移 → 输入：双方流+逐拍价格表 → 输出：our_craters/their_craters{t0,t1,prod,dmg}+totals | window=24 拍、卖方按单笔价值 top=60（cell 25 代码常量，**自报**）；dmg≤0 不计 |
| ⑥ | 热图半分相关 r≥0.9 反伪影闸 | **已实现可测**（TRUST/NOISE/NOT_COMPUTABLE/INSUFFICIENT 四态判例过；样例真数据实跑双图过闸） | occupancy/presence 10x10 网格；局交替分两堆比图，r≥+0.9 才信；双控制=卡方 vs 均匀+top10 格质量占比 → 输入：各局棋盘网格 → 输出：corr_half/gate/chi2_dof/top10_share/flat_share | gate=r≥+0.9（cell 26/27 自述，**自报**）；卡方自由度=unlocked 格数−1 |

**未纳入六判据范围**（登记备查）：cell 23 LEADER_REF 08-30 #1 宏观形状 245 局分布（自报硬编码数组，可后补为参照层）；cell 28-31 生产率四桶/用工共识界 490 seat-seasons（自报）；cell 39 BRANCHER 决策树提取（置换检验 1500 次+留一验证，需特征库，列为后续）。

## 二、关键读数

1. **测试**：94 判例 7 文件全绿（records 13 / criteria 39 / divergence 8 / baseline 10 / adapters 10 / run_report 10 / extract_replays 4）。金值含 leoprovorov cell 11 例题（五局 3-1-1 → D=0.4、K=3）、p_q 严格大于边界（D=0.25 不触发 q=0.25）、crater dmg=5×(100−60)=200 手算值、收敛四态、语言三分合成流。
2. **样例输出**（`orderbook_p4up_lab/samples/xray_p4up_sample_report.json/.txt`，cohort=TFC 2026-09-23 全部 24 局、7 胜 17 负、24 个不同世界）：
   - [C1] GLOBAL=ADAPTIVE（canon 口径 vary 100%，首分叉 t=0；跨世界 move 方向/位置参数噪声为主）；within-world=无同世界重复局如实报（INSUFFICIENT 面）；feats 大样本横断（n=179）：day0 canon vary 95.8% 但 **bundle 口径 t=0 全样本 K=1=单一开局线**、t=5 四线 163/14/1/1。
   - [C2] 24 对手全部 unrelated（plan<0.5）、24 个单例基因群——09-23 窗内 TFC 无镜像/近亲遭遇。
   - [C3] TOO_FEW（n=0，无评分轨迹）。
   - [C4] class=SCHEDULER（三带 r=0/0/0）——**限界实证**：语言日带从 d6 起，恰在 TFC 六日磁带终点之后；d72+ 跨世界 router 分叉使跨局短语不复现，"逐世界路由"被并入"逐局即兴"读数（见 §三-3）。
   - [C5] 决定性局 112250771（margin −18,636）：我方砸坑 6 个、对手吃一阶伤害 **$1,065,032**；对侧 6 个坑我方仅吃 $10,022——TFC 卖流武器化面的对手伤害侧读数（hole-size 口径，非因果转移）。
   - [C6] occupancy 半分 r=0.9995 / presence r=0.9972 双过 r≥0.9 闸；chi2/dof=347.5/1296.1（棋盘使用高度结构化）；top10 格质量 16.5%/33.0% vs 平坦 10%。
   - [TAPE] 全 24 局 p10/p25/p50=**0/41/72**（EARLY_FORK 档，最近邻 DSM Δp25=18）；**胜局同口径（仅 7 胜）=41/72/72**；对照 leoprovorov 自报 TFC 145/145/146（SIX_DAY_TAPE）——差异解剖见 §三-1。
3. **基线 JSON 结构**（`data/opponents_baseline.json`）：`version/source/caliber/tape_tier_scheme/teams[11]/published_window_means_self_reported/caveats/usage`；teams 行=`{team, wins, p10, p25, p50, tape_tier, note}`（cell 16 ROWS 逐字对齐，`self_reported: true` 全局声明）；caliber 注=bundle 口径+D(t)/p_q 公式+仅胜局+店开拍 [72,144,216]+p25="两半 agent 的边界"；tape_tier 四档（DAY0_FIRE ≤4 / EARLY_FORK <72 / SHOP1_FORK <144 / SIX_DAY_TAPE ≥144）为**我方派生分层**（对齐店开拍），非原文数字。

## 三、样例报告核心发现（工具级首跑即出的三个读数）

1. **TFC 磁带对读差异（挂账）**：我方 09-23 cohort 胜局同口径 p10/p25/p50=41/72/72 vs 自报 145/145/146。解剖（我方实测）：①cohort 内 day0 即两线（20 局 5-hire 开局 vs **4 局 4-hire 开局全败**）=版本混样实证；②feats 大样本（179 局、全日期）t=0 bundle K=1（单线）但 t=5 已 163/14 分线（两线胜率 29%/36% 无决定差）；③胜局 bundle 曲线 t<41 全同（D=0）、t=41 起 1/7 局脱轨、t=72（首店）7 胜局散成 4 线——即我方窗内 TFC 在**首店**分叉，自报口径在**二店**（~145）分叉。归因排序：版本演化（09-21+ 新版/AB）> 样本窗差（自报≤09-20 vs 09-23）> 胜局数差（7 vs 88）。数据源已撤回（georgymarin episodes 403）不可复核→**挂账**（同 mining §五-6 DSM 张力处置）。
2. **口径噪声分离实证**：feats day0 canon vary 95.8% vs bundle t=0 K=1——canon 保留移动方向/位置参数，跨世界棋盘布局不同即"全不同"；bundle 并类后开局线全同。判决分层用 bundle，行为门（C1）判"反应"时用 canon+within-world，两口径必须随判声明。
3. **C4 对磁带族的结构性盲区**：语言日带 6-11 起算（x-ray 为避 t<48 盲区），恰把 0-6 日磁带段排除在外；"六日磁带+逐世界 router"的队在 C4 读 SCHEDULER。修正读法=C4 与 C1 组合判（C1 的 within-world 全同+ C4 后段融掉=router；C1 within-world 也分叉+ C4 融掉=真即兴）。

## 四、异常与限界

1. **x-ray 源不可翻译处（有意裁剪）**：绘图层（matplotlib/pandas 全部图表）、联网件（cell 3 KING 梯子爬取/ListEpisodes/回放 CDN/LeaderboardService、cell 8 作者主页探测）不移植——离线工具+比赛已截止语义已死；cell 20-23 宏观参照（08-30 #1 形状 245 局分布云，自报）不在六判据内；cell 28-31（生产率四桶/490 seat-seasons 用工共识）超任务范围未移植。**阈值多为作者代码常量、无推导文档**（0.25/0.10/0.95/0.98/1.0/0.9/24/60/8 全标自报），换阈值必须随判重声明。BARCODE 的 md5(json sort_keys) 忠实移植。
2. **数据缺**：①`orderbook_whzy66_lab/evidence/exp066_arena.json` **无逐局行**（仅对级聚合 n/WLT/h2h/wool behavior），任务候选数据之一不成立，未作判据输入；②战役内无任何评分轨迹（episodes 清单被剥离 updatedScore）→ C3 真数据实测缺；③feats-band 无 hands 通道/数量桶化/无价格棋盘 → 仅 day0 片段判读（lossy_notes 全程声明）；④真数据补给线=find：`ext/fingerprint-scan/raw/ashok205-shards/replays_*.parquet`（**全量 replay_json，georgymarin v79 撤回前下载**）——本次经 duckdb(bwrap) 抽 TFC 24 局打通全链，其余队/日期同命令可扩。
3. **盲区与自报纪律**：t<48 可观测盲区（一切 agent 同拍同令）；x-ray 全部校准数（53.8% unit-turn/490 seasons/08-30 形状/语言锚/盲测 7/7）系作者自测未复核，只入 CRITERIA_SPEC 注记不进读数；leoprovorov 基线全自报（其仪表盘可看不可重算）。
4. **本方实测面**：样例全部读数出自 TFC 09-23 cohort（n=24）+ feats 179 局横断，实测数字均带样本口径；样本小（胜局仅 7）→ tape 对读差异只给归因排序不下定论。

## 五、建议（分级）

1. **[集成顺序]** ①baseline+divergence 先行（零 harness 依赖，即刻喂判决分层：面板对手按 DAY0_FIRE/EARLY_FORK/SHOP1_FORK/SIX_DAY_TAPE 四档配比）→ ②C2 镜像线+C1 双重分类作面板组局前对手预扫（frozen-rival/同底盘指认）→ ③安全窗口经 `judgment_hook.py`+`--p4up` 默认关开关把 C3/C5/C6 读数块并入 run_judgment evidence → ④C4 作 wrapper/行为门附加体检。步骤全文见 `orderbook_p4up_lab/INTEGRATION.md`。
2. **[与 49 P1 合并]** 49 P1（评测协议整包：alperen 四件套+shiiin9 世界 CI+ΔΦ lockstep+选优双尺）与本包合并成**一张 P4 读数清单**（判据→门禁级→阈值），七衔接点已逐条写入 INTEGRATION.md §4（C2 镜像线=frozen-rival 复盘的对手侧、C1 within-world=世界簇 CI 的行为侧、C5 crater=ΔΦ 卖单实验的伤害侧、C6 半分闸=热图类读数的反伪影门、baseline tape_tier=BT 面板配比、C3 收敛=读数时机）。**一处防混淆**：C3 的"收敛"（评分轨迹是否已停）与 49 P1 的"判决重跑同结论率"（verdict 稳定性）是两个量，合并时分列勿并。
3. **[情报纪律·中]** TFC 磁带对读差异挂账入 §三-1 口径账本（与 mining §五-6 DSM 张力同册）；10-07 开源潮二轮若 georgymarin episodes 恢复/换址，用其胜局样本重对 p10/p25/p50。
4. **[仅登记]** cell 39 BRANCHER 决策树提取（置换检验+留一验证）列为 P4 后续件；cell 23/28-31 参照层（自报）可后补为判决参照带。

## 六、来源登记

| 来源 | 通道 | 抓取/使用日期 |
|---|---|---|
| https://www.kaggle.com/code/destbreso/x-ray-your-agent | 本次实现直接依据 `ext/closing-kernels/destbreso-xray/x-ray-your-agent.ipynb`（2026-10-02 实抓归档件，cell 13-27/32-37 全码逐节移植；SHA 锚 3ca5da4f…） | 2026-10-02 |
| https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-final-update | `ext/closing-kernels/leoprovorov-iaf-final/`（cell 16 ROWS 硬数据+cell 11/17 数学区；SHA 锚 e4e83741…） | 2026-10-02 |
| `2026-10-02-closing-kernels-mining.md` | 本战役档案（六判据定义/出处/自报口径总表） | 2026-10-02 |
| `ext/fingerprint-scan/band-analysis/feats-band.jsonl`（1,128 局）+ `ext/fingerprint-scan/raw/ashok205-shards/replays_*.parquet` | 本战役在册数据（georgymarin v79 撤回前下载）；feats 横断=直接读，replay 抽取=duckdb 经 bwrap 沙箱（断网/根只读/仅 /tmp 可写） | 2026-10-02 使用 |
| `orderbook_whzy66_lab/evidence/exp066_arena.json` | 本战役既有判决证据（读结构后判定无逐局行，未作输入） | 2026-10-02 |

## 七、需登记行（本任务不改 INDEX.md/JOURNAL.md/registry.jsonl，供安全窗口登记）

INDEX.md（references 表追加一行）：

| `2026-10-02-xray-p4-integration.md`（+ 工具包 `../../fn_work/legacy_software/kaggle_simulations/orderbook_p4up_lab/`：criteria/records/adapters/divergence/baseline+data/opponents_baseline.json/extract_replays/run_report/test_* 六判据 94 判例+samples/ TFC 09-23 cohort 24 局+样例报告+INTEGRATION.md） | 依据 `ext/closing-kernels/destbreso-xray/x-ray-your-agent.ipynb`（cell 13-27/32-37 移植，SHA 3ca5da4f…）+ `ext/closing-kernels/leoprovorov-iaf-final/`（cell 16 ROWS 基线，SHA e4e83741…）+ `ext/fingerprint-scan/` 数据（feats-band 1,128 局 + ashok205-shards parquet，duckdb 走 bwrap 抽取）；本次零新增下载 | 2026-10-02 | P3 判决尺升级工具级落地：X-ray 六判据（GLOBAL/WITHIN-WORLD 双读数、镜像线 0.95+BARCODE 分叉日、收敛三件套阈值随判、语言指纹三分、crater 卖压、半分闸 r≥0.9）+leoprovorov p10/p25/p50 11 队对手画像基线（全自报标源）；94 判例全绿；TFC 09-23 样例实跑：crater 对手一阶伤害 $1.065M、热图双图过闸 r≈0.999、tape 胜局同口径 41/72/72 vs 自报 145/145/146（版本混样+样本窗差挂账）；exp066_arena 无逐局行、无评分轨迹两数据缺实证 | P4 判决尺安全窗口集成（INTEGRATION.md 步骤）；49 P1 评测协议整包合并的读数清单输入 |
| JOURNAL.md 追加一行 | | | | `2026-10-02 P3 判决尺升级：x-ray 六判据工具级移植+leoprovorov p25 基线落 orderbook_p4up_lab/（94 判例全绿，TFC 样例报告 samples/），与 49 P1 衔接点写 INTEGRATION.md；未动共享 harness、未 commit` |

registry.jsonl 追加一行（id 按五件并行编号顺延，如主会话另有编号请替换）：

```json
{"id": "a51050-6", "date": "2026-10-02", "phenomenon": "P3 判决尺升级：destbreso X-ray 六判据+leoprovorov p25 磁带基线工具级并入 P4（orderbook_p4up_lab）", "target": "P4 判决尺/评测协议整包", "expected_signal": "安全窗口按 INTEGRATION.md 接入 run_judgment（--p4up 默认关）；49 P1 合并出单张 P4 读数清单；TFC 磁带对读差异挂账在 10-07 二轮对质", "status": "pending", "scored_in": ""}
```
