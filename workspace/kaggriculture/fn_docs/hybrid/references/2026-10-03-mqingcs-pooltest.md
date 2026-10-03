# mqingcs 双策略池测判决（dff20b-1，2026-10-03）

数据源（全实抓，一手）：
- 件：`ext/monitor-round2-probe/`（mqingcs/kaggressulture-two-policy-source，Apache-2.0，2026-10-03 03:25Z 入库；11 版本文件+policy_parameters.json 212KB）
- 上游：`ext/mqingcs_upstream/`（degnonguidi/best-agent-ranking kernel output，2026-10-03T06:06Z kaggle CLI 实拉，provenance 见其 PROVENANCE.md）
- 判决：`fn_work/legacy_software/kaggle_simulations/orderbook_mqingcs_lab/`（harness+证据 `evidence/mqingcs_arena.json`，bwrap 沙箱全程）
- 口径：与 pooltest_arena/exp066/godv7 同构（中性块 674000+i*131，12 fold 双席，`_fold_arm` 折叠，H1 王座锚）；sim_bridge 在环认证 30/30（baseline 缓存 30/30 附证）

## 一、判据判定表

| 件 | verdict | 依据 |
|---|---|---|
| **last_dance_56720309（主版）** | **BEATS_CEILING** | vs 王座 H1 h2h **0.8333**（10W2L0T，12 fold 双席）；96 局面板零红局零错误；装载 0.13s（entry=risk_probation_entry） |
| last_dance_56720309_016 | UNRUNNABLE（组件） | 装载过但末 callable=`_decay_plants(farm, step)`（引擎 unit 语义函数，非 agent 入口）；被主文件 exec 进 _UNIT_NS 复用 |
| last_dance_56720309_017 | UNRUNNABLE（组件） | 独立 exec 即 NameError `FARMER_MOVES`（依赖 _016 命名空间；末 7 轮收尾规划器，被 exec 进 _PLANNER_NS） |
| last_dance_56720309_019 | UNRUNNABLE（组件） | 装载过但末 callable=`pair_value`（H10 价值原语，arity/语义非 agent）；被 exec 进 _IC_VALUE |
| observed_56713902（提交形态=包装器） | UNRUNNABLE | 装载即 FileNotFoundError："requires its authorized 24-episode task library"（KAGGRICULTURE_PRIVATE_ASSETS 未随包，符合 DATA_ACCESS 预期） |
| observed_56713902_001（成熟专家） | LOAD_OK_UNTESTED | 装载通过（末 callable=_sc29_liquidity；4 个 value 键全可解析）——按任务纪律不烧局；提交形态仍=包装器（缺库 UNRUNNABLE） |
| observed_56713902_009（学习分支） | UNRUNNABLE | 装载即 FileNotFoundError（value 键 observed_56713902_009_010 不在 policy_parameters 亦不在 dependency_spec→缺任务库分支） |

判定尺：BEATS_CEILING（vs 王座 H1 h2h≥0.5）/ COMPETITIVE（0.35-0.5）/ WEAK（<0.35）/ UNRUNNABLE（装载失败或红局>20%）。变体澄清：`_016/_017/_019` 非独立策略版本，是主文件的内部组件（unit 语义 333 行/收尾规划器 392 行/H10 价值原语 171 行，主文件以 `publication_assets.source()` exec 复用；与 observed 侧 _001_004/_001_005/_001_007 同文件长度=共享生产血统）——故预算集中于唯一 agent 入口（主版 96 局全面板，>任务预估 4×48 局的一半，同构口径四对手全覆盖）。

## 二、关键读数（本池实测；Never quote the peak）

**面板（12 fold 双席=24 局/对手，sim 引擎 96/96，零红局）**：

| 对手 | 角色 | h2h | W/L/T | mean margin | tm_us / tm_opp | rpx_us / rpx_opp |
|---|---|---|---|---|---|---|
| H1 | 王座锚（oc_c3 行为孪生，BT 527.8） | **0.8333** | 10/2/0 | +1575.1 | 87568.5 / 85993.4 | 0.8666 / 0.7888 |
| mpx | 面板强件 | 0.8333 | 10/2/0 | +1761.9 | 87682.7 / 85920.8 | 0.8657 / 0.7873 |
| r40 | 弱锚 | 0.8333 | 10/2/0 | +2865.0 | 88602.9 / 85737.9 | 0.8396 / 0.6199 |
| A | 弱件锚 | 0.75 | 9/3/0 | +2001.0 | 87801.7 / 85800.8 | 0.8395 / 0.6124 |

**同构横比（战后开源潮四件，同尺同面板）**：

| 件 | vs H1 | vs mpx | vs r40 | vs A | verdict |
|---|---|---|---|---|---|
| syx | 0.9167 | 1.0 | 1.0 | 1.0 | BEATS_CEILING |
| **last_dance（本次）** | **0.8333** | **0.8333** | **0.8333** | **0.75** | **BEATS_CEILING** |
| taeyan | 0.8333 | 0.6667 | 1.0 | 0.75 | BEATS_CEILING |
| romansvet | 0.8333 | 0.8333 | 0.75 | 1.0 | BEATS_CEILING |

- **种子洞模式（败局归因）**：12 种子里恰 2 个（**674262、675048**）四对手全败、双席对称（margin −276~−1661 区间）；674393 仅对 A 败；其余 10 种子四对手全胜。= 世界条件性弱点（≈2/12 世界），非对手驱动——四条面板的 6 个败 fold 里 5 个集中在同 2 种子。
- **装载形态**：包件单文件主策略（11,351 行，纯 stdlib），末 callable `final_v40_risk_entry`；harness 层注入 `KAGGRICULTURE_UPSTREAM_MAIN` + 包根 sys.path（件本体零修改）；上游 main.py 只 AST 解析不执行。装载 0.13s/局 0.65s 均值。
- **上游常量匹配**：dependency_spec 4 条 spec（94490/553065 字符两族）对实拉 kernel output main.py（1,026,965B，sha256 a16e0e9b…d82ab，与 kernel 日志自报哈希一致）全部 UNIQUE-OK——当前线上版本与包完全兼容。
- **sim_bridge 认证**：在环 30/30（last_dance vs r40 双引擎逐局终局资金对照 rate=1.0，无降级）+ composite 缓存 30/30 附证；烟测局（official 引擎）与面板同种子同席位 margin 逐位一致（674000-s0 vs r40 = +9806）=双引擎又一互证。
- **预算**：156 局次（baseline 30+在环 30+面板 96），elapsed 1336.5s，4 worker。

## 三、机制对照表（复盘价值：Last Dance 市场层 vs 我方同域判例）

我方判例锚点：PREDICT v1 判负（分析 23，2026-09-27）；R28 债务账本提前卖判负（分析 30，红区第 7 负）；R27 日新高变现+谷底闸门判正（分析 30 P2，h2h 0.775，发射 56641599）；持货等峰值判负（−$1.2k~−3.2k/局）。

| Last Dance 机制（源码定位） | 它怎么做 | 我方同域件 | 我方判决 | 差异点 |
|---|---|---|---|---|
| 对手麦流观测 `_wctg_observe`（L10155） | 公开库存 delta−自家单−town draw=rival 净流；相位门控（t%4==3 记 rival 买≥20；t%4==0 记卖≥0.6×前值）成对计数，≥6 对→predator 标志 | PREDICT extrapolate_sells+infer_rival_sells | **判负**（预测写入 9975 步+避让 3329 次；h2h 0.000） | 它观测不外推：净流只作事件计数驱动"停开新仓"，不写入主计划、不改出货动作——正是分析 23 的结论"防御应为门非推迟"的活体实现；我方判负的是预测→改自身动作这条链 |
| carry 仓位规模 `_wctc_size/_wctc_gain`（L10194-10228） | 有界枚举 m∈[10, min(90,room,cash)]，按每单位边际报价（`_r37_market_price`）模拟双方交错买卖清算后取收益最大 m；对手 carry 规模 EMA（α=0.5，≥2 见证） | 持货等峰值（判负）；R27 日新高变现（判正） | 持货等峰值**判负**；R27 **判正** | carry 期限=1 轮（town draw 轮买、次日必卖，_WCT_LAST=708 收尾前清仓），非跨日等峰值；赚的是 town draw 前后的结构性价差，规模由清算模型算出而非拍脑袋 |
| 逆向时点识别 `_wctv_observe`（L10229） | 检测"对手 t−1 卖≤−15 且 t 买≥+15"×4 事件→v_stop（停开新 lot） | 谷底闸门（R27 判正组件） | **判正**（在 R27 内） | 同为"识别对手谷底行为"形态；我方=价格口径门（当日报价创新高才卖/谷底不卖），它=行为口径门（对手先砸后接的证据→停买）；触发后都不改存量仓的出场 |
| 执行成本下界 `_mr_cost_lower`（L11011） | 现金 delta+他品卖收下界（对手卖单排最前最坏序）−费上界 vs 报价曲线"正常成本"；只在 rival_net==0（对手该轮未动麦）时采信 | 实现价缺口测量（分析 24：0.721 缺口钉死在自造 glut 谷底自伤） | 无对应机制判决（只测量未闭环） | 它把执行贵了多少做成**可观测下界**并驱动防御；我方停在测量层——同域问题、不同处置（测量 vs 检测器闭环） |
| realized-loss 检测 `_hg_receipt`（L10744/11039） | 下界超额>0→事件+slippage 累计；不记账、不重排卖单 | R28 债务账本（r36_debts） | **判负**（604 恒等违例/h2h 0.3917） | 债务账本=提前卖在原 due_step 记债抵扣（主动会计+重排），败在恒等式实现；它=被动见证（排除对手干扰后数证据），形态是"检测器"不是"账本" |
| 有界试用期 `risk_probation_entry`（末段） | 证据不足→激活限时 24 步（1 天）试用；证据足（≥6 事件）→本局永久停新 carry；报价清算值盖不住已知成本时临时防御 | 无直接对应（最近=守卫族+红区收档） | 无对应 | 机制自带止损与自动退出：时间有界的自禁（episode 级）；我方守卫族全是判据门（价格/世界口径），无"限时试用"形态 |

另注：其市场层是**加法层**——carry 仓位对生产控制器隐蔽（`_wct_agent` 从 parent 视野里扣掉 carry 麦），生产主干不被市场层污染；我方 PREDICT 恰败在预测直接写入主计划。

## 四、同域机制差异点清单

它做了我们判负过的事、但形态不同：
1. **跨拍持有**——"持货等峰值"我方判负，它的 carry 也是跨拍（买→隔轮卖），但期限有界（1 轮）+价差来源结构性（town draw 确定性消耗）+规模由清算模型封顶；差异在"等什么"（等事件 vs 等更高价）与"多久"（1 轮 vs 无界）。
2. **对手卖流推断**——PREDICT 的 infer_rival_sells 判负，它同样从公开面推断对手净卖流，但只做减法（含 draw 修正）+事件计数，不外推不预测——判负的是"推断→外推动作"，不是"推断"本身。
3. **入场门 vs 出场门**——它的一切防御都管**入场**（停开新仓/试用期），出场恒定（次日必卖、708 前清仓）；我方 R27 的门管**出场**（日新高才卖）。两个门方向互补，不冲突。

形态根本不同（不可类比判负）：
4. **检测器 vs 账本**——realized-loss 检测不改单不记账，与债务账本的"记账+重排"是不同机制类；我方 R28 之负不能外推到检测器形态。
5. **成本下界 vs 实现价测量**——它闭环（下界→事件→停开仓），我方开环（缺口→归因报告）。

## 五、自报对照行（自报≠可迁移；全部只登记不作判决依据）

| 项 | 自报内容 | 来源 |
|---|---|---|
| 名次声明 | "The IDs identify the implementations, not their rank. **No final competition score is claimed.**"（56720309/56713902=实现标识非名次） | 包 README（2026-10-03 实读） |
| Observed 归档对照 | 16 世界×2 席×16 对手 475/512（成熟参考 451/512，30 翻正/6 新负）；"512 contexts contain only 16 independent worlds…neither measure Last Dance nor establish current leaderboard strength" | 包 README（自报存档数） |
| 发布校验 | seed 20261002 双席 6 路径 4,314 决策逐位一致（源/资产分离校验，非竞技读数） | 包 README（自报） |
| 上游 kernel 日志 | "280 paired games: 191-53 -> 280-0; 89 losses turned into wins…mean margin change +758"；entry `_cxd_agent` wraps `_cxtb_agent` | kernel_output/best-agent-ranking.log（kernel 自报，非我方实测） |
| 本池实测 | last_dance vs H1 0.8333（10/2/0）；面板/种子洞见上表 | evidence/mqingcs_arena.json（2026-10-03） |

## 六、异常与限界

- **种子洞（2/12）**：674262/675048 双席四对手全败，margin 负得不多（−276~−1661）——世界条件性弱点，根因未拆（留复盘：疑与特定 shop 解锁序列下 carry 清算模型失准相关，未验证）。
- r40/A 弱锚掉分（0.8333/0.75）即上述种子洞的直接投影；对照 syx 的弱锚 1.0——弱锚不干净≠强，是世界覆盖问题。
- sim_bridge wall_speedup 0.953（≈1）：本件 agent 计算重于引擎，仿真器无提速收益（不损正确性，30/30 一致）。
- observed_001 可装载但未测：按任务纪律不烧局；其提交形态（包装器）缺任务库 UNRUNNABLE，故"可装载"不等于"可发射"。若用户要补测需先裁合规（其推理完整需 24 局私有任务库，我方无授权持有）。
- 面板 n=12 fold：0.8333 的 95% 置信区间宽（±~0.22），横比读数按"带内同档"理解，不区分 0.75-0.92 间的排序。
- 上游为 kernel 最新版本快照：作者若重跑且常量变更，本档以 sha256 锚定（a16e0e9b…d82ab）。
- 判决先行·只测不发·不提交；上线决策移交用户。

## 七、建议（分级）

1. **[高·立即]** last_dance 入"战后开源强件"名录（第四件 BEATS_CEILING，与 syx/taeyan/romansvet 同带），机制对照表收割进复盘轨（§三/§四——尤其"防御管入场不管出场""检测器≠账本"两条判例修正）。
2. **[中]** 种子洞根因拆解（674262/675048 两世界的行为画像，验证 carry 清算失准假设）——为我方"世界条件性弱点"清单添一个外部样本。
3. **[低]** observed_001 是否补池测移交用户（先裁私有任务库合规边界；不裁则维持 LOAD_OK_UNTESTED 登记）。
4. **[低]** mqingcs_upstream 归档随 PROVENANCE 已闭环；终榜（10-14）后对表该队实际名次，回填"公开件≠提交件"警示第 9 例。

---

### 需登记行（主会话处置；本报告不改 INDEX/JOURNAL/registry）

- `references/2026-10-03-mqingcs-pooltest.md`（本报告：mqingcs 双策略池测判决——last_dance BEATS_CEILING 0.8333/96 局零红局；observed 缺任务库 UNRUNNABLE×2+可装载未测×1；机制对照表 6 条+同域差异 5 条）
- `ext/mqingcs_upstream/`（上游 kernel output 归档：main.py sha256 a16e0e9b…+submission.tar.gz+log+PROVENANCE；dependency_spec 4 条 UNIQUE-OK）
- `fn_work/legacy_software/kaggle_simulations/orderbook_mqingcs_lab/`（判决 lab：judge_mqingcs_arena.py+evidence/mqingcs_arena.json 156 局次+run_full.log）
