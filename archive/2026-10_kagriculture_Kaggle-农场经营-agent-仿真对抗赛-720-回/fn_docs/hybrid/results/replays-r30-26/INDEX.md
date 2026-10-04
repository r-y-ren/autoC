# 语料：26 局 round-30 线上局集 strip 归档（S3 门③ seated 重演最小输入，2026-09-23）

## 来源与筛选
- 局集清单：`../2026-09-23-round30-read.json` → `round30.games`（26 局，W/L=21/5，无 T；席位 0×11/1×15）。
- 源件：本机 `/tmp/r30/episode-<ep>-replay.json`（round-30 拉取 41 件中的 26 件；round-29 的 15 件已按清单排除，如 112403139）。
- 源件单件 ~30MB 全量双席观测，26 件 ~780MB，远超预算——存 strip 最小投影（json.gz）。

## strip 形态（kaggle-replay 兼容子集，门③直接可驱）
- `steps[0]`（head）双席**逐字保留**（孪生 `new_state_from_replay_head` 需要：farms/market.inventory+prices/town/day/hour/双席 private/status）。
- `steps[t>=1]`：seat0=`{action + 共享最小观测}`、seat1=`{action}`（`replay_transition_actions` 只读 action，兼容不改码）。
- 共享最小观测 = step/day/hour/market.inventory/双席 private/双 farms（含双方资金与 tiles）/town.unlocked_shops——两席位共享 market/farms/town（实测逐步相等），private 逐席真实分化（早期相同系起始对称）。
- 顶层：`info` **逐字**（`twin.new_state_from_replay_head` 从 `info.seed` 取杂草/商店 RNG 真种子——缺它会回落 seed=0 导致重演漂移，已实测踩坑修正）、configuration/rewards/statuses/final（终局资金+双席 private）。
- **seed 可得性**：26/26 局 `info.seed` 在场（`configuration.seed` 恒 null 是官方惯例，真种子在 info）——门③ seated 重演可用真种子驱动。

## 保真验证（归档后置，26/26 通过）
每件经孪生引擎 `build_state_from_replay(strip,0)` + `run_to_end(自身动作流)` 整局重演，
**终局双席资金与 rewards 逐位一致**（26 局总耗时 5.0s，约 0.19s/局）。
即 `replay_action_diff`（门③a）可直接以本目录语料驱动 L1/verbatim 双 callable 重演对比。

## 体积登记
- 26 件合计 **5343914 字节（约 5.34MB）**；单件 184814 - 229577 字节。全量观测形态无需降级抽样（预算 <10MB 达成）。

## 清单（按局号升序；margin=我方终局差；src_sha256=源件）
| ep | 对手 | 我席 | 结果 | margin | seed | strip(字节) | src_sha256 |
|---|---|---|---|---|---|---|---|
| 112429867 | bvgr | 1 | W | 55346 | 1825501814 | 217066 | `31cbf305b0006f9e` |
| 112431033 | Florian | 0 | W | 50950 | 2013941152 | 214222 | `744ae11309f2b053` |
| 112432199 | Artur Markosyan | 1 | W | 770 | 786146079 | 187560 | `ab3de7379bd0e4ae` |
| 112433355 | Thiago Munhoz da Nóbrega | 0 | W | 36166 | 1883261866 | 224169 | `2f92baf765033d9c` |
| 112434475 | NALLA SUMANG | 0 | W | 33721 | 963182245 | 219105 | `d57eca7b12adb0c0` |
| 112435662 | Oiti Roy | 0 | W | 51580 | 240876256 | 221676 | `1606e1cc5027a531` |
| 112436859 | Shubham Phapale | 0 | W | 21841 | 1705553586 | 229577 | `7fa8c1b30e2a5a86` |
| 112438060 | hanhan761 | 1 | W | 4794 | 2009279466 | 198416 | `5f0adc3d5e0a75d5` |
| 112439305 | mohui666 | 1 | W | 43808 | 161402123 | 227913 | `b6e52bf1100b608f` |
| 112440436 | kaito ide 31 | 1 | W | 5147 | 435866961 | 215912 | `241d8753829cd64d` |
| 112440493 | Sai Syam | 1 | W | 55 | 841473039 | 192045 | `c32bcea9902a9940` |
| 112441644 | Yuchuan Ding | 0 | W | 6556 | 1388158282 | 212980 | `10d549ecbc17fbec` |
| 112442810 | Alvaro Llamojha | 0 | W | 2864 | 1647385154 | 192031 | `9dae162c7d057e26` |
| 112443969 | Bldr2 | 1 | W | 8982 | 671940665 | 197250 | `c71a79c2ddf9506b` |
| 112445139 | MAOSEN  | 0 | L | -9859 | 219073637 | 217741 | `639f19b0b2467b97` |
| 112446302 | wind | 1 | L | -11302 | 1439493993 | 191867 | `5f6228789f67cf1c` |
| 112447520 | MOHAMMADJAFAR ZAMANI | 1 | W | 5628 | 1360429471 | 212127 | `04552ae66db216d7` |
| 112448710 | nyayassist | 1 | W | 5454 | 671494671 | 207848 | `a124ac4fa0e85c71` |
| 112449890 | tagokoro | 0 | W | 3554 | 1900972921 | 191133 | `af9eddb49bc93eb5` |
| 112451110 | Jacob Alstrup | 1 | W | 2209 | 973657130 | 193817 | `079aec21b67c66ac` |
| 112452290 | leave you | 1 | L | -3207 | 1911990026 | 228152 | `cd7f0ae31f4b40d7` |
| 112453461 | Satkar sarvankar | 1 | W | 6773 | 1918725083 | 194059 | `0e535bb7e77a2b29` |
| 112454627 | Dude and Destroy | 1 | L | -3229 | 176568822 | 197734 | `5e69bb9c27a398f4` |
| 112455881 | trantrikien239 | 1 | L | -194 | 427304807 | 184814 | `b115b0583e0121c5` |
| 112457053 | 抵扣豆浆 | 0 | W | 1174 | 720683523 | 187942 | `6f20377e2ed50a1c` |
| 112457102 | 先过我的Gemini | 0 | W | 943 | 906608145 | 186758 | `93a376ce911e35bf` |
