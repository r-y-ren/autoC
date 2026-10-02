# 2026-10-02 ahmed·track 补深挖（分析49 登记缺口 P5/a51050-4）——V48 谱系正主机制清单 × 我方基底对表 × V43 EXP277-279 × 榜位轨迹

> 抓取窗口 **2026-10-02 12:05–12:10 UTC**（=CST 20:05–20:10）；通道：kaggle CLI 2.2.4（kernels list/pull）。时点：比赛 09-30 23:59 UTC 已截止，官方终评窗 ~10-14 出榜。
> 纪律：实抓带来源+时间戳；作者自报数字逐条标"自报"；专名一律从既有文件/CLI 输出程序化拷贝（用户名 `ahmedberatozer` 取自 `ext/final-hours/provenance.md`，未手键）。
> 产物归档：`references/ext/ahmed_deepcut/`（26 ipynb + 26 kernel-metadata + `extracted_main/` 26 解码源 + `kernels_list_2026-10-02.csv` + `provenance.md` + `SHA256SUMS.txt` 80 行）。
> **判据结论（一句话）**：拿到增量。①26/26 件全量落档、25 件解码源与作者声明 SHA256 逐字节一致；②V48 谱系机制清单以 EXP 编号全量解出（EXP149→EXP335 共 24 层）；③**血统裁决拿到硬证据：我方基底 dadee25a 与 ahmed V48 源 4b540288 系两套独立实现，"我方基底=ahmed V48 血统下游"在字节层不成立**（G4 双源冲突的关键增量）；④V43 EXP277-279 机制与自报证据链解出。

---

## 〇、任务对照（49 登记缺口）

分析49 行 93 登记：`ahmed·track | V48 正主；V43"Recovering Lost Harvests"（EXP277 定向仓库/EXP278-279 动作等价改写） | 我方基底即其 V48 血统下游 | 深挖缺口：本轮档案以 09-28 五强为准未覆盖——列入 10-07 二轮跟`。本篇即该缺口的提前补册（P5 改进方向"ahmed·track 补深挖"、registry `70d179-5` expected_signal 第三项）。

注意：**本篇系赛后补深挖，全部提案按战后生效口径，无窗口内动作**（49 时点声明沿用）。

---

## 一、材料与抓取（26/26 全量，来源 S1-S3 见文末）

`kaggle kernels list --user ahmedberatozer --page-size 100 --csv`（2026-10-02 12:05 UTC）返回 36 件，其中 kaggriculture 系 **26 件**（V23/V25/V31/V34-V57；缺号 V24/V26-30/V32-33/V37 未公开），另 10 件 casmi26 系属他赛题未拉。26 件逐件 `kaggle kernels pull <ref> -m` 全部成功（作者署名 Ahmed Berat Özer；lastRun 戳 09-11 19:05 ~ 09-22 12:50，**09-22 后无任何 kaggriculture 新 run**——与 final-window-sweep §4"未找到更新"互证）。

各 notebook 内嵌完整 agent 源码，四种内嵌形态程序化解出为 `extracted_main/<slug>__main.py`：

| 形态 | 件数 | 完整性核验 |
|---|---|---|
| `%%writefile main.py` 直写（V25–V42） | 10 | 全部 MATCH（\r\n 归一化后哈希=作者声明） |
| `SOURCE_BYTES` 字节常量拼接（V43–V51） | 9 | 全部 MATCH |
| `SOURCE_BLOB`→b85+zlib（V52–V57） | 6 | 全部 MATCH |
| `V23_TEMPLATE_B64`→b64+zlib（V23） | 1 | 解出 template 底盘（哈希=notebook 自身 assert `985d0722…`）；终稿哈希 `6eb728a4…` 需执行 cell3 补丁链，标 MISMATCH 系口径说明 |

**25/26 与作者声明 SHA256 逐字节一致**（EXTRACT_INDEX.tsv `verify` 列）。对照复核：V43 与 `ext/final-hours/ahmed_v43__…ipynb`（09-30 17:55Z 拉取）同哈希 `8bd567ed…`，其 main.py `919fc1d6…` 一致——V43 自 09-14 21:41 lastRun 后未改版，此前归档可互证。

---

## 二、V48 谱系机制清单（EXP 编号全量，24 层）

ahmed 系源码=**单文件 wrapper 层叠**：底盘（routes/chassis/市场控制器）+ 按 EXP 编号逐层包裹的修正臂，每层 `agent=globals().pop('agent')` 换装。V48（"Clear the Queue"，sha `4b540288…`，357,742B）源内全部机制层：

**A. 底盘与早期适配层**（EXP149–193）
| 层 | 机制 | 出处（源注释自报） |
|---|---|---|
| EXP-149 | Shop0908 生产/卖单提前量/终局货物救援 | v25 |
| EXP-154 | 日终仓储守卫（aurax7 Reactive v2 day-end storage guard）+ **E182 七拍清算器 steps 712-718 按 −price×qty 降序卖**（Dmitrii Gluzdov） | v28 |
| EXP-155 | prvsiyan V221B 有限番茄投资 | — |
| EXP-157 | v31 生产与卖单优先级 | v31 |
| EXP-167 | Dmitrii Gluzdov "Two Coins, One Sheep"：二拍存货预留/已排取货保护/部分未来单扣减 | — |
| EXP-168 | lucifer19 "Harvest Nocturne"：三拍预留门（公开占格相似度） | v34 |
| EXP-173 | yhay81 shop-router-0911-simple 开局市场序列 | v31 |
| EXP175/179/182/193 | 卖单竞速/提前量调参层 | v35-v38 |

**B. 经济与守卫层**（EXP216–260）
| 层 | 机制 |
|---|---|
| EXP216/217/219 | 经济化喂食+肥料售卖；计划次日服务先于酌情减料；仅当本次喂食决策可影响时才记照顾信用 |
| EXP226 | 实物谷物保留完整两天才削减买单 |
| EXP231 | 用已注资当前订单保护投入品（不拿观测实物当未分配现金垫） |
| EXP240/242 | 已承诺作物等原生工人序号；已承诺羊服务期间保原生索引 |
| EXP257 | V39 底 + 注资原子开局（funded atomic opening） |
| EXP258 | 原创安全契约（safety contracts） |
| EXP260 | 合并层；V41 保持冻结主对照 |

**C. V43 三件**（EXP277/278/279，详 §四）

**D. 竞速/镜像/清队列层**（EXP283–335，即 V44→V48 增量）
| 层 | 机制 | 对应版本（notebook 自报） |
|---|---|---|
| EXP283 | **克隆门卖单抢pre-emption + 掉量时竞速升级**（clone-gated sale pre-emption with drop-time race escalation） | V44 同拍卖单竞速：对手执行同一公开磁带时预留提前 4→8 拍、对手当拍甩卖升 24 拍；自报 paired +467.8、胜点 +12.5pp [10.59,14.41]（自报）；压力克隆 fastclone24 仍输 11-53（自报如实披露） |
| EXP284 | **step-0 麦往返**：一单买 70 麦 + 下一单同拍卖出（替换 V43 开局的 15 麦两单+第三单卖） | V45；对市场中性、对 lineage 克隆非中性 |
| EXP288 | **镜像门**：首拍后现金与我方相等的对手=执行了同一首拍磁带 | V46 首拍微观结构 |
| EXP293 | **卖单提前量**（sdy623/jaxa623 "Beyond 48-0" 机制）+ step-1 饲料抢位攻击（每条该谱系磁带在首个市场拍 index 1 买 5 饲料） | V46/V47 |
| EXP298/303 | 逐品项日程缓存/资源快照缓存（性能层，行为不变） | — |
| EXP334 | **清队列主臂**：删除卖不出东西的现金品卖槽、不挪动购买单 | V48 本体 |
| EXP335 | **空可买品卖槽也算洞**（无购买单存在时） | V48 本体 |

**E. 附加件**：v44y pre-guard（在 hour 21-22 预报价 hour-23 日终仓储守卫将抛掉的量）；`final_price_guard`（V55 起收尾函数）。

**版本时间线（26 件 notebook 首格自报，全自报）**：V23(09-11 适应性路线)→V25→V31→V34(观测市场时机)→V35(公开响应卖+注资羊扩)→V36(守卫四拍卖)→V38(聪明喂食)→V39(赶集前备货)→V40(按店铺选计划，step 144 一次；Yusuke Hayashi Shop Router 0913)→**V41(REVIEW：直对全胜但 95% 队级点区间 −1.14~+12.22pp 过零门 FAILED，如实降级)**→V42(生产适配市场；时延门 116/63ms 失败如实披露)→**V43(回收失收：黎明仓溢救援)**→V44(同拍卖单竞速)→V45(首拍麦往返)→V46(首拍微观结构)→V47(反应式市场协调)→**V48(清队列)**→V49(V48+Thomas Tschinkel "The 2945 Farm" 公开经济层 COURIER/CARROT/CARROT2…，自报上游 live 2944.7)→V50(早纱承诺)→V51/52(精简羊群/纱路线)→V53(开局签名+当前 meta 卖流：引 Pipe16 idle-workers(nathanjacob)与 dmitriigluzdov "More Wheat, Smarter Sales" 的实卖历史进卖单预测器)→V54(换用"最新公开最强生产谱系"，弃 V53/54 分支)→V55(溢价品预留 40→41 拍；42/43 回退被拒)→V56(种子预算+肥料规则)→**V57(资金顺序不变量：修 V56 同拍优化器把 HIRE/BUY_* 挪到注资卖单之前的因果洞)**。

**纪律注**：V41/V42/V55 的门失败与回退全部如实披露（自报），该"负结果入册"风格与我方判据纪律同构；V53/V54 明示改用他家公开谱系=**血统聚合器**（与 V23 donor thomastschinkel、V49 Tschinkel 2945 层一致）。

---

## 三、对表：我方基底（dadee25a）vs ahmed V48 谱系——继承/漏/改 + 血统裁决

### 3.1 血统裁决（G4 双源冲突的硬证据，本篇最大增量）

`fn_docs/behavior_inventory.md` G4：dadee25a 血统双 PROVENANCE 冲突（opponents/PROVENANCE.md 记 kaitofukami/无许可 vs v48plus/README.md 记 Ahmed Berat Ozer/Apache-2.0），`fn_docs/provenance_dadee25a.md` 现行口径="双源并列、原创归属两账号间未定"。本次拿到 ahmed 全系真源后可给出**字节层裁决**：

| 证据 | 内容 |
|---|---|
| 尺寸/哈希 | 我方基底 `v48_derivative/main.py` 107,008B sha `dadee25a…2664a`；ahmed V48 真源 357,742B sha `4b540288…`——**非同一字节**（ahmed V48 notebook 的 tar 构建格明示 main.py=其 SOURCE_BYTES 本体，不存在第二种"提交包解码真源"） |
| 结构 | 我方=b85+zlib 打包 **12 模块**（v19_terminal/v21_route_memory_search/v22_market_impact/v22_weed_repair/v23.{state_encoder,simulator,policy_library,planner}/v24.market_maker/v44.gold_floor/v48.fast_route_router）+ 6 条 719 步路由磁带；ahmed=单文件 wrapper 层叠 + EXP 编号臂 |
| 标识符 | 双方共享私有标识仅 6 个平凡项（`_fib`/`_get`/`_shed_access_tiles`/`_value`/`__init__`/`__future__`）；共享函数仅 `projected_shed`/`agent` 级；**我方 0 个 EXP 标记**，ahmed 24 个；反向：ahmed 源 0 命中 kaito/gold_floor/fast_route/yarn_first |
| 时序 | 我方字节首拉 **2026-08-31**（kaitofukami notebook "40/40 Early Floor \| 39/46 Top-10 \| v48 Fast Routes"，见 opponents/PROVENANCE.md + digest public-bot-reverse-eng-20260920）；ahmed V48 lastRun **2026-09-17 22:09**——下游不可能先于上游 |
| 名字碰撞 | 我方模块内 docstring 原文："The default remains the validated **v43/v44 backbone**…first shop YARN_STORE -> **Kaileh57** train-only YARN continuation at step 88…**taiseiu** train-only continuation at step 120"——**v43/v44/v48 全是 kaitofukami 自己的版本号**（其系另有 v20/v21/v41/v48 "Sparse Closed Loop"/"Fast Routes"，见 prior-art-techniques-2026-09-19 §142）；ahmed 独立另起 V23-V57 版本号，两系 vNN 重合纯属撞名 |
| 架构互证 | kaitofukami v48 逆向 digest（2026-09-20 精读）："离线轨迹记忆+在线稀疏路由：6 条 719 步宏磁带+步 88/120/153/216 按公开商铺事件一次切换+反克隆抢卖/影响分排序/718 终局清仓三窄反馈器"——与解码实读逐项吻合（gold_floor clone_preempt、v22_market_impact impact_score、v19_terminal） |

**裁决**：dadee25a=kaitofukami 自家 v48 "Fast Routes" 构建（其内部 v19→v48 版本栈），**不是** ahmed "V48 — Clear the Queue" 的下游。v48plus/README.md:52-54 把 dadee25a 归为 Ahmed Berat Ozer 属**撞名误归**；49 报告"ahmed·track V48 正主（我方基底字节上游）"在字节层不成立，应改述为"**同名不同物：ahmed 是 'V48 Clear the Queue' 谱系正主，我方基底是 kaitofukami 'v48 Fast Routes' 谱系——两系共祖于公开生态（Tschinkel/Dmitrii Gluzdov/aurax7/yhay81 等同批致谢），无直接字节血缘**"。对外引用维持"双源并列"口径的合规动作不变，但"两账号间未定"可更新为"字节源=kaitofukami 构建已证；ahmed 为同名第三方谱系"（呈用户裁决后落 `provenance_dadee25a.md`）。

**残留未证**（如实标注）：kaitofukami 的 v48 构建是否在**机制思想**上受过 ahmed 早期公开版（V23-V43，09-11~09-14）影响——不可证伪/证实（kaitofukami 首拉 08-31 早于 ahmed 全系 lastRun，且其 notebook 无 ahmed 致谢字样）；ahmed V53+ 反向吸收 Pipe16/dmitriigluzdov 实卖历史=公开生态互喂属实。

### 3.2 机制对表（概念层：继承/漏/改）

前提：3.1 已证无字节继承，下表"继承"一律指**概念等价物在我方基底存在**（生态共祖或独立发明）；"漏"=ahmed 谱系有而我方基底无等价物；"改"=同类机制不同实现/判据。

| # | ahmed V48 谱系机制 | 我方基底（解码实读） | 判定 |
|---|---|---|---|
| 1 | 磁带/路线计划执行+店铺事件调度（V40 step-144 按首两店选计划） | 6 条 719 步宏磁带 + 步 88/120/153/216 按公开商铺事件一次切换（v48.fast_route_router） | **改**（同类思想：都是"公开店铺事件选路线"，ahmed 全局选计划、我方选延续段；每拍只评一个子策略） |
| 2 | 终局清算（EXP-154 E182 七拍 steps 712-718 按 −price×qty 降序） | v19_terminal：terminal_market/monetizable_terminal_units 718 两步机 | **改**（等价目的、我方更窄；教训库"榜前对手卖单更少更大"两边同证） |
| 3 | 克隆检测/抢卖（EXP283 掉量竞速升级） | v44.gold_floor：clone_preempt_horizon 2/clone_streak_required 24/clone_distance_threshold 2.0 + clone_veto + bakery_capital | **改**（我方=公开资产签名距离法（_public_signature/clone_distance）；ahmed=卖单掉量观测+竞速升级时变提前量 4→8→24 拍） |
| 4 | 镜像门（EXP288 首拍现金相等） | v19/gold_floor `_public_signature`+clone_distance（作物/建筑/动物/手逐坐标） | **改**（我方判据更细、ahmed 判据更省；均可议；haodou V94 镜像门已判"触发 78.5% 仍负"——此族整体黄区） |
| 5 | 首拍麦往返（EXP284 买 70 单+下単同拍卖回） | v24.market_maker `round_trip_plan`/`best_round_trip_quantity` | **继承（概念等价）**——我方也有麦往返计划器，量/单形态不同 |
| 6 | 同拍清队列（EXP334/335 删死卖槽+合并重复+挪可执行现金卖单，不挪购买） | v22_market_impact `reorder_market` + v23.policy_library `reorder_sell_slots`（按需求分重排） | **改**（我方=重排打分；ahmed=删槽+合并+前移的拓扑手术。49 P2 的 `[]` 保索引空槽对照恰是这一族的未开采残项） |
| 7 | 卖单提前量/竞速（EXP293 sdy623"Beyond 48-0"式抢跑+step-1 饲料抢位） | 无对应抢位攻击；gold_floor 的 clone_preempt 仅 2 拍级 | **漏**（攻击性微观结构：step-0/step-1 抢位攻击在我方基底缺失；我方战役内 day0 抢跑族 50 P1 已实测翻负=不抄动作但需知对手有） |
| 8 | 黎明仓溢救援（EXP277） | v23/v24 有 projected_shed/_shed_after_market/_shed_access（投影守卫）但**无"卖现有存货换回将被丢弃货物"的定向回收** | **漏**（49 P4"三谷底品产出-消化平衡"的对手侧解法之一：仓储损失 5,713→4,376 单位自报） |
| 9 | 日终仓储守卫+预报价（EXP-154 + v44y pre-guard hour21-22 预抛） | v24.market_maker reserve_breakdown（保留路线成本/退出窗，不记卖信） | **部分继承**（我方=成本保留口径；ahmed=物理仓容守卫+预抛） |
| 10 | 喂食经济学（EXP216/217/219 照顾信用；EXP226 两日谷物保留；EXP231 已注资订单保护） | v24 reserve_breakdown/"Existing BUY orders are not credited until they execute"注释族 | **部分继承**（同思想的保守保留口径两边独立出现=生态共识；细节判据不同） |
| 11 | 性能/规划件（EXP278 deepcopy 特化、EXP279 路径长度精确化、EXP298/303 日程缓存） | v23.planner build_sparse_planner（稀疏规划） | **部分**（我方有稀疏化思想，无其等价改写证据链） |
| 12 | 资金顺序不变量（V57：禁把 HIRE/BUY_* 挪到注资卖单之前） | 无对应不变量（我方 reorder 只动卖单槽） | **漏**（但我方"只重排卖单"天然免疫该因果洞——结构差异非缺陷） |

**净读**：概念等价 5/12（#5 继承、#1/#2/#3/#4/#6 全是"同题不同解"）、部分 4/12、纯漏 3/12（#7 抢位攻击、#8 仓溢回收、#12 资金序）。可战后借鉴的绿区残件=**#6 清队列拓扑手术**（正对 49 P2 `[]` 空槽对照实验的机制对面）与 **#8 仓溢回收**（正对 49 P4 产出-消化平衡的仓储损失 23.6% 自报改善）；#7/#12 属对手情报（知悉即可，#7 我方战役已判负）。

---

## 四、V43 "Recovering Lost Harvests"：EXP277-279 机制与自报

V43（sha `919fc1d6…`，321,555B，lastRun 09-14 21:41）三件套（源码+notebook 评估格实读）：

1. **EXP277 定向仓库救援**（`_r148_overflow`，"Original targeted contracts"）：step%24==23（日终拍）当黎明送货将超共享仓容（`_r97_delivery` 报 loss）时，**只卖出"将被丢弃货物等量替换"的现有库存**，使黎明后完整仓库向量与原注资动作完全一致（`_r148_same_stock` 校验）；原田间活与市场单前缀全保留；被弃货物按**存入顺序的可回收后缀**取（非无序总量/未来预测）。机制名"Recovering Lost Harvests"即此。
2. **EXP278 动作等价性能改写**：普通 JSON 容器 deepcopy 特化（`_r149_deepcopy`，原子类型直返+memo 语义对齐 stdlib），保 deepcopy 语义——属**动作等价改写**（49 行 93 命名吻合）。
3. **EXP279 原控制器保留的路径精确化**：`_proposals` 资源束提案（单/双资源束+直接搬运闭包）+ `_R150_HOME_DISTANCE` 预计算回程长度（无临时移动列表）；继承 EXP278 证据的前提=同 448 局复现全部 322,112 候选动作且观测不变、终局回报双匹配。

**自报评估表**（V43 notebook 评估格，全自报、未独立复核）：

| 队列 | W/L/T | 严格胜率 | 均现金额 |
|---|---|---|---|
| Development V43 / V42 | 99/0/13 vs 87/3/22 | 88.39% vs 77.68% | +7,169.19 vs +7,011.30 |
| Independent V43 / V42 | 412/10/26 vs 375/14/59 | 91.96% vs 83.71% | +6,259.49 vs +6,134.61 |
| Direct V43 vs V42（独立） | 39/3/22 | 60.94% | +116.86 |
| Historical top / opponent recordings | 114/6/0；146/4/0 | 95.00%；97.33% | +21,626.16；+19,979.46 |

- 32 保留世界配对：own cash **+96.14**、relative margin **+124.88**、match points **+4.58pp**，世界级 bootstrap 95% CI：现金 [54.27,151.19]、margin [72.46,189.78]、points [2.90,6.47]pp（自报）。
- **作者自设限界**（值得抄进我方评测纪律）："反应面板 7 配置含同谱系回放路由器，不是 7 支独立强队"；"历史录像不可对改动作反应"；"局部分差可移动接近局，不是新生产经济或保底天梯分"；"多数面板胜来自 V42 自身，剔除后 384 局 373/7/4 vs 370/9/5，点差仅 +0.65pp"。
- 账本：448 对全过官方现金/品项核账；**仓储损失 4,376 vs 5,713 单位**（自报 −23.6%）；EXP278 记 896 局全物理账；EXP279 复现 322,112 动作后继承。
- **时延门自报**：EXP277 冻结 Windows 时检 71.66ms **失败**；EXP278 52.16ms **失败**；两者如实保留为失败；发布件 EXP279 过独立八局隔离检查（Windows max 43.81ms；Linux 同 5,752 动作重放 max 17.58ms）——**"共享进程/诊断计时不是验收计时"**口径与我方 48 分析的测量链纪律同构。
- 关联：flexonafft 09-30 16:57 重打包 V43 时自报"EXP277/278 runtime 失败、live_rating_guarantee=None"（49 行 35）——与本篇源内自报时检失败互证。

---

## 五、榜位轨迹（ahmed·track = 队 "track"，TeamId 16687649，成员 a2nt1as2n/ahmedberatozer/omerlleez）

来源：战役内各 LB CSV 快照实读（同名行程序化提取）：

| 快照（UTC） | Rank | Score | LastSubmission |
|---|---|---|---|
| 09-24 API 单页（ladder-trajectory 转录） | #1495 | 1905.8 | — |
| 09-29 13:41:16Z | #5322 | **701.1**（换交暂态） | — |
| 09-30 17:41:44Z（sweep6 快照） | #531 | 2083.9 | 09-30 12:48:44 |
| 09-30 17:53:03Z（49 引用点） | #539 | 2075.2 | 09-30 12:48:44 |
| 09-30 23:31:06Z（lb_final） | #422 | **2135.0** | 09-30 20:28:30 |
| 10-02 10:45:33Z（本篇最新） | #471 | 2091.8 | 09-30 20:28:30 |

读法：701.1→2075/2083 的"已收复"是换交暂态回归（49 判定沿用）；**截止前 7h 他家又交了 1 件（20:28:30），从 2075 拉到 2135（+60）后终评窗 Elo 收敛回落 2091.8**。我方 1796.2 不变（无新交），相对差 +295.6（10-02 读数）。与 49 表"+279.0"一致量级。**该队最后一小时仍在换件**——ahmed 的 V57（09-22）之后无新 kernel，但提交动作到截止前 3h：榜上活跃版本很可能高于公开 V57（"公开件≠提交件"第 8 例）。

---

## 六、情报增量与可学点（绿区过滤）

1. **血统裁决证据链**（§3.1）→ G4 可收口：归源更新呈用户裁决。
2. **评测纪律三口径**可直接抄：①门失败如实入册（V41 CI 过零降级、V42/EXP277/278 时检失败保留）；②"反应面板≠独立强队/剔除自对阵后重算"的自设限界；③"共享进程计时≠验收计时"。——并入 49 P1 评测协议整包的对手侧同证。
3. **机制绿区残件**：清队列拓扑手术（EXP334/335，正对 P2 `[]` 空槽实验）、黎明仓溢定向回收（EXP277，正对 P4 产出-消化平衡）。
4. **版本纪律观察**：ahmed 全系每版"只动一个市场参数/加一层"（V45/V55/V57 均单变量）+ 门失败不发版——与我方"单件消融"仪器四件套同构；其 V54 大回退（弃 V53/54 分支换公开最强谱系）显示**谱系聚合是头部公开玩法**。
5. **下档必查**：track 队 10-07/10-15 是否开源收尾件/拆解（成员 3 人：a2nt1as2n、omerlleez 尚无公开件——开号监控名单补 2 人）。

---

## 七、来源清单（均 2026-10-02 12:05–12:10 UTC 抓取）

| # | 来源 | 通道 | 戳 |
|---|---|---|---|
| S1 | https://www.kaggle.com/code?user=ahmedberatozer（kernels list --user） | kaggle CLI 2.2.4 | 2026-10-02 12:05Z，36 件快照存 `ext/ahmed_deepcut/kernels_list_2026-10-02.csv` |
| S2 | https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v{23,25,31,34-57}（26 件，ref 见 provenance 表） | kernels pull -m | 2026-10-02 12:05–12:07Z |
| S3 | 解码源 `extracted_main/`（26 件，25 件 sha 与作者声明一致） | 程序化提取 | 2026-10-02 12:08Z |
| A1 | `fn_work/legacy_software/kaggle_simulations/v48_derivative/main.py`（dadee25a，解包 12 模块+6 磁带实读） | 本地只读 | 2026-10-02 |
| A2 | `fn_docs/provenance_dadee25a.md`、`fn_docs/behavior_inventory.md` G4、`fn_docs/references/digests/public-bot-reverse-eng-20260920.md`、`opponents/PROVENANCE.md`、`v48plus/README.md` | 档案复读 | 2026-10-02 |
| A3 | 榜位轨迹：lb_final/…23:31:06.csv、results/…17:53:03.csv、ext/lb-20261001/…17:41:44.csv、ext/postseason-platform/lb_20261002/…10:45:33.csv、results/2026-10-01-ladder-trajectory.md | 档案复读 | 2026-10-02 |

## 需登记行（INDEX.md，勿在本篇代改）

1. `references/ext/ahmed_deepcut/`（provenance.md + SHA256SUMS.txt + 26 ipynb/metadata + extracted_main 26 解码源 + kernels_list 快照）｜kaggle CLI kernels list/pull｜2026-10-02｜ahmed·track 补深挖全量归档；25/26 解码源 sha 与作者声明一致
2. `references/2026-10-02-ahmed-deepcut.md`｜本轮｜2026-10-02｜V48 谱系 24 层机制清单+dadee25a 血统字节裁决（kaitofukami v48 Fast Routes，非 ahmed V48 下游）+V43 EXP277-279 机制自报+榜位轨迹
