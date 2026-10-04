# 2026-10-02 战后开源潮·池测判决（P1）——5 件许可干净提交件级开源件本池实测（判决先行·不发射不提交）

> 任务=赛后五件并行任务之一（P1 池测判决）。时点 2026-10-02（比赛 09-30 23:59 UTC 已截止，官方终评窗至 ~10-14/15）。件源=`2026-10-02-postseason-github-scan.md` §三 A 池测建议序（坐标经报告文件程序化派生+GitHub REST 复核 2026-10-02 12:0xZ）；归档 `fn_work/legacy_software/kaggle_simulations/orderbook_postseason_lab/pieces/<短名>/`（git clone --depth 1 12:06Z，逐件 LICENSE+provenance.md）。证据=`orderbook_postseason_lab/evidence/pooltest_arena.json`（逐局行 288+面板 h2h/WLT+verdict+认证记录）。harness=`orderbook_postseason_lab/judge_pooltest_arena.py`（复用 exp066_arena/godv7_arena 判决基建；bwrap 沙箱内执行：根只读+/tmp+lab 可写+pieces 只读+断网）。
> **纪律**：判决只认本池实测；自报数字标"自报"未复核；Never quote the peak；读数=12 折双席（每对 24 局）口径，胜率=硬通货，margin/realized_px 只作参考；不改 INDEX/JOURNAL/registry（登记行见 §七）；不 git commit、不在线提交。

## 一、判据判定表（5 件 verdict+依据，均 2026-10-02 实测）

判决规则（同 EXP-066/godv7）：BEATS_CEILING=vs 王座 H1 h2h≥0.5 / COMPETITIVE=0.35–0.5 / WEAK<0.35 / UNRUNNABLE=装载失败或红局>20%。面板={H1 王座锚（H1/oc_c3 行为孪生，BT 527.8）、mpx、r40（弱锚）、A（弱件锚）}，每对 n=12 fold 双席=24 局，中性块 674000+i*131（i=0..11），h2h=judge_r44._fold_arm 双席折叠（缺席/红局 fail-closed 记负）。

| # | 件（坐标/许可） | 装载形态 | 判定 | 依据（本池实测） |
|---|---|---|---|---|
| 1 | **syx** = sunyuxiang136/kaggriculture-silver-agent `main.py`（Apache-2.0，HEAD be16043a） | 整包单文件 5,814,850B 纯标准库，末 callable `agent` 直跑（零修改） | **BEATS_CEILING** | vs 王座 H1 h2h=**0.9167**（11W1L0T）≥0.5；面板 mpx/r40/A 全 1.0（36W0L）；96 局 **0 红**；margin vs H1 +7,155.5；装载 0.82–0.87s |
| 2 | **taeyan** = TaeyanG4/kaggriculture-strategy-meta `agent/c1200_final.py`（Apache-2.0，HEAD 9e7daeb3） | 整包单文件 21,479,707B 生成件（base64+lzma 内嵌源码 exec），纯标准库，末 callable `agent` 直跑（零修改） | **BEATS_CEILING** | vs H1 h2h=**0.8333**（10W2L0T）；mpx 0.6667（8W4L）/r40 1.0/A 0.75（9W3L）；96 局 **0 红**；margin vs H1 +1,759.9；装载 0.61–0.72s |
| 3 | **romansvet** = romansvet/kaggriculture `submission/`（Apache-2.0，HEAD 4444cc7a） | 整包多文件 37 文件（main.py+kagg3/+theta.npy 30,896B+residual_head.npz 59,370B 随仓）；harness 适配=每局清 kagg3* 模块缓存（件本体零修改） | **BEATS_CEILING** | vs H1 h2h=**0.8333**（10W2L0T）；mpx 0.8333/r40 0.75（9W3L）/A 1.0；96 局 **0 红**；margin vs H1 +6,389.4；装载 0.11–0.13s |
| 4 | **carson** = CarsonBurke/kaggriculture（MIT，HEAD fbbf76f4） | 需权重——**仓内不带**：打包线 `scripts/build_submission.py --checkpoint runs/ppo/best.pt`，无 runs//无任何权重文件/无提交入口 main.py；LFS 仅 tensorboard 日志指针 | **UNRUNNABLE** | 装载失败（缺 checkpoint 权重，实证见 §三）；打包器另有 provenance/eval 证据绑定门（'will not package a checkpoint unless its provenance and evaluation evidence match'） |
| 5 | **debmal** = debmalyaroy/kaggriculture（MIT，HEAD c681c269） | Rust 编译件+配置包——**仓内缺件**：v63 tarball=main_config.py 桥+agent-stdio+agent.json+base/routes.json(~4.8MB route 表)+学习层 payload；README 明言 "The repository ships **no data** (replays, tapes, route tables, weights, builds)" | **UNRUNNABLE** | 缺提交配置 payload（实证见 §三）：agent-stdio **编译过**（bwrap 内 cargo build --release -p agent --bin agent-stdio 8.76s，产物 4,187,272B），但 `--config configs/agents/c4.agent.json` 实测 `load .../base/routes.json: No such file or directory (os error 2)` |

**三件可跑件全部 BEATS_CEILING（vs 王座 0.83–0.92，非边缘未触发翻倍加测），两件缺件 UNRUNNABLE。**

## 二、关键读数

### 2.1 自报（榜位/分）vs 本池读数 对照表（自报均未复核；官方终榜 ~10-15 出）

| 件 | 自报（榜位/分/对局，来源 README 抓取 2026-10-02） | 本池读数（2026-10-02 实测，判决只认本池） |
|---|---|---|
| syx | **银牌**（"Kaggriculture 银牌方案完整源码"/"Silver Medal Solution"，作者口径 Shawn404；官方未发奖）；自报 <3ms/step | **BEATS_CEILING**：vs 王座 **0.9167**（11W1L0T/12 折）；面板 1.0×3；margin vs H1 **+7,155.5**；终局钱 93,627 vs 86,472；实现价 0.8655/对手 0.7797 |
| taeyan | 提交号 **56719658**（c1054，09-30）/**56722176**（c1200，10-01——**晚于截止存疑**）；自家 ladder "c1200 beat every earlier version (118W8L2T)"；c111 曾 2350.6 after 56 games | **BEATS_CEILING**：vs 王座 **0.8333**（10W2L0T）；mpx 0.6667/r40 1.0/A 0.75；margin vs H1 **+1,759.9**；终局钱 87,735 vs 85,975；实现价 0.7953/对手 0.7907 |
| romansvet | 峰 **2,858**/收官 **2,230（rank 330 of 10,246, provisional）**；提交号 56718602/56707958（终两席 vrp27_vm_m3/vrp26）；~7.7k 浮点 ES 策略 | **BEATS_CEILING**：vs 王座 **0.8333**（10W2L0T）；mpx 0.8333/r40 0.75/A 1.0；margin vs H1 **+6,389.4**；终局钱 101,374 vs 94,985；实现价 0.7374/对手 0.8113（低实现价+高总量卖流形态） |
| carson | **#12 of 10,246**（"final submissions placed 12th"）；BC→PPO、Rust 位级仿真、LeJEPA、联盟 PPO | **UNRUNNABLE**（缺 checkpoint，未跑局；自报 #12 无法复核或迁移） |
| debmal | v63.14=**56718979**（自报 41W/12L/1D）/v63.16=**56720196**（自报 53W/11L）；v63.17 "built, not submittable" | **UNRUNNABLE**（缺 route 表/配置 payload，未跑局；自报 WLT 无法复核） |

**自报≠可迁移双向提示**：本战役已 8 例"自报高分迁不动"；本批反向同证——自报中低榜位（#330 provisional）或未发奖（银牌自报）的件在本池可超王座，榜位与本池 h2h **不可直接换算**（对手分布/BT 语义不同；终评 BT 单次定榜 vs 本池固定面板）。

### 2.2 逐件面板表（h2h / W-L-T / mean_margin / realized_px 我|对，每对 24 局）

**syx（BEATS_CEILING）**

| 对手 | h2h | W-L-T | mean_margin | 终局钱 我\|对 | 实现价 我\|对 | 红局 |
|---|---|---|---|---|---|---|
| H1（王座） | 0.9167 | 11-1-0 | +7,155.5 | 93,627\|86,472 | 0.8655\|0.7797 | 0 |
| mpx | 1.0 | 12-0-0 | +7,094.7 | 93,620\|86,525 | 0.8653\|0.7783 | 0 |
| r40（弱锚） | 1.0 | 12-0-0 | +7,052.1 | 93,749\|86,697 | 0.8656\|0.5774 | 0 |
| A（弱件锚） | 1.0 | 12-0-0 | +7,139.7 | 93,727\|86,588 | 0.8657\|0.5755 | 0 |

**taeyan（BEATS_CEILING）**

| 对手 | h2h | W-L-T | mean_margin | 终局钱 我\|对 | 实现价 我\|对 | 红局 |
|---|---|---|---|---|---|---|
| H1（王座） | 0.8333 | 10-2-0 | +1,759.9 | 87,735\|85,975 | 0.7953\|0.7907 | 0 |
| mpx | 0.6667 | 8-4-0 | +1,278.0 | 87,593\|86,315 | 0.8219\|0.7901 | 0 |
| r40（弱锚） | 1.0 | 12-0-0 | +2,140.8 | 88,230\|86,089 | 0.8006\|0.5671 | 0 |
| A（弱件锚） | 0.75 | 9-3-0 | +1,686.8 | 87,806\|86,119 | 0.8112\|0.5671 | 0 |

**romansvet（BEATS_CEILING）**

| 对手 | h2h | W-L-T | mean_margin | 终局钱 我\|对 | 实现价 我\|对 | 红局 |
|---|---|---|---|---|---|---|
| H1（王座） | 0.8333 | 10-2-0 | +6,389.4 | 101,374\|94,985 | 0.7374\|0.8113 | 0 |
| mpx | 0.8333 | 10-2-0 | +6,255.5 | 101,382\|95,127 | 0.7369\|0.8112 | 0 |
| r40（弱锚） | 0.75 | 9-3-0 | +5,851.3 | 98,122\|92,270 | 0.7492\|0.6153 | 0 |
| A（弱件锚） | 1.0 | 12-0-0 | +6,147.0 | 97,626\|91,479 | 0.7498\|0.5913 | 0 |

弱锚正常线（godv7 口径 ≥0.8）：syx 全过；**taeyan A 面 0.75、romansvet r40 面 0.75 各有一面低于线**（各 3 败，见 §四.2）。

### 2.3 装载形态与归档（pieces/ 每件 LICENSE+provenance.md）

| 短名 | 形态 | 入口 | 依赖/权重 | 归档（HEAD，抓取 2026-10-02 12:06Z） |
|---|---|---|---|---|
| syx | 整包单文件（交件形态原样） | 末 callable `agent(observation, configuration=None)`（文件尾 `agent = globals().pop('agent')` 主动落末位） | 纯标准库；无权重 | be16043a，37 文件 23MB |
| taeyan | 整包单文件（生成件） | 同上（`del agent` 重定义落末位） | 纯标准库（base64/lzma 内嵌）；无权重 | 9e7daeb3，1,394 文件 1.6GB（全谱系 c001–c1200+验证配置） |
| romansvet | 整包多文件（+适配器：清 kagg3* 模块缓存） | 同上（文件内注释明言 last-callable 契约） | numpy；theta.npy+residual_head.npz 随仓 | 4444cc7a，1,650 文件 37MB |
| carson | 需适配器+**需权重（缺）** | 无（打包器产出 main.py，硬性要 checkpoint） | torch 仅 train extra；runs/ppo/best.pt 不随仓 | fbbf76f4，301 文件 9.8MB |
| debmal | **Rust 编译件+配置包（缺件）** | main_config.py 桥→agent-stdio 子进程（actTimeout 1.0s/首拍 ~4.8MB route 装载） | cargo 1.98.1 编译过；agent.json/base routes/学习层全缺 | c681c269，1,098 文件 20MB |

### 2.4 判决基建与口径

- **harness**：`orderbook_postseason_lab/judge_pooltest_arena.py`（exp066_arena 同构：`j23._load_entry` 末 callable 全新命名空间逐局装载、`judge_r44._fold_arm` 双席折叠、`jg.econ_face` 干净 margin、BASE_PX milkwin 实现价）；godv7_arena 同构（外层适配层、bwrap 沙箱、多文件件模块缓存清理）。
- **认证记录（30/30 必附）**：composite lab 09-30 30/30 缓存附证（`orderbook_composite_lab/evidence/sim_auth_cache.json`，n_checked 30/n_match 30/rate 1.0，含逐局对照全记录）+ **每件在环 30/30**（件 vs r40 双引擎逐局终局资金对照）：syx 30/30（wall_speedup 1.203）、taeyan 30/30（1.097）、romansvet 30/30（1.595）——全部 consistency_ok，面板跑口走 sim 引擎（快线）。
- **局次预算**：baseline 认证 30+每件在环认证 30×3+面板逐局行 288=**408 局次**（3 件×96 局+认证 120）。每件快筛 96 局=任务预算上限（4 对×12 折双席）。
- **沙箱**：bwrap（根只读+/tmp+lab 可写+pieces 只读+--unshare-net）全程；debmal 编译 fetch 在沙箱外=纯下载（等同 clone 抓取面），build 在沙箱内 --offline。pieces/ 归档零污染（git status 复核 0 变更）。
- **确定性自证**：syx vs H1 首跑与断点续跑两次读数全同（0.9167/11W1L0T、mpx/r40/A 全 1.0）。

## 三、carson/debmal 装载失败实证（UNRUNNABLE 合法判定）

**carson（缺 checkpoint）**：仓内权重文件全量检索（*.pt/*.npz/*.npy/*.pth/*.ckpt/*.safetensors/*.bin）=**未找到**；`runs/`、`artifacts/` 不存在；`scripts/build_submission.py` argparse `--checkpoint` 为 required（README 步骤 5 "Package and validate a submission" 明示从 `runs/ppo/best.pt` 打包）；`.lfsconfig` 仅排除 `results/tensorboard/**`（5 个 LFS 指针=训练日志非权重）。结论：提交件=Python 神经推理包+训练 checkpoint，checkpoint 不随仓（自报 #12 的可迁移物不存在于公开仓）。

**debmalyaroy（缺提交配置 payload）**：编译面 OK——`cargo build --release -p agent --bin agent-stdio`（bwrap 内 --offline）8.76s 过（依赖 crates/dayobs+policy+kagg-engine+agent），产物 `target/release/agent-stdio` 4,187,272B；装载面 FAIL——`agent-stdio --config configs/agents/c4.agent.json`（c4.agent.json="v63.12_rl_c4 expressed as managers"）实测退出于 `load .../configs/agents/base/routes.json: No such file or directory (os error 2)`。缺件清单：agent.json（v63 候选）、base/routes.json+router.json（route 表=按世界录制 top-player 路线，首拍 ~4.8MB 装载）、policy.bin/shield.json/knobs.json/dispatch//rshell/shell/endg/gt/preempt/group_knobs（学习层件）。README 明言仓"ships **no data** (replays, tapes, route tables, weights, builds)"，`configs/route_tables/` 仅 70B/476B/35B refit 小 JSON 非 route 表，`data/` 不存在。v63.x 自报强度（41W12L1D/53W11L）主体在 route 表+学习层，公开仓不可重建，故 UNRUNNABLE（缺件）而非"弱件"。

## 四、异常与限界

1. **run2 中途死亡（未复现）**：taeyan 判决落证后、romansvet 在环认证期进程静默退出（无 traceback/无 OOM 留痕，22GB 主机 8GB 空闲；单局官方引擎 romansvet 探针 7.1s 正常、run3 同认证 30/30 过=**非件侧崩溃**，工作假设=后台任务被环境回收）。损失经断点续跑（POOLTEST_RESUME 证据并档）全量恢复；syx 终读数与首跑逐位一致。
2. **弱锚面异常（行为盲点提示）**：taeyan vs A 0.75（9W3L）、romansvet vs r40 0.75（9W3L）低于 godv7 弱锚正常线 0.8；胜率硬通货不受影响（判据只看 vs 王座），但提示两件对特定弱对手形态有盲点（taeyan 负于 A 件 3 局、romansvet 负于 r40 3 局，红局 0=真败非缺席）。
3. **认证记录口径**：每件在环 30/30 以摘要入证（n_checked/n_match/rate）；逐局对照行由 sim_bridge 生成但 **pass 时不落盘（degrade-only 记录口径，exp066 同构）**——逐局全记录仅基线缓存（composite lab sim_auth_cache.json）在档。若需逐件逐局对照行须加跑一轮强制落盘认证。
4. **样本量**：每对 12 折双席=24 局、每件 96 局；三件 vs 王座 0.83–0.92 远高 0.5 线（非"边缘"），未触发翻倍加测；24 局/对的 h2h 粒度=1/24≈0.042。
5. **HP_TELEMETRY stdout 噪声**：件层遥测打印（taeyan c1200 内嵌层动态拼接串，romansvet 局内亦有观测），不修不管，不影响动作与判决。
6. **未加测 C_final/h1x_a**（我方活跃件）：任务口径"可加"，预算 48–96 局/件已由 4 对面板占满；如需与计分对直接对照属加测项（§五 P2）。
7. **Taeyan 56722176 提交号晚于截止**（10-01 交）存疑待平台侧核（扫描报告 §四.4 同注）；本池读数只针对 `agent/c1200_final.py` 字节（=自报验证版 c1064 字节）。
8. **自报数字全部未复核**（银牌/#12/#330/2,858/2,230/提交号 WLT）；官方终榜 ~10-15，名次均 provisional。
9. **本池≠Kaggle 榜**：固定面板 h2h 与 BT 单次定榜语义不同，BEATS_CEILING 只声明"本池超王座"，不推断榜位。

## 五、建议（可行动项分级）

### P0 [高] 三件 BEATS_CEILING 入复盘对标
- **syx（0.9167 全面碾压+margin +7.2k+实现价 0.8655 高价卖流）**为本批最强、也是公开 2965/V39-V46 系谱+"赛后调优可超王座"的直接实证；**romansvet（7.7k 浮点 ES+numpy/C kernel、低实现价高总量卖流）**为完全异构的第二形态；**taeyan（c1200 分层服务链）**第三。建议三件机制拆解进复盘轨（syx 三模态=黄金磁带+DSM DP+泊松截胡；romansvet 日规划器+residual head）。
- 分流：流程级（复盘轨+kb）。

### P1 [高] "公开系谱衍生可超王座"进复盘结论
- syx 明示致谢 haideptry "2965 Master Hybrid Engine"（V39/V46 系谱）；taeyan 基于 public V37/Ahmed 系谱1100 个 candidate 迭代——两件均以公开件为底座+赛后强化超我方王座（H1/oc_c3 BT 527.8）；与 godv7（同系谱 WEAK 0.25）对照=**系谱底座+迭代强度差决定段位**，公开件生态位再证。
- 分流：流程级。

### P2 [中] 加测项（预算外，需另批）
- 三件 vs 我方计分对 {C_final 56721419, h1x_a 56721643} 直接对照（回答"赛后开源件是否已在计分对之上"）；BEATS_CEILING 边缘翻倍（24 折）本次未触发（非边缘），如需终审可加。
- 分流：流程级（判决基建已备，跑口即 judge_pooltest_arena.py 的 PANEL 扩展）。

### P3 [中] carson/debmal 复测登记（补件监控）
- carson：等 checkpoint/权重投放（同 msdsm 权重监控档）；debmal：等 route 表/配置包补发（其编译链已验证可复现：agent-stdio 8.76s），或裁决是否接受 chassis+layers 构型代跑（≠提交件，需用户裁决）。
- 分流：流程级（监控档）。

### P4 [低] 判决基建沉淀
- POOLTEST_RESUME 断点续跑（证据并档+跳过已判决件）与"多文件件惰性 import 不可被跨局模块清理误伤"（load→run→load 串行口径）入 harness 惯例；专名查询程序化派生纪律沿用（本报告仓名坐标自扫描报告文件派生）。
- 分流：流程级。

## 六、来源清单（均 2026-10-02 实抓/实测）

| # | 来源 URL / 端点 | 通道 | 戳 |
|---|---|---|---|
| S1 | `2026-10-02-postseason-github-scan.md` §三 A（仓名坐标+自报口径程序化派生） | 本地文件 | 扫描 10:40–11:25Z |
| S2 | api.github.com/repos/{sunyuxiang136/kaggriculture-silver-agent, TaeyanG4/kaggriculture-strategy-meta, CarsonBurke/kaggriculture, romansvet/kaggriculture, debmalyaroy/kaggriculture}（license/branch/pushed 复核） | GitHub REST | 11:0xZ（复核）/12:0xZ |
| S3 | git clone --depth 1 ×5 → orderbook_postseason_lab/pieces/{syx,taeyan,carson,romansvet,debmal}/（HEAD：be16043a/9e7daeb3/fbbf76f4/4444cc7a/c681c269；逐件 LICENSE+provenance.md） | git | 12:06Z |
| S4 | 5 仓 README/submission/UPLOAD.md/docs/history/submission.md/docs/solution.md（自报口径引用，标"自报"） | 本地归档 | 抓取 2026-10-02 |
| S5 | 池测判决 harness `judge_pooltest_arena.py`（bwrap 沙箱内执行 ×4 跑次：run1 syx+run2 taeyan+run3 syx 恢复/romansvet+preflight carson/debmal） | 本池实测 | 12:38–15:11Z |
| S6 | 证据 `orderbook_postseason_lab/evidence/pooltest_arena.json`（逐局行 288+面板+verdict+认证+预算 408 局次） | 本池实测 | 终证 15:11Z |
| S7 | sim_bridge 认证：composite `orderbook_composite_lab/evidence/sim_auth_cache.json`（30/30 基线全记录）+每件在环 30/30（syx/taeyan/romansvet 摘要入证） | 本池实测 | 09-30 缓存/10-02 在环 |
| S8 | debmal 编译/装载实证：`orderbook_postseason_lab/build/debmal_build/build_log.txt`（cargo build 8.76s 过）+`agent-stdio --config c4.agent.json` ENOENT 探针 | bwrap 实测 | 12:19–12:2xZ |
| S9 | carson 缺件实证：仓内权重全量检索=未找到；build_submission.py argparse 门 | 本地归档核查 | 12:0xZ |

## 七、需登记行清单（主会话统一登记；本任务不改 INDEX/JOURNAL/registry/requirements）

**1. `fn_docs/hybrid/references/INDEX.md`（表格行，五列=路径|来源|抓取时间|摘要|用途）：**

`| `2026-10-02-opensrc-pooltest.md`（+ fn_work/legacy_software/kaggle_simulations/orderbook_postseason_lab/ 全部产物：judge_pooltest_arena.py、evidence/pooltest_arena.json（逐局行 288+认证+预算 408 局次）、pieces/{syx,taeyan,carson,romansvet,debmal}/ 归档（LICENSE+provenance.md，HEAD be16043a/9e7daeb3/fbbf76f4/4444cc7a/c681c269）、build/debmal_build/ 编译实证） | GitHub：github.com/{sunyuxiang136/kaggriculture-silver-agent, TaeyanG4/kaggriculture-strategy-meta, CarsonBurke/kaggriculture, romansvet/kaggriculture, debmalyaroy/kaggriculture}（REST 复核+git clone --depth 1 实抓）；坐标自 2026-10-02-postseason-github-scan.md §三 A 程序化派生；[前次] 该扫描报告 | 2026-10-02（12:06Z 归档，12:38–15:11Z 池测） | P1 池测判决 5 件许可干净提交件：syx BEATS_CEILING（vs 王座 H1 0.9167/11W1L，面板全 1.0，margin +7,155）、taeyan BEATS_CEILING（0.8333/10W2L）、romansvet BEATS_CEILING（0.8333/10W2L，ES 7.7k 浮点+numpy/C 形态）、carson UNRUNNABLE（缺 checkpoint）、debmal UNRUNNABLE（缺 route 表/配置 payload，agent-stdio 编译过 8.76s 但 routes.json ENOENT）；96 局/件 0 红；每件在环 sim_bridge 30/30；自报（银牌/#12/#330/56718979 等）vs 本池 5 行对照全落档；自报≠可迁移双向提示（自报中低榜位件可超王座，榜位≠池内 h2h） | 复盘对标（P0 三件机制拆解+P1 公开系谱可超王座结论）；加测项（vs 计分对 {C_final,h1x_a}）；carson/debmal 补件监控复测 |`

**2. `fn_docs/governance/JOURNAL.md`（一行）：**

`| 2026-10-02 | analyze | **P1 池测判决：5 件许可干净开源件本池实测——3 件 BEATS_CEILING 全超王座**——syx（银牌自报单文件 5.8MB）0.9167/11W1L 全面板碾压+margin +7.2k；taeyan（c1200 21MB 生成件）0.8333；romansvet（ES 7.7k+theta 随仓）0.8333；均 96 局 0 红+在环 sim_bridge 30/30；carson UNRUNNABLE（缺 checkpoint）/debmal UNRUNNABLE（缺 route 表/配置，Rust 件编译过但 routes.json ENOENT）；自报≠可迁移双向提示（自报 #330 件可超王座，榜位≠池内 h2h）；弱锚面异常 taeyan-A 0.75/romansvet-r40 0.75；run2 静默死亡经断点续跑全量恢复（syx 两次读数逐位一致） | 三件入复盘对标（P0）+vs 计分对加测呈裁+carson/debmal 补件监控 |`

**3. `fn_docs/hybrid/analyses/registry.jsonl`（一行，接 a51050-4/5 之后）：**

`{"id": "a51050-4a", "date": "2026-10-02", "phenomenon": "开源潮池测判决（a51050 池测队列提案执行）：5 件许可干净提交件本池实测", "target": "复盘对标/开源件强度带", "expected_signal": "逐件 verdict（BEATS_CEILING/COMPETITIVE/WEAK/UNRUNNABLE）+自报 vs 本池对照行，判决只认本池实测", "status": "achieved", "scored_in": "orderbook_postseason_lab/evidence/pooltest_arena.json + 2026-10-02-opensrc-pooltest.md（3 件 BEATS_CEILING：syx 0.9167/taeyan 0.8333/romansvet 0.8333；2 件 UNRUNNABLE 缺件）"}`
