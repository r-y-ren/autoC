# 过滤抽查清单（clone 过滤人工核对用）

- 本队名（语料实测，频次最高）：`renyxin`
- 克隆判定：开局 turns 1-51 动作流（replay steps[1..51]，farmer+hands+market 规范 JSON）sha256（64 hex）== v48 家族路由前缀签名
（参照 routes.json 6 条路由，实测合并为 1 个有效签名——六路由前 88 步共享前缀）。
- 抽样：层状确定性（自博弈 3 局 / 克隆命中 17 局 / 其他 162 局，各取 episode id 升序前 4，不足顺延），本清单 12 局。

| 局 id | 席 | 队名 | 判定 | 依据 | 结果 | 终局边际 |
|---|---|---|---|---|---|---|
| 111278140 | 0 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111278140 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111873568 | 0 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111873568 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111979240 | 0 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111979240 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111302976 | 0 | renyxin | own_team | TeamNames==renyxin（本队名） | W | 46.0 |
| 111302976 | 1 | Aashka Kapadia | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | L | -46.0 |
| 111307477 | 0 | renyxin | own_team | TeamNames==renyxin（本队名） | L | -128.0 |
| 111307477 | 1 | EdwardHwang@123 | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | W | 128.0 |
| 111313034 | 0 | Rishabh Roy | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | D | 0.0 |
| 111313034 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111325325 | 0 | renyxin | own_team | TeamNames==renyxin（本队名） | L | -1648.0 |
| 111325325 | 1 | Rudransh Singh Rathore | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | W | 1648.0 |
| 111452441 | 0 | xmkevin2004 | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | L | -1916.0 |
| 111452441 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | W | 1916.0 |
| 111779236 | 0 | renyxin | own_team | TeamNames==renyxin（本队名） | L | -72.0 |
| 111779236 | 1 | habe.sq | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | W | 72.0 |
| 111911261 | 0 | Aashka Kapadia | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | D | 0.0 |
| 111911261 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | D | 0.0 |
| 111913520 | 0 | HHHyyds | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | W | 53.0 |
| 111913520 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | L | -53.0 |
| 111914682 | 0 | BHackers | clone_v48 | 前51步哈希 37841b2618739a58188ac3c852267bcb7a082125b306d106f1ba7cf4ffca0bfe == v48 前缀（路由 bakery_capital/default/farm_fast/yarn_fast/yarn_second/yarn_third） | L | -1813.0 |
| 111914682 | 1 | renyxin | own_team | TeamNames==renyxin（本队名） | W | 1813.0 |

- 全库：{'games': 182, 'total_seats': 364, 'kept': 162, 'excluded': {'own_team': 185, 'clone_v48': 17, 'other': 0}, 'kept_by_category': {'full': 162}}
