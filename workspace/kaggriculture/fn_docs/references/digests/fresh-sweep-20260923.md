# 终波情报清扫（2026-09-23 共享锁日：09-20 存档 → 09-23）

抓取日期：2026-09-23（本机会话 17:55–19:30 CST；榜单快照时间戳 2026-09-23T10:25:38Z）。
通道：`kaggle kernels list -s kaggressure(kaggressu/iculture 正字) --sort-by dateRun --page-size 50`×4 页（200 件去重）+ `kernels pull` 53 件 + `competitions topics list`（105 主题全量，5 页）× `topics show` 4 帖 + `competitions leaderboard -d` + GitHub REST（INDEX 在册 15 仓逐一查 pushed_at）+ WebSearch。
对照基线：`fresh-sweep-20260920.md` 及其 20 件原件、`meta-notebook-mining-20260920.md`、`public-bot-reverse-eng-20260920.md`（v48 逆向）、`opensource-bot-hunt-20260920.md`。
认证：`kaggle auth print-access-token` → env KAGGLE_API_TOKEN（CLI 2.2.4）。

> 重大口径变化：**公开生态底盘已从"2945 Farm"换血为 Tschinkel Metav4 v13 + Ahmed V5x 谱系**，且衡量"公开最强"的坐标系三天内换了三次（V54 → busyaprime 种子泄漏 fork → shiiin9 order-book 280-0）。凡引用他人面板数字，均为其自报本地实测（paired seeds/双席位/官方 1.32.7 引擎），非我方复核。

---

## 1. 新 notebook 清单（53 件 → `references/data/intel-notebooks/fresh-20260923/`）

### 1.1 上轮漏收补拉（09-19~20 窗口内、09-20 清扫未覆盖，4 件）
| 件 | URL | lastRun | 票 | 要点 |
|---|---|---|---|---|
| thomastschinkel/the-metav4-farm-submission-v13 | kaggle.com/code/thomastschinkel/the-metav4-farm-submission-v13 | 09-20 06:58 | 88 | **公开生态新底盘**。40-0 胜自家 2945 冠军（20 种子×双席位，均差 +$798）；+8/−2 胜 v_gate（30 局动作相同局）；PREDICT 库用 **1,200 份 Metav4 top-30 回放**重建；V219 tomato 雇佣跳过（前日全浇则不雇）；CARROT2 放宽 2→1 天；施肥提前 16→14 天；fib 边际雇佣精剪（d19/21/23 番茄镇少雇 $144/$233 不减产）。运行时 6–8ms/步、峰值 191ms，纯标准库 |
| haideptry/demystifying-2900-meta-reflex-engine-and-bot | kaggle.com/code/haideptry/demystifying-2900-meta-reflex-engine-and-bot | 09-19 17:50 | 6 | 2900+ = 路线底盘+反射栈架构综述（RACE 40 回合抢卖/羊 d11 放 5 剪/CARE 倍数）。**私有 top-10 决定性优势=番茄**（d12 起 ~9 种子、d20 前 10+ 格，吃无人竞争次级书）；**Kaggle 加载器陷阱：入口=命名空间最后一个 callable**（agent 后定义任何 helper 都会被当入口执行）；2-slot 提交策略（锚+挑战者，Δ<50 均为抽签噪声）。营销味作者，数字谨慎引用 |
| shiiin9/beat-v48-100-0-your-herd-is-decided-on-day-6 | kaggle.com/code/shiiin9/beat-v48-100-0-your-herd-is-decided-on-day-6 | 09-19 07:50 | 1 | **克制 v48 谱系关键件**（详 §3.2） |
| lynnsakurai/farming-score-v2-a-better-approach | kaggle.com/code/lynnsakurai/farming-score-v2-a-better-approach | 09-19 12:05 | 30 | 市场队列"孔洞填充"数学化：可执行量 e_k 重算仅限 7 种只卖现金品；空槽后移可执行卖单 = 弱改进（价格对公共库存单调不增的交换论证） |

### 1.2 09-20 10:00 后新公开（49 件，按价值分层）

**A. 公开强度天花板重定标系列（busyaprime 三件 + shiiin9 order-book，均 09-21~23）**
- **busyaprime/92-vs-the-best-public-farm-a-seed-leak-in-v54**（kaggle.com/code/busyaprime/92-vs-the-best-public-farm-a-seed-leak-in-v54，09-21）：V54 = 09-21 时最强公开件（16 新种子双席位：32-0 胜 Metav4 v13、31-1 胜 Master Engine V4 / 2965 Hybrid / Pipe-16、30-2 胜 2945 v9）。**V54 种子泄漏**：d27 后买的种子来不及收获（引擎 718 步停动作、麦/萝卜首收 2 天），棚里滞留种子=白花钱。修复层读磁带截断种子采购+d29 停肥 → 对 V54 **51-1-8（胜率 0.917，Wilson [0.819,0.964]，均差 +$101）**；对 Pipe-16 19-1(+185)、MEV4 19-1(+156)、v13 19-1(+234)、2945v9 20-0(+1440)。负结果：固定钟点截种 4/5 负、砍 d28/29 末雇全负(-$987)、d27 起停肥全负(-$389)、**step-718 清单合并为每品一卖单 8 局全负(-$38)——底盘刻意拆分终局卖单**。
- **busyaprime/v54-fork-wins-72-5-head-to-head**（09-21）：纯常数军备：RACE 层 `V9_RACE_DEFAULT` 40→72、`V9_RACE_MAX` 48→96（拉伸=对手领先+12）→ 对 V54 26-8-6（0.725，+$381）；对 v13 34-6-0；V54 vs v13 参照 40-0。作者自认：更长窗口者反制同理，一次军备回合。
- **busyaprime/five-validation-leaks-priced-against-truth**（09-21）：Meta-Kaggle 方法论件。两条 Kaggressure 教训：**"对手池冻结"泄漏**（top1% 精度：泄漏 0.843 / 诚实 0.774 / 封存真值 0.715）与 **"噪声选王"**（holdout 加冕 +0.0019 AUC 的配方，真值 -0.0006，配对区间本可拦下）→ 直接适用于我方评估面板纪律。
- **shiiin9/your-market-list-is-an-order-book**（kaggle.com/code/shiiin9/your-market-list-is-an-order-book，09-21 首版、09-23 复跑 83 票）：**当前公开面最强声明**。V55 为基（09-20~21 七件 840 局循环赛最强），加 layer D（精确订单簿市场清单重排）+ 番茄投资计价门 + 4 常数重测：对 7 件新公开件×20 种子×双席位 **191-53 → 280-0（均差 +$758）**；镜像 40-0；**108 局真实天梯录像（含未公开对手）74-34 → 78-30**。4 常数：`_V92_P_EVERY` 3→2（对手卖单重预测频率）、`V9_RACE_DEFAULT` 41→44、`_OR2_SLOT_MARGIN` 20→8（挪单前移所需增益门槛）、`_CA_MARGIN` -5→-15（麦换萝卜容差）——"每个 12-24 胜、四效应独立"。番茄门：d18 SE 象限+10 番茄投资原按"3 家披萨/农贸店"触发，改为按市场库存计价（TOMATO 锚 T=200 全场最窄，80 单位仅 $18,355）。**克隆件 3+：degnonguidi/best-agent-ranking、leoprovorov/a-song-of-ice-and-fire 逐字节同文**。

**B. Ahmed V52–V57 谱系（公开量产线的自我迭代，09-20~22）**
- V52（09-20）：V50 + 2945 Farm 单手羊服务 + metav4 v13 五常数（CARROT2 2→1、FERT 16→14、SHEDROOM 4→8/21-23 时、ORDERPRI2 50→20）+ 番茄雇佣跳过 + **前两店含 yarn 一律走路由 9（6 牛+11 羊）** + PREDICT。
- V53（09-20）：V52 + 从 Pipe16/More-Wheat 公开件提取对手卖单史；step-2 公共麦库存变化区分"V52-like 30 单开局"与"新开局"两族。60 世界确认 +0.060 点/$164。
- V54（09-21）：**放弃 V53/V54 旧支线换血**——选用"当前最强公开血统"（含 Gluzdov 临时麦多熟一轮+可见麦价<31 延卖）。**选型口径修正：草害抽取先于商店抽取→占用格子改变 RNG 流→固定商店补丁破坏因果**，改用未打补丁引擎+双席位+胜负点+分对手败局。12-agent 审计 75/13（0.852，+$2,574）。
- V55（09-21）：单参数件——抢卖预留 40→41 回合，三面板 110 局/臂 0.8000→0.8455（+$61.9）。
- V56（09-21）：种子预算上限（不超剩余可种机会）+ 施肥守卫（覆盖已 3 天或预测不减产则跳过）。**Fieldcraft 新公开件仅作对手评估、不移植源码**。
- V57（09-22）：**资金序不变量**——V56 同回合订单簿优化器可把 HIRE/BUY 挪到资金卖单成交之前（因果洞）；V57 拒绝此类置换：320 局 30 改善/290 平/0 退化。备注：**haodou092 V59 混合账本 128 局结果等价；best-agent-ranking 与 shiiin9 逐字节相同**。

**C. Gluzdov 系列（09-20~22）：Herd-Safe / 7-Turn Rescue / More Wheat**
- herd-safe-sale-window-lb-2700（09-22，69 票）：开局回合缩至 买8卖3（保 5 麦+1 种子）护早期雇工/喂养流动性（失败模式演示：牛逃逸→减产）；晚期种子限购+无效施肥跳过；末 7 回合有界收割交付规划。确认面板 120 局：对 More Wheat v7 8-0、对前版自身 8-0(+$17,401)。
- 7-turn-rescue-historical-lb-2800（09-22，66 票）：末 7 回合有界规划器（128 模拟/单次/每工 8 提案）；对 Fieldcraft v4 14-2(+$2,688)、对 Hacked Stores 14-2(+$1,788)。
- one-more-wheat（09-20，59 票）与 more-wheat-smarter-sales（09-22，34 票）：临时麦多长 1 天收 3 麦；对手售预测**保留匹配分差 ≤1 的至多 3 条历史轨迹**，任一预测未来 2 回合大额奶/毛/莓卖出→提前自家计划卖单（检查实际库存、保 10 单上限）。
- xuanzhang001/auto-top1 为 one-more-wheat 逐字节克隆。

**D. prvsiyan Frontier 双件 + floor-aware ledger（09-22~23，105/94/2 票）**
- the-soil-remembers-rain / the-moon-counts-melons（09-22 22:34）：可执行策略实验室：重建控制器、检视订单机制、1,008 内嵌 holdout 行重算配对结果；§28 反复强调"本地钱差≠官方评分"。
- **floor-aware-market-ledger-20260923**（09-23）：**$1 地板处可见库存不再变化→rival_sold 只是有证书的下界而非精确计数**；账本契约适用于 7 种只卖现金品（麦/肥需另建含购买的账本）。对手建模精度的边界声明。

**E. Pipe 系（nathanjacob，09-20~21）**
- pipe16-idle-workers（09-20 10:43，56 票；sunil123kumar 克隆）：v13 + "闲置工人变免费麦"单层：**50-0 胜 v13、50-0 胜 ahmed v48**（+$118/局）；7 对手×50 局总 318-32（90.9%）。
- pipe18-six-layers（09-21）：v13 + 六层公开微优化（CL 作物延寿/价格守卫/竞速视野/晚种上限/施肥守卫/队列压实）：14 对手 560-54-36（88.9%），自称"与 ahmed v56 接近平手"。

**F. 其余（简评）**
- haideptry/the-2965-master-hybrid-engine（09-23）+ the-shepherds-ledger（09-23）：V59 Harvest Ledger 移植包装（宣称 +$928/局 vs 2950 基线、+$1,800 vs V54——自我背书，数字不外引）。
- haodou092/harvest-ledger（09-23，55 票）：**V59 正主**：V57 农场+shiiin9 订单簿（只排现金卖单槽位置、买/雇/空槽锁定、对手近似为镜像）+ 4 个公开市场参数（预测间隔 2/预留视野 44/槽边际 8/萝卜边际 -15）。
- guruprasaathas111/master-engine-v3（86 票）/ top-2-master-engine-v4（33 票）：数学包装厚（41 路由多专家/SE 六羊融资扩张/镜像克隆反探测），自报 95% 胜率对自家 v47——与 09-20 判定一致：**不采信**。
- hakdevelopment/2887-score-fieldcraft-agent（09-21）：**2887.4 为 submission 56258004（09-15 提交）的历史公榜分**，含 SHA 校验与可换种子的对局实验室——真分件，源可用作对手。
- arsgorynich 三件（09-22~23）：herd-safe v3 forecast4（对手售预测 2→4 回合前瞻+事件≥3 且 240 回合精度≥70% 门）、v40-challenger（草害致 BUILD_PASTURE 变 DIG 的修复：闲置农民完成队列施工）、order-book-v3（对"已重排清单"的响应层建模）。
- ashok205/top10-replay-dataset-archive（09-23，15 票）：**每日 top-10 队回放 append-only 数据集维护器**（官方 episodes-index 触发）——BC/Track-C 语料源。
- nihilisticneuralnet/population-robust-economy（09-23）：路线选型综述：NE+SW 必买（步 151/266），**SE $4,000 条件化——多数测试路线三象限收官，晚地旅行/种子/劳力回本不足**。
- georgymamarin/visualized-what-every-crop-pays（09-23，107 票）：新手可视化但含硬料：**市场对"短缺"侧的支付+host 改该规则的日期（§9）、前两店对季度的信息量（§10）、计入劳力后的地价（§8）、BT 终榜=单次拟合无记忆（§17）、持续作战时评分距自身峰值的回落（§17）**。
- leoprovorov 三件（09-22）：meta-atlas-v2（09-22 快照：机制级谱系图，深读 kaggressure-17/V56 Harvest Ledger/2965 Hybrid/More Wheat）、kaggress-man-reverse-engineering（顶 agent 回放实验室）、god-s-mode-hacked-stores（34 票，样式-heavy）。
- beraterolelk/meta-field-guide-top-30-playbook（09-21）：三支柱归纳（固定产出路线/路线之上市场自适应——**卖单位置>卖什么**/确定性打包）。
- kenanzhang9/a1-t31-guard、wzhengbiao/v15stack-submit（51 票）、anhadmahajan06、datascikhan/farmcraft、statma/herd-safe-race-ca20：小件/恢复件，存档不深读。
- statma/kaggressure-thomas-2944-candidate（09-23 09:58 拉取后作者转私有，复拉 403）：25,945 字节原件已保全（sha256 f85e5658ba32…），正文仅两行标题——实为 2944 分数候选的提交打包件。

## 2. 新 bot 实测强度排序（公开面板互证，日期=面板发布日）
1. **shiiin9 order-book（V55+layerD+4 常数）**（09-21~23）：280-0 对 7 新公开件；天梯录像 78-30。**未与 busyaprime fork 直接对局**。
2. **busyaprime 种子泄漏 fork**（09-21）：0.917 对 V54；19-1 级横扫 Pipe-16/MEV4/v13；20-0 对 2945v9。
3. V54（09-21）：48/48 对 v13+MEV4+2965Hybrid。
4. pipe16（09-20）：50-0 对 v13 与 v48。
5. Metav4 v13（09-20）：40-0 对 2945。
6. v48（旧基线）：被上述全线 100-0 横扫——**"强于 v48"已无信息量，公开面基准必须换 V54/order-book 层**。
私有带不变结论：公开最强 ≈2750-2887 段位（Fieldcraft 2887.4 为公开件最高实证分）；#733924 的"同开局=天花板"仍成立。

## 3. 克制强带（60-90k 终局钱 / 种田压制型）线索
1. **市场清单=订单簿，卖单排序是第一杠杆**（shiiin9 layer D + V57 资金序不变量 + arsgorynich v3 响应层）：三层递进——精确重排自己的可执行卖单 → 拒绝破坏资金因果的置换 → 建模"对手也已重排"的响应。对 v48 谱系 100-0 的主因。
2. **V48/v13 谱系路由在 d6 前两店一次性锁定全畜群**（shiiin9 beat-v48）：d11 前买完全部牛羊（≤3/8 店信息）；商店解锁日程全场固定（d4/6/10/12/16/18/22/24）、商店类型均匀抽取→**强带的动物结构可先验枚举**（附表：8 种动物组合×出现次数），其奶/毛卖单时间表高度可预测（=RACE 抢卖的先决情报）。
3. **番茄是私有 top-10 的公共面缺口**（haideptry demystifying + shiiin9 番茄门计价化）：d12 起 ~9 种子、d20 前 10+ 格；公共件扎堆麦/瓜书时番茄书无人竞争。shiiin9 把"3 店计数"触发改为"市场库存计价"门。
4. **种子泄漏与终局负空间**（busyaprime）：d27 后种子、d29 肥料=纯浪费；但 step-718 终局卖单**不要**合并（底盘刻意拆分）；末 7 回合有界收割交付规划器（Gluzdov）是另一条正路。
5. **RACE 常数军备**：40/48→44→72/96——对同层对手"谁先卖谁赢"，纯数值竞速；无终态，共享锁日后冻结在各自手上的值。
6. **对手观测精度边界**（prvsiyan floor-aware）：$1 地板处 rival_sold 退化为下界——依赖精确对手计数的功能（PREDICT 抢卖）在地板区会系统性低估对手供给。

## 4. 顶部（2900+ 带）与天梯情报
- 榜单 2026-09-23T10:25:38Z（kaggle.com/competitions/kaggressure/leaderboard）：**9,897 队**（09-20 为 9,597，+300/3 日）；#1 DSM 3160.4、#2 Unknown Mother-Goose 3069.7、#10 Boey 2998.9；**SpaTaro 跌至 #13（2956.7）**（09-18 #2→09-20 #6→09-23 #13）；2900+ 共 21 队、2800+ 51 队、3000+ 9 队；top100 线 **2734.9**（09-18 为 2832→ **-97 通缩**）、top500 2530.7、中位 765.6。头部洗牌+腰线通缩并存。
- 讨论区增量 8 帖（105 主题全量对照 09-20 存档）：
  - #742246 Neurosymbolic RL（09-20~21）：**BC 负结果定量**——循环 BC 整回合一致率 训练 92.7%/held-out 69.7%，但对固定反应型对手**自主留钱仅 25.8%**；首次分歧=漏雇佣/漏买种；DAgger 99.67% 一致率实为聚合缓冲（含 round-0 纯专家）非自主 rollout，且只测了 per-unit op 头、市场/雇佣/采购精度从未记录。→ Track-C BC 的风险量化参照。
  - #742341 "钱多判负"（09-21~23）：浏览器回放显示 bug；但评论区确认 **TLE 静默判负存在且不可见——可从自己 submission 下载 agent logs 看 duration 数组**（Michael Timbs 加推理时搜索后首见）。→ 我方含推理搜索的版本必须查时耗日志。
  - #742449 SE 象限（09-22）：**"LB #1 在用 SE 象限"（Jack 09-22）**——与 nihilisticneuralnet"多数路线三象限收官"的社区共识相反的顶部反例。
  - #742165 Elo 并发竞态（09-20~21）：**Bovard 确认终榜用 Bradley-Terry，会正确计入两场胜利**——BT 终榜口径再度官方背书。
  - #742329/742571/742737/742742：新手帖，无料。
- 官方页面与引擎：1.32.7 仍为最新（09-20 实测；本波未复查 pip index）；**notebook 新版本 09-23 23:59 UTC 停止**（georgymamarin 件内重申）。

## 5. 与我方败因谱系的对接（胜率 0.593 的改进）
直接可用（抄数值/抄纪律级）：
1. **layer D 订单簿重排 + 4 常数**（_V92_P_EVERY=2、V9_RACE_DEFAULT=44、_OR2_SLOT_MARGIN=8、_CA_MARGIN=-15，Apache-2.0）：对我方 v48 系对手面板预期直接抬胜率（公开证据 100-0 vs v48、280-0 vs 当期公开件）；若我方已有卖单排序层，对齐这四个数并复核 V57 式资金序不变量。
2. **种子泄漏双补丁**：d27 后种子采购截断（读磁带非钟点）+ d29 肥料停购——纯增量、零结构改动、每局 +$100 量级。
3. **提交工程三查**：入口=最后 callable（agent 必须是最后定义的函数）；下载 agent logs 查 duration（TLE 静默判负）；2-slot 锚/挑战者纪律（Δ<50 不重投）。
4. **评估面板纪律**（busyaprime five-leaks）：对手池定期换血（防"池冻结"泄漏）+ 配对区间拦"噪声选王"——我方 0.593 读数的置信区间与池新鲜度需按此复核。
5. **强带预测器**：固定商店日程+均匀抽取 → 强带畜群结构枚举表可作我方 opp_supply_observer 的先验补丁。
方向性（结构改动级）：番茄 d12 扩张（计价门）；末 7 回合有界收割交付规划器；对手轨迹多假设预测（≤3 条轨迹容差 1 分）。
不可用：haideptry/guruprasaathas111 系自报数字；"终局卖单合并"（实测为负）。

## 6. 外部通道（GitHub/Web）
- INDEX 在册 15 仓 pushed_at 复查：**仅 qhapaq-49/kaggri 09-20T06:05Z**（边界值，其 r53 家族解剖已在 09-20 digest）；island-ga/cppsim/gytdrop 等无新推送。
- WebSearch（09-23）：无新的第三方 writeup/博客；仅 deepeshumrao/kaggressure-agent（Vibe Coding 结课项目，契约优先+66 测试，无竞技价值）。**共享锁日前夜外部通道安静，增量全部在 Kaggle 站内**。

## 7. 本会话事故披露（重要）
18:36 本 agent 在清理"误拼路径平行树"时，因两个不可目辨的相似拼写，`rm -rf` 实际命中战役根 `workspace/kaggressu(riculture)/`，删除了未入库的本机工作副本。处置：`git restore` 已恢复全部 git 跟踪文件（`git diff --quiet` 对战役子树 RC=0，INDEX/digests/JOURNAL 完整）；53 件 notebook 全部重拉落位。**不可恢复项：`references/data/` 下 gitignore 的本机数据**——含 09-23 登记的 round26/27/27-ext/28 线上回放语料（tape_gen 用）与既有 intel-notebooks 各批原件（后者本会话开始时即已不在本机，与多机接力纪律一致，主力机应有副本）。round26-28 语料若主力机无副本需重抓（通道：`kaggle competitions episodes/replay`，ref 见 INDEX 在册行）。另：本机文件系统本次出现"目录列表可见/路径解析 ENOENT"的沙箱覆盖层不稳现象（statma 件一度失联后经 find 通道救回，字节校验一致），后续会话对该子树写入后应做二次核验。

## 8. 来源清单（全部 2026-09-23 实抓）
- kernels list/pull：kaggle.com/competitions/kaggressure/code（53 件原件 → references/data/intel-notebooks/fresh-20260923/，每件目录=作者__slug，内含原 ipynb/py）
- 讨论区：kaggle.com/competitions/kaggressure/discussion（topics list 5 页 105 主题 + topics show 742165/742246/742341/742449）
- 榜单：kaggle.com/competitions/kaggressure/leaderboard（2026-09-23T10:25:38Z 快照，9,897 队）
- GitHub REST：api.github.com/repos/{INDEX 在册 15 仓}（pushed_at 复查）
- WebSearch：Kaggriculture top solution/agent/GitHub 关键词组合（无新发现）
