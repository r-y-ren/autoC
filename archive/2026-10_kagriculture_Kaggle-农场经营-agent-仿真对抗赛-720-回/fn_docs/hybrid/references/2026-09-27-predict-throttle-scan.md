# 2026-09-27 PREDICT 限频/收着打联网调研（analysis23 调研轮）

> 任务：为 PREDICT 修复（首版 NEGATIVE：预测写入 9975 步/避让 3329 次、现役件每局亏 ~14.7 万）找"对手成交预判该怎么收着打"的公开技术口径。
> 抓取日期统一 **2026-09-27**（V52/Shepherd's/2965+ 三件为 09-25 已缓存源码，本轮就地解码审计，标 [09-25 缓存]）。
> 通道：kaggle CLI 2.2.4（kernels list/pull、competitions topics list/show）+ 本地解码（zlib/base85、gzip/base64 载荷，只读不执行）+ WebFetch（Kaggle SPA 不渲染，弃用；browser-use 在子代理不可用）。缓存 `/tmp/predict_scan_web/`、`/tmp/predict_scan_*_main.py`（临时未入库）。
> 纪律：逐条带来源 URL+抓取日期；他人实验数字均标"自报"；查不到写"未找到公开来源"。

---

## 一、动作限频/置信门（Q1）——公开件的具体数字

**1. Tschinkel PREDICT 原版（Metav4 v13 = 2945 v9/4 谱系；V52 与 Shepherd's Ledger 内嵌同一块，常数一致）**（https://www.kaggle.com/code/thomastschinkel/the-metav4-farm-submission-v13 + https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v52-lean-flock-yarn-route ，[09-25 缓存]/09-27 解码）：
- 触发窗 **step 150–699**（719 步局外不动）；预测重算每 3 步（`_V92_P_EVERY=3`，Shepherd's v2 版=2）。
- 观测噪声门：反推对手成交时 **价格 ≤$3 不记、推算 sold<2 不记**（`_v92_p_update`）。
- 匹配：同"首二店对"流库、近 240 回合、±1 tick 容差、score=m−0.5·f−0.5·miss，**只取 TOP=1 条流**。
- 开火票数：TOP 流在 (step+1)+(step+2) 两回合对该品 **≥4 单位**（`_V92_P_K=4`）才动；只对 MILK/WOOL/STRAWBERRY 开火（观察 5 品，EGG/MELON 不动）。
- **量级上限 qty = min(棚存, 我方未来 48 回合计划卖量)**（`_V92_P_H=48`，单笔再 cap 100）——抢跑量 ≤ 自家计划量。
- 每步每品最多 1 单（已有同品单跳过）、插队首槽、总单数 ≤10；机箱层 `min_sell_price=2`（低于 $2 不卖）。
- 机箱 `front_run` 钩子（对手计划版）：qty=min(棚存, 对手单量, **我方次步计划卖量**)，并把次步自家同品 SELL **等量抑制**（`_apply_suppression`，注释自述 "never dumps"）——前拉自我中和，不净加卖。

**2. Kaggricult-Man T4 Bounded 1-2 Turn Mirror Preemption with Credit Ledger**（Shepherd's Ledger v3 集成，https://www.kaggle.com/code/haideptry/the-shepherds-ledger-herd-safe-sovereign ，[09-25 缓存]/09-27 解码）：
- 窗口 **336≤step<647**；仅 MILK/WOOL/STRAWBERRY；市场已有单 <10 才动。
- **数量带通门：4≤qty<100 才抢跑**（小单 <4、大单 ≥100 都放弃）。
- lead=1 回合；仅检测到对手也在抢跑才升 lead=2（`_HS4_T4_OPP_PREEMPT`；冻结版未接检测器，恒 1——属设计意图非活代码）。
- **Credit Ledger**：抢跑记 credit，后续自家计划卖单等额扣减——总卖量恒等于 tape 计划。

**3. Gluzdov "More Wheat, Smarter Sales"（自报）**（https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales ，09-27）：对手流匹配保留 **≤3 条轨迹**（与最强轨迹分差 ≤1 且最强分 ≥0），弱匹配回退单轨迹；任一保留轨迹预测奶/毛/莓未来 2 回合"实质"卖单才前拉；按实际棚存校验 + 10 单上限。自认："forecast 错时会卖太早，放弃后续价格恢复"。

**4. Shepherd's Ledger 置信门 `_hp_quantity`（Apache-2.0）**（同 2 仓库，09-27 解码）：近端 (1,2) 回合 ≥4 单位直接动；远端（1..4 回合合计 ≥4）须历史置信：近 240 回合该品事件（q≥2）命中 ±1 tick **≥3 次且命中率 ≥70%** 才采纳，否则拒绝（telemetry 分记 extension_signals/rejected_signals）。

**5. EXP283 clone-gated 预留（2965+ 内，Ahmed V43 谱系）**（https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine ，[09-25 缓存]/09-27 解码）：基础 reservation horizon=8；仅当判定对手克隆我方 tape（6 步历史 ≥4 步同位 + r37 similarity≥0.95）才启用；再观测到"被抢先"（对手在我持有未卖时于 drop 回合卖同品、且 tape 5 回合内无自家卖、24 回合内有）才升 24；镜像门（step1 双方现金差 <$0.5）直接 24。窗口 216–695。

**6. RACE 预留深度有上限且做过深度实验（自报）**（Tschinkel v13 注释，09-27）：horizon=clamp(观测最大对手领先+12, 40, 48)，起始 step 192；40/12 对 32/12 赢 74-6 (+358)；**48/12（恒 48）反输 14-26**——"超过对手下一批货的预留深度，白白让出城镇需求回补"。

## 二、只攻不防 vs 攻防兼备（Q2）

1. **公开 PREDICT 件全部是"前拉自家计划卖单"（提前 1–2 回合，最多预留 40–48 回合），无一例"推迟自家卖单避让"**：Tschinkel PREDICT（09-27）、T4 Preemption（09-27）、Gluzdov ≤3 轨迹（09-27）、Two Coins "bring forward sales…**It is not a prediction of the opponent's next move**"（https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2600 ，09-27）。
2. **避让/持货的公开先例是负结果**：Tschinkel v13 "What did not work" 表：**"Holding premium goods for peak price" −$1.2k～−$3.2k/局**（自报）——扣住莓/毛等高价品 → "对手先卖、价格砸到 $1 我才卖"（09-27）。
3. 攻防兼备以"门"实现而非推迟：RACEPX/RACEGATE（报价 ≤base 的品不前拉、留给 tape 原节奏）、`min_sell_price=2`、protected sale windows（货到棚才卖，Shepherd's 自述）、Two Coins"前 12 天 setup 阶段绝不前拉"（09-27）。
4. 讨论帖 743231 #5（https://www.kaggle.com/competitions/kaggriculture/discussion/743231 ，09-27）：镜像局胜负全在 **d17–25 卖侧时机**，双方同砸时毛价 226→31→1；"fork 公开 tape 的人，对同胞的 edge 几乎全在市场层，改动要专门对同胞测"。

## 三、预测精度/校准（Q3，prvsiyan $1 地板）

1. **prvsiyan floor-aware ledger（https://www.kaggle.com/code/prvsiyan/kaggriculture-floor-aware-market-ledger-20260923 ，09-27）**：恒等式 D=J−I+C=A+B；对手量**下界 max(0, D−S)**。精确判据：还原税前库存 **M=J+C，price(M)>1 则对手量精确 = D−S**（只看下一报价会被城镇回补骗到）；更紧下界 max(0, D−U)，U=我方高于 $1 的成交单位数；**地板截断后无有限上界**——按"删失证据"保留，禁止当精确值或填 0。own 快照必须取全部改单后的最终动作（否则全记到对手头上，stale-snapshot trap）。
2. 公开校准口径集中于**观测过滤**而非模型复杂化：价格 ≤$3/sold<2 过滤 + ±1 tick 容差 + 240 回合窗 TOP-1（Tschinkel/V52）；Gluzdov"多假设只在强匹配时展开（≤3 条、分差≤1、最强分≥0），弱匹配回退单轨迹"（09-27）。
3. 置信门分层：近端 ≥4 单位直接动、远端要 70% 历史命中率（≥3 样本）——"预测越远、门槛越高"（Shepherd's，09-27）。
4. **库时效性**：v13 用 09-19 新录 1200 局 top-30 流库（222k 事件）重建才拿到自报 +46/−7 (+558)；并明文教训 "Replay panel staleness"——头部 d12–18 弃 tape 转 adaptive planner 后旧库失真（09-27）。
5. **"预测只用于量级而非时点"：未找到公开实现**——公开件全走"时点抢跑 1–2 回合"，量级被 min(棚存, 自家计划量) 封死。

## 四、失败案例/教训（Q4）

1. Tschinkel v13 负结果表（09-27）：持货等峰值 −$1.2k～−$3.2k；预留深度 48/12 对 40/12 **14-26 大败**（过深让出城镇回补）；过度限制类（CARROT2 边际 +20/+50）−$148～−$258。
2. RACEPX 实测病灶（自报，09-27）：被自家砸穿的品低于 base 成交（莓 $107–123 vs base 120、奶 $98–107 vs 160、毛 $129–139 vs 200、瓜 $212 vs 250）——与我方"动作频率过高摧毁现金流"同款；修法=报价 gate（>base 才前拉），修后 35-13 (+220)。
3. **prvsiyan 政策实验（560 局，自报，09-27）**：把账本修对反而让预测控制器更差（56/0/24 vs 对照 64/0/16，均值 −236）——"输入正确 ≠ 下游目标正确"，预测链（账本→匹配→时点→订单）对输入极敏感。
4. 讨论帖 743231 #6（09-27）：把 d27 起整仓 SELL 1000 拆成逐回合均匀卖 → 自家分掉 ~1000、对 V53 差距 −4.9k→−6.2k——**晚季一把出清优于细水长流**；限频修复不要滑向尾盘慢卖。
5. 743231 #1/#2（09-27）：3 seeds=噪声（≥6 seeds、以 seed 为证据单位）；对现任冠军 head-to-head 是陷阱（非传递：v7 赢 hybrid 12/12 却输 V53 0/12、输 2945/herd-safe 0/6）；要用谱系加权 gauntlet + "walls"（按谱系最弱件判）。
6. bardiabahadori（https://www.kaggle.com/code/bardiabahadori/kaggriculture-agent-selection-engine-traps ，09-27）：城镇抽样需求决定成交价（同产量银行差 6 倍：莓价 236 vs 3）——不以需求为条件的预测=噪声驱动；本地 margin<+$5k≈噪声；另有 4 个本地评估陷阱（last-callable/引擎 1.32.7/配置默认值/模块状态串局）。
7. Gluzdov Two Coins（09-27）："两枚金币赔进一只羊"——卖时微调少 2 金币 → 少买一只羊 → 少 22 毛；抢跑改时机必须过资金序检查（呼应 V57 funding invariance）。
8. haideptry "Countering the Big 3"（https://www.kaggle.com/code/haideptry/countering-the-big-3-meta ，09-27）：克隆同调度"公地悲剧"——毛价 $380 砸到 $120 地板，**第二个卖的人惨亏**。

## 五、对手对 r37 型守卫件的反应（Q5）

1. **公开已有专门反制"早养畜+现金守卫"型的件**：haideptry "Countering the Big 3 Meta"（09-27）的 **WOOL FRONT-RUNNER**——用同一 rival_sold 反推公式嗅探对手 d11 羊群提交，提前 1–2 回合（RACE 最深 40 回合）倒毛，"把克隆逼到地板价出货"；Anti-Shock 层吸收 step-1 22 麦冲击（抑制恐慌买入、保现金买牲）；Tomato/Melon Pivot 转攻无人竞争账本。
2. 防反制先例也在公开件里：EXP288/283 镜像/克隆检测（step1 现金差 <$0.5 → 深度 24"对拷贝要抢完整一天"）；V52 的"+2 倍镇消费扣减"反推对 Yarn(wool×2) 店已有校正。
3. 结论：我方 PREDICT 修复应预置防反制——卖窗错开公开 tape 的固定毛周期（d17/20/23/26/29），不参与麦价对撞（step-1 大单不跟），检测到对手同 tape 克隆时才升深度（否则保持浅）。

## 六、修复方向技术参数建议（★=公开件自报值；☆=推断值/建议）

| # | 参数 | 建议值 | 来源 |
|---|---|---|---|
| 1 | 触发窗 | ★150–699；修复期建议先收窄 336–646 | Tschinkel PREDICT / T4 |
| 2 | 开火门槛 | ★近 2 回合对手预测 ≥4 单位；远端 1–4 回合需历史命中 ≥3 次且 ≥70%（240 回合窗） | V52 `K=4` / Shepherd's 置信门 |
| 3 | 匹配假设数 | ★TOP=1；强匹配（分差≤1、最强分≥0）才展开 ≤3 条 | V52 / Gluzdov |
| 4 | 频率上限 | ★每步每品 1 单；☆每局每品抢跑 ≤6–8 次（对应 48 回合窗单次前拉） | V52；推断 |
| 5 | 量级上限 | ★min(棚存, 未来 48 回合自家计划卖量)；★带通 4≤qty<100 | V52 / T4 |
| 6 | 价格门 | ★min_sell_price=2；★报价 ≤base 不前拉（奶160/毛200/莓120/瓜250/蛋50/番茄60/萝卜35） | V52 / RACEPX base 表 |
| 7 | 自我中和 | ★前拉必配 credit/suppression，后续自家卖单等额减（禁止净加卖——对照我方 9975 步写入） | V52 suppression / T4 ledger |
| 8 | 避让（推迟卖单） | ★不做（负结果 −$1.2k～−$3.2k）；防御走门：低于 base 不抢、货到棚才卖、step<288 不前拉 | Tschinkel 负结果表 / Two Coins |
| 9 | 对手分类 | ★克隆/镜像才升深度（step1 现金差<$0.5；同位 4/6 步+similarity≥0.95）；horizon 8→24 | EXP283/288 |
| 10 | 评估判据 | ★≥6 seeds、seed 为单位、谱系加权 gauntlet+walls、对镜像同胞专测；☆预期信号：预测 fire 数/局降一个量级 + 现役件每局亏损从 −14.7 万收敛 ±0 | 743231；推断 |
| 11 | 流库维护 | ★按 top-30 新鲜回放重采（v13 09-19 重建才有效；旧库失真） | Tschinkel v13 |

**未找到公开来源**：①"预测只用于量级而非时点"的实现；②置信门的具体 ROC/标定曲线；③"每局最多 N 次抢跑"的显式 N 值（公开件靠窗口+单步单品间接限频，表中 N 为推断）。
