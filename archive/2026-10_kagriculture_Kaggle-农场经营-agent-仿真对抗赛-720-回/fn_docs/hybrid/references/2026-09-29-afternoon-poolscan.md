# 2026-09-29 午后池面采用扫查册（第三轮·"策略公开与采用潮"）——11:15Z 晨扫截稿后的公开增量 + 池面同源采用指纹

> 任务：查 09-29 午后新增公开情报，定位"谁公开了什么、谁在批量采用"。窗口 **09-29 11:15Z → 14:05Z**（榜面快照 13:44:46Z）。
> 通道：kaggle CLI 2.2.4（kernels 全量翻页×608 件 / topics list+show / datasets list / leaderboard download / **team-submissions+episodes+replay 跨队回放指纹**）+ REST API（Bearer，credentials.json 缓存 token）+ GitHub REST。
> 纪律：逐条带来源 URL+抓取日期（均 2026-09-29）；自报标"自报"；我方解包/重算标"重算"；查不到写"未找到"；工作件在 /tmp/scan3/（未入仓）。基线=2026-09-29-kaggle-channel-scan.md、-github-channel-scan.md、2026-09-28-family-topband-deepcut-scan.md。

---

## 〇、直接回答："策略公开了吗？谁在批量采用？"

**午后公开面零新增**：11:15→14:05Z 无新 kernel/新 run（唯一 guru 13:09 为纯重跑）、无新讨论帖、无策略分享/评测帖、GitHub 无战略级推送、顶强未开号、Wool Front-Runner 系反制件无新版本。"今日午后有人放出新策略"**不成立**。

**"公开件被批量采用"成立，采用潮现在进行时**（回放指纹实锤，见二）：
1. **同源运行时采用实锤**：sadanamaru（#235，今日 11:31 提交）与 haideptry/prairieee（#1446）、leoprovorov 本人（#1357）、**我方 H1** 前 72 步行动迹逐字节同哈希（sha72=7af65472f33a，跨世界/跨对手稳定）——即 step1009 同门底盘开局书族新增一名今日第三方采用者（其分 1334→2387 收敛爬升中）。采用对象=公开件（tetsutani promoted bytes / leoprovorov MarketShock-M1-WR1K 运行时，经 flexonafft v106、haideptry v12 打包）所在的同门底盘系。
2. **真正把同门带打沉的是第二波血潮——BUY5 族**（`BUY_ANIMAL COW 1 + BUY_PRODUCT WHEAT 5` 开局，mooman 分类"BUY5 型"在册）：M&M&P&Q(#1)/Vadim(#5)/akmr(#9)=akimaru/Yizhou(#10)=yaphellee/monsaraida(#14)/Ueddy(#29)/unreal(#30)/アナコンダ(#63)/high frequency farming(#79) 今晨 06:47→午后 13:40 **集体新交终件并集体大涨**。该族公开出处**未定位**（cha22 公开件重算为 BUY20/SELL15 旧 frontier 开局，非此族）。
3. **第三波：BUY10/SELL10 便宜开局系**（senkin13/Mositaku/Constantin/Jun_value，10:30-10:49 集中提交，收敛 2300-2400）——与 devasad67 公开仓"便宜开局 [BUY 10, SELL 10, BUY 5 WHEAT]"一致（C 级归因，未逐字节核）。

## 一、公开面增量对照（vs 晨扫 11:15Z）

| 面 | 增量 | 判定 |
|---|---|---|
| kernels（608 件全量翻页 diff） | 仅 guruprasaathas111/game-theoretic-master-discrete-optimization 13:09 重跑；SHA ed89be8c 与晨扫 v3 **逐字节同**（重算）=纯重跑无内容增量 | **无新公开件** |
| 新建 kernel | 0（全 608 件均有 run 时间戳，无"发布未跑"件） | 未找到 |
| votes 增量（11:15→13:45） | icefire v24 +5（95→100）、haideptry shepherds +3、kaggricult-man +3、god-s-mode +2、tetsutani +2、cha22 +2，余 +1 | 常态关注，无爆款 |
| 讨论区 | 744287（08:19）后**无新帖**；744219 新增 11:13 Navneet 无内容回复（"@linkinpony 感谢信息"）；743993 无新回复（仍 6）；744277 评论止于 08:21 | **无策略分享/评测帖** |
| GitHub（388 仓，与晨扫同） | 3 推送：smarino76 13:45 "Update documentation and add semantic features"（skim）；yen-ghub 12:01 "early Melon pair on day 9 against 5-Melon openers"（终局微操续）；graceyunliu results 分支 13:53 evolve 报告（frontier=O162_THREE_SHOPS65=THIRD FARM CLUB 克隆，本地 GA，无新 tape） | 无战略级 |
| 数据集 | 仅 dariushafshar/kaggle-competition-leaderboard-intelligence 13:01 更新（榜形面板 235 行 57 字段，跨赛情报非策略）；官方日包 09-29 版 00:03 已在晨扫 | 无策略件 |
| 顶强开号 | Majkel1337/majkel1337/SpaTaro/tarosqrd2/Boey/UnknownMotherGoose/akimaru/yaphellee/vadimvasilenko/ku0807/gauravgs1007/monsaraida/sadanamaru 名下 kernels 全 "Not found"；senkin13 仅 2023-2025 他赛旧件无 kaggriculture 件（kernels list --user 复验） | **仍未开号** |
| Wool Front-Runner 系反制件 | haideptry/countering-the-big-3-meta 等无新 run/新版（608 件 diff 内无） | **未找到新版本** |

## 二、池面同源采用指纹（本轮新方法：跨队回放指纹）

**方法**（重算）：`team-submissions <team_id>` 任意队可查（双活跃提交+实时 publicScore）→ `episodes <sub_id>` → `replay <ep_id>` 下载（34MB/件）→ 对目标队 agent 前 24/72 步（farmer+hands+market 全动作）拼接取 SHA256。**有效性验证**：同件 2 局（不同世界/不同对手）sha24/sha72 完全相同（leoprovorov/sadanamaru/haideptry/我方 H1 各 2 局）→ 前 72 步为**剧本化开局书（世界无关）**，跨队同哈希=同底盘同源强证据（非完整运行时同一性，见限制）。

| 族 | 成员（回放取样 18 队） | 指纹 | 采用判定 |
|---|---|---|---|
| **族X 同门底盘书（BUY8/SELL3+BUY_SEED WHEAT 1）** | leoprovorov #1357（12:08 新交）、haideptry/prairieee #1446（00:32）、**sadanamaru #235（11:31 新交）**、我方 H1 #829 | **sha72 全同 =7af65472f33a**（sha24=01a785b15bee） | **sadanamaru=今日新增同源采用者实锤**；leoprovorov/haideptry=MarketShock-M1-WR1K 公开/打包线（晨扫在册） |
| 族Y 便宜开局变体（BUY10/SELL10→BUY_SEED…） | senkin13 #237（10/10/BUY_SE…）、Mositaku #281（8/8）、Constantin #208（6/1）、Jun_value #298（10/10+次拍 BUY WHEAT 30） | 步 1 变体、步 2-5 与族X 同构（同底盘+开局替换）；sha24 互异 | 集中提交 10:30-10:49，收敛 2300-2400；与 devasad67 公开仓便宜开局一致（C 级归因） |
| **族Z BUY5 型（BUY COW1+BUY WHEAT5）** | Vadim #5、Ueddy #29、unreal #30、アナコンダ #63、highfreq #79、M&M&P&Q #1、monsaraida #14、akmr #9、Yizhou #10（近支） | sha24 互异（同开局不同实现/版本），步 2-5 族内近同（PICKUP COW→SELL WHEAT 1→HIRE×5→BUILD_PASTURE→PLACE COW） | **top 段集体新交终件、集体大涨=换血主力**；公开出处未定位；mooman"BUY5 型 7-3"口径在册、graceyunliu tapes.json 有 vadimvasilenko 同开局 tape |
| 其他 | masayoshi #182（BUILD_PASTURE 开局）独立；flexonafft Igor Zharov #2583（10:11，1444.1）族X 侧近支 | — | flexonafft 榜位仍低（1447.5） |

**旁证（重算）**：haodou V89 源 7041 行 `orders[:2]==[['BUY_PRODUCT','WHEAT',8],['SELL','WHEAT',3]]`+`orders[2:]==[['BUY_SEED','WHEAT',1]]`=族X 开局检测自检；cha22 公开件 `V9_OPENING_STEP0=(("BUY_PRODUCT","WHEAT",20),("SELL","WHEAT",15))`=旧 frontier 开局（非族Z）。step0 小麦买/卖换流动性开局书在池面呈多数量变体扩散（20/15、13/30/30、10/10、8/8、8/3、6/1）=机制级采用潮痕迹。

**名册新情报（LB members 字段，实据）**：akmr=**akimaru**（顶强名单在册者，#9 还在涨）；Yizhou=**yaphellee**；Attention Is All You Seed（#40，+90）=aurax7 等 5 人队；haideptry 队=haideptry+prairieee 双人；M&M&P&Q=morimo/msd0110/piiiiiiiii/qistripute；Happy Farm=alexesn 等 4 人；high frequency farming=gunhcolab/hweowe/markslavin；Mositaku=versavice；Nathan Jacob #955=nathanjacob（pipe 系公开作者）。

## 三、榜面涨跌对照（11:15:09Z → 13:44:46Z）

**同门带（继续下沉但趋缓）**：Georgy 2180.7→2150.9（−29.8，#606）；Lynxx 2028.3→**1999.3**（−29.0，#952，**09-27 后无新交=纯被刷**）；tetsu2131 2073.0→2064.2（−8.8，#797，09-27 后无新交）；Alperen Aydın 1932.5→1912.8（−19.7）；我方 H1 2069.5→**2053.0**（−16.5，#829）；statma 1786.3（−9.6）/prvsiyan 1778.3（−3.3）/shiiin9 2116.1（−10.7）平缓；**haodou 1594.3→1639.7（+45.4，V89 收敛上行）**、Alperen Söylen 2114.2（+30.4，另一人）、guruguru000 2103.5（+40.3）。

**大涨（族Z 为主）**：Yizhou 2767.2→2874.5（**+107.3，#27→#10**，13:06 又新交）；Vadim 2835.2→2926.0（+90.8，**#13→#5**）；aurax7 队 2613.9→2703.9（+90.0，#40）；Ueddy +86.6（#57→#29）；unreal +63.1（#53→#30）；monsaraida +46.3（#24→#14）；akmr +31.1（#10→#9）；Gordeev Max +25.9；abozten +25.3；M&M&P&Q +25.1（#1 稳）。

**下沉**：DSM −51.4（12:54 新交 2112.4 收敛中勿读死）；TKNP −39.1；DECEM −30.3；Anton Tikhonov −28.8；Boey −21.7；yuto083 −25.0（13:09 新交）；**leoprovorov −228.5（2075.4→1846.9，12:08 新交 1329 收敛中拖低）**。

**机制注记**（重算自 team-submissions）：①榜分=双活跃提交取高（Yizhou max(2870, 1408)=2874.5 等）；②11:15 后仍有数百件实时出分（13:40 仍在进件），in-window 提交=队列释放补跑+截止（09-30 23:59Z）前终交潮；③新交读数 40-70 局才收敛（多数队已 46-135 局），大额 dScore 多为收敛噪声；④新队 3：molspace #3577 1118.7（13:15）、Maksymilian Dec #8521（11:36）、Kurapapa #9706（12:07）。

## 四、结论行（对照分析37 §一禁区）

1. **判定**："策略公开→池面批量采用"**部分成立**：公开发生在昨夜-今晨（MarketShock-M1-WR1K 打包件/tetsutani promoted bytes/便宜开局/G793），采用潮午后进行时——实锤=sadanamaru 今日入列同源族（sha72 全同）；但**同门带普跌的主因是 BUY5 族终件换血**（tetsu/Lynxx 拿 09-27 旧件挨刷，族Z 全员今晨-午后换新件）+ 评级漂移，而非"单一公开策略被批量套用定向压制"。
2. **[禁区7 登记不移植]** sadanamaru 同源采用=公开件增量移植面再添一例（横测 0/6 维持）；其 2387 收敛值提示族X 底盘+外挂仍能进 2300+，与 mooman"公开系天花板 2000-2100"口径并读（其分未收敛，勿引）。
3. **[A1 素材]** 族Z BUY5 开局书=我方完全无对应开局变体的对手大类（top30 半壁），建议列为 P4 回放择优/A1 画像必采指纹族；其公开出处待下轮（截止后开源潮）定位。
4. **[运维]** 13:40 仍实时出分；744277"无需重交"持续有效，勿因 pending 重交烧配额（实录烧 1 sub 在案）；我方读数按 40-70 局口径。
5. **[C 级]** 便宜开局（BUY10/SELL10）被池面批量吸收迹象=devasad67 公开仓外溢的旁证，只登记。

## 五、来源清单（均 2026-09-29 抓取）

| 来源 URL | 通道 | 版本/读数 |
|---|---|---|
| https://www.kaggle.com/code/guruprasaathas111/game-theoretic-master-discrete-optimization | kernels pull 全文 diff | 13:09 重跑，SHA ed89be8c 同晨扫 v3 |
| kernels 全量 608 件（kaggle kernels list --sort-by dateRun/dateCreated 翻页）+ votes diff | CLI | 11:15 后仅 1 重跑 |
| 顶强开号复验（Majkel/SpaTaro/Boey/UMG/akimaru/yaphellee/vadimvasilenko/ku0807/monsaraida） | kernels list --user | 全 "Not found" |
| https://www.kaggle.com/competitions/kaggriculture/discussion/744277 、/744219 、/743993 （topics list/show 全量 100 帖） | CLI topics | 无新帖；744219 11:13 新回复 |
| https://github.com/smarino76/Kaggriculture/commit/b6b944a2 、https://github.com/yen-ghub/kaggriculture-agent/commit/58f3b5b3 、https://github.com/graceyunliu/kaggriculture （results 分支 evolve/reports/20260929-095309.md） | GitHub REST | 3 推送 triage |
| https://www.kaggle.com/datasets/dariushafshar/kaggle-competition-leaderboard-intelligence （13:01 版下载） | datasets list/download | 榜形面板，非策略 |
| https://www.kaggle.com/competitions/kaggriculture/leaderboard | leaderboard download | 快照 2026-09-29T13:44:46 vs 11:15:09 |
| team-submissions/episodes/replay（18 队 35 提交 26 回放：Yizhou/Vadim/Ueddy/unreal/senkin13/Mositaku/sadanamaru/masayoshi/flexonafft/haideptry/leoprovorov/アナコンダ/highfreq/M&M&P&Q/akmr/Constantin/Jun_value/monsaraida + 我方 H1 双局验证） | CLI 新用法 | 指纹 sha24/sha72 见二 |
| https://www.kaggle.com/code/abhinav0370/cha22-agent （pull 解读 V9_OPENING_STEP0）、/tmp/scan_k/haodou_v89_main.py 7041 行（晨扫缓存重读） | kernels pull/本地缓存 | 开局书归属旁证（重算） |
| [前次] 2026-09-29-kaggle-channel-scan.md、2026-09-29-github-channel-scan.md、2026-09-28-family-topband-deepcut-scan.md | 见各篇 | 基线 |

## 六、限制

① 72 步同哈希=同底盘开局书同源，**不等于完整运行时同一性**（72 步后行为未比对；族Z 成员 sha24 互异但开局同族，可能为同架构不同实现）；② 族Y 与 devasad67 便宜开局的对应为形态级（C 级），未做其仓源码逐字节对照；③ 族Z 公开出处未定位；④ 回放取样 18 队/26 局非全池，排名段覆盖偏 top300；⑤ publicScore 全部为实时未收敛读数（40-70 局口径），"大涨"含收敛成分（尤 leoprovorov −228、DSM −51）；⑥ 12h 内 token 端点 429 限流一次（改用 credentials.json 缓存 Bearer 续扫，22:51Z 到期）；⑦ georgymarin 拉取 403 持续、ashok205 数据集 403 持续，未复扫。
