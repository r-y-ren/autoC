# 情报地图：K-03 可用外部资料（2026-08-31 实抓核验）

所有条目均经 `kaggle kernels pull` / `kaggle datasets download` 实抓到 `.tmp-intel/`（notebook 原文 + 数据集），非模型记忆。核验日期 2026-08-31。

## A 级（直接可用，已验证内容）

### A1. raykkretzschmar/kaggriculture-rank-your-agent（102 赞）
- 实抓: `.tmp-intel/kaggriculture-rank-your-agent.ipynb`（38 cells）
- **shop-demand 表（关键经济修正）**：决定实现价格的不是 glut 曲线而是 `base price × shop demand/day`。MILK 3 店 160 基价 18/day——16 奶牛供不满，整季卖 266；EGG 2 店 50 glut 至 42；MELON 0 店（只有镇中心）→ Melon Mateo 上限 44k 的根因；WOOL 1 店；WHEAT 5 店 30/day ≈ 永不崩（ballast）。
- **两条引擎勘误（作者自称"规则书写错"）**：CARE 实为 +1/日非 +2（kaggriculture.py `_daily_refresh_animals`）——我方全量 CARE 策略不受影响；**NW 未解锁时 (4,4) 是唯一可用 shed access tile，其余三个 access tile 落在锁定象限，PICKUP/DROP 静默 no-op，雇手 spawn 在锁定 tile 损失首回合**——我方 `_shed_access` 动态计算，无此漏洞。
- **本地评级协议**：Bradley-Terry（Elo 尺度 400/10x 锚 1500）+ seat bias 检查 + 840 局/20min 预算 + "把上一版自己加进对手池"。
- **MIT 许可参考对手池已拉取**: `.tmp-intel/refs/`（agents_manifest.csv 教学梯子 tier0-5 每档带 lesson；crop_economics.csv；baseline_league.csv H2H 数据；broker_bea.py 等源码）。可与 evaluate 池合并。

### A2. raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta（138 赞，56 cells）
- 实抓: `.tmp-intel/kaggriculture-findings-from-zero-to-top-meta.ipynb`
- 引擎细节：melon 浇水窗 age 6..12 cap 6（16 tile 满执行=96 melon，漏窗 70 是常见静默泄漏）；**HARVEST 进 unit inventory，SELL 只看 shed，不先 DROP 市场不可见**（我方已有 DROP 时序）；**肥料可 SELL**（我方 3 处 SELL FERTILIZER 已实现）。
- 方法论对照：与我们的 ablate 门同构——含"第四象限：广域阴性结果"（expansion 在当前 meta 失败的系统性证据，印证我们 LAND 门）和 C90-C95 迭代史（idle-labor 花费纪律、feed-first 保护——对应我们 FM-R6-2）。
- 回放日志：c14→multi-leader meta 演化、horizon arms race、"为什么相同上传天梯分不同"（bank 随机性）。

### A3. cjlcjlcjl/kaggriculture-what-the-top-farms-do（74 赞，31 cells）
- 实抓: `.tmp-intel/kaggriculture-what-the-top-farms-do-a-live-meta.ipynb`
- **硬编码验证**（官方每日数据集，Elo 3000+）：kakuteki 3136 / venks 3117 / Wufang Hong 3146 全 trace 局局 100% 相同；**LB#1 Seb 决策一致但执行自适应（35-66%）**——与 DNA-test liveness profile 互证：顶部分两层（脚本层+自适应执行层）。
- 崩盘表：wool/straw/milk 60-80u 崩、melon ~158u、tomato/carrot 500-850u、wheat/egg ~3000u（ballast）。
- **动物日产 1 肥料（boolean，未收集当日蒸发）→ 卖肥料 free-money loop，top 局卖数千单位**；wheat 浇水到不了 6 cap 必须施肥，melon 浇水即满施肥浪费——肥料分配优先级与我方 WHEAT_FARM 设计一致。
- 卖法：4-8u 小批量 metered，先卖后买同 turn 排序。

### A4. kaitofukami/40-40-early-floor（127 赞，Top-10 段位公开 agent）
- 实抓: `.tmp-intel/40-40-early-floor-39-46-top-10-v48-fast-routes.ipynb`（**含完整 main.py 107,008 bytes, SHA-256 dadee25a…，16 测试**）
- v48 = v43/44 兼容地板 + first-shop 快路分支（YARN step88 → Kaileh57 线；FARMERS step120 → taiseiu 线）+ 窄 BAKERY 资本恢复。冻结动作流面板：旧 first-20 40/40、Top-10 holdout 39/46、Top-30 97/140。
- 方法论与我方同构且更严：chronological team-split holdout、lineage 只做评估元数据 runtime-blind、promotion gate 全过、§8 明列 falsification 条件。v47 全 PASS 事故（3,000×11 局）→ 结构性单子策略调用不变量（719=719）——对_submit 前冒烟有直接参考价值。
- **直接可用实验**：将 v48 加入本地对手池与我方 v7.2/v9.2 H2H，把"130 分类差"翻译成行为差与面板胜率。

## B 级（可用，未深读）

- boatlee/v16-rc5（298 赞）8C/4S premium market lead；salemali7/kaggriculture-2900（HarvestForge-X）；tetsutani/adaptive-farming（139 赞）；prvsiyan frontier 系列（96/85 赞，08-27/28 仍在更新）；romantamrazov/hamburger（128 赞，"何时卖"范式的来源）；beicicc/c20-exact-replication-control（fukami 引用）。均已列 kernel 榜，未实抓全文。
- georgymamarin/kaggriculture-episodes 数据集（fukami 的 lineage fold 原料，与 destbreso genomes 互补）。

## C 级（线索，待审）

- 讨论区 "960 Matchups and a PPO Plateau"（discussion/736439，WebSearch 2026-08-31）：RL/PPO 路线与 plateau 讨论；CLI 2.2.4 无 discussion 子命令、internal API 方法名不匹配，未抓正文。
- LinkedIn 帖（luobill2017）：winning mix = heuristics+ML+RL+planning+opponent modeling；Reddit r/reinforcementlearning AMA（规则制定者）。

## 对 K-03 的三个直接行动项（均不耗提交配额）

1. **fukami v48 入池**：与 v7.2/v9.2 本地 H2H + 把其 6 路线分支结构与我们 62 种子注册表对照——它是"公开可下载的 764+ 段位行为"。
2. **shop-demand 表修正我方经济模型**：我方 PRICE 曲线是 glut 侧；把 `base×shop_demand` 作为定价上限约束（MILK 266 / MELON 0 店）复核 v9.2 的 crop 权重。
3. **参考对手池合并**：MIT 的 tier 梯子（含 lesson 字段）可作为 evaluate 报告的固定基准层，Bradley-Terry 评级直接抄协议。
