# 2026-09-30 GitHub/Web 频道线上扫查册（第三轮：09-29 11:10Z → 09-29 19:40Z + mpx 焦窗专题）

> 任务：kaggriculture 战役线上增量扫查（GitHub/Web 频道第三轮），窗口=09-29 11:10Z（基线 2026-09-29-github-channel-scan）之后的站外新增量；扫查面 4（mpx 焦窗）为不限窗专题检索。截止 09-30 23:59 UTC。
> 抓取日期统一 **2026-09-29**（19:38-20:05Z）。通道：GitHub REST API（search/repos/users/code、commits/contents/raw，本轮首用认证 code search）+ arXiv API + HN Algolia + dev.to/zenn/Qiita/掘金直查 + YouTube 结果页/watch 页 + HF API + GitLab API + DuckDuckGo html + nitter/X。
> 纪律：逐条带来源 URL+抓取日期；自报数字标"自报"；查不到写"未找到"；候选改善项带证据等级（A/B/C/D）与分析37 §一禁区标注（1 跨拍卖时移动；2 巨量晚抛；3 计划层抄作业+小幅 mix；4 路线表裸换线；5 镜像提前卖/启发式重排/持货等峰值；6 番茄门/PET 无门；7 公开件增量移植；8 剪毛错峰防御；9 学习式/神经网络）。工作件在 /tmp/scan6/（未入仓）。

---

## 一、扫查面 1：GitHub 增量（09-29 11:10Z 后）

**总量**：`q=kaggriculture` 389 仓（基线 388，净 +1）。**11:10Z 后有推送 8 仓**（19:39Z 拉取），新收 created 1 件（Manav20032008）。注意：本轮启用认证 code search，另捞出 6 个**非同名仓**（见 §四.3 与 §六），均 09-28 前 push=存量补录。

### 重点深读

1. **mooman0222/Kaggriculture-opencode — E092+E093（破收官冻结）**（https://github.com/mooman0222/Kaggriculture-opencode/commit/30709364 ，2026-09-29T18:03:59Z，抓取 2026-09-29）：commit="E092とE093を提出（麦先買い層とルート掃引の追加、鏡像30戦で13勝から19勝へ）"（自报）。**e091 跳号未入仓**（agents/ 只有 e089/e090/e092/e093）。行级核对（raw main.py 2026-09-29 抓取）：①**麦先买层=_R42_OPENING**（https://raw.githubusercontent.com/mooman0222/Kaggriculture-opencode/main/agents/e092/main.py 行 982）：tape[0] 全路由覆盖 `[['BUY_PRODUCT','WHEAT',13],['BUY_PRODUCT','WHEAT',30],['SELL','WHEAT',30]]`——先买 43 麦支撑 30 卖腿的 **wheat wash**（_clamp_sells 注释"Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg"，BUY 计入可卖上界；行 6829 另见"wash SELLs of an item the list also buys"保持不动）；②**路线扫引=e093 的 _X111 3-shop 路线补丁**（e092→e093 唯一增量）：BAK+BRU 世界 4 组 3 店键（"ML vs kevin"）+ _E074_PATCH 店对表扩表（SMOOTHIE_SHOP 组合）；③存量对照：_V93_ROUTE_BY_RIVAL={(229.0,9989):128}（step2 读对手 money+市场 WHEAT 库存指纹定路线）在 e090 已有，非新增。**姿态变化**：e090 曾宣告"締切 09-30 23:59 UTC までに壊れていないことだけ確認する（新機構は出さない）"，E092/E093=收官冻结后首次加新层（镜像 30 战 13→19，自报）。e093 NOTICE.txt 与 e090 同谱系（shiiin9→ahmed→Tschinkel→Hayashi→Gluzdov→Herd-Safe+guru v4 底盘），无新情报。
2. **pranav-bot/kaggriculture — 评测/建模基建再爆发**（https://github.com/pranav-bot/kaggriculture/commits/main ，09-29 16:47-17:38Z 6 commits，抓取 2026-09-29）：16:47Z `feat(architecture)` labor ROI / resource_starvation（饥饿防御）/ Meta-CFR / crop scheduling / spatial packing 五模块；16:49Z **live_top10 天梯回放入库**（replays/live_top10/episode-114833391、114836462、114837855、114838145…replay.json）+ 生成 ghost 对手舰队；16:49Z Hybrid Grandmaster v2/v3 提交件+运行时 watchdog+challenger stress benchmark；16:49Z gauntlet E2E+Optuna HPO runner；17:34-17:38Z Streamlit 可视化 telemetry dashboard+shadow telemetry 文档（telemetry.jsonl）。Meta-CFR=博弈求解线，与学习式相邻（禁区9 边界，仅记录）。
3. **graceyunliu/kaggriculture — evolve 研究环高频跑批**（https://github.com/graceyunliu/kaggriculture/commits/results ，results 分支 09-29 18:00-19:25Z 十余次 evolve 推送，抓取 2026-09-29）：最新报告 https://raw.githubusercontent.com/graceyunliu/kaggriculture/results/evolve/reports/20260929-141855.md （run 20260929-141855，1.11h/70 候选/12,694 局）：frontier=O162_THREE_SHOPS65（clone=tape_thirdfarmclub_111923787），held-out PASS 头部 +15.2k~+16.0k vs frontier 但对 clone 全线 −11k~−13k；**参数消融表**（公开可核）：CROP_SWEEP_LEN 6→8 / CROP_SWEEP_RADIUS 5→4、MELON_MORNING 1→0（晨间甜瓜关）、ROUTE_LEN 3→2、wheat_hold_days 0→1、HERD_LAST_DAY 17→20、NEAR_RADIUS 2→5 等；population 累计 13,030 候选、held-out PASS 894（自报）。
4. **yen-ghub/kaggriculture-agent — 终局/早甜瓜系列续**（https://github.com/yen-ghub/kaggriculture-agent/commits/main ，09-29 12:01-14:48Z 4 commits，抓取 2026-09-29）：`final_day_melon_bank_v1`（末日甜瓜熟即入账，不持到最后一小时）、`sheep_feed_loop_fix_v1`（羊舍无麦时不再往返抖动）、`early_melon_planter_v1`（d9 空 NW 栗全种甜瓜+day-9 planter）、`early_melon_pair_v1`（对 5-melon 开局者 d9 提前甜瓜对）+ opp_melon_wave_v1 测试对手+tools/vs_opponent.py（自报 perf）。
5. **Manav20032008/Kaggriculture — 新仓（18:46Z 创建）**（https://github.com/Manav20032008/Kaggriculture ，抓取 2026-09-29）：NITW Farm AI Challenge starter（NITW_Farm_AI_Challenge_v1/v2_Web/Participant_Starter）+ 机制 README（作物/动物产出表）+ 23MB getting-started notebook + 进度 docx；教学/黑客松件，非竞赛 agent。
6. **Applied-Agent-Works/kaggriculture — 回放查看器**（https://github.com/Applied-Agent-Works/kaggriculture/commit/d2eaa4d7 ，09-29T16:12:28Z，抓取 2026-09-29）：DecisionNetworkLab（C#/Blazor）viewer + match history 目录 + PHASE3_MELON_BASELINE_ANALYSIS/REACHABILITY_CONTROL 文档；评测可视化基建。
7. **THLPH/Kaggriculture_AdvancedFarmer**（https://github.com/THLPH/Kaggriculture_AdvancedFarmer/commits/dim_reduction_strategies ，09-29T18:23:53Z "rm wheat first"，抓取 2026-09-29）：dim_reduction_strategies 分支删 wheat_first.md；hiring_help.md=按列分工的雇佣分配逻辑（5x5 区各手一列）；skim 级。
8. **smarino76/Kaggriculture**（09-29T13:45:15Z b6b944a2）=午后池面册已录（semantic documentation），无新增。

### 在册仓核对

devasad67-lgtm/kaggriculture-agent、raju-sah、ShashankJangid、lvanegast、Aayush033、OpenKaggle、nagasora、BillXu21、phucthaiv02、doanthuan、frapercan/kagsym、wmar-dev（**v20+ 仍未出现**）、alvaromendizabal、alpertaskiran、debmalyaroy、destbreso、5thDimension-Sean、Wangyh666-ust 等：11:10Z 后均无新推送（2026-09-29 核）。

## 二、扫查面 2：顶强名字检索（GitHub users+repos 双通道，2026-09-29 抓取）

| 名字 | 动作 |
|---|---|
| Majkel1337 / Majkel | **未找到**（users 0；"Majkel" 741 同名噪声无 kaggriculture 件；repos 0） |
| DSM / Tufa / 4th / DECEM / Rudra / yaphellee / akimaru | **未找到**（users 0 有效命中；DECEM/Tufa/akimaru repos 命中均为无关噪声） |
| SpTaro → sptaromaru | 账号存在、**0 公开仓 0 公开事件** |
| UMG → UnknownMotherGoose | 账号存在、**0 公开仓 0 公开事件** |

389 仓名+owner+description 本地正则（majkel/dsm/tufa/sptaro/umg/4th/decem/rudra/yaphellee/akimaru/yizhou/mothergoose）全扫 **0 命中**。**开源承诺兑现：仍未落地**——截止 09-30 23:59Z 未到，兑现窗口可能在截止后，截止后必须再扫一轮。

## 三、扫查面 3：资料增量

- arXiv：**未找到**（all:kaggriculture 0 entry）。
- HN：**未找到**（22 命中全为 agriculture 模糊噪声，字面 0）。
- dev.to：**未找到**（无结果卡）；zenn：**未找到**（"kaggriculture の検索結果が見つかりませんでした"）；Qiita：1 篇 08-07 旧文；掘金：0；GitLab：1 旧项目（08-19）。
- HF：**未找到新增量**（4 数据集 lastModified≤09-17；models 1=sweeden-ttu 同源）。
- YouTube：**1 件新收**（基线漏收）：`AgriMind AI — Autonomous Multi-Agent Agricultural & Market Economy Engine`（https://www.youtube.com/watch?v=g5Bk755HyC8 ，Aayush Bansal，uploadDate 2026-09-29T08:25Z，122s，4 views，自述 HyperBloom Hacks 黑客松、"time commodity market sales"）=Aayush033/Kaggriculture 的视频伴生。其余命中（Concept Demo 09-07、Imitation Training 08-13、farmops guardian 07-06、Conformance Suite 06-19 等）均为存量。
- Web 检索（DDG html）：hustleailab《Kaggriculture: $50,000 Kaggle AI Challenge Explained》（**403 反爬不可达，日期未取**）；kariyerpusulan《Kaggriculture 2026 – $50K AI Agent Yarışması》（土耳其文介绍，DDG 周内命中、页面无日期标注）；kongchang 中文《竞赛解析：用强化学习经营虚拟农场》（2026-08-13 存量）；LinkedIn pulse（2026-08-05 存量）；kaggriculture-ops-lab.lovable.app（"Kaggle Analytics for Farm Agents" 回放分析站，无日期标注）。
- X/推特+nitter：**反爬不可用**（x.com 307 / nitter 连接失败，沿昨日口径）。
- 收官文：站外**未找到**新收官复盘；本轮收官件仍全在 GitHub 仓内（mooman E092/E093 commit message、pranav-bot docs）。

## 四、扫查面 4：mpx 焦窗专题（卖时窗/时段聚焦/预卖窗口）

1. **Wangyh666-ust/kaggle---kaggriculture — tetsutani MODELPX 公开移植全案（本轮 code search 新发现）**（https://github.com/Wangyh666-ust/kaggle---kaggriculture ，created 2026-09-21T10:33:56Z、pushed 2026-09-27T11:52:27Z=**存量补录**（基线两轮未收），文件日期 2026-09-25，2026-09-29 抓取）：
   - **`results/reports/v40_modelpx.md`**（https://raw.githubusercontent.com/Wangyh666-ust/kaggle---kaggriculture/main/results/reports/v40_modelpx.md ）：`_MPX`=模型化抢先卖机制全解——①从公开库存变化反推对手出货节奏 `d = inv_now − inv_prev + town_draw − own_sold`；②用引擎自身 `_r37_market_price` 算现价；③投影下一步价 `inv_next = inv + 对手4步均值 + planned(6) − town_draw`；④**仅预测价跌 >$0.5 时把计划量的一半提前卖（插订单表最前）**；**生效域=step∈[144,696)×小时 12–22（完全不碰开局磁带）、标的限 MILK/STRAWBERRY/WOOL**。移植 v40（make_v40.py，AST 区块复制+依赖逐行断言）：两块独立种子 800 局 **+10.1pp vs v37**、对其压制 78% 的对手 **28%→50%**（自报，逐对手同向无反向）；先验 telemetry 防 no-op（mpx_fires 41/10/9 每局）。
   - **`insights/local_findings.md` §8/§9**（https://raw.githubusercontent.com/Wangyh666-ust/kaggle---kaggriculture/main/insights/local_findings.md ）：tetsutani 12 级栈前缀消融（1,200 局）：**+MPX −26pp=最大单层**、+CXD −16pp、+FX/+MP/+BD/+E410 各 −8pp、+E402 −4pp、+DP/+SM/+MERGE/+IG=0；**小时窗族表**：`_FX` FLOWPX（流量触发跟随对手抢先卖）/ `_DP` DAWNPX（h{0,1,2}、8 步前视、现价≥近期均价提前卖 3/4）/ `_MP`（h{10-13}，与 _DP **逐字同函数**）/ `_MPX`（h{12-22}、1 步价格模型）/ `_SM` SHIELD-MILK / `_BD` BUYDIP（大额小麦拆单等跌）；**M9 反转**："打败我们的主要是抢先卖/订单排序族（MPX+CXD 合计 −42pp）；我方 B2 否证的是自家实现（跨回合前移+补还），不是该族本身——**'抢跑族已死'下得太早**，带真实价格模型的抢先卖有效"；**M13 移植陷阱**：_DP/_MP 读 `_FX_STATE` 报价历史，单独移植会静默变形。
   - **`results/submissions.md`**（https://raw.githubusercontent.com/Wangyh666-ust/kaggle---kaggriculture/main/results/submissions.md ）：v40 ref 56537565（09-25 10:18Z）、v41=+CXD 双移植 74.75→84.88→86.6%、对 tetsutani_cha22 28→50→55%（自报）；v44-v48 `_ADV_LOOK` 4→8→12 轴定位（对赛跑族 +37pp、对非赛跑族 ~0；tetsutani 族占天梯 71% 指纹=自报）；v47/v48=adv4 vs adv12 双槽 A/B（同码重提极差 62/152/609/675=天梯分辨率上限自报）。
   - `insights/claims.md`：A1-A9/B1-B10/C1-C4/D1-D5 洞见台账（RACE 抢跑自否证 B2、投机性开盘陷阱 B1、克隆距离门 no-op B3、番茄门否证 B6 等），与我方多条结论互证。
2. **mooman 麦先买层（窗口内，见 §一.1）**：同回合 BUY WHEAT 13+30→SELL WHEAT 30 的 wash=买侧预置支撑卖腿——与"预卖窗口"同族异向；与公开 B1"投机性开盘陷阱（开盘小麦往返灾难性滑点）"直接对冲（证据张力，两家反向）。镜像 30 战 13→19（自报）。
3. **卖时窗公开链索引**：5thDimension-Sean/kaggriculture-master（https://github.com/5thDimension-Sean/kaggriculture-master ，pushed 09-23=存量）evidence 库含 sunil123kumar「kaggriculture-sale-window」notebook v3 metadata 与 dmitriigluzdov herd-safe-sale-window 提取件——与我方已录 herd_safe_window 同链，无新版本。DDG "MODELPX kaggriculture" **0 命中**（该词公开面仅 tetsutani 原栈与 Wangyh666 移植件）。
4. code search 顺带捞出的非同名仓（均 09-28 前 push=存量）：Kinjuriu/washamba_bots（route_moon_md*.py "sell window" 匹配）、seshurajup/myclew（best_of_all_blueprint.md）、straf10/Kaggriculture（s9_live_read 分析）、Tamizharuvi2006/Kaggriculture（apex_next/ml_engine README_ML_PLAN）、binhtran23/sidequest_1（kaggriculture-most-powerful-route 切片）。

## 五、候选改善项（证据等级+禁区标注）

1. **MODELPX 同型外证包**（Wangyh666：双种子 800 局 +10.1pp、栈内 −26pp 最大单层、M9 家族反转"模型化抢先卖≠已否证的 RACE 抢跑"）→ 我方在飞 MODELPX 焦窗件的**方向外证**（证据 B：自报+可核方法学）；我方件为自主实现，禁区7 不触；其生效域参数（144-696×h12-22、MILK/STRAW/WOOL、跌$0.5 门、半量前置）**只作对照不移植**（抄参数=禁区7）。
2. **_DP/_MP 依赖链移植陷阱（M13）** → 若我方焦窗含"现价 vs 近期均价"类比较，需自查其历史状态依赖是否闭合；证据 B。
3. **mooman wash 开局（R42）vs 公开 B1 投机性开盘陷阱** → 证据张力记录（两家反向）；不移植（近禁区3/7）。
4. **graceyunliu 参数消融表**（CROP_SWEEP/MELON_MORNING/wheat_hold_days 等）+ **pranav-bot live_top10 回放集**（episode-114833391 等）→ A1 画像/C7 数据燃料，证据 A（文件可取）；Meta-CFR/学习式=禁区9 不采。
5. yen-ghub final_day_melon_bank（熟即入账）等收尾微操 → 家族证据，禁区7 已关，仅记录。
6. mooman E092/E093 **破冻结**信号（镜像 13→19）→ 截止前各家仍在加层，我方"收官稳态"假设需保持警惕；仅态势记录。

## 六、限制与未复核清单

① 强度数字全部自报（Wangyh666 +10.1pp/mooman 13→19/graceyunliu +15k 均未我方复核）；② Wangyh666 仓 pushed 09-27=存量新发现（补录性质，非窗口增量），但其 v40_modelpx.md 为 mpx 面唯一同型公开全案；③ **code search 本轮首用**（基线盲区）：按名检索会漏非同名仓，本轮捞出 6 件均存量，但不能排除仍有漏；④ hustleailab 403、kariyerpusulan/lovable 无日期标注、X/nitter 反爬不可用；⑤ Manav 23MB notebook 与 graceyunliu evolve 海量跑批表未逐行核；⑥ 389 仓净 +1 与新收 1 件吻合（本轮无消失件）；⑦ e091 跳号原因未获证（可能只提交未推送）。
