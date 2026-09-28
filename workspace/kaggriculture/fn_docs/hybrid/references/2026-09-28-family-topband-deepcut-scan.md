# 2026-09-28 同门头部五强深挖×全网增量（分析30 调研轮）——来源与机制册

> 任务：对"同策略高分同门"中最优秀的五强（Georgy Mamarin 2345 / tetsutani 2307 / haodou092 2216 / Lynxx 2211 / Alperen 2188）做函数/常数级深挖，并扫 Kaggle 外渠道新代码/资料。
> 抓取日期统一 **2026-09-28**（17:00-17:50 轮）。通道：kaggle CLI 2.2.4（kernels pull / datasets download / legacy API versionNumber）+ base85 解包 + 本地重算 + GitHub/HF/GitLab/gist/视频站直查。
> 纪律：逐条带来源 URL；自报数字标"自报"；我方重算标"重算"；查不到写"未找到"。临时解包件在 /tmp/a30-b1/、/tmp/a30-b2/、/tmp/a30-c/（未入仓）。

---

## 一、五强公开件获取状态

| 选手（榜位/分） | 件 | 获取状态 | 关键事实 |
|---|---|---|---|
| Georgy Mamarin（#404/2345.4） | georgymarin/kaggriculture-what-2600-farms-do-differently + /kaggriculture-visualized-what-every-crop-pays + 数据集 georgymarin/kaggriculture-episodes | 源码经 fn28_cache 09-28 12:12 缓存（与 09-25 版 diff=0）；**17:08 起 kernels pull 403（作者疑似关闭下载）**；数据集 09-28 00:25 版已下载重算 | 研究件=live 数据仪表盘（245,890 局）；提交件私有 |
| tetsu2131/tetsutani（#484/2307.3） | tetsutani/demand-preserving-turn-sale-timing（09-27 02:50 run）+ adaptive-farming/shape-the-shop/market-smart 三辅件 | **全量到手；内嵌 base85 归档解包=promoted 生产 main.py 全文 10,137 行（SHA256 55be5d5f… 校验一致）** | 件自称 "exact promoted submission bytes"——同门最高分的可读完整产线 |
| haodou092（#703/2215.6） | haodou092/kaggriculture-harvest-ledger（**现行 V82**；V81=02:23 版） | V82 全量到手；**V81 一手源码未获取**（版本钉选拉取 403、API versionNumber 400） | **V82 notebook 首格明文："V82 rolls back the unsuccessful V80/V81 sale-horizon experiments to the online-proven V79/V76 production engine"**；08:47:08Z 有新提交入榜（2215.6 收敛中） |
| Lynxx/lynnsakurai（#713/2210.6） | lynnsakurai/farmer-john-and-the-idle-seller（09-27 09:29 run） | 全量到手；**35 段 base85 内嵌 submission_competitive_step1010.tar.gz（main.py 1,148,715B）已解包全读** | "提交件私有"为误判——完整提交就在件内；NOTICE 直系=shiiin9/your-market-list-is-an-order-book（我方 Layer D 同源） |
| Alperen Aydın（#769/2187.5） | alperen5252525 **5 件**：turn-one（09-15）/metacounter（09-13）/ready-stock（09-17）/first-in-line（09-18）/market-rhythm（09-19） | 全量到手（此前记 3 件有误） | 三主件内嵌完整 evaluation_evidence.json（12 holdout 种子簇 paired CI+官方 parity+frozen-rival 败局复盘） |

来源：https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing 、https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-idle-seller 、https://www.kaggle.com/code/haodou092/kaggriculture-harvest-ledger 、https://www.kaggle.com/code/georgymarin/kaggriculture-what-2600-farms-do-differently 、https://www.kaggle.com/code/georgymamarin/kaggriculture-visualized-what-every-crop-pays 、https://www.kaggle.com/datasets/georgymamarin/kaggriculture-episodes 、https://www.kaggle.com/code/alperen5252525/kaggriculture-first-in-line-stock-into-income 、/kaggriculture-market-rhythm-sale-policy 、/kaggriculture-ready-stock-earlier-sales 、/turn-one-market-advantage-kaggriculture 、/kaggriculture-metacounter-r1-scored-agent （均 2026-09-28 pull）。

---

## 二、Georgy Mamarin 机制/数字（重算=我方按其代码在 09-28 00:25 数据集版上执行）

1. **九项行为中位数 top=mid 全同**（窗口 4 天：top 2500+ band=239 座/115 队，mid p45-55=1,538 座/587 队）：first land day 6=6、peak crew 12=12、hires 268=268、plantings 239=239、carrot 40=40、melon 12=12、strawberry 33=33、tomato 0=0、wheat 154=154；**final bank 99,616 vs 95,862（+4%）**。结论句（cell 1）："top plays the middle's game and banks +4%"。取样偏差自述："fetcher pulls top-rated ones first——缺口是线索不是结论"。
2. 我方画像同形（重算）：tiles 239、straw 33、melon 12、crew 11、hires 267、carrot 51/wheat 143；我方 bank 中位 88,167 vs top 99,616（**−11.5%**）vs mid 95,862。
3. 价格区间（220,176 局重算，倍数 vs base）：strawberry/milk/wool/fertilizer 的 lo_med=**0.01（半数局触 $1 地板）**；hi_med 1.78/1.30/1.09/1.00；wheat 0.88-1.80；tomato 1.00-1.50（hi_p90 4.12）。
4. 引擎常数（crop-pays 件自算）：**melon 净卖 158 件即到 $1 地板**；wheat 卖 400 件几乎不动；稀缺 hinge：carrot 短缺 1000 件付 **$531=15×base**、tomato **54×base**（knee T=200 vs carrot 450）；一整仓 100 melon 一次性抛实收 <首价梦想 90%。
5. 平衡补丁（engine 1.32.7，2026-08-15 合入）测量：carrot 峰值中位 42→**56（×1.33 唯一大涨）**、tomato 天花板 $152→**>$1,800** 但采用率仍个位数；top 座位补丁落地前一天（08-14）就加种 carrot（引擎 PR 公开领先）。
6. 城镇需求：**约 1/3 赛季一个 wool 买家都没有**（无 Yarn 店）；carrot 典型季 ~270 店铺需求，双 Pet Cafe 开局 ~800、倒霉开局 <150（五倍摆幅 day6 定"world"）。
7. 两条推论原文："When you sell moves more money than how much you grow"；"spread your sales into trickles…price slides while you sell"（**注意：trickle=拆单族，与我方 R26 跨拍拆单毒张力，见分析30 §三**）。
8. 其他（cell 31/34 重算）：单 bot 多局银行离散 cv 中位 26%；双银行同世界相关 +0.73（对局内 margin 才是干净尺）；09 月中旬以来中位胜局 ~96-100k 停涨。

## 三、tetsutani 机制清单（file:line=解包 main.py 10,137 行；强度数字均自报）

| 机制 | 定义 | 自报证据 |
|---|---|---|
| RACE 预留视界（L3728-3886） | `horizon=clamp(max对手lead+12, 40, 48)`；窗 step192 起；GAP=3；对手卖量=库存差分−town_draw 修正 | 40/12 镜像 **73-7(+308)/74-6(+358)**；44/12 赢但对浅基线 65-15；**48/12 掉到 14-26**（视界过深反噬） |
| **RACEPX 抛售门（L3886-3966）** | 提前卖仅当 `quote≥base+0`；glut 品留给磁带+城镇排水；禁 unlock 时点/step%4==0 提前 | 实现价表：被自己冲垮的品 strawberry $107-123/base 120、milk $98-107/160、wool $129-139/200、melon $212/250、fertilizer $43/100；被城镇排走的品 wheat $38/25、carrot $54/35、tomato $125/60、egg $52/50 |
| r36_debts 债务账本（L3987-4052/8183-8240） | 每笔拉前卖量在原 due_step 记债、后续拍抵扣——**跨拍提前不双卖的会计核心** | — |
| MODELPX 领卖（L7750-7812） | MILK/STRAWBERRY/WOOL；step144-696；对手流=公开库存差分滑窗 12 取近 4；`inv_next=inv+rival_avg+planned(6)−town_draw`；**`p_next<p_cur−0.5` 才卖**；帽 3/6/10（quote≥100→10） | 各档"measured"晋升（数字未在注释） |
| step738/809 就绪提前（L7500-7574/8183-8240） | 只提前磁带 4/3 拍内本就要卖的量、货已在仓、保护首个计划单、跳 dawn/BUY_PRODUCT 拍；step809 另需 quote≥50+扣债 | — |
| **step928/948 日内新高变现** | EGG/MILK/WOOL/CARROT/TOMATO/STRAWBERRY/MELON 当日报价**严格创新高→立即卖全部可卖量**（price×avail 排序）；step950-953 并入最早同品槽/移到首个花费单前 | — |
| _s793 固定卖单闭包（L7889-7953） | 只动槽位不动量；SELL 限"投影覆盖且同拍不买"；FIXED 单只能后移；ΔΦ>0.5（_v44y lockstep 逐品自己 vs 自己回放收入差）才收；budget 800；41 遍链 | 遥测收敛至不动点 |
| _r37_quote_priority（L1753-1827） | 排序键=对手小批将砸掉的暴露收入（在田 yield→batch clamp(8,24)→曲线价差）；只排连续 SELL 块内不同品 | — |
| CT_TABLE 身份反击（L4086-4109） | step2 (money, 市场 WHEAT) 识别 2 支具名紧现金磁带并搭车；"checked unique over 4,604 games" | 与其 market-smart 件"No opponent identity table"声明**矛盾** |

私有件画像（重算，团队 16636536）：近 7 天 crew 11、tiles 239、carrot 48/wheat 146、胜率 61%（98/160）、margin 中位 +556、rating 最高 2919。推断：私有提交≈Step1008/1009 产线本体（推断）。

## 四、haodou092 V82 / lynnsakurai / alperen 机制要点（file:line=各解包 decoded_main.py）

**haodou V82（=V79/V76 生产引擎+PET 门）**：Chassis 13 路线磁带（406-986）；`_R37_MARKET_PARAMS` 引擎价格全表含 WOOL sq×3.2 平方崩塌（1753-1783）；`_v44y_lockstep` 锁步评分器（6044-6119）；`_r36_reserve+r36_debts` 债务账本（1678-1731/3987-4050）；RACE 自适应视界 clamp(max lead+12,40,48)（3729-3866）；EXP283 克隆→视界 8、EXP293 输 race→24、**EXP288 step1 现金差<0.5→视界 24（只调视界不加卖）**（5770-5870）；MODELPX（7753-7806）；日新高变现 step928/948（8728-8985）；step752 同侧合并（7716-7748）；E182 终局 712-718 物理规划器（64 模拟+支配前缀）+step718 按 −price×qty 清算（8341-8386）；CS 换种记账 credit（5680-5750）；CTRTABLE 指名反制（4077-4108）；44 遍闭包链（7895-7935）。**V82 增量=d10-23 且 PET_CAFE 已解锁时 `_CA_MARGIN −15→−22`（用后即还原）**。

**镜像门口径辨析（核心）**：V81 Spatial Mirror Gate（逐坐标指纹相等→卖窗 4→7 拍，自报 +38.2 中位 0）vs 我方已判死"镜像提前卖"（−80k）——触发生态更窄、幅度更小、有 debts 记账；**但作者 24h 内在线判其 unsuccessful 并回滚**，在线结论与我方负结果收敛一致。该家族在线存活的只有"视界调制"（EXP288/293）。

**lynnsakurai step1010**：把 41 遍闭包链压缩为一次不动点调用（≤48 趟，环检测后按 41 相位快进 `_S1010_REFERENCE_PASSES=41`）；语义等价自报。谱系 NOTICE：shiiin9 Layer D → ahmed V55/56 → Tschinkel → yhay81 → Gluzdov 七拍救援 → Herd-Safe。

**alperen**：`_ADV_LOOK` 演进 3→6（ready-stock）→8（first-in-line，自报 paired +540.6 [406.5,673.5]）→**24（market-rhythm）**；`_adv_apply` 把未来 k 拍内磁带计划 SELL 中已入仓部分拉到队首、保护首个计划单、同拍有 BUY_PRODUCT 整层弃权；**`_ADV_BOOK=False`（不记账不扣减——与 haodou 相反）**；QR 队列搜索（3 想象队列×两趟相邻交换）**自报 CI 过零 +20.8 [−19.0,+62.7]**；C9 条件开局（非 BAKERY 路线砍麦对倒+step1 批量雇工买畜，自报 75%→96%）；`_e334/_e335` 同侧合并+`[]` 保索引空槽；内嵌 evaluation_evidence.json=12 种子簇 paired CI+frozen-rival 败局复盘+official parity+候选消融表+source_inventory sha256。

## 五、三家共性缺件 vs 我方（分析30 §三依据）

三家全有、我方全无或严重薄：①执行期市场单手术层；②agent 内置引擎价格模型（`_R37_MARKET_PARAMS` 全表进决策环）；③债务/抵扣账本（提前卖必配到期抵扣=净零）；④终局 712-718 物理清算+−price×qty 收尾；⑤克隆/镜像检测只调参不加卖；⑥种子簇 paired CI+frozen 败局复盘+official parity 评测纪律。我方完全缺的模块：日新高变现簇、MODELPX、债务账本式提前、lockstep 评分器、712-718 物理规划器、自适应预留视界。

---

## 六、Kaggle 外渠道全网增量（GitHub 387 仓库 triage + 深读 10 件）

**今日（09-28）新推送 5 件**：

| 来源 URL | 更新 | 内容 | 相关面 |
|---|---|---|---|
| https://github.com/mooman0222/Kaggriculture-opencode | 09-28 02:37 | 日文战役仓库：e058/e060/e085/e086/e087 五套完整提交件开源（~10.2k 行）+"GitHub 公开件收割调查"文档 | 同族（ahmed v41 衍生）；**调查文档=本轮最高价值单件** |
| https://github.com/wmar-dev/kaggriculture | 09-28 04:01 | 实验日志式 repo（v10-v19，replay 诊断/否证记录/真实 Kaggle 分登记） | 方法论对照 |
| https://github.com/alvaromendizabal/kaggriculture | 09-28 07:19 | frontier ceiling-escape / meta refresh 研究检查点 | 对手 tape 对标体系 |
| https://github.com/graceyunliu/kaggriculture | 09-28 | "frontier refresh: new opponent tapes (09-24/09-27)" | 对手回放收集方法 |
| https://github.com/alpertaskiran/kaggriculture | 09-28 07:40 | "Expand physical routes and RL market policy" | 同族混合架构 |

**重点深读两条**：
1. **mooman0222 GitHub 收割调查**（https://raw.githubusercontent.com/mooman0222/Kaggriculture-opencode/main/.opencode/knowledge/refs/github-2026-09-27.md ，09-27）：387 仓库 triage+12+ 公开 agent 对战表（自报）——`r34l_v7`（Rudra，实时 2445）6W18L 是其唯一负手；haodou_ledger_v68 16W8L；doan v5/v6/v7 鹅引擎 **+112k~+144k**；aurax7_v5 24W0L；multiroute_v70（flexonafft 复原克隆）24W0L+35,854；ca25（statma）22W2L。**顶层名录**：UMG/Majkel/4th/DECEM/SpaTaro/kuro（源码未公开）+ Rudra/r34l、prvsiyan、farm2945、flexonafft、statma、doan 系。机理线索：`BerryBook` 按**星期几需求预测**定种植节奏（移植需农场外科）；doan README"入口=最终 callable 不一定是 agent"；其 09-27 后分降判定为"对手群体换血"非自身退化。
2. **frapercan/kagsym**（https://github.com/frapercan/kagsym ，09-25）：唯一公开点名 v48 的对手件——**天梯按胜率（Bradley-Terry）拟合，"对最强公开 agent 多赚 25% 的钱只换 2 个点的胜率"**；自报对 v48：我方赚 115-135k vs 他们 ~51k。方法：引擎克隆合法性（38k 步/s）+匈牙利指派+CEM（弃 PPO 三否证）；测量卫生：seed 族互斥、ledger.jsonl、最终 callable 逐美元对照、**torch 线程敏感 bug（同 seed 12 线程 $42,242 vs 1 线程 $48,387）**、钉死 kaggle-environments==1.32.7。

**次重点常数**：amerob/kaggriculture（08-13）价式 `price(inv)=base+sign·amp·f(|inv−I0|)` 精确复现 9 行价表+全季 town 排水 WHEAT 525→MELON 30；conchocon154（09-10）市场深度表（melon 全季 ~26.7k 封顶、"不对冲甜瓜"镜像 10-0、**16 手 32,800 vs 10 手 55,200=少而大再证**）；destbreso/kaggriculture-cppsim（09-14）bit-exact C++ 引擎（源头 nikital7 kernel 4000x-environment-speedup-kaggriculture）；Ashee-Softworks（09-24）starter 行为定位+常数；sweeden-ttu/kaggriculture_1_37_muzero（09-27）空间采样 MuZero；diffmap/kaggicultureRL（08-20）回放模仿→PPO 三段课程。

**旧新发现 20+ 仓库**（skim 级）：Applied-Agent-Works、OpenKaggle/kaggriculture-research、rooklift/krobus（回放查看器）、lopeznomar/ops-lab、emanuellcs、akmalkhaniub/mcts、pomagrenate/MPC、rafifariqrabbani25、prabhuken01、VynoDePal、Rohanjain2312、mayur-samrutwar、mohui666、iZackk26（240 组实验 99 发现）等。**资料**：HF 数据集 ThanThoai9x/kaggriculture-rsp-decisions（743,899 行决策 Parquet，残差策略范式）；YouTube 5 条（模仿训练/一致性套件/入门向）；gist Sunwood-ai-labs 对手-市场关系图。**博客/论文/论坛：未找到**（arXiv/HN/dev.to/zenn/Qiita/掘金 0 命中；Google/Bing/DDG 反爬不可用，以 GitHub/HF/GitLab/gist/视频站直查兜底）。

**跨频道线索（回灌基线核对）**：nikital7/4000x-environment-speedup-kaggriculture（Kaggle kernel，cppsim 源头）；Nikita Lugovoy（提交 55440039，amerob 复刻来源）。

---

## 七、限制与未复核清单

① 五强私有提交本体均未公开（tetsutani/lynnsakurai 解包件为 promoted/内嵌产线，"即其提交"属推断）；② tetsutani/haodou/alperen 全部强度数字自报、无分层消融；③ Georgy ipynb 无运行期输出，§二数字全部为我方重算（取样偏差与原作一致）；④ haodou V81 一手源码未获取；⑤ V82 PET 门（本地自报 +49.56）与 haideptry −22 无门版在线 −443 Elo 的矛盾未裁决；⑥ mooman/frapercan 对战数字自报未经我方复核（注意其"最终 callable+线程敏感"复核条件）。
