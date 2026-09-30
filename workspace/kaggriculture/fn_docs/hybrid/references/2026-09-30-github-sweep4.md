# 2026-09-30 GitHub/Web 频道线上扫查册（第四轮：09-29 19:40Z → 09-30 05:20Z，开源兑现+可复刻专题）

> 任务：kaggriculture 战役线上增量扫查（GitHub/Web 频道第四轮），窗口=09-29 19:40Z（基线 2026-09-30-github-sweep3）之后的站外新增量；扫查面 1 开源兑现核查（逐名）与 3 可复刻清单为不限窗专题。截止 09-30 23:59 UTC（抓取时余 ~18.6h）。
> 抓取日期统一 **2026-09-30**（05:18-05:45Z）。通道：GitHub REST API（认证 search/users/repos/code、commits/contents/trees/events、raw）+ HN Algolia + YouTube 结果页/watch 页 + DuckDuckGo html。
> 纪律：逐条带来源 URL+抓取日期；自报数字标"自报"；查不到写"未找到"；候选改善项带证据等级（A/B/C/D）与分析37 §一禁区标注（1 跨拍卖时移动；2 巨量晚抛；3 计划层抄作业+小幅 mix；4 路线表裸换线；5 镜像提前卖/启发式重排/持货等峰值；6 番茄门/PET 无门；7 公开件增量移植；8 剪毛错峰防御；9 学习式/神经网络）。**复刻授权口径（本轮）**：Apache 可移植署名 / 无许可走干净室。工作件在 /tmp/scan8/（未入仓）。

---

## 一、扫查面 1：开源兑现核查（逐名，2026-09-30 05:20Z 核）

**结论：截止前 ~18.6h，十名全数未落地。** 逐名（users+repos+code 三通道）：

| 名字 | 结果 |
|---|---|
| Majkel1337 | **未找到**（users 0、repos 0）；`majkel` 用户存在（2011 建）**0 公开仓 0 公开事件**（updated 2023） |
| DSM | **未找到**（"DSM kaggriculture" repos 0；全库 code 命中仅 Wangyh666 `reverse/profiles/dsm.md` 画像件=他方转述） |
| Tufa | **未找到**（repos 1125 全噪声；"Tufa kaggriculture" users/repos 0） |
| SpTaro | **未找到**（SpTaro repos 0；sptaromaru 账号存在 **0 公开仓 0 事件**，updated 2023-05） |
| UMG | **未找到**（UMG repos 4837 全噪声；UnknownMotherGoose 账号存在 **0 公开仓 0 事件**，updated 2025-09） |
| 4th | **未找到**（"4th kaggriculture" repos 0） |
| DECEM | **未找到**（DECEM repos 全噪声 December 系；"DECem kaggriculture" 0） |
| Rudra | **未找到**（Rudra repos 全噪声；"Rudra kaggriculture" users/repos 0） |
| yaphellee | **未找到**（users 0；账号直查 404；code 0） |
| akimaru | **未找到**（akimaru repos 13 全噪声；`akmr` 账号 0 仓（2023）、`akimaru` 账号 2 仓全无关（2016 PHP SDK）；"akimaru kaggriculture" users 0。旁证：`Yizhou` 账号=无关人（Claude 插件作者，9 仓无 kagri 件）） |

- 389 仓名/owner/description 正则复扫 **0 命中**（沿 sweep3 口径）；code search 按名+kaggriculture 共现 **0 新命中**。
- **开源承诺兑现：仍未落地。** 距截止 <19h，若顶强在截止后开仓，兑现窗口仍在截止后——**截止后必须再扫一轮**（与 sweep3 触发一致）。

## 二、扫查面 2：GitHub 增量（09-29 19:40Z 后）

**总量**：`q=kaggriculture` 389 仓（与基线持平，净 0；created>09-28 仍为 raju-sah/Aayush033/Manav 3 件全存量）。**19:40Z 后有推送 2 仓**（05:20Z 拉取）。

### 重点深读

1. **doanthuan/kaggriculture — step1009 复刻三连发（Apache-2.0，本轮最大可复刻件）**（https://github.com/doanthuan/kaggriculture ，pushed 2026-09-30T00:51:39Z，抓取 2026-09-30）：
   - **09-30T00:41:35Z `Switch to tetsutani step1009 with a deeper sale look-ahead`**（https://github.com/doanthuan/kaggriculture/commit/b3251226 ）：情报（自报）——**tetsutani 09-28 重发 step1009，天梯被其复制品灌满**（6 局近期败局回放=step1009 或近变体；对 horizon-48 构建 72-82% 小胜）；复刻件=step1009+**`_S809_LOOK` 3→12**（ready-stock 销售前瞻加深，"v9 race horizon 对新构建无效但 look-ahead 层有效"），seeds 9500-9529 对 plain step1009 **85%**；第二槽变体 `_S738_LOOK=8+_S809_LOOK=8` 对 plain 80%、对 main.py H2H 57%。`agents/public/tetsutani_step1009.py`=未改上游文件。
   - **09-27T23:48:38Z `Replay top teams' ladder games as route plans`**（https://github.com/doanthuan/kaggriculture/commit/f0cbd39f ）：tools/tape.py=**录影带对手**（回放录制 episode 单席于原种子；录得单位数 turn 级锁定+贷款垫付保同步，score 净贷款）；tools/tape_ledger.py=钱账本（"leaders run eight geese where we run two"）；proto/leader.py=tetsutani 底盘+**Boey 录像路线库按店铺解锁选路**+地追平+逃逸喂工+末回合甩卖，184 tapes 胜 52.7%（均 +$1.8k，自报），ref 56613129。
   - **09-27T01:43:40Z `Race premium sales 48 turns ahead`**：V9_RACE 44→48（复刻微调），seeds 9300-9339 对 plain tetsutani 65%（自报）；clone_counter.py 否证（外挂 overlay 负于 plain——父级已预留 44 层）。
   - README（09-30 抓取）：主 agent 持 prvsiyan《Kaggriculture Frontier | The Moon Counts Melons》Apache-2.0 件（LICENSE+NOTICE.txt 随 tar 提交=**署名移植合规样例**）；`agents/public/` 公开对手池 13 件（ahmed v48/55/57、aurax7_v5、farm2945、haideptry 2965hybrid、haodou ledger v68、metav4_v13、prvsiyan melons、shiiin9 orderbook、tetsutani demand+step1009）+tools/eval.py（胜率评测：双席 n 种子、draws 0.5、last-callable 载入同梯口径）。
2. **homeshwarnelakurthi/Kaggriculture — V44-V52 崩盘四因实录（09-22 内容，19:42-19:47Z amend-repush 无新内容）**（https://github.com/homeshwarnelakurthi/Kaggriculture/commit/115417a6 ，2026-09-30 核）：一独立线 09-15→09-22 连发 9 版全"离线赢、上梯掉分"（2546.9→1727.3，−826 分）；V44 胜 V43 24-0 仍掉 399 分。四因：**①按币差排名而赛事只记胜负**（V47 因少输 132 币发过 0 胜/8 局件）②只对前一版比、无固定锚→9 级链式爬坡漂移③4-20 局小样本 vs ±74 rating 噪声带④弱对手（barnyard +83k~99k）膨胀均值。真信号被压：最强池手（wide）连 4 版 0 胜仍照发。处置=V43 原件重发（ref 56471368，哈希核对）+tools/ladder.py 梯况工具。（事件核：19:42:32Z 推 ade59759、19:47:05Z 回推 115417a6=同内容 amend，无隐藏增量）
3. **graceyunliu/kaggriculture — evolve 3 新跑批（results 分支 03:45/04:25/05:06Z）**（https://github.com/graceyunliu/kaggriculture/commits/results ，抓取 2026-09-30）：最新 https://raw.githubusercontent.com/graceyunliu/kaggriculture/results/evolve/reports/20260930-002712.md （run 002712，0.64h/40 候选/7,932 局，KAGG_FIXED_SHOPS=1 口径）：held-out PASS **894 不动**（平台期）、头部 +15.1k~+16.0k vs frontier 但对 clone 全线 −11k~−13k；**消融表复现稳键**（MELON_MORNING 1→0、ROUTE_LEN 3→2、CROP_SWEEP_LEN 6→8、HERD_LAST_DAY 17→20、NEAR_RADIUS 2→5 在 ≥4 候选重复出现）；诊断列新格式（day22-29 drivers：sales_rev/missed_water/idle_turns 拆分）。
4. **THLPH/Kaggriculture_AdvancedFarmer — RL_Lion 新分支**（https://github.com/THLPH/Kaggriculture_AdvancedFarmer/tree/RL_Lion ，创建 09-29T18:24Z、push 至 09-30T02:38Z，抓取 2026-09-30）：RL_Lion/Kaggriculture_RL_v2、v2_1、RL_LION 三 notebook+mp_worker.py 29KB（"real env RL"）→ **禁区9 仅记录**。

### 在册仓核对（19:40Z 后无新推送，2026-09-30 核）

mooman0222（**e094+ 未出现**，末次 18:03Z E092/E093）、devasad67-lgtm（09-28 单提交后静默）、pranav-bot（末次 09-29 17:38Z telemetry 后静默）、yen-ghub（14:48Z）、raju-sah（09-29 10:50Z）、ShashankJangid（06:30Z）、Wangyh666-ust（**09-27 后仍无 v49+**）、Applied-Agent-Works（16:12Z）、smarino76（13:45Z）、Manav（18:46Z）、wmar-dev（v20+ 仍未出现）等全部无增量。graceyunliu 主分支亦静默（增量在 results 分支）。

## 三、扫查面 3：可复刻清单（本轮新发现件逐个）

| # | 件 | 策略/内容 | 许可→复刻路径 | 复刻难度 | 预期价值 | 禁区 |
|---|---|---|---|---|---|---|
| 1 | doanthuan step1009+_S809_LOOK=12 复刻件 | 公开旗舰底座+ready-stock 销售前瞻 3→12 步加深；对 plain 85%（自报） | **Apache-2.0**（LICENSE+NOTICE 随 tar）→可移植署名；上游 tetsutani 件同仓内嵌未改版 | 低（单参数层；M13 型依赖闭合需自查） | **P4 对照基线刷新**（step1009=天梯新常态指纹）；look-ahead 层外证 B | 策略参数移植=禁区7；只作对照/家族证据 |
| 2 | doanthuan tools/tape.py 录影带对手 | 单席回放+turn 级单位锁定+贷款同步；184 tapes 路线库对照 | Apache-2.0→可移植署名 | 中（依赖 kaggle-environments 本地包+replays 下载管线） | **P4 评测尺升级**：与我方 frozen-rival paired 同构、且给出"对手不可下载"时的替代口径 | 评测基建合法（A3） |
| 3 | doanthuan tools/eval.py+agents/public/ 池 | 双席种子胜率（draws 0.5、last-callable 同梯）+13 公开强手池 | Apache-2.0→可移植署名 | 低 | P4 评测尺/A1 对手库（池含 step1009=新指纹族锚点） | 评测基建合法 |
| 4 | homeshwarnelakurthi V44-V52 四因 | 币差 vs 胜负计分错位/链式爬坡漂移/小样本/弱对手膨胀 | **无许可→干净室**（仅方法论复述） | 低 | **BT 终评口径输入**：终评=两周 BT 胜负赛，币差尺失效先例；P4 反面清单 | 方法论引用合法 |
| 5 | graceyunliu 消融稳键表（09-30 3 runs） | MELON_MORNING=0/ROUTE_LEN=2/CROP_SWEEP 8×4/HERD_LAST_DAY=20/NEAR_RADIUS=5 | 无许可→数据事实引用 | 低 | A1/C7 数据燃料（参数后验） | 仅数据 |
| 6 | （存量补录）Vineet5-Data/Obsidian_git `_attic/_sweep15.py` | BUY5 型扫查脚本（08-22 停更） | 无许可→干净室 | — | BUY5 指纹族旁证（族Z 已录） | 仅记录 |
| 7 | （存量补录）Ryo0326-hub（09-13 停更）/IMINABO1（09-17）/Beiciccc（08-09） | Majkel 自适应组合研究+Cycle 回归教训 / journal+clone-gated eval / C30-C35 精确字节·随机·对照实验系列 | 无许可→干净室 | — | 评测方法论史（Beiciccc 对照设计可作 P4 参考） | 仅记录 |

## 四、扫查面 4：资料增量（收官文/教程/评测/BT 终评方法论）

- **BT 终评方法论：未找到站外新件**。DDG 三组查询（"kaggriculture Bradley-Terry/final evaluation/终评"、"kaggriculture 总结/复盘/攻略"、"kagriculture tutorial"）**0 相关命中**；HN Algolia 字面 0（3 命中全 agriculture 噪声）；YouTube 16 结果逐个看表全为 06-21~08-13 存量（Imitation Training/Concept Demo/Conformance Suite/Feasibility Advisor/Vibe Coding 等，无窗口内新视频）；dev.to/zenn/Qiita/掘金沿 sweep3 口径无新增（未再复扫）。**终评口径仍只有仓内文本**：竞品"只记胜负、榜单显示最高分 bot、最近 2 提交入终评"（analysis22）+ 截止后两周 BT（analysis39/43）+ 本轮 homeshwarnelakurthi 币差失效实录。
- **收官文：站外未找到**；本轮最佳收官文本=doanthuan 三连 commit message（step1009 灌满天梯的天梯侧观察=终交潮态势一手）。
- **新教程/评测件：未找到**（pranav-bot docs/creating-agents.md 仍为唯一教程件，无新版）。

## 五、候选改善项（证据等级+禁区标注）

1. **step1009 天梯新常态指纹**（doanthuan 复刻验证 85% 胜 plain+"天梯被复制品灌满"，自报+可核方法学，证据 B）→ A1 画像新增指纹族（step1009 系）；我方 MODELPX/收官件需按"对手=step1009 变体"重估。禁区7 已关：其 `_S809_LOOK` 参数不移植。
2. **tape 录影带对手+路线库选路**（证据 B，Apache-2.0）→ P4 评测尺升级素材（tape 单席锁定口径 vs 我方 frozen-rival；路线库按店铺解锁选路属 A1 条件路由合法形态）；**库表内容不移植**（禁区4/7）。
3. **BT 终评=胜负口径**（homeshwarnelakurthi 币差尺失效四因，证据 A/B：ref 56471368 可核）→ P4/终验尺确认：**胜率>币差**，与我方 P4 胜率主尺一致；对其余臂的币差排序结论降权。
4. **graceyunliu 稳键消融复现**（证据 A 文件可取）→ C7 参数后验；对 clone 仍全线 −11k=其 frontier 派生对录像系无效，反证"clone 系（第三农场俱乐部/Majkel tape）不可用参数消融打穿"。
5. THLPH RL_Lion、graceyunliu evolve 引擎 → **禁区9**，仅态势记录。

## 六、限制与未复核清单

① doanthuan 85%/65%/52.7%、graceyunliu +15k 均自报未我方复核；② homeshwarnelakurthi 19:42Z ade59759 已由 API 取回（与 115417a6 同内容，确认无隐藏增量），但 git 历史细节（force-push 原因）未证；③ X/推特+nitter 反爬不可用（沿口径）；hustileailab 403 未复核；④ Vineet5-Data/Ryo0326/IMINABO1/Beiciccc 四件为存量补录（窗口外停更仓），未逐文件精读；⑤ YouTube 表为结果页 16 条抽样，可能有未入样新视频；⑥ 389 仓持平+0 新建=本窗口纯存量仓增量；⑦ e091 跳号、e094 是否私有提交未获证；⑧ 开源兑现核查以 GitHub 为限（Kaggle 侧开号由 kaggle 频道轮复验）。
