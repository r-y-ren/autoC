# round-23 败局法证（Track-B DTSP v1，submission 56342843）

- 日期：2026-09-19（round-23 二次采样 19 局 8W-11L @500.9 之后）
- 作者：software agent（round-23 败局法证任务包）
- 数据：官方回放 20 份（`references/data/online-replays/round23/`，含 1 份镜像自博弈 ep110616242）；
  round22（v13.8）18 份（含 1 镜像）。深度统计：`exports/probes/planner_bench/round23_deep_stats.json`（现役产物）
  与 `exports/probes/round22_deep_stats_regen.json`（本探针同脚本再生）。
- 工具（新增只读探针，不改现役代码）：`scripts/round23_loss_forensics.py`（逐局台账/分型）、
  `scripts/round23_disaster_dtsp_probe.py`（灾难局 DTSP 黎明决策离线重建，复用 planner_offline_bench 同机制）、
  `scripts/round23_dtsp_stepdiff_probe.py`（逐步动作指纹接合判定）、`scripts/round23_dtsp_engagement_probe.py`（反事实口径）。
  中间数据：`exports/probes/round23_forensics/`（gitignored）。
- margin 口径：本文 margin=单局我方终局资金−对手终局资金；"局均 margin"=各局 margin 之和/局数
  （与 JOURNAL"累计 margin -4,455（66.6k vs 71.0k）"同口径；19 局 margin 总和 -84,641）。

---

## 0. 头号发现：DTSP v1 线上零接合（本 round 战绩 = v13.8 战绩）

**证据（最强口径，零反事实）**：把官方回放逐步记录的 observation 原样喂给纯 v13.8 agent（与 main.py 同语义
exec 装载、每局全新命名空间），逐步比对动作流：

- **19 局官方局 + 1 局镜像 × 719 步 = 全部 719/719 逐字节一致（100.0%）**；镜像局（双席均为我方提交）两席亦 719/719。
- 已排除哈希序噪声：PYTHONHASHSEED ∈ {0,1,999,12345} 四档复跑灾难局均 719/719。
- 判定：**DTSP v1 线上未改变任何一个动作**。线上轨迹与纯 v13.8 逐位一致——这同时被孪生口径独立印证：
  灾难局从 d10 注入的"反应式基线"rollout 终局 28,806 = 真值（twin_noise 0.0）。

含义：round-23 的 8W-11L、margin -4,455 **不是 DTSP 的成绩**，是 v13.8 在 round-23 对手盘上的成绩。
P3 的 fail-open 护底按设计工作了（行为=旗关 v13.8），但接合本身没有发生。

三个候选根因（线上无遥测，回放不可判别，见 §7 未解问题）：
1. `DTSP_RUNTIME_CONFIG` 未进入官方运行时命名空间（entry.py 接线只认 main.py 命名空间的全局）；
2. twin 指纹/引擎装载在官方环境失败 → 首黎明即粘性关断；
3. 每黎明 overage 预算 < min_projector_budget_s → `keep_yesterday`（首日无计划=恒默认）。

三者产生完全相同的可观测签名。**修复接合 = v2 的第 0 项**（见 §6 V2-1）。

---

## 1. 11 败逐局分类表

带定义：<1k 惜败 / 1-2k 运气带 / 2-5k 结构带边缘 / 5-20k 结构带 / ≥20k 崩局带。
两维模式：strong-opp=对手 d24 现金 ≥55k 而我方引擎正常；my-collapse=我方 d24 <35k（对手 <55k）；both=两者；mid-ramp-gap=两者都不是的中期爬坡差。
对手结构分型主判据=其收入结构+种植/畜群画像（`opponent_typing`，证据随行 ledger JSON）。

| # | episode | 对手 | margin | 带 | 两维模式 | 对手主型(标签) | opp d24 | 我方 d24 |
|---|---|---|---|---|---|---|---|---|
| 1 | 110616342 | D S S Kumar | -47,480 | 崩局 | strong-opp | wheat_heavy(重畜+重麦+快扩) | 73,841 | 40,091 |
| 2 | 110619633 | Philipp k-s | -15,185 | 结构 | strong-opp | herd_heavy（峰值 27 头，COW20） | 64,578 | 52,801 |
| 3 | 110620722 | vlad101 | -30,636 | 崩局 | strong-opp | berry_melon_heavy（d11 即 21.0k） | 69,520 | 39,364 |
| 4 | 110623033 | Chirag Bhatnagar | -16,657 | 结构 | mid-ramp-gap | wheat_heavy | 41,660 | 38,769 |
| 5 | 110627506 | Kushpreet Singh | -21,972 | 崩局 | strong-opp | herd_heavy(重麦+快扩) | 60,314 | 39,281 |
| 6 | 110628635 | Yan Slabodich | -26,382 | 崩局 | both | herd_heavy(重麦+快扩) | 64,280 | 33,295 |
| 7 | 110629738 | Giovanni M. Dall'Olio | -23,251 | 崩局 | my-collapse | balanced（MILK d19=82 崩价局） | 50,708 | 24,961 |
| 8 | 110630917 | Lebansty Valan | -11,796 | 结构 | strong-opp | wheat_heavy | 61,099 | 42,360 |
| 9 | 110633089 | lixinglong ye | -45,492 | 崩局 | strong-opp | herd_heavy（峰值 16 头，d10 已 7.3k） | 85,966 | 35,072 |
| 10 | 110634204 | Hiroyuki Fujimaki | -24,717 | 崩局 | my-collapse | herd_heavy（GOOSE 8，**灾难局**见 §3） | 42,410 | 17,681 |
| 11 | 110635317 | S Aishvarya | -5,679 | 结构 | my-collapse | herd_heavy（单象限 COW 11 头） | 46,940 | 28,430 |

败因模式分布（启发式口径）：6× early_press（开局即被压制，d12 落后 ≥5k）、3× mid_ramp_gap、2× steady_gap；
两维口径：**6× strong-opp、3× my-collapse、1× both、1× mid-ramp-gap**。
对手主型分布：败局 herd_heavy=6 / wheat_heavy=3 / berry_melon=1 / balanced=1；
胜局（8 局）balanced=3 / wheat_heavy=3 / herd_heavy=1 / berry_melon=1——**herd_heavy 对手是我们最危险的类型**（败局 55% vs 胜局 12.5%）。

---

## 2. 惜败 vs 结构带：没有运气带，全是结构带

- **margin >-2k 的"运气带"：0 局**。11 败中最小的是 -5,679（110635317），其余全部 ≥-11.8k。
- 结构带（≤-2k）= 全部 11 局。共性两条，分界线干净：
  - **对手强度线**：opp d24 ≥ 58k 的局 **0/7 胜**（6 局 strong-opp + 1 局 both 全在此带；胜局对手 d24 最大 56.6k/Eduardo2c，其 final 69.2k 也是 8 胜中对手最强）。
    即：对手 d24 现金 ≥ ~58k 时 v13.8 从未赢过。
  - **我方引擎线**：我方 d24 < 35k 的局 **0/4 胜**（110628635 33.3k/110629738 25.0k/110634204 17.7k/110635317 28.4k；次低 35.1k 不入带）——我方经济塌方局，与对手强弱无关。
- "我们怕谁"画像：**同构但更大的对手**。6/11 败局对手是我们自己的 herd+berry 核心打法的更强执行者（终局 85k-122.5k，
  畜群 12-27 头、NE+SW 多在 d7-d11 双开）；叠加一种市场形态：**动物产品早衰局**（MILK/WOOL 在 d13-d19 跌破 90 死价线），
  我方畜群线熄火且无改道杠杆（败局中 2 局明确：110634204 双死价、110629738 MILK d19=82）。对手的 GOOSE 线本身不是判别器（4 局对手买 GOOSE：我们 2 胜 2 败）——
  判别器是**整体经济规模**（对手终局 ≥ ~85k 我们全败；≤ 69.2k 我们全胜）。

---

## 3. 灾难局 ep110634204（vs Hiroyuki Fujimaki，-24,717）深挖

### 3.1 时间线（逐日实测，全表见 `exports/probes/round23_forensics/disaster_110634204_timeline.json`）

| 日 | 我方现金 | 对手现金 | 我方畜群 | 关键事件 |
|---|---|---|---|---|
| d0 | 335 | 23 | 4 头（2S+2C） | 标准 opening：买 2C+2S，5 麦+4 瓜 |
| d6 | 340 | 193 | 5（+1C） | NE 解锁；首植草莓；**这是我方全季最后一次买畜** |
| d7 | 1,612 | 989 | 5 | 我卖 WOOL 10 只得 1,818（181/只）；**对手买 GOOSE 4**、WOOL 卖 3,474（193/只） |
| d9 | 1,860 | 3,761 | 5 | 对手瓜田上量（MELON 16 格） |
| d10 | 281 | 8,300 | 5，**空棚 3→12** | SW 解锁+建棚耗尽现金；对手 GOOSE 线再 +4（d11），蛋/瓜双线日入 3k+ |
| d11-d12 | 174→263 | 7,604→8,631 | 5 | 黎明现金 <450+reserve，买畜机械化不可能 |
| d13-d17 | 6,246→6,856 | 11,538→16,350 | 5 | **WOOL 88→43、MILK 114→68（双双跌破 90 死价线）；现金可买 2 头但零买畜动作**；crew 被压在 10（对照组 12） |
| d19-d29 | 11,257→28,806 | 29,904→53,523 | 5 | 现金全程堆积无消费出口；WOOL 跌至 1-11；P4 出清后终局 28,806 |

对手结构：GOOSE 8（蛋线日入 700-1,200）+ MELON 15-16 格（d10-d20 日入 3,000-5,456）+ 3S/2C；终局 53,523。

### 3.2 是哪种失败？——v13.8 执行器的设计行为在独特市场形态下的连锁塌方，非对手砸线、非开局买畜失败、非饲料断供逃亡

- **不是对手干扰砸线**：对手没卖 WOOL/MILK 压价（它卖蛋和瓜）；崩价是市场吸收与双场供给的形态（本局 WOOL 206→88（d13）→5（d19），
  19 局唯一双产品死价局——其余 18 局 WOOL d13 均在 151-241、d19 多数 ≥148；MILK d19 <90 的仅 3 局）。
- **不是买畜订单被拒**：d7 之后**买畜动作一次都没有发生**（动作流为空），是策略侧闸门关闭：
  d11-12 黎明现金（174/281）过不了钱包门 → d13+ MILK/WOOL 跌破 `DEAD_PRICE_FLOOR=90`（constants.py:174）+
  曲线门（`_curve_gate_ok`，跌势投影）→ 冻结买畜；`ANIMAL_BUY_LAST_DAY=20` 前窗口本开着但价格门不再放行。
- **crew 被压低**：本局 hands 上限 10（其余局 12），与 d12 现金 174 触发的保守路径一致（hires 268，8 胜局带 286-295）。
- 结果：12 个空棚+5 头到终局，动物线收入死，作物线又被 v13.8 默认配额封顶（草莓 24 格），现金 d19 起堆积无处消费。
  **规划器层面没有任何"把畜群预算改道作物/买地"的运行态杠杆**。

### 3.3 孪生规划的黎明决策（离线同机制重建）与反事实

线上无遥测（step `info` 全空），用 bench 同机制管线（同孪生、同投影器 trimmed_mean@0.25×pess0.75、同计划空间）逐黎明重建：

- 投影器在 d3-d13 一致选择 **C1 档×配额 1.25×时点 -1×折扣 0.90**（`P|A|B1|C1|HEALTHY|LOW|1.25|-1|0.90`）；d14 起切 C2/C3@0.80。
- **从 d10 黎明注入该计划**（对手=回放真实动作，单变量）：**终局 50,825 vs 真值 28,806（+22,019）**；
  反应式基线=28,806=真值（逐位），证明增量全部来自计划覆盖。**从 d13 注入则无效**（28,505≈28,798）——挽回窗口在 d10-d12。
- 但注意：线上该局 DTSP 零接合（§0），这个 +22k 是"若接合"的反事实，不是已实现收益。
- 免责的诚实注记：+22k 后仍以 -2.7k 落败——计划空间能把灾难局拉回平局带，赢不了 GOOSE+瓜的 53.5k。

---

## 4. 对照 round22（v13.8，9W-8L，局均 margin -2,915）

- **同引擎证明**：§0 已证 round23 线上=v13.8 逐字节；round22 本就是 v13.8。因此两 round 差异全部来自
  **对手盘与市场抽取**，不存在"DTSP 的增益局/新败局"。round23 对手终局均值 71,045 vs round22 68,745（强 2.3k），
  局均 margin -2,915→-4,455，胜率 52.9%→42.1%（n=17/19，二项噪声带内）。
- 败因同族（round22 8 败）：strong-opp=2、both=2、mid-ramp-gap=4、my-collapse=0（两维口径，55k/35k 同阈值）；
  败局对手均值 81.6k。**两 round 的败因谱系一致**：强对手压制为主族，我方塌方局每个 round 都有
  （round22 的 Dancing_Chaos 局我方 d24 仅 24.2k、终局 43.7k——灾难局的轻度版）。
- 新形态差异：round23 的 my-collapse 3+1 局中 2 局与"动物产品双死价"市场形态相关（110634204/110629738），
  round22 8 败无此明显双死价标记——属市场抽取波动，但暴露了同一个结构缺口（§6 G1/G2）。

---

## 5. v2 旋钮建议（每条带官方局证据；**全部需离线 bench 复裁**）

**V2-1｜第 0 项（非旋钮=接合修复+接合遥测）：让 DTSP 真正上线**
- 证据：§0——20/20 局 × 719 步动作流与纯 v13.8 逐字节一致；镜像双席同证；灾难局若接合 d10 反事实 +22.0k（§3.3）。
- 影响局数：全部 20 局（当前所有局的"DTSP 表现"均为伪口径）。
- 预估挽回：以 P2.6 official bench 同口径（14 局×42 注入点，DTSP 对反应式 mean Δ=+782.6）为下界参考；
  灾难局单局 +22.0k。修复后需 1 发线上探针验证接合（动作流出现可归因偏离即接合成功的可观测信号）。
- **需离线 bench 复裁**（P2.6 已 PASS；此处新增的是"接合后线上复验"门）。

**V2-2｜容量档默认 C1@1.25×早时点（plans.py 现有轴：capacity_tier/quota_scale/timing_shift）**
- 证据：灾难局 d10 注入 C1@1.25×(-1) → +22,019（唯一有官方局全季反事实的档位选择）；
  投影器在 **19/19 局的 d3 黎明与 d10 黎明均首选 C1 档×配额 1.25**（engagement 探针 best_plan 字段，逐局 JSON）。
- 影响局数：my-collapse/both 家族 4 局（110628635/110629738/110634204/110635317）为主要受益面；
  strong-opp 6 局无反事实、幅度不可估。
- 预估挽回：灾难局 -24.7k→-2.7k；其余塌方局按同机制类推但**未逐一实测，不给数字**。
- **需离线 bench 复裁**：P2.6 的 mean Δ=+782.6 是对反应式的注入点均值，未按"死价塌方局"分层；建议补塌方局分层消融。

**V2-3｜负面结论：不要在买畜时点轴（herd_day_shift/animal_buy_last_day_shift/herd_start_day）上找塌方局的解**
- 证据：灾难局 d13 注入（时点 +0 计划）终局 28,505≈无效果——窗口不是约束，**价格门才是**
  （MILK/WOOL < 90 死价冻结 + 曲线门，constants.py:174-175；这三键平移买不了死价市场里的畜）。
- 影响局数：my-collapse 3 局中时点轴挽回≈0。
- 该结论免去了 v2 在时点轴上的无效调参。

**V2-4｜终局出清档（p4_force_tier/sell_batch_mult/sell_price_discount）维持现状**
- 证据：灾难局 d20 黎明实测 DTSP 对反应式 **+18**（28,507 vs 28,489，中性）；投影器 d20 的选择是 C2@0.80
  （18/19 局）。110623033 的终局被拉开是产能差（d24 后对手 +36.5k vs 我方 +22.8k）而非出清差。
  出清档不是本 round 败因的显著项。

---

## 6. 现有空间缺口清单（"现有 29 键旋钮面内缺该杠杆"）

- **G1｜死价/弱市买畜闸不可参数化**：`DEAD_PRICE_FLOOR`/`DEAD_PRICE_FROM_DAY`/`_curve_gate_ok` 不在 29 键面内。
  灾难局（19 局唯一 WOOL+MILK 双死价局）证明：一旦动物产品早衰，v13.8 只能停买+空棚+现金堆积，
  面内无"折价买畜/关死价闸"的杠杆。与 P2.6 已登记的 105367844 plan_space_gap 局同类（面内无计划能赢反应式）。
- **G2｜反应式侧无"畜群预算→作物线改道"运行态杠杆**：DTSP 计划轴的 quota 1.25/LINE_CAPS 就是这个杠杆
  （灾难局 +22k 即来自作物线扩容吃下堆积现金），但 v13.8 反应式没有等价运行态旋钮——接合修复（V2-1）前该缺口不可达。
- **G3｜对早期强压制对手（d11-d12 即 20k+：vlad101/lixinglong/D S S Kumar 型）无进攻性产能参数**：
  mode_scale_entry_herd=12、mode_scale 窗 4-16 均为默认值；b_branch_force 只能在现有分支里强制，无"更凶"档。
  对手 d24 ≥58k 的 7 局（6 strong-opp + 1 both）全败、胜率 0/7，说明天花板差距是结构性的，旋钮面内无解。
- **G4｜对手模型风格池覆盖不足**：opponents.py 内置 winner_balanced/wheat_suppressor 两风格；
  本 round 出现 GOOSE 线（Hiroyuki/Philipp）与单象限重畜（S Aishvarya，NW 单象限 COW 11 头终局 59.5k）等新形态，
  均不在池内——接合后这些局有 opponent_model_gap 风险。

---

## 7. 未解问题

1. **接合失败根因三选一不可判**（Runtime config 未注入 / twin 指纹官方环境失败 / overage 预算耗尽）：
   线上遥测不落盘（step `info` 被清空）。建议：官方 unpack 语义本地复现 + 下一发探针带"必注入"验证配置，
   以动作流可归因偏离作为接合成功的可观测判据。
2. **runtime 投影段 Ω 不带对手史**：`planner/runtime.py` 黎明投影用 `build_default_models()`（静态池+悲观），
   而 bench 的裁决管线带 `history`——接合后线上真实效果可能低于 bench 口径，需在 bench 增设"无史 Ω"消融对照。
3. round22→round23 胜率回落（52.9%→42.1%）在对手盘变强（均值 +2.3k）下属抽取噪声还是 meta 漂移，
   n=17/19 无法判别；若需要更小方差，建议晋级线判断继续用局均 margin+WR 双轴。
4. 灾难局 d0 开局（投影器 d0 选 opening C，线上实际打的是 v13.8 默认 opening A）的完整反事实未跑；
   若 v2 需要评估开局变体，应补 d0 注入 rollout。

---

## 附：证据文件索引

| 文件 | 内容 |
|---|---|
| `exports/probes/round23_forensics/round23_ledger_forensics.json` | 19 局逐局台账（margin/带/模式/对手画像/证据字段） |
| `exports/probes/round23_forensics/round22_ledger_forensics.json` | round22 同口径台账（v13.8 对照） |
| `exports/probes/round23_forensics/disaster_110634204_timeline.json` | 灾难局 30 日全时间线（含逐日市价/动作计数） |
| `exports/probes/round23_forensics/disaster_dtsp_reconstruction.json` | 灾难局逐黎明投影选择+旋钮覆盖+d10/d13 注入四口径+消融 |
| `exports/probes/round23_forensics/dtsp_stepdiff.json` | 20 局逐步动作指纹（接合判定主证据） |
| `exports/probes/round23_forensics/dtsp_engagement.json` | d3/d10/d20 反事实口径接合+逐黎明计划选择 |
| `exports/probes/round22_deep_stats_regen.json` | round22 深度统计（replay_deep_stats.py 再生） |
