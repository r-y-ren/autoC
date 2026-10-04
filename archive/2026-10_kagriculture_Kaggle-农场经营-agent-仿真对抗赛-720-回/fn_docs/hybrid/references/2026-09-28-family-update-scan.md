# 2026-09-28 同门公开件增量扫描（analysis 调研轮）——晨扫之后的新版/新件

> 任务：核查 09-28 晨扫（2026-09-28-execution-faces-scan.md，截稿约 03:05，其时已收录 haideptry V79 02:13 / haodou V81 02:23 / god-s-mode v23 03:04）之后，同门公开件有无新版本提交、有无新的同门件（关键词：order book/slot/queue/clear queue/market list/same-turn/execution）。
> 抓取日期统一 **2026-09-28**（午后轮）。通道：kaggle CLI 2.2.4（kernels list 按 dateRun 全量排序 + kernels pull + API v1 kernels/pull 取 currentVersionNumber + competitions topics list/show）。
> 纪律：逐条带来源 URL+版本号；自报数字标"自报"；查不到写"未找到更新"。不改仓库代码。

---

## 一、在册同门件版本核查——全部无新版（未找到更新）

方法：`kernels list --competition kaggriculture --sort-by dateRun`（版本保存必触发新 run，lastRunTime 即最新版本时间）；辅以 API `currentVersionNumber` 交叉验证。晨扫截稿（~03:05）后**无任何在册件产生新 run**：

| 件 | 最新版本时间（CLI dateRun） | 版本号 | 结论 |
|---|---|---|---|
| haideptry/the-2965-master-hybrid-engine | 09-28 02:13（晨扫已收 V79） | kernel v16 | 未找到更新 |
| haodou092/kaggriculture-harvest-ledger | 09-28 02:23（晨扫已收 V81） | **81**（与晨扫一致） | 未找到更新 |
| shiiin9/your-market-list-is-an-order-book | 09-21 23:16 | v2 | 未找到更新 |
| uninhibitedscholar/kaggressury-beyond-48-order-sequencing（注：实名 kaggriculture-beyond-48） | 早于 09-24 | v1 | 未找到更新 |
| ahmedberatozer 全系（kaggriculture 最高 V57，09-22 12:50） | 09-22 | — | 未找到更新（其 09-28 07:55 新跑 casmi26-v4g-inference 属他赛题，非 kaggriculture） |
| alperen5252525 三件 | ≤09-19 | — | 未找到更新 |
| guruprasaathas111/top-2-master-engine-v4 | 09-27 19:04（晨扫已收） | — | 未找到更新（但同作者 V5 见二-2） |
| tetsutani/demand-preserving-turn-sale-timing | 09-27 02:50 | — | 未找到更新 |
| lynnsakurai/farmer-john-and-the-idle-seller | 09-27 09:29 | — | 未找到更新 |
| destbreso/x-ray-your-agent | 09-27 23:00（晨扫已收） | — | 未找到更新 |
| georgymarin/kaggriculture-what-2600-farms-do-differently | 09-27 22:10（晨扫已收） | — | 未找到更新 |
| leoprovorov/god-s-mode-hacked-stores | 09-28 03:04（晨扫已收 v23 内容） | v23 | 未找到更新 |

## 二、晨扫后新动作两条 + 晨扫漏收一件

### 1. leoprovorov Part 3《A Song of Ice and Fire | Fixed + Flexible》v22（09-28 07:11 run）——在册外（晨扫只收了 Part 1/2），今晨有新版本说明
来源：https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible （kernel v22，72 票，2026-09-28 pull；配套数据集 leoprovorov/a-song-of-ice-and-fire-interactive-dashboards）。

内容=回放统计研究件（榜单头部队伍"冰与火"分解）+ 末格哈希校验提交件：
- **Majkel1337（榜顶）461 胜局逐命令叠加**：11,828 命令-单位中仅 **906（7.7%）为"冰"**（每局都提交）；其中 63% 属移动类；**种植 3% 冰、市场卖出 1% 冰**——头部卖单几乎纯反应式。**Day 0 是磁带**：首日 99 个命令-单位 87 个冰、平均一致率 93%；day1-6 降到 35-48%，day7 之后 25-32%。首块地购买时点固定（459/461 同拍）。
- **十一支头部队伍 bundle 分歧度**（整回合为一 bundle、同 hands 数+同命令类才计同）：THIRD FARM CLUB 前 6 天一条剧本（step0-72 平均分歧 0.004）；**feel the agi(151)/AI是我的豆包(146)/THIRD FARM CLUB(145) 在第二店开启（step 144）后 7 步内分叉**；Majkel1337(4)/SpTaro(2)/M&M&P&Q(1) 前 4 步即分叉；**剧本最短的 M&M&P&Q 样本平均胜分最高**。
- **64 商店世界**：首两店有序对定义 world；Majkel1337 世界间最长共享前缀=step 145（PET_CAFE→FARMERS_MARKET vs YARN_STORE），全场相似度仅 22.5%；样本小（每 world ≤8 局）自述"是线索不是结论"。
- 方法论（可复用为诊断器）：**分歧曲线三分段**——平段可硬编码、店开虚线处可做公开变量查表、无虚线抬升段才需读状态规则；"我方平在头部抬升处=过刚，我方抬升在头部平段=浪费灵活性"。
- **提交件版本说明（v22 新增，原文）**："The last cell now submits **MarketShock-M1-WR1K**: MarketShock-M1 with one audited day-21 local watering repair and exact parent pass-through everywhere else."——即 d21 局部浇水修复；底座仍是 Seven-Turn Rescue Wide Search（yhay81 shop-router v3 路由 + Tschinkel state router 谱系 + step 712-718 有界终局规划器）。MarketShock-M1 本体机制**不可读**（payload 为 base85+SHA256 校验打包），名字暗示市场冲击向变体，仅作观察项。自报谱系 cred：yhay81/aurax7/Tschinkel，Apache-2.0 NOTICE 齐全。

### 2. guruprasaathas111《Master Engine V5》v3（09-28 02:34 run）——晨扫漏收（只登记了其 V4），谱系=top-2-master-engine-v4 → V5
来源：https://www.kaggle.com/code/guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f （kernel v3，65 票，2026-09-28 pull；标题 "Master Engine V5: Game-Theoretic Market Intelligence & Adaptive Livestock"，自报 95.1% 胜率/+17.5M 净利差，未独立复核）。

与我方关注面的增量（源码行级摘录，均为公开占用格推断、无对手私有库存）：
- **R44 现金响应探针（EXP175，注明改编自 leoprovorov "Two Coins Mirror Counter v1"）**：step 336-648 中，若指纹相似度 ≥0.90 连续 6 拍 → 卖窗提前量 2→3 拍；此时**主动打一发纯 SELL 探针批**（r36_debts 记账 step+3、货值 ≥100），下拍比对双方 money 增量——`own>0 and rival>0 and abs(own-rival)<=max(5.0, 0.05*probe)` 判定镜像克隆 → 卖窗 3→**4 拍**。纯卖探针避免"等额消费误判为抢先"。
- **R37 引卖排序（quote prioritization）**：卖单排序键=**"Revenue exposed to a small rival batch, not nominal headline revenue"**——按对手公开在田 tiles 的同品 yield_units 汇总 × 引擎价格曲线 × 当前市场库存，估"对手小批将砸掉的暴露收入"，暴露大者先卖。
- **R36 多拍卖窗债务账本**（Gluzdov E184 谱系："pulling planned sales 2-3 turns forward captures peak market prices"）+ V224 卖单前置排序（step≥144 起 SELL 前移过 BUY_PRODUCT）。
- 其余：13 路线磁带 step 144 选择（yhay81）、V231 step 216-227 奶牛切换（MILK≥WOOL 且 2 奶店）、V233 d12+ 融资东南 6 羊圈、V234 紧急饲喂、hour 23 room guard（shed ≤99）、step 718 shed 清算。
- 注意：R37/R44 的"镜像卖窗加宽"与 haodou V81 Spatial Mirror Gate（+38.2）同族但触发链不同（指纹 streak + 现金响应探针双门 vs 逐坐标指纹相等单门）；**自报数字全部未独立复核**。

### 3. 讨论区晨扫后仅一新帖（无官方回复、非执行主题）
743993 "Will the submissions be open sourced after the competition ends?"（https://www.kaggle.com/competitions/kaggriculture/discussion/743993 ，2026-09-28 07:02 发，0 回复）——比赛尾段社区对终赛后开源的疑问，与执行面无关。

### 4. 关键词新件检索——未找到新同门件
`-s "order book"/"queue"/"same-turn"/"execution"/"market list"/"slot"` × dateRun 排序：命中最新的均为在册件或上述两件，**未发现晨扫后新公开的执行族 notebook**。

## 三、候选（进提案的增量，已对照"已证负勿推"清单过滤）

1. **镜像门控卖窗的升级触发链（R44 双门阶梯）**：指纹 ≥0.90 streak≥6 → 提前 2→3 拍；纯 SELL 探针 + 双方 money 增量匹配 → 3→4 拍。区别于已判死 PREDICT：不做对手来单预测，只用公开指纹 + 自家探针响应。与晨扫候选 2（haodou 门控）同臂，提供"分级而非一刀切 7 拍"的实现口径（B 级：V5 自报 95.1% 未复核；haodou +38.2 中位 0）。
2. **冰火分歧诊断器（评估基建）**：把我方 agent 多 seed 的 turn-bundle 分歧曲线叠到头部曲线（THIRD FARM CLUB 6 天剧本 / Majkel1337 day0 93% 一致）上判"过刚/过柔"——服务晨扫"执行精度判决实验设计"，也再次印证头部 d21-28 卖单纯反应式（1% 冰）。数据入口=ashok205 top10 回放归档（在册）。
3. **R37"对手暴露收入"排序键（谨慎）**：与已证负的"启发式重排"同族——仅当槽位编排臂以回放择优（Layer D 口径）为主体时，可把"对手暴露收入"作为候选排序先验喂给回放评估，不建议独立上线启发式重排。

## 四、未找到 / 限制

① 在册 12 件晨扫后全部无新版（第一节表）；② 无新执行族 notebook/讨论帖；③ MarketShock-M1 提交件 payload 哈希打包不可读，机制仅知"day-21 局部浇水修复"一行说明；④ V5 的 95.1%/+17.5M、R36/R37/R44 各层效果均为自报且无分层消融披露；⑤ ice-fire 件 461 局/十一队口径为该作者自算（配套数据集可复核但本轮未复算）；⑥ CLI dateRun 与 API lastRunTime 两口径不一致时以 CLI（更新）为准，版本号以 API currentVersionNumber 为准。

## 五、来源清单（均 2026-09-28 抓取）

| 来源 URL | 通道 | 版本 |
|---|---|---|
| https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible | kernels pull（markdown+末格构建代码全文） | v22 |
| https://www.kaggle.com/code/guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f | kernels pull（全文源码） | v3 |
| 其余在册件版本核查 | kernels list --sort-by dateRun + API v1 kernels/pull（currentVersionNumber） | 见第一节表 |
| https://www.kaggle.com/competitions/kaggriculture/discussion/743993 | competitions topics list/show | — |
| [前次] 2026-09-28-execution-faces-scan.md（晨扫基线与已证负清单） | 见该篇 | — |
