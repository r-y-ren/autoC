# 2026-09-27 改进面调研（analysis24 调研轮）——3000 分段靠什么、我方未用面值不值

> 任务：找"还没试过的改进面"，重点=顶部选手（3000+）靠什么拿分。只调研+写纪要。
> 抓取/计算日期统一 **2026-09-27**（georgymarin 数据集版本 2026-09-26；标注 [09-25 缓存] 者沿用前轮）。
> 通道：kaggle CLI 2.2.4（leaderboard/kernels pull/kernels list）+ kagglesdk get_topic/list_comments + GitHub REST/raw + 本地计算（stream_hash/episode_features 分析，脚本临时于 /tmp/fn24，未入库）。缓存 `/tmp/fn24/`、`/tmp/kbscan/`（临时）。
> 纪律：逐条带来源 URL+抓取日期；他人实验数字标"自报"；查不到写"未找到公开来源"。
> 已扫勿重复：09-25 topband-strategy-scan、09-27 predict-throttle-scan；已证负勿推（PREDICT 抢跑判负、番茄门/麦簇/换种/卖侧四臂全负）。

---

## 一、DSM 模板库再探（Q1）

1. **XZDang13/kagglefarm 已消失**：https://github.com/XZDang13/kagglefarm 09-27 返回 404（09-25 尚可抓），用户 repo 列表中已无该库，GitHub 全站搜 kagglefarm 无 fork 存活。"Waypoint 模板库+Local Service"的唯一第三方 RE 信源**不可复验**；仅存我们 09-25 缓存（/tmp/kbscan/kf-tmpl.md、kf-final.md）。证据等级维持 **C**（Local Service 打包访问细节仍无一手来源）。（GitHub REST，2026-09-27）
2. **一手回放实测升级了"模板库"假设**（georgymarin/kaggriculture-episodes `stream_hashes.csv`+`agents.csv`+`teams.csv`，数据集 2026-09-26 版，本团队 09-27 计算）：DSM 307 局公开对局的动作流前缀，**top1 同前缀占比 0.769@t24 / 0.759@t48 / 0.759@t100 / 0.752@t136 / 0.567@t200 / 0.557@t300**（distinct 前缀仅 17~95 个）——一局游戏前 5.7 天动作逐字节相同、局间只在中后段分叉 = **固定调度/模板库 + 后段执行**，与"模板库"假设一致（证据等级 **B**：公开回放可复算）。对照：DECEM top1 0.39@t24→0.15@t300（反应式）；M&M&P&Q 0.61@t24→0.067@t300（前两天固定、t136 后大分叉）。
3. **DSM 无血缘**：destbreso "Who is beating you, and is it you?"（https://www.kaggle.com/code/destbreso/who-is-beating-you-and-is-it-you ，09-27）明言"当前第一名没有亲属——其对手在一致性分布上无双峰、近 7 场败局全部来自血缘之外"；rank15 同款、rank50 血缘规模 1。头部不是公开 fork 生态的一部分——其模板为私有。
4. **3000 段要什么量级优势（对照我方 ~1400-2000）**——本轮实算（同上数据集，09-27）：**各段宏观指纹几乎相同**（peak_crew=12、first_land_day=6、tiles≈239、wheat≈163、strawberry=33、melon=12，1400→3000 各段一致；DSM 自身=crew11/tiles239/wheat163/carrot31），**优势不在结构**；DSM 局内 margin 中位 +3,556、胜率 0.787（n=324）；3000 段整体 margin 中位仅 +791。742856（[09-25 缓存]）：2250+ 对手 40% 局由 <$100 决出、78% 由 <$1,000。cha22（见二-1）："gap is conversion, not scale"，11k 回放上最稳健的胜负差=**实际成交单价 +8-10%（同回合成交配对竞速）**（自报）。→ 3000 段=稳定小优势换胜率，不是大 margin。

## 二、高分段公开策略普查（Q2，09-25 后新件优先）

1. **abhinav0370/cha22-agent（https://www.kaggle.com/code/abhinav0370/cha22-agent ，09-27）**："route-replay agent"——**每个店序（route）预计算 719 步动作磁带 + 运行时 router 选路 + 反应式安全/市场层**。自报本地全池回归 57 对手 1368 局 1337W/0T/31L（97.7%）、均差 +6,670；其天梯败局复盘四条：①输在 **d18-29 晚季转化**（前 17 天领先、后段被翻）；②**非商店抽签**——把败局的原店序重放进仿真差距反而扩大，"头部赢在执行不在运气"；③稳健胜负差=**同回合卖单成交竞速**（实际单价 +8-10%）；④土地/作物/畜群/现金轨迹与头部差距仅几千——"差的是转化不是规模"。其对手池含 observed_timing_r37（我方谱系）：cha22 24-0、均差 +7,033（自报）。
2. **salemali7/kaggriculture-2900 "HarvestForge-X"（https://www.kaggle.com/code/salemali7/kaggriculture-2900 ，09-27）**：由 3 个公开 reference run（92165990/92185587/92223213）逆向重构，三条轨迹"生产序列几乎一致、市场决策 99.91% 一致"——头部 run 是可挖的模板；核心 **8C/4S**（step0 1牛4羊→step192 8牛4羊）、麦/莓/瓜轮作、V16-RC5 "需求门控一回合前拉"（gate=当回合无城镇需求且棚有货，s+(q−s)=q 不变量，买/雇不动）。自报 60/60 胜重构核心、24-0 胜 Kaito V27/Rayk C71/llcc 公开件。
3. **742246 Neurosymbolic RL（xaxipiruli，https://www.kaggle.com/competitions/kaggriculture/discussion/742246 ，09-27）**：对强公开件 **0 胜**；对 v48 缺口 77% 集中在**草莓+羊毛的生产量**（"gap is production, not timing"，种得多但保活率仅 1/3）；三大教训=边际价定价（名义价错算亏 40-66% 三次）、hour-0 陷阱（hands=0）、对角线扫描骗人（悬崖是作物类别一个变量）；其自身 CEM 最优把作物密度打到 0（种地挤掉畜群经济 −41~−50k，其执行器口径，弱件结论慎用）。
4. **dzjiann RL 复盘（https://www.kaggle.com/competitions/kaggriculture/discussion/743716 ，09-27）**：196 核 RL 打公开件 ~90% 胜率但封顶 top-100，**对高分对手反而弱于其数学规划/DP 手写法**；self-play 迅速平台期——"堆算力+self-play 不够"。与 742246 同款结论。

## 三、我方未用面核实（Q3，正负都收）

1. **条件路由库（DSM 模板路线）——强正证据**：Tschinkel "95.5% Win Rate via Replay Routing"（https://www.kaggle.com/code/thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing ，09-27）：1 个开局 + turn144 按公开状态选路（town 要毛→羊路线/要奶→牛路线/否则留开局），5 条内嵌磁带、9 决策节点、p99 0.016ms/回合；44,096 局 held-out（689 条未见回放、32 seeds、双座位）：**单条固定回放 84.6%→路由 94.5%→同开局面路由 95.5%**（+11pp）。**拼接约束=开局哈希同组**（623 个开局、最大族占 36%；组外拼接"是在赌博"；语料最强单条回放 90.8% 因族规模=1 而无法路由）。另有 OpenKaggle/kaggriculture-research（https://github.com/OpenKaggle/kaggriculture-research ，09-27）hybrid 系 agent：首店公开后在两个冻结公开锚点间路由（YARN 首店→A 否则 B），`shop_policy.py`="Bounded, own-state routing between complete public-history action tapes"+`model.json` 决策树（step144/648、阈值 9888 等），只用自家+公开状态（其章程明文禁止对手身份入运行时）。cha22 同架构（二-1）。
2. **V93 敌指纹路由表——只有诊断件、无效果证据**：destbreso "who-is-beating-you"（09-27）给败因分类学（t72 前分叉=开局问题/揭示点分叉=路由问题，补法=**给输的世界补一条路线**/揭示间分叉=策略旗标）+"97% predictable: Extracting decision trees"、"Can I Clone You From Your DNA?"（08 月件，09-27 检索）做对手指纹提取；但**敌指纹键控路由的正/负效果实验未找到公开来源**；OpenKaggle 章程明文"不把对手身份写入运行时策略"（合规敏感）。克隆门控预留（EXP283，[09-25/09-27 已扫]）是唯一邻近先例。
3. **BUY_PRODUCT 喂麦时点——公开负结果**：arsgorynich "Herd Safe v3 Experimental Risk Aware Feed"（https://www.kaggle.com/code/arsgorynich/herd-safe-v3-experimental-risk-aware-feed ，09-27）："**physically confirmed feeding produced no final-cash improvement; audited behavior mostly abstained**"；"prior v3 feeding change alone had not established superiority over v2"；scenario-robust ordering 12 屏 12 负被否。evgendvorkin 件用 BUY_PRODUCT（[09-25 缓存]）但无量化收益。
4. **day0 作物结构/重排——期望值低**：destbreso "Everyone is playing the same opening"（https://www.kaggle.com/code/destbreso/everyone-is-playing-the-same-opening ，09-27）：t24 覆盖率 94%、最大开局族加权 15.1%（修正后）；新开局 48h 内扩散至近半座位（面板 33 采纳 0 回退），但"**换开局买到的只有自己迭代的约 1/4**"、开局间无可利用的循环（零 cycle、无 counter-pick）；叠加本轮分段指纹实测（一-4）各段 day0 结构相同——重排 day0 预期收益小。

## 四、Rust 仿真器（Q4，debmalyaroy/kaggriculture-simulation）

1. **可用性（https://github.com/debmalyaroy/kaggriculture-simulation README，09-27）**：Apache-2.0、锁定 kaggle-environments **1.32.7**（与官方一致）；差分套件逐回合比对全状态（双方现金按 IEEE-754 位模式）→ **byte-identical**；550k 步/s（1 线程 ~770 局/s）。
2. **16x 属实**：同 20 局 Python agent：官方 env.run 2.52s/局（1 进程）/1.41（2）vs `kagg tournament` 0.30/0.15s/局（银行值逐局核对一致）。Python agent 直接跑（submission 文件原样执行），kaggsim 纯标准库、Python 3.10+。
3. **判决实验配套件**：`kagg compare`=配对 McNemar+逐对手分解（我们 ≥6 seeds/walls 口径正对口）；world 分层 tournament（stratified/world_weighted_score）；`screen_continuations(..., at_step=144)`=按世界给"同一前缀磁带的候选续段"排名（条件路由库的现成工具）；回放续跑/首个分叉定位；CI 出 Linux 静态 musl 预编译二进制（Docker/Kaggle dataset 亦有）。
4. **集成成本=低-中**：下载/编译一个二进制 + `pip install -e .`，把我方 agent 入口喂给 `kagg tournament` 即可，无需引擎再验证（自带 fidelity certifier）；限制=仅默认配置、tape 工具开环、镜像局两座位共享解释器（模块状态串局陷阱——bardiabahadori 已报）。替代件：destbreso kagsim（2000 局/s）/"From 1 to 24k episodes a second"（09-27 检索到，未细读）。

## 五、败局面（Q5，三类败因对照）

1. **通用拆解工具**：destbreso "who-is-beating-you"（09-27）：血缘近邻=卖单差异分类（earlier/later/more/not-at-all，同局对照）；血缘外败局=强度差，"答案是更好的 agent 不是更好的旗标"。
2. **重畜群对手**：反制件已存在（haideptry Wool Front-Runner，[09-27 已扫，勿重复]）；本轮补充=salem 8C/4S（4 羊→8 牛，比 6牛11羊 更奶向，自报 24-0 胜 Kaito/Rayk/llcc）与 arsgorynich forecast4（对 Herd-Safe v2/More Wheat v9/Order Book v3 合计 20W/4L，自报、4 seeds 小样本）；两件均自报，**无独立复核**。
3. **小麦流水引擎**：lynnsakurai "Farmer John and the Wheat Seller"（https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-wheat-seller ，09-27）给**可执行量机制**：e_{i,j}=min(q, 余量)，e=0 的单占队列槽但不产生需求；"inherited closure"把后位可执行现金卖单前移补洞（保相对序与量）——对"麦流占槽"对手/自家卖单排布有直接机械口径；cha22 对 one_more_wheat/wheat_microstructure 类全胜（自报）。**专门针对"小麦流水引擎"打法的公开拆解未找到**。
4. **清群转种植**：**未找到公开拆解**；邻近证据=742246"种植挤掉畜群经济"（其执行器 −41~−50k）、haideptry Tomato/Melon Pivot 转无人竞争账本（[09-27 已扫]）；destbreso 败因分类学可作诊断框架（揭示点分叉→补路由，见三-2）。

## 六、改进面候选清单（按预期收益排序；A=一手实测/官方，B=自报实验或多源互证，C=单方 RE/未证）

| # | 改进面 | 证据等级 | 依据（来源见各节） |
|---|---|---|---|
| 1 | **条件路由库+同开局面拼接**（开局族约束下按公开状态选磁带路线，揭示点拼接；自有路线库） | **A/B** | Tschinkel +11pp（44k 局 held-out，三-1）；cha22 架构+97.7% 全池自报（二-1）；OpenKaggle hybrid 决策树路由（三-1）；DSM 前缀指纹 B（一-2） |
| 2 | **同回合卖单成交竞速 + d18-29 晚季转化**（订单簿配对锁步的槽位/时点执行；尾段变现） | **B** | cha22：11k 回放稳健差=实际单价 +8-10%、"conversion not scale"、败局复盘 d18-29（二-1）；我方分段实测"结构同、margin 薄"（一-4）；742856 小分差口径 |
| 3 | **队列占位管理**（零执行单占槽 + 后位可执行卖单补洞；配合 layer D 空槽位次语义） | **B** | lynnsakurai 可执行量公式/inherit-closure（五-3）；Tschinkel `['SELL',...,0]` 占位技巧（三-1）；742943 空槽位置性（[09-25]） |
| 4 | **判决实验提速基建**（Rust 仿真器：16x、McNemar、续段筛选）——是 1/2/3 的判据放大器 | **A** | 四-1~3 |
| 5 | **世界覆盖补路线**（按败局"揭示点分叉"归因给输的世界补路由，而非改全局） | **B** | destbreso 败因分类学"fix is coverage: another route for that world"（三-2/五-1） |
| 6 | V93 敌指纹路由表 | **C** | 只有诊断件（三-2）；无效果实验；合规敏感（OpenKaggle 章程拒用对手身份） |
| 7 | BUY_PRODUCT 喂麦时点 | **C（偏负）** | arsgorynich 喂养确认无终局现金收益（三-3） |
| 8 | day0 作物结构重排 | **C（偏负）** | 开局已收敛、换开局≈迭代收益 1/4、分段指纹同构（三-4/一-4） |

## 七、对我方四条未用面的价值判断

1. **条件路由库（DSM 模板路线）：升为最高优先**——公开界三个独立强件（Tschinkel/cha22/OpenKaggle hybrid）同架构且有 +11pp 单变量效果证据，DSM 前缀指纹进一步支持"头部=模板库"；我方若做，注意拼接约束（同开局族）与"只用自家+公开状态"边界。
2. **V93 敌指纹路由表：降级/窄化**——公开无效果证据、身份键控有合规争议；仅保留克隆/镜像门控（EXP283 形态）+ 用 destbreso 分类学做败因诊断（诊断价值 > 路由价值）。
3. **BUY_PRODUCT 喂麦时点：不推**——公开唯一相关实验为负（arsgorynich），且我方已证负面多在卖侧频控，喂养侧无量化正收益先例。
4. **day0 作物重排：不推**——全场开局同构（t24 覆盖 94%）、结构指纹跨分段一致、换开局收益仅迭代 1/4；同样的精力投 2/3（卖单竞速、晚季转化）期望更高。

## 八、未找到公开来源

① DSM 本体一手公开面（成员无公开 notebook/repo；XZDang RE 库已 404）；② "3000 段需要 X 优势"的官方换算或经验公式（只有 Elo/BT 定性+薄 margin 实测）；③ 敌指纹键控路由的正/负效果实验；④ BUY_PRODUCT 喂麦时点的正向量化收益；⑤ "清群转种植"与"小麦流水引擎"两类打法的专门公开拆解；⑥ 本轮未复核 arsgorynich/salem/cha22 自报数字（均标注自报）。

## 九、来源清单（除标注外均 2026-09-27 抓取/计算）

| 来源 URL | 通道 | 日期 |
|---|---|---|
| https://www.kaggle.com/competitions/kaggriculture/leaderboard （2026-09-27T09:17:19Z 快照：DSM 3112.9 / Boey 3017.4 / M&M&P&Q 3003.7；3000+ 仅 3 队、2600+ 115 队） | kaggle CLI leaderboard -d | 09-27 |
| https://www.kaggle.com/code/thomastschinkel/kaggriculture-95-5-win-rate-via-replay-routing | kernels pull | 09-27 |
| https://www.kaggle.com/code/abhinav0370/cha22-agent | kernels pull | 09-27 |
| https://www.kaggle.com/code/salemali7/kaggriculture-2900 | kernels pull | 09-27 |
| https://www.kaggle.com/code/arsgorynich/herd-safe-v3-experimental-risk-aware-feed | kernels pull | 09-27 |
| https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-wheat-seller | kernels pull | 09-27 |
| https://www.kaggle.com/code/destbreso/who-is-beating-you-and-is-it-you 、https://www.kaggle.com/code/destbreso/everyone-is-playing-the-same-opening | kernels pull | 09-27 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/742246 、/743716 、/743214 、/743384 、/743179 、/743249 、/743760 、/743772 | kagglesdk get_topic/list_comments | 09-27 |
| https://github.com/OpenKaggle/kaggriculture-research （CAMPAIGN_CHARTER_v1.0.md、agents/hybrid_*、shop_policy.py、REPRODUCIBILITY.md） | GitHub REST/raw | 09-27 |
| https://github.com/debmalyaroy/kaggriculture-simulation （README 全文） | GitHub raw | 09-27 |
| https://github.com/XZDang13/kagglefarm （404，删除确认） | GitHub REST | 09-27 |
| https://www.kaggle.com/datasets/georgymamarin/kaggriculture-episodes （episode_features/agents/teams/stream_hashes/episodes.csv，2026-09-26 版；分段指纹、DSM 前缀指纹、top 队 margin 为本团队 09-27 计算） | kaggle datasets download + 本地计算 | 09-27 |
| [前次] 2026-09-25-topband-strategy-scan.md、2026-09-27-predict-throttle-scan.md（742856、742943、haideptry 系、V52 等） | 见该两篇 | 09-25/27 |
