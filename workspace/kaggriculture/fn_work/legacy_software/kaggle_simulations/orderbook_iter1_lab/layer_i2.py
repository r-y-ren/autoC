# ---- 件 I2：HERD 报价门控卖序 + COURIER 当日可送品优先出（statma 精简移植） ----
# 形态：尾块注入件（构建时文本拼接进提交源，与基座同命名空间）；本文件为块体
# 片段，不含宿主捕获/入口（由 build_iter1.py 组装）。仅用基座裸名
# （_ix_projected 由共享段提供）；stdlib-only。
#
# 语义移植自 statma ca25（sha c4b72e64…）的 HERD/COURIER 两件（v9 家族）。
# **只移植订单层/守卫层可表达的部分**（任务口径）：
# - HERD 报价门控卖序：羊毛/奶报价 ≥150 + 店铺结构才换畜种的门（源件
#   _v9_herd_choose 同口径）→ 门开时把"计划外卖量"按源件卖序放头
#   （源件 _v9_herd 的 rewritten.insert(0, SELL product extra)）：
#   extra = 同拍投射仓 − 现挂卖量 − 磁带余计划卖量；报价 ≥2 才出；
# - COURIER 当日送卖=当日可送品优先出：源件"送达单元进首卖槽"的市场面
#   （V9_COURIER 送达→market.insert(0)/原单加量挪头，按报价×量降序）推广到
#   **当日入仓品**（同拍投射仓较拍前净增的 COURIER 品目）：优先出（首槽）。
#   仅 hour>=12（源件 V9_COURIER_FROM_HOUR）且 step<718 生效。
#
# **不可移植（如实报，不硬做）**：HERD 产线换畜种（BUILD_COOP→BUILD_PASTURE、
# BUY_ANIMAL/PICKUP/PLACE GOOSE→SHEEP/COW 指令改写）= 磁带手术级，非订单/守卫
# 层可表达；COURIER 的走位送货（worker 路径+DROP 时机）= 物理层，同不可移植。
# 本层只动 market 订单，零跨拍挪量（R23/R26 红线），不改 farmer/hands。
#
# 零足迹纪律：门关/无可改/异常 → 返回原动作对象（同对象）。触发面：每拍记
# herd/courier 门开、插量/挪头次数与单元数（judge 汇总）。
_I2_REPORT = dict(calls=0, changed_turns=0, herd_gate_open_ticks=0,
                  herd_inserts=0, herd_insert_units=0, herd_no_extra_ticks=0,
                  courier_ticks=0, courier_boosts=0, courier_boost_units=0,
                  courier_inserts=0, courier_insert_units=0, courier_hoists=0,
                  errors=0)

_I2_HERD_MIN_WOOL = 150         # 源件 V9_HERD_MIN_WOOL（羊毛报价门）
_I2_HERD_MIN_MILK = 150         # 源件 V9_HERD_MIN_MILK（奶报价门）
_I2_HERD_MAX_EGG_SHOPS = 1      # 源件：羊置换 ≤1 家 BAKERY+BRUNCH_SPOT
_I2_HERD_MAX_EGG_SHOPS_COW = 0  # 源件：牛置换 ≤0 家
_I2_HERD_MIN_MILK_SHOPS = 3     # 源件：牛置换 ≥3 家 PIZZA/ICE_CREAM/SMOOTHIE
_I2_COURIER_ITEMS = ("STRAWBERRY", "MILK", "WOOL", "MELON")   # 源件 V9_COURIER_ITEMS
_I2_COURIER_FROM_HOUR = 12      # 源件 V9_COURIER_FROM_HOUR


def _i2_reset():
    _I2_REPORT.update(calls=0, changed_turns=0, herd_gate_open_ticks=0,
                      herd_inserts=0, herd_insert_units=0, herd_no_extra_ticks=0,
                      courier_ticks=0, courier_boosts=0, courier_boost_units=0,
                      courier_inserts=0, courier_insert_units=0, courier_hoists=0,
                      errors=0)


def _i2_qty(raw):
    """挂量解析：int/整值 float→int；bool/其余→None（不确定，保守保留）。"""
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, float) and raw.is_integer():
        return int(raw)
    return None


def _i2_herd_product(obs):
    """HERD 报价门（源件 _v9_herd_choose 同口径）：≥150 报价+店铺结构。

    返回 'WOOL'/'MILK'/None（门关）。只读公开面（town/market）。
    """
    try:
        shops = ((obs or {}).get("town") or {}).get("unlocked_shops") or []
        prices = ((obs or {}).get("market") or {}).get("prices") or {}
        egg_shops = sum(s in ("BAKERY", "BRUNCH_SPOT") for s in shops)
        if (egg_shops <= _I2_HERD_MAX_EGG_SHOPS and "YARN_STORE" in shops
                and int(prices.get("WOOL", 0)) >= _I2_HERD_MIN_WOOL):
            return "WOOL"
        milk_shops = sum(s in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP")
                         for s in shops)
        if (egg_shops <= _I2_HERD_MAX_EGG_SHOPS_COW
                and milk_shops >= _I2_HERD_MIN_MILK_SHOPS
                and int(prices.get("MILK", 0)) >= _I2_HERD_MIN_MILK):
            return "MILK"
        return None
    except Exception:
        return None


def _i2_planned_sells(obs, item, step):
    """磁带余计划卖量（源件 _v9_herd 同口径）；拿不到→0（宁紧勿松：少放量）。"""
    try:
        player = int((obs or {}).get("player", 0))
        native = _IMPL.chassis.players.get(player)
        if not native or native.get("route") not in _IMPL.chassis.routes:
            return 0
        planned = _IMPL.chassis.future_sells(native["route"], item, step + 1)
        return max(0, int(planned or 0))
    except Exception:
        return 0


def _i2_post(observation, action):
    """HERD 报价门卖序 + COURIER 当日可送品优先出（同拍后处理）。

    输入: 当前拍 observation+宿主动作 / 输出: 调整后动作（无可改=原对象）/
    错误: 异常吞掉回退原动作（同对象零足迹）。
    """
    _I2_REPORT["calls"] += 1
    try:
        if not isinstance(action, dict):
            return action
        market = action.get("market")
        if not isinstance(market, list) or not market:
            return action
        try:
            step = int((observation or {}).get("step", 0))
        except Exception:
            step = 0
        if step == 0:
            _i2_reset()
        shed_now = (((observation or {}).get("private") or {}).get("shed")) or {}
        proj = _ix_projected(observation, action)
        prices = (((observation or {}).get("market") or {}).get("prices")) or {}
        out = [o for o in market]
        changed = False

        def _selling(item):
            total = 0.0
            for o in out:
                if isinstance(o, (list, tuple)) and len(o) >= 3 \
                        and o[0] == "SELL" and o[1] == item:
                    q = _i2_qty(o[2])
                    if q is not None:
                        total += max(0, q)
            return total

        # ---- HERD 报价门控卖序（源件 insert(0, extra) 语义） ----
        product = _i2_herd_product(observation)
        if product:
            _I2_REPORT["herd_gate_open_ticks"] += 1
            stock = max(0, int(proj.get(product, 0) or 0))
            extra = stock - _selling(product) - _i2_planned_sells(observation, product, step)
            if extra > 0 and int(prices.get(product, 0)) >= 2 and len(out) < 10:
                out.insert(0, ["SELL", product, int(extra)])
                changed = True
                _I2_REPORT["herd_inserts"] += 1
                _I2_REPORT["herd_insert_units"] += int(extra)
            else:
                _I2_REPORT["herd_no_extra_ticks"] += 1

        # ---- COURIER 当日送卖=当日可送品优先出（源件 首槽/加量挪头） ----
        hour = step % 24
        if hour >= _I2_COURIER_FROM_HOUR and step < 718:
            delivered = []
            for item in _I2_COURIER_ITEMS:
                delta = int(proj.get(item, 0) or 0) - int(shed_now.get(item, 0) or 0)
                if delta > 0:
                    delivered.append((item, delta))
            if delivered:
                _I2_REPORT["courier_ticks"] += 1
                delivered.sort(key=lambda kv: -float(prices.get(kv[0], 0)) * kv[1])
                for item, delta in delivered:
                    stock = max(0, int(proj.get(item, 0) or 0))
                    spare = stock - _selling(item)
                    if spare <= 0:
                        continue
                    n = min(int(delta), int(spare))
                    if n <= 0:
                        continue
                    existing = None
                    for o in out:
                        if isinstance(o, (list, tuple)) and len(o) >= 3 \
                                and o[0] == "SELL" and o[1] == item:
                            existing = o
                            break
                    if existing is not None:
                        q = _i2_qty(existing[2])
                        add = n if q is None else min(n, int(spare))
                        if add <= 0:
                            continue
                        out.remove(existing)
                        if q is None:
                            out.insert(0, existing)      # 不确定挂量只挪头
                            _I2_REPORT["courier_hoists"] += 1
                            changed = True
                            continue
                        out.insert(0, ["SELL", item, q + add])
                        changed = True
                        _I2_REPORT["courier_boosts"] += 1
                        _I2_REPORT["courier_boost_units"] += add
                        _I2_REPORT["courier_hoists"] += 1
                    elif len(out) < 10:
                        out.insert(0, ["SELL", item, n])
                        changed = True
                        _I2_REPORT["courier_inserts"] += 1
                        _I2_REPORT["courier_insert_units"] += n
        if not changed:
            return action          # 同对象零足迹
        _I2_REPORT["changed_turns"] += 1
        return dict(action, market=out)
    except Exception:
        _I2_REPORT["errors"] += 1
        return action          # 异常吞掉回退原动作（同对象零足迹）
