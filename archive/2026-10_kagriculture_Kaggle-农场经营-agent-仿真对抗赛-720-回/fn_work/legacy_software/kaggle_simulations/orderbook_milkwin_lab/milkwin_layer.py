# ---- 件 MX：MODELPX 参数级实验层（牛奶窗变现实验） ------------------------
# 形态：尾块注入件（构建时文本拼接进 oc_c3 提交源，与宿主同命名空间）；本文件为
# 块体片段，不含宿主捕获/入口（由 build_milkwin.py 组装）。仅用基座裸名
# （projected_shed/FarmView/_S758_HIST/_S804_HIST/_RACE_STATE 由 oc_c3 提供）；
# stdlib-only。
#
# 语义（任务 milk-window 口径，参数级·守恒零跨拍红线不碰）：
# - 阈位：MODELPX 压力测试 p_next<p_cur-__MX_THR__（基线 0.5；扫描 -0.2 更敏
#   /-1.0 更钝）。基座 4 处同名比较全部同参替换（基座三档 hour-1 克隆共享）。
# - 帽位：MODELPX 量帽三档（基线 3/6/10）→ MILK 侧加权放大（6/12/20 或
#   10/20/30）；STRAWBERRY/WOOL 保持 3/6/10。基座档位式（默认 max(1,planned
#   //2)/planned/10）与 hour-1 无条件 10 全部同参替换（_mx_cap/_mx_cap_h1），
#   价格模型 planned=6 原样保留（只动量帽不动预测模型）。
# - 窗内地毯（__MX_CARPET__ 开关；臂 3 条件加跑）：d14-20（step 336-480）内
#   MILK 日新高追加单放开（帽 20/步）——当日窗内公开价追平/刷新日内高点即加
#   挂（p_now>=day_max，每日首窗拍视为首高）；只加同拍挂卖（零跨拍挪量
#   R23/R26 红线）、量限同拍投射仓未挂余量、同拍买侧 MILK 存在不动、满 10 单
#   不加新单（maxMarketOrdersPerTurn 不截既有单）、回写 MODELPX 自挂簿记防
#   自卖误判对手流；异常吞掉回退原动作（同对象零足迹）。
# - 其余一切（画像器/C3/终局清算/磁带 blob）零触碰。

_MX_THR = __MX_THR__
_MX_CAPS = {"MILK": __MX_CAP_MILK__,
            "STRAWBERRY": __MX_CAP_OTHER__, "WOOL": __MX_CAP_OTHER__}
_MX_CARPET_ON = __MX_CARPET__
_MX_WINDOW = (336, 480)     # d14-20 窗（任务口径 step 336-480）
_MX_CARPET_CAP = 20         # 地毯追加单步帽 20 件
_MX_STATE = {}
_MX_REPORT = dict(calls=0, carpet_steps=0, carpet_orders=0, carpet_units=0,
                  errors=0)


def _mx_get(obj, key, default=None):
    """观察字段读取（dict/Struct 双形态；异常→default）。"""
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)
    except Exception:
        return default


def _mx_reset():
    _MX_STATE.clear()
    _MX_REPORT.update(calls=0, carpet_steps=0, carpet_orders=0, carpet_units=0,
                      errors=0)


def _mx_cap(item, p_now, step, planned):
    """MODELPX 量帽三档（默认/中/高）：基线 (3,6,10)=max(1,planned//2)/
    planned/10 逐档等价；planned 仅基座语义等价用（价格模型不参改）。"""
    c1, c2, c3 = _MX_CAPS.get(item, (3, 6, 10))
    if p_now >= 100:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 30:
        return c3
    if (step % 24) in (10, 11, 12, 13) and p_now >= 10:
        return c2
    return c1


def _mx_cap_h1(item):
    """hour-1 各档基座无条件 10=高档帽；参数化取该品 c3。"""
    return _MX_CAPS.get(item, (3, 6, 10))[2]


def _mx_post(observation, action):
    """窗内地毯：d14-20（step 336-480）MILK 日新高追加单（帽 20/步）。
    输入: 当前拍 observation+宿主动作 / 输出: 追加后动作（无可改=原对象）/
    错误: 异常吞掉回退原动作（同对象零足迹）。"""
    try:
        if not _MX_CARPET_ON:
            return action
        _MX_REPORT["calls"] += 1
        step = int(_mx_get(observation, "step", 0) or 0)
        if not (_MX_WINDOW[0] <= step < _MX_WINDOW[1]):
            return action
        if not isinstance(action, dict):
            return action
        mkt = _mx_get(observation, "market", {}) or {}
        prices = _mx_get(mkt, "prices", {}) or {}
        p_now = int(prices.get("MILK", 0) or 0)
        if p_now <= 1:
            return action
        player = int(_mx_get(observation, "player", 0) or 0)
        st = _MX_STATE.setdefault(player, {"day": -1, "day_max": -1})
        day = step // 24
        if st.get("day") != day:
            st["day"] = day
            st["day_max"] = -1
        if p_now < st.get("day_max", -1):
            return action                     # 非当日新高
        st["day_max"] = p_now
        market_orders = [list(o) for o in (action.get("market") or [])]
        for o in market_orders:
            if len(o) > 1 and o[0] == "BUY_PRODUCT" and o[1] == "MILK":
                return action                 # 同拍买侧存在→不动（保守）
        selling = 0
        hit = None
        for o in market_orders:
            if len(o) >= 3 and o[0] == "SELL" and o[1] == "MILK":
                selling += max(0, int(o[2]))
                hit = o
        try:
            stock = projected_shed(action, FarmView(observation))
        except Exception:
            return action
        avail = int(stock.get("MILK", 0) or 0) - selling
        take = min(avail, _MX_CARPET_CAP)
        if take <= 0:
            return action
        if hit is not None:
            hit[2] = int(hit[2]) + take
            out_orders = market_orders
        else:
            if len(market_orders) >= 10:
                return action                 # 单位帽满→不加（不截既有单）
            out_orders = [["SELL", "MILK", take]] + market_orders
        result = dict(action, market=out_orders)
        # 回写 MODELPX 自挂簿记（防自卖误判为对手流）
        for hname in ("_S758_HIST", "_S804_HIST"):
            h = globals().get(hname)
            if isinstance(h, dict):
                pv = h.get(player)
                if isinstance(pv, dict) and pv.get("step") == step:
                    own = pv.setdefault("own", {})
                    own["MILK"] = int(own.get("MILK", 0) or 0) + take
        rs = (globals().get("_RACE_STATE") or {}).get(player)
        if rs is not None and rs.get("prev_action") is not None \
                and rs.get("step") == step:
            rs["prev_action"] = result
        _MX_REPORT["carpet_steps"] += 1
        _MX_REPORT["carpet_orders"] += 1
        _MX_REPORT["carpet_units"] += take
        return result
    except Exception:
        _MX_REPORT["errors"] += 1
        return action

# （入口 _mx_agent 由 build_milkwin.py 组装于块尾并做末函数归一）
