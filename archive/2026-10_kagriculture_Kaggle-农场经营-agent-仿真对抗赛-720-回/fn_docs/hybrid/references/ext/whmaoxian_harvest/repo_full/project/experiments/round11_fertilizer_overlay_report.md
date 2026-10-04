# 第 11 轮：闲置雇工施肥候选，未激活而否决

候选 [round11_fertilizer_overlay.py](round11_fertilizer_overlay.py)，SHA256 `006e0b582bba4ce5a021b1284bcaeec1a40601f57d2f835776206271c4f67789`；从冻结 V9 原样复制并追加 [tail](round11_fertilizer_overlay_tail.py)。方案只允许当天无后续原生任务、当前动作 `PASS` 的雇工在确定会于当夜增产的草莓/番茄上施肥，且须已持有肥料，或可在不占用已知原生投入的前提下取 1 份肥料。它不购买肥料，也不猜未开的商店。

两个官方 720 步烟测：`217881086` 和草莓报价较高的 `1193292362`，双方均 `DONE`、无 stderr、终局均与 V9 自战打平；候选的 `tasks_started`、`fertilize_requests`、`confirmed_fertilized` **全为 0**。[高草莓烟测](round11_fertilizer_overlay_smoke_high.json)中记录的 62 个 `FERTILIZE` 物理动作全是继承 V9 的动作，不能记作候选增量。候选未证明实际增产、入仓或增售，因此不进入开发赛程、不晋级、不提交。

官方刷新逻辑在 `kaggle-environments==1.32.7` 中同时以 `production_count > max_yield` 限制持续作物产出次数，并以 `yield_units` 上限限制地块存量；候选的成熟期边界依此计算。V9 及第 10、11 轮确认/备用赛程未改动。

后续按“原样跑一局、逐回合统计挡板”的 [诊断脚本](round11_fertilizer_overlay_diagnostic.py)复核高草莓世界：30 个回合存在已浇水、当夜可增产且未施肥的地块；16 个回合通过价格门槛，其中 **15 个回合所有雇工都有非 `PASS` 任务**，仅余 1 个回合的 `PASS` 工人还有后续原生任务。主挡板是真实劳动饱和，并非未来任务保护范围过宽。若强行改写，必须牺牲原 V9 的物理工作；按这次实验边界不做 V2。
