# 2026-09-30 Kaggle 频道第三轮扫查册（终交潮增量）——14:05Z 午后扫查后的公开增量 + 改进线索

> 任务：扫 09-29 14:05Z 午后扫查（基线=2026-09-29-afternoon-poolscan.md）之后的 Kaggle 频道增量，回答"有无新公开策略/代码、我方版本（mpx 焦窗件 h14-22 + oc_c3）还有改进方向吗"。窗口 **09-29 14:05Z → 19:46Z**（榜面快照 19:46:18Z；截止 09-30 23:59Z）。
> 通道：kaggle CLI 2.2.4（kernels list 全量翻页 dateRun/dateCreated + kernels pull ipynb 解包 diff + topics list/topic-messages + leaderboard download + team-submissions + datasets list/view）+ REST API（Bearer，credentials.json 缓存 token，22:51Z 到期）。
> 纪律：逐条带来源 URL+抓取日期（均 2026-09-29）；自报标"自报"；我方解包/重算标"重算"；查不到写"未找到"；工作件在 /tmp/scan5/（未入仓）。基线=afternoon-poolscan + kaggle-channel-scan + github-channel-scan。

---

## 〇、直接回答

**"有无新公开策略/代码？"——无全新公开策略。** 本窗口唯一"新代码"是 **guru v4 + flexonafft v107 双双换装打包 lynnsakurai "Farmer John and the Idle Seller"（Step1010 idle-seller）**，其内嵌 main.py（1,148,715B，SHA 03165654）与基线 09-28 family-topband-deepcut 已解包的 lynnsakurai 内嵌件**逐字节同**（重算）——即旧机制新打包，非新策略。leoprovorov ice v25/god v27 纯重跑（与 v24/v26 逐字节同）；evgendvorkin v32 无新版。

**开源兑现（重点①）未提前落地**：743993（"Will the submissions be open sourced after the competition ends?"）仍 6 回复无新回复；顶强开号复验 Majkel1337/akimaru/yaphellee/vadimvasilenko/monsaraida/ku0807/tarosqrd2/UnknownMotherGoose/masspeaks 名下 kernels 全 "Not found"，DSM 三子（denden12/shimishige）仅他题旧件、linkinpony 仅 dinov3 旧件。**顶强仍未开号**（与 GitHub 频道"兑现窗口在截止后"互证）。

**我方版本改进方向**：本窗口**未暴露可打我方 mpx 焦窗形态的新机制**。Step1010 reorder loop=基线已在执行面覆盖的"同回合同卖单槽序重排"（V44Y/CXD/OR2 系），非新杠杆。唯一弱线索=对手池向 idle-seller 收敛→市场行为保守可预测（详见四）。

## 一、公开面增量对照（vs 午后 14:05Z）

| 面 | 增量 | 判定 |
|---|---|---|
| kernels 新 run（dateRun 全量，14:05Z 后） | 5 件：evgendvorkin 19:31 / leoprovorov ice 19:06 / leoprovorov god 19:05 / guru game-theoretic 18:10 / flexonafft 16:28 | 5 新 run |
| 内容 diff（ipynb cell-source SHA，重算） | leoprovorov ice **v25=v24 逐字节同**（ba3baee8）；god **v27=v26 同**（b9381a9f）；evgendvorkin v32 无新版=纯重跑 | **无内容增量** |
| guru game-theoretic v3→**v4** | 整体换装：v3=自家"Pure Uncompressed V49"（sha ed89be8c）→ v4=**打包 lynnsakurai "Farmer John and the Idle Seller" Step1010**（Provenance 明文+PAYLOAD_B85 内嵌） | **有增量（换装）** |
| flexonafft multi-route v106→**v107** | v106=打包 leoprovorov MarketShock-M1-WR1K（lzma）→ v107=**换装 lynnsakurai Step1010 idle-seller**（同 provenance，同 1,148,715B main.py） | **有增量（换装）** |
| 新建 kernel | 0（dateCreated 全量 100 件无"发布未跑"空 run 件；dateRun 全 160 件均有 run 戳） | 未找到 |
| votes 增量 | icefire +6（100→106）、flexonafft、guru、evg 票微动，无爆款 | 常态 |
| 讨论区 | **新帖 2**：744364（15:26，7 回复）、744380（16:32，3 回复）；743993 无新回复（仍 6）；744277 队列帖票 10→14（已 RESOLVED）；无官方评估/终评方法论帖 | **无策略分享/开源帖** |
| 顶强开号 | Majkel/akimaru/yaphellee/vadim/monsaraida/ku0807/tarosqrd2/UMG/masspeaks 全 "Not found"；DSM/linkinpony 仅他题旧件 | **仍未开号** |
| 数据集 | **新 1 件**：manjunadhpadarthi/farmbench-artifacts（19:41，FarmBench 15 经济决策评分器，评测基建非策略）；官方日包 09-29 版**未出**（最新 09-28 00:03）；georgymarin 00:10 版仍 403；leoprovorov dashboard 无新版 | 1 新分析件（评测类） |

## 二、Step1010 idle-seller（guru v4 / flex v107 共同打包件）——重点③ MarketShock 采用潮后续

**采用潮转向（重算）**：基线（09-29 kaggle-channel-scan）MarketShock-M1-WR1K 采用潮=flexonafft v106 + haideptry v12 打包 leoprovorov 运行时。**本窗口 flexonafft（16:28）与 guru（18:10）双双把打包对象换成 lynnsakurai "Farmer John and the Idle Seller"**，且 provenance 逐字相同（retrieved September 29, 2026）。即**公开打包群体从"leoprovorov MarketShock"轴心转向"lynnsakurai idle-seller Step1010"轴心**，自报口径"two wins against MarketShock on seed 290911, +1401 cash each"（自报未复核）——打包者声称 idle-seller 压过 MarketShock。

**机制（重算解包 main.py 1,148,715B，SHA 03165654=基线同件）**：provenance 称 "Step1010, based on the accepted Step1009 production controller. Its **bounded reorder loop detects stable orders and cycles while preserving farm commands, market quantities and inventory constraints**." 源内实证（行级 grep）= 多代同回合同卖单槽序重排层并存：`_r37_reorder_sales`(L1827)、`_v44y_reorder`(L6121，"replay the engine's per-slot/per-unit lockstep for SELL and BUY_PRODUCT")、`_cxd_reorder`(L6862)、`_OR2`/`V219`、`E182 last-seven-turn physical closure planner`(712-718)。核心=**只重排 SELL 单槽序抢同回合成交，货量/库存/农田指令保持不变**（"preserving market quantities and inventory constraints"）。

**归属再认定（重要）**：午后池面扫查把族X"step1009 同门底盘开局书族"（sha72=7af65472f33a，leoprovorov/haideptry/sadanamaru/我方 H1 共享）暂记于"MarketShock-M1-WR1K 打包线"。本件 provenance+SHA 证实该底盘实为 **lynnsakurai "Farmer John and the Idle Seller"（Step1009→Step1010）**——leoprovorov/haideptry 的 MarketShock 亦内嵌/沿用此 idle-seller 底盘。故"同门带共用底盘=lynnsakurai idle-seller"，非 leoprovorov 原创。

## 三、讨论区增量（2 新帖，均为方法学杂谈，非策略/开源）

1. **744364** "Advice needed, Directory filled with previous agents and old strats / reports"（https://www.kaggle.com/competitions/kaggriculture/discussion/744364 ，09-29 15:26，7 回复）：新手问迭代 agent 时目录污染/旧策略残留；回复=git 分支/删 bloat/迁移摘要。**非游戏策略**。旁注（17:30 一回复）："my agent had been referring to very old submissions which were scoring much higher as a 'submit agent recommendation'"——agent 污染工作流现象，运维级，无战略价值。
2. **744380** "Do you use RL to train the executors, or the agents as a whole?"（https://www.kaggle.com/competitions/kaggriculture/discussion/744380 ，09-29 16:32，3 回复）：RL 训练单元（executor vs 整体）。**唯一技术点**（16:37 一回复）："fixing the shops per seed is important in RL for paired comparisons — otherwise your agents may learn the causal (unintended) effect that weeds have on the shop (letting your own plant die is best because in a paired world future shop rolls turn out better cause they share the same RNG seed list)"——**配对评测须按 seed 固定商店，否则学到杂草→商店滚动的伪因果**。对 P4 评测尺/A1 配对比较有直接方法学价值（C 级）。
3. **743993 开源帖后续：未找到新回复**（仍 6，Syed Asad Ali top-50 价格信号论为最新）；官方评估/终评方法论帖（742856 系）无新回复；744277 队列运维帖已 RESOLVED 无新关键信息（"无需重交"持续有效）。

## 四、榜面变动（13:44:46Z → 19:46:18Z，重算 team-submissions+leaderboard CSV diff）

**前 30 涨跌**：DSM 2982.9 **#3→#1**（+23.7，denden12/masspeaks/shimishige 16:13）；M&M&P&Q 2980.4 **#1→#2**（−103.3，15:42 新交收敛噪声勿读死）；DECEM #2→#3；Vadim #5→#4、Boey #6→#5、UMG #8→#6、Yizhou #10→#7（+4.5）、tetsuya 组 #13→#8、monsaraida #14→#11、akmr #9→#12；**新面孔 Zenith（proptiter）#13**；**matsu997 #14（+862.9，#1056→#14，15:28 新交收敛暴涨）**、seek inspiration（kurupical）#30（+247.6，#132→#30）=大额收敛回补；Victor@Tufa #4→#17（−130.9，16:47 新交收敛下行）；Majkel #7→#10（−54.7）；TheEggman #15→#29（−61.6）。族Z（BUY5）系集体缓降（Ueddy #29→#37、unreal #30→#39、Attention #40→#43）但 Yizhou/monsaraida/tetsuya 上行。

**同门带（继续下沉）**：Georgy 2150.9→**2065.5**（−85.4，#606→#701，06:19 无新交=纯被刷）；tetsu2131 →1970.7（−93.5，#797→#932）；Lynxx →**1899.4**（−99.9，#952→#1108，09-27 后无新交）；shiiin9 →2049.6（−66.5）；Alperen Aydın 1918.8（+6.0）；statma 1971.8（+185.5，13:58 新交收敛上行）；haodou 1630.5（−9.2，V89 收敛中）；leoprovorov（AlekseiProvorov）1799.6（−22.9，12:08 新交收敛拖低）。

**我方（renyxin TeamId 16784420，#1255）**：team-submissions 双活跃件 **56685146=1848.8**（18:51:02）+ **56685176=1503.0**（18:52:11），榜面取高 **1848.8**。两件均 **18:51 新交（窗口内）**，快照时仅 ~1h 局数，**未收敛**——按 40-70 局口径勿读死（对照基线"峰落 1233→950"模式）。注：ref 56685146/56685176 即当前在飞 mpx+oc_c3 对（任务口径），其读数以收敛后为准。

**机制注记**（重算）：榜分=双活跃提交取高；13:44→19:46 数百件实时出分（终交潮，截止 09-30 23:59Z 前）；大额 dScore（matsu997 +862、seek +247、Victor −131、M&M&P&Q −103）多为新交收敛噪声非实力跳变；新队净增 15（10159→10174）。

## 五、mpx 版改进线索（新情报 vs 我方焦窗形态 h14-22）

**结论：无强反制/无强新杠杆；仅 1 条弱方向 + 1 条归属修正。**

1. **[弱·对手画像]** idle-seller Step1010=保守市场行为（"preserving market quantities and inventory constraints"，只重排槽序不动货量/时点）→ 采用该底盘的对手**卖窗窄而稳、按稳定订单周期出货、平时"idle"**。我方 h14-22 焦窗集中卖可：(a) 在 idle-seller 非出货缺口集中抛、避开其稳定周期强拍；(b) 同回合卖单竞速时匹配其槽序重排优先级抢成交。=A1 画像新指纹族（idle-seller 底盘），与午后 BUY5 族并列必采。证据 C 级（打包 provenance 自述+源码机制核实，无独立战报）。
2. **[归属修正]** 族X 同门底盘=lynnsakurai idle-seller（非 leoprovorov MarketShock）——A1/P4 的对手谱系基线更正：同门带共用底盘的真正出处是公开 idle-seller，其 MarketShock 变体亦在此底盘上。影响 gengame 语料/kinship 谱系预期。
3. **[C 级·P4 方法学]** 744380 "配对评测按 seed 固定商店，否则学到杂草→商店滚动伪因果"——若我方 mpx 焦窗评测用配对同种子，须固定 seed 商店序列，避免 A1 误学伪因果。仅登记。
4. **[不移植]** guru/flex 打包件工程卫生（hash 钉死+LICENSE/NOTICE 保留+双席 smoke）已在基线断言清单在册，本件同族无新增。

## 六、来源清单（均 2026-09-29 抓取）

| 来源 URL | 通道 | 版本/读数 |
|---|---|---|
| https://www.kaggle.com/code/guruprasaathas111/game-theoretic-master-discrete-optimization | kernels pull ipynb diff（v3 缓存=/tmp/scan3/guru_new） | v4 换装 lynnsakurai Step1010 |
| https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent | kernels pull ipynb diff（v106 缓存=/tmp/scan_k/flexo） | v107 换装 lynnsakurai Step1010 |
| https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible 、/god-s-mode-hacked-stores | kernels pull ipynb diff（v24/v26 缓存=/tmp/scan_k/icefire24、godsmode26） | v25/v27 纯重跑同 |
| https://www.kaggle.com/code/evgendvorkin/kaggriculture-version-31-26-09-bronze-going-up | API kernels/pull currentVersionNumber | v32 无新版 |
| https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-idle-seller （打包件内嵌 main.py 1,148,715B 解包，SHA 03165654=基线同） | b85 解包 tar | Step1010 idle-seller 机制（reorder loop） |
| kernels 全量（dateRun 8 页 160 件 / dateCreated 5 页 100 件）+ votes diff | CLI/API | 新 run 5 件、新建 0 |
| 顶强开号复验（Majkel/akimaru/yaphellee/vadim/monsaraida/ku0807/tarosqrd2/UMG/masspeaks/DSM/linkinpony） | kernels list --user | 全 Not found/仅他题旧件 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/744364 、/744380 、/743993 、/744277 （topics list + topic-messages 全量） | CLI | 2 新帖；743993 仍 6 回复 |
| https://www.kaggle.com/datasets/manjunadhpadarthi/farmbench-artifacts （view+files） | datasets list/view | FarmBench 评测器，19:41 新 |
| 官方日包 https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-2026-09-28 （00:03，最新）；georgymarin/leoprovorov dashboard | datasets list | 09-29 日包未出；georgy 403 |
| https://www.kaggle.com/competitions/kaggriculture/leaderboard （快照 2026-09-29T19:46:18 vs 13:44:46）+ team-submissions 16784420 | leaderboard download + team-submissions | 见四 |
| [前次] 2026-09-29-afternoon-poolscan.md、-kaggle-channel-scan.md、-github-channel-scan.md | 见各篇 | 基线 |

## 七、限制

① Step1010 "two wins against MarketShock +1401/局"、idle-seller 强度全部自报未复核；② guru/flex 打包件内嵌 main.py 与基线 lynnsakurai 件 SHA 同=同件，但 provenance 的 Step1010 vs Step1009 版本标签无法从 1.1MB 源内唯一钉版（源为多代实验层累叠，含 E182/V219/V233/V44Y/OR2/CXD 等历史层）；③ matsu997/seek inspiration/M&M&P&Q/Victor 大额 dScore 为未收敛读数（40-70 局口径），非实力跳变；④ 我方 56685146/56685176 读数（1848.8/1503.0）快照时仅 ~1h 局数未收敛；⑤ ice v25/god v27 "纯重跑"依据=与 v24/v26 缓存 cell-source SHA 逐字节同，非逐行 diff 全文；⑥ FarmBench artifacts 仅读 metadata+文件清单（含 results/rationales.md、states/land_ne_timing.json），未深读评测结论（评测基建非对手策略，价值有限）；⑦ token 22:51Z 到期，本窗口内有效；⑧ 官方 09-29 日包按 00:03 规律将在 09-30 00:03 后出，本轮未覆盖。
