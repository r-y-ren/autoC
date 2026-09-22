# 开源 bot 猎获 digest —— GitHub 仓库专项（2026-09-20）

抓取方式：GitHub REST API 全站检索（repo 名/描述，`total_count=361`，较 09-19 快照的 359 **+2**）+ 定向 README/raw 源码逐文件实抓（本 digest 所有引文均为 2026-09-20 当日原文摘录）。**范围说明：** Kaggle 讨论区/notebook 的"09-19 后新增"扫描由另一路 agent 负责，本文不含；但 GitHub 仓库指向的 Kaggle notebook 线索在 §6 登记移交。发现时间统一为 **2026-09-20**。

一句话结论：**GitHub 上没有自称 2600+/top100 的可抄现成 bot；但找到了三件比分数更值钱的工件**——① island-ga（MIT）：可运行的"自有开局剧本"离线搜索全管线，其 envelope 基因组就是顶部天梯开局先验；② kaggri（Apache-2.0 移植层）：公开 notebook 王者家族（thomastschinkel/yhay81 系）被逐行解剖，**开局一行改动（`_R42_OPENING`）= 192 局 64:0 全胜、场均 +2.5 万金币**——直接命中我方"开局点火竞速"痛点；③ cppsim（Apache-2.0）：1.32.7 位精确 C++ 引擎，2 万局/秒，离线搜索吞吐上一个量级的现成基座。

---

## 1. 仓库总量与显著仓库总表

全站检索 `kaggriculture`（+ 变体拼写 `kagriculture`/`kaggiculture` 共 21 仓）按星数序，含 agent 实现且值得记录的：

| 仓库 | ★ | 语言 | license | 最近 push | 自称强度（原文口径） | 定性 |
|---|---|---|---|---|---|---|
| diffmap/kaggicultureRL | 4 | Python | **MIT** | 08-20 | "Open-source policy system"（无 LB 分数） | RL 三模式（单座/双座自博弈/回放模仿）+Rust 批量引擎；09-19 已登记，本次无更新 |
| rooklift/krobus | 3 | JS | 无 | 08-15 | — | 回放查看器（非 agent），工具类 |
| destbreso/kaggriculture-cppsim | 3 | C++ | **Apache-2.0** | 09-14 | "bit-exact @1.32.7, 4139 eps/s 单线程" | 位精确模拟器，见 §2B |
| destbreso/kaggriculture-island-ga | 0 | Python | **MIT** | 08-25 | "Quote the confirm mean"（分数不公开，§8 声明） | **开局剧本离线搜索管线，本次最大发现，见 §2A** |
| gytdrop/KaggricultureAgent | 2 | Python | 无 | 08-12 | "~116k local mean (8 seeds×2 seats)" | 72 顶级回放挖出的启发式，见 §2D |
| CDrookieDc/kaggriculture | 1 | Python | 无 | 08-21 | "31k-34k vs starter(3.4k)" | 鹅核心规则引擎，见 §2E |
| qhapaq-49/kaggri | 0 | Rust/Py | **Apache-2.0**（移植层） | **09-19** | "03 > 01 > 02"（用户观测，未独立验证） | **公开 notebook 王者家族解剖+Rust 化，见 §2C** |
| asajjadi/kaggriculture | 0 | Python | 无 | 08-05 | "100% win rate"（对 starter/random/pass 本地） | 单文件 stdlib 贪心，见 §2F |
| akmalkhaniub/kaggriculture-mcts-agent | 0 | Python | 无 | **09-19** | "Prototype, 7 pytest pass" | **跑在虚构环境上**，见 §2G |
| bravefe/Kaggriculture | 2 | Notebook | 无 | 09-08 | — | 官方教程+动作格式汇编（团队练习仓） |
| Alloysj/Kaggriculture-agents | 1 | Python | 无 | **09-17** | v3 "~17.8k vs starter"（README 只写到 v3，仓库已有 v10） | v1→v10 演化史；v10 无文档 |
| pomagrenate/kaggriculture | 0 | Python | 无 | 08-24 | — | Receding-horizon 控制器 + 引擎文档拷贝 |
| deepeshumrao/kaggriculture-agent | 0 | Python | MIT | 07-11 | vibe coding capstone | 教学向，无天梯证据 |
| COK-ZhangZiliang/Kaggriculture | 0 | Python | Apache-2.0 | 08-28 | "Deterministic baseline agent" | 其 terminal-liquidation 思想被 gytdrop 采纳实证（§2D） |

自称 2600+/2900/top100 的仓库：**GitHub 检索为 0**（`kaggriculture 2600/2900/top 100` 均 total_count=0，2026-09-20 实测）。已知 2900 自称（salemali7）只在 Kaggle notebook 侧，09-19 digest 已登记。

---

## 2A. destbreso/kaggriculture-island-ga（MIT）—— 最大发现：自有开局剧本的离线搜索全管线

来源：README + genome.py/compiler.py/executor.py/engine_facts.py 原文实抓
（https://github.com/destbreso/kaggriculture-island-ga ，pushed 2026-08-25）+ 配套 notebook《Island GA | An owned schedule is a moat》（https://www.kaggle.com/code/destbreso/island-ga-an-owned-schedule-is-a-moat ，原件已拉取存档 `references/data/intel-notebooks/island-ga-moat-0920/`）

**作者核心论点（与我方局面完全同构）**：这个天梯打的是"base schedule + thin adaptive layer"——base 决定下限，自适应层在其上加分，两者投入可分离；"the base is where the cheap points are"。我方开局点火输 3-5 天的问题，就是 base schedule 不够强的问题。

### 基因组（12 个数 + 4 张表，全部有边界）

```
ne:  NE 象限解锁日 (4-8)     sw:  SW 解锁日 (7-12)    se: SE 解锁日 (11-14 或 None)
plateau: 日雇人上限 (8-14)   ramp_full: 到顶天数 (4-12)   tomato_day: 番茄窗口起点 (8-16)
melon2: 甜瓜第二波 0/1       sellpol: daily/sweep/hybrid
herd:  [[day, 动物, n], ...] 波次      prog: 各象限作物分配表
```

### envelope 物种 = 顶部天梯开局先验（"aggregates measured across the top of the ladder"）

作者明示这不是任何人的录像转录，而是**梯顶聚合测量**（NE 窗口/雇人平台期/作物区间）：

- **NE d6 解锁，SW d10，SE 不开**；plateau=12 手，ramp=8 天；tomato_day=8；melon2=1
- **d0 herd：COW×2 + SHEEP×2**；d6 +COW×2；d8 +SHEEP×1；d10 +COW×1
- 作物：NW{WHEAT8, CARROT3, STRAW4, MELON2}，NE{WHEAT10, CARROT4, STRAW5, MELON6}，SW{WHEAT12, CARROT5, MELON8}
- 按 compiler 逐日展开的 **d0 具体订单**（hour 1 市场槽，≤10 单）：`BUY_SEED WHEAT 9 / CARROT 4 / STRAWBERRY 5 / MELON 3`（首次种植量 = n+1）+ `BUY_ANIMAL COW 2 + SHEEP 2` + `HIRE×2`（ramp 曲线 d0 只雇 2：`min(12, 2+12·d/8, 2+active/5)`）→ d0 即 4 种子+2 牲畜+2 雇工全点火；d≥2 才开始 hour0 卖出；NE 种子 d5 买入、d6 播种；SW d10；甜瓜第二波 d12 买种 d13 播。
- 适应度实测：**envelope $53.7k / intensity $44.3k / random $41.3k / bound-mix $36.3k**（seed 11 vs idle）；同 spec 换 sellpol：daily $39.6k / sweep $42.6k / **hybrid $53.7k** —— 卖出策略基因一项差 14k（"drainage details are worth more than most crop swaps"）。

### 管线五步（compiler 是真算法）

1. tile 落位（牲畜棚近端优先，作物填充余量）→ 2. 播种日展开（wheat/carrot 每 m+1 天循环；melon 1-2 波；ongoing 作物窗口内单次）→ 3. 产量投影（牲畜产量自放置日起计、首收一次性 lumpy 结算）→ 4. 市场通道（**hour 0 卖、hour 1 买+雇、种子严格先于土地**、每回合 ≤10 单溢出顺延）→ 5. **Financing by optimism**：购买按 spec 日子照发、不管现金模型批准与否——"引擎里买不起的订单静默失败且零成本，而漏排的浇水第二次不过夜就死；schedule 排少了致命、排多了免费"。

### Executor（参考件，作者故意做简单）

贪心最近任务 + 固定优先级栈：**URGENT_WATER（连续 1 天未浇）> FEED > HARVEST=WATER > PLANT > BUILD > COLLECT > CARE > DIG**；tile 认领防撞；两阀门：delivery-before-sell（未来 8 回合要卖的货先入棚）、animal ledger（BUY_ANIMAL 按 d+2/+4/+7/+10 阶梯重发，达标即停防双买）。教训原文：水位优先级放错 → "17 plants to ZERO by day 9"。

### 评估纪律（可直接抄的工程件）

CRN（同种子配对比较）screen 3 种子 11/23/47 → **DISJOINT confirm 5 种子** → 报 confirm 不报 screen；arena 双座位朝向 + **Bradley-Terry 拟合**（与官方定榜同模型）；submit 前预检：语法/stdlib-only/seat-1 裁剪观测/最差回合延迟 vs 1s/确定性。**适应度 = 赢率不是钱**：`1000×(0.10×vs-idle-bank + 0.45×Φ(μ/σ) vs 强固定对手 + 0.45×Φ vs 自适应公开对手)`——"比赛记的是胜负符号，最大化期望金额是在优化计分板永远读不到的量"。

### 量化结论（notebook 实测，全部 2026-09-20 实抓）

- 引擎精确松弛上界（relaxed bound）：**$229,450** vs idle；公众共识路线忠实执行仅 **72.8k**（3 种子均值）；week-four top12 真实局 **91.5k 中位**、最好略过 100k；一条 Morita 录像带 **183.5k**。
- **"Walking is the money"**：同一 construction plan，录像逐字重放 147.3k，重写 dispatcher 重执行只有 72.8k（恢复 0.49）——**走位编排值一半**。
- **94% 的座位在 turn 24 前共享同一张开局**；score>950 以上是"scripted continent"，计划偏差中位数 0.2%。
- 最长运行 144 代/8,445 局：screen 49.5k → confirm 36.0k（13.5k winner's curse）——screen 种子太少会被搜出来（learnable quiz）。
- **作者保留两样东西不公开**（notebook §8）：①私有 executor（同基因同种子 reference 执行 27k、他的执行 54k——**2 倍乘数在执行层**）；②搜索返回的 schedule（"fielded schedule is deducible from replays within days, its value is highest exactly while it is fresh"）。**因此仓库内没有"最优基因组成品"可抄——可移植的是全部方法学 + envelope 先验 + MIT 全码。**

## 2B. destbreso/kaggriculture-cppsim（Apache-2.0）—— 1.32.7 位精确 C++ 引擎

来源：README 原文（https://github.com/destbreso/kaggriculture-cppsim ，pushed 2026-09-14）

- **上游署名清楚**：引擎核心是 **nikital7 的位精确 C++ 移植**（Kaggle notebook《4000x Environment Speedup Kaggriculture》，https://www.kaggle.com/code/nikital7/4000x-environment-speedup-kaggriculture ），解决了三件难事：CPython Mersenne Twister 精确复刻（init_by_array 播种、53-bit double、`_randbelow` 拒绝采样）、**Python dict 插入序语义（100 格 shed 上限决定哪些货物死掉）**、slot-index 市场结算。destbreso 补丁到 1.32.7（carrot/tomato/egg 凸 `F_HINGE` 稀缺分支 + carrot 5x 振幅），并用对抗法重验证：1.32.6 旧构建在 traces/ 每一条 1.32.7 trace 上都发散，补丁后 719 步逐钱逐库存一致（含 shed-cap 压力下 85-114k 重局）。
- 吞吐：**4,139 局/秒/核，24,442 局/秒（10 核全开）**，裸 C++ idle 局 111μs（对照真实环境 0.97 局/秒）。`run_many` 批量 GIL 释放。
- 自带 fallback 模式：kagsim 自检失败自动降级真实环境（"degrades to slow instead of to wrong"）+ golden trace CI。
- **对我方意义**：我方 twin.py 已做引擎孪生；若叠加 kagsim/nikital7 路线的位精确快引擎，开局剧本离线搜索（GA/beam）吞吐上量级。Apache-2.0 可直接用码。

## 2C. qhapaq-49/kaggri（Apache-2.0 移植层）—— 公开 notebook 王者家族的解剖报告（09-19 仍活跃）

来源：README + docs/notebook_algorithms.md + assets/notebooks.json + NOTICE 原文（https://github.com/qhapaq-49/kaggri ，pushed **2026-09-19**，日语项目）

- **vendor 归属**（NOTICE 原文）：notebook 家族作者 = "Ahmed Berat Ozer; **thomastschinkel; yhay81**; destbreso; aurax7; tetsutani; prvsiyan; Dmitrii Gluzdov. **Public route data and routing maps: yhay81**"——即 09-19 digest §6b 里 74.5%/93.8% 胜率的 public-state-router + shop-router 一族（内部代号 **r53**）。
- 家族共同构造：**13 条预计算动作路由，按 day-6 公开商店的有序对选路**，d27 后切终局路由 2；r53 劳务分配 + 动态卖出 horizon（实测 288-695 手被最终赋值为 4）；终局 712-718 手只模拟自己的操作/衰减/卖库存做局部搜索（默认 64 sims×1 迭代×每工人 4 候选，内部上限 256×2×16）；施肥 beam search 宽 8 深 8（01）；用**对手公开产量**估计价格下落敏感度；仓库溢出规避；羊→牛置换 + 条件性追加羊投资。
- **★ 开局一行定胜负（本次最高价值单条情报）**：01 与 03 的全部源码差异只有 `_R42_OPENING` 一行——01/02 开局 `小麦购买 13 → 30`、卖出请求量 30；03 改为 `小麦购买 5 → 10`、卖出请求 60（**少买种子多卖货，现金周转更快**）。seed 0-31 双座位 Rust 总共 192 局：**03 对 01/02 各 64 局全胜，场均收益差 +25,139 / +25,929**。作者结论原文："初手の 1 行が大きな対戦差を作る"（开头一行就造成巨大对局差）——**开局市场/资金状态是最重要的验证对象**。
- notebooks.json：04 = "user identifies as current notebook SOTA"；05 = "user-provided latest, **2026-09-18**"（蒸馏 teacher）。作者下一步 = 以 05 为 teacher 的 PPO 蒸馏 + 向量化环境（PyTorch 2.13/CUDA 13），PPO 学习器未实现。
- 强度声明全部标注"用户观测、未独立 LB 验证"（文档有专门的观察/实测分离纪律，值得学习）。

## 2D. gytdrop/KaggricultureAgent（无 license）—— 72 顶级回放挖出的启发式，~116k 本地均值

来源：CHECKPOINT_RESUME.md 原文（https://github.com/gytdrop/KaggricultureAgent ，pushed 2026-08-12）

- 方法论：从 **72 个 top 玩家回放（144 局，分数 100k-158k）**直接挖策略蓝图，纯启发式 + tier 任务分配 + sticky claims 防工人震荡；本地 8 种子×2 座位 **~116k 均值**。
- **开局蓝图**（d0-d3 直接对照物）：土地 3 象限（**NE d7、SW d11，永不买第 4 块 @4000**）；劳动力 **d0 雇 5 人**、d1-6 ~3、d7 到 8、d11+ 11-14；牲畜 14 PASTURE（8 COW+6 SHEEP）全日喂+照料；作物 42 STRAWBERRY（d10-16）、12 MELON（d10 收）、~7 WHEAT（2 日循环）。
- Terminal liquidation（自 COK-ZhangZiliang/Kaggriculture 挖来后对照引擎源码修正）：d28 只喂一次只留早晨小麦；d29 全卖永不喂；d28 停买饲料；**d29 hour14 起所有携带单位强制入棚清仓（last scored step = 718）**。实证 +3,630/局（16/16 胜，p=0.000）。另测"glut-weighted sell ordering"= 纯噪声（p=0.975）否决。
- RL 教训（与 09-19 digest §6a RL 共识互证）：Decision Transformer 重写上线 Kaggle 得 ~27k，**-113k 回归**；DT A/B p=1.000 无影响，已断开。最终形态 = 纯启发式 + 终局清算。

## 2E. CDrookieDc/kaggriculture（无 license）—— 鹅核心规则引擎（09-19 已登记，本次补细节）

来源：README via API 原文（https://github.com/CDrookieDc/kaggriculture ，pushed 2026-08-21）

- 鹅核心 ~28 coop 环绕棚（鹅 2 egg/日/tile，egg 市场 log 形 glut 吸量大卖；**每鹅每天 1 个 ~$90 免费肥料 = 全场最高单动作价值**，价格 ≥$60 就收）；小麦骨架填满剩余格（5 日循环，town shops 全季抽小麦保价 ≥$25 常见 $40+）；甜瓜脉冲 8 格（d0-1 与 d10-12 两播，~$6-7k/波，town center 每日抽 1 melon 保价）；**刻意回避 cow/sheep/strawberry/tomato/carrot（卖 100-150 单后崩到 $1 底）**。
- 控制器：3×3 sector-owner 制（每单位拥有自己 sector 的格），消除贪心重分配的往返震荡（旧版 70% 回合浪费在走路上）。
- 本地 1.32.7：vs starter 31k-34k : 3.4k（全种子双座位）；迭代史 v1 18754 → v3.2 32094。

## 2F. asajjadi/kaggriculture（无 license）—— 干净的单文件 stdlib 贪心模板 + 两条补充事实

来源：README/NOTES 原文（https://github.com/asajjadi/kaggriculture ，pushed 2026-08-05）

- 每回合从 obs 全量重推导（无跨回合状态）：任务构造（WATER/HARVEST/FERTILIZE/DIG/PLANT/PLACE/FEED/CARE/COLLECT_FERTILIZER/机会性 BUILD）→ 打分 `YIELD_DENSITY[type] × 当前市价`，**作物多样化软惩罚**（自己多格同作物折价，防自砸价）+ **town shop 需求加成**（结构性需求）→ 按 `value/(1+距离[+取货绕棚罚])` 分配，urgent 任务（差一天变 weed/逃跑）乘大系数必胜优先。
- **补充事实①（补 09-19 digest 未解问题 1 的社区口径）**："1.6 vCPU / 6.5GB / 100MB submission ceiling"——非官方但与 100MB 包限口径一致，后续可再向官方 FAQ 网页核。
- **补充事实②**：种当天算第一个未浇水日——"the game turns a plant into a weed after 2 consecutive unwatered days and **the planting day itself counts as the first unwatered day**"（引擎文档已有此条，此仓再次独立确认）。
- 自报局限清单有价值：无对手建模（对手 crop mix 可见）、land/hire ROI 粗糙、肥料目标不分作物（应优先 wheat/carrot——只有它们天然到不了产量帽）、town shop 预解锁无对冲。

## 2G. akmalkhaniub/kaggriculture-mcts-agent（无 license）—— 定性：虚构环境，无天梯证据

来源：SPECIFICATION.md + kaggriculture/agents.py 原文（https://github.com/akmalkhaniub/kaggriculture-mcts-agent ，pushed **2026-09-19**）

- UCT MCTS：120 iters、rollout_depth 6、c=1.414、greedy rollout；分支因子 = 每 tile 动作（成熟→HARVEST、湿度<60→IRRIGATE、养分<60→FERTILIZE、空格→PLANT×{CORN, SOYBEANS, WHEAT}）+ NOOP。
- **但其环境 AgriculturalSimEnv 是虚构的**（moisture/nutrients/maturity/weather、CORN/SOYBEANS、200-turn 局——均非 Kaggriculture 真实引擎；SPECIFICATION 的动作空间/约束也与真实赛题不符，vibe-coding 产物）。对我方搜索空间设计无直接参考价值，仅作"存在 MCTS 尝试"的登记。

## 2H. 其他带过

- rooklift/krobus（3★，无 license，08-15）：回放查看器（main.js + market/replay 模块），工具非 agent。
- pomagrenate/kaggriculture（08-24，无 license）：自称 "Model-Based Receding-Horizon Control"，README 主体是引擎文档拷贝（含 melon 浇水 age10 到帽/施肥 age8、tomato ages8-11 四收、strawberry ages10/12/14/16 后枯成 weed 等细则，与 island-ga engine_facts 互证）。
- Alloysj/Kaggriculture-agents（**09-17 活跃**，无 license）：v1→v10 迭代，README 只记到 v3（~17.8k vs starter）；v2 踩过的坑有共享价值——非 ongoing 作物种植当天 `yield_units=1` 但 `first_yield_day` 前不可合法收割，只查 `yield_units>0` 会反复尝试非法收割卡死。
- kw0809suzuki-oss/relation-flow-agent（**09-20 push**，日语"公開用の牧場実験記録"）：GitHub Actions 实验流水线（pattern mining/vector-flow），未见强度声明，观察名单。
- diffmap/kaggicultureRL（MIT）：无代码更新（08-20 后未动），09-19 评估不变。

---

## 3. 与我方 v13.8（四层调度器+市场计划器）的差异对照

1. **开局构造层缺位**：island-ga/qhapaq-49 家族/gytdrop 三家全部把开局当**离线预计算问题**（GA 搜 spec / 13 条预计算路由按 d6 商店选 / 72 回放挖蓝图）；我方 v13.8 是在线调度器推导。island-ga 用数字证明共识开局离上限还有 229k-72.8k≈3 倍空间——开局竞速输 3-5 天不是执行问题，是我们的 base 没被搜过。
2. **开局一行钱万金**：kaggri 家族 01→03 一行（少买种 13/30→5/10、多卖 30→60）= 场均 +2.5 万。我方开局点火的第一性指标应是 **d0-d3 现金周转速度**（早卖+少压种子），不是"任务全排满"。可立刻做的实验：以我方 twin+v10.3 系开局为 base，对 d0-d3 的 BUY_SEED/SELL 数量做 ±1 邻域扫描（CRN 3+5 种子纪律照抄 island-ga）。
3. **卖出即排水不是收入时点**：island-ga sellpol 基因一项 14k；hybrid（日率+3 日补扫）>sweep>daily。我方市场计划器可加 sellpol 维度。
4. **走位值一半**（147.3k vs 72.8k）：同样的计划，谁执行谁少走谁赢——我方四层调度器的 routing 层价值上限比计划层高。
5. **终局清算三件套**（gytdrop，可直接抄思路）：d28 停买饲料/只喂一次、d29 全卖永不喂、d29 hour14 起全员强制入棚（last scored step=718）。
6. **RL/DT 再证不可救**：gytdrop DT -113k 回归 + diffmap RL 系无 LB 证据；纯启发式+离线搜索是主流胜形态，与我方技术路线一致。
7. **吞吐基座**：cppsim/nikital7 位精确 C++（24k 局/秒/机）是离线搜索的现成加速器，Apache-2.0。

## 4. 版权与合规标注

官方政策锚（09-19 digest §3）：host "Anything freely and publicly available is fair use"（737788）；公开代码共享须在 Kaggle 本赛区、9-23 23:59 UTC 锁（741281）。GitHub 代码的合规按 **license** 分档：

| 仓库 | license | 合规结论 |
|---|---|---|
| destbreso/kaggriculture-island-ga | **MIT** | **可直接抄码**（保留版权声明） |
| destbreso/kaggriculture-cppsim | **Apache-2.0** | **可直接抄码**（保留 NOTICE） |
| qhapaq-49/kaggri | **Apache-2.0**（移植层；vendor 内 notebook 原件各自保留原归属） | **可直接抄码**；其 vendor 的 notebook 家族本是 Kaggle 公开共享件（共享即 OSI 授权，规则 §3.6），抄前查 vendor/notebook_0x/source.py 头部原 notice |
| diffmap/kaggicultureRL | **MIT** | 可直接抄码 |
| COK-ZhangZiliang/Kaggriculture | Apache-2.0 | 可直接抄码 |
| gytdrop / CDrookieDc / asajjadi / Alloysj / akmalkhaniub / rooklift / pomagrenate / bravefe 等 | **无 license = 默认版权保留** | **只能学思路/看数字，禁止抄代码** |

注：host 口径"freely and publicly available is fair use"覆盖公开可见性，但保险做法仍是以 OSI license 为抄码底线——无 license 仓一律走"思路借鉴+自写实现"。

## 5. 新增原件登记

- `references/data/intel-notebooks/island-ga-moat-0920/island-ga-an-owned-schedule-is-a-moat.ipynb`（86.9KB，`kaggle kernels pull destbreso/island-ga-an-owned-schedule-is-a-moat`，2026-09-20）——island-ga 配套 notebook 原件，§2A 全部 notebook 数字的上游。已随本 digest 登记 INDEX。

## 6. 移交 Kaggle 侧 agent 的线索（GitHub 来源指向，未在本路展开）

- destbreso 系列 notebook：`a-dna-test-for-agents`、`a-week-four-x-ray-of-the-top-twelve`（top12 91.5k 中位、score>950 scripted continent）、`everyone-is-playing-the-same-opening`（94% seats 同开局@turn24）、`mutants-at-the-top-genetic-potential-of-a-replay`（榜首最不强计划固定；live agent 早期贴 spine 晚期分化）、`kaggriculture-what-kind-of-optimisation-is-this`、`six-checks-before-you-waste-a-submission`、`kagsim-the-engine-at-2000-episodes-per-second`。
- nekkon（Luka Duvanov）：`the-top-agent-is-a-720-turn-replay-not-a-strategy`。
- nikital7：`4000x-environment-speedup-kaggriculture`（cppsim 上游）。
- 价格曲线参数实抓讨论帖：discussion/734412（island-ga 称在此核过 1.32.7 价格参数；georgymamarin 在该帖实测 melon glut 行为）。
- qhapaq-49 notebook 05 = 2026-09-18 的最新公开 notebook（可能对应 09-19 后 Kaggle 侧更新，值得对号）。

## 未解问题

1. **island-ga 搜索成品 genome 与私有 executor 不公开**（作者明示 §8）——我方可按其 MIT 管线自搜；envelope 先验是否仍是 9 月中旬 meta 需用我方 twin+回放复核（该仓 pushed 08-25，早于 9 月平衡与 meta 演化）。
2. **kaggri 的 03（+2.5 万开局改动）在真实天梯的独立验证缺失**（作者自标 strength_verified=false；01 "比 02 强 ~100 rating" 也是用户观测）。
3. **RAM/vCPU 配额官方数值**仍未定（asajjadi 口径 1.6 vCPU/6.5GB 为单一社区来源）。
4. GitHub 361 仓中 push 日期在 09-19 之后的十余仓（cdcoonce、S-Riku-tus、pig7selene、SARTHAK-AIML-0182、chukka-venugopalam、superdanich7-jpg、Gluzdov-Dmitrii、ZeelVavliya、masaki0219、qhapaq-49 等）未逐一深读——多数为 0★ 无描述，建议下轮扫描时以"push 日期>09-14"为过滤器复扫。
5. qhapaq-49 的 routes_01/02.json.z（预计算路由，sha256 d29122…，01/02 完全同数据）内容未解包分析——按任务纪律未下载大件；若需要 d6 商店条件路由的逐 turn 序列，可后续定点解包。
