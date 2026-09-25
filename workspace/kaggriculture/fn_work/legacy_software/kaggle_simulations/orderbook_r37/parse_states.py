# -*- coding: utf-8 -*-
"""parse_episode_states（R19/R20 共享）：对局状态序列解析。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补·共享函数】）：
replay JSON → 逐步双席规范行 {step, seat, action, money, hands, animals_grid,
tiles}；解析口径经分析22 考古实测校准（磁带 step X ↔ replay si X+1；
steps[t][seat].observation 为该步执行后值；action 由前一拍观测算出）。
调用方：replay_guard_verdict, count_shearings。
"""
from __future__ import annotations

import json
from typing import Any, Dict, List

_SEATS = 2  # 双席：steps[t] 恰 2 席、observation.farms 恰 2 场


def _bad(where: str, msg: str) -> ValueError:
    return ValueError(f"replay 格式不符：{where} {msg}")


def _missing(where: str, name: str) -> ValueError:
    return ValueError(f"replay 缺字段：{where}.{name}")


def _grid_entry(cell: Dict[str, Any], ident_key: str, ident_val: Any) -> Dict[str, Any]:
    """格子 dict → 规范条目：identity 键改名 type，其余观察子键原样带。

    观察字段有就带、没有就省略该子键（不补默认值）。
    """
    return {"type": ident_val, **{k: v for k, v in cell.items() if k != ident_key}}


def _extract_grids(where: str, tiles_raw: Any) -> tuple:
    """farms[seat].tiles[y][x] → (animals_grid, tiles)；键 (x,y)，x=列 y=行。"""
    if not isinstance(tiles_raw, list):
        raise _bad(where, f"应为 list，实为 {type(tiles_raw).__name__}")
    animals_grid: Dict[Any, Any] = {}
    tiles_map: Dict[Any, Any] = {}
    for y, row in enumerate(tiles_raw):
        if not isinstance(row, list):
            raise _bad(f"{where}[{y}]", f"应为 list，实为 {type(row).__name__}")
        for x, cell in enumerate(row):
            if cell is None or cell == "LOCKED":
                continue  # 空格/未解锁格不上图
            if not isinstance(cell, dict):
                raise _bad(f"{where}[{y}][{x}]",
                           f"应为 None/\"LOCKED\"/dict，实为 {type(cell).__name__}")
            if cell.get("crop"):
                ident_key, ident_val = "crop", cell["crop"]
            elif cell.get("kind"):
                ident_key, ident_val = "kind", cell["kind"]
            else:
                raise _missing(f"{where}[{y}][{x}]", "crop/kind（无法定 type）")
            tiles_map[(x, y)] = _grid_entry(cell, ident_key, ident_val)
            if cell.get("animal"):
                animals_grid[(x, y)] = _grid_entry(cell, "animal", cell["animal"])
    return animals_grid, tiles_map


def _inventory(where: str, private: Any) -> Dict[str, Any]:
    """private 的 shed+seeds+随身 inventories 合计（分析22 tot_inv 口径）。"""
    if not isinstance(private, dict):
        raise _bad(f"{where}.private", f"应为 dict，实为 {type(private).__name__}")
    total: Dict[str, Any] = {}
    for part in ("shed", "seeds"):
        sub = private.get(part)
        if sub is None:
            continue
        if not isinstance(sub, dict):
            raise _bad(f"{where}.private.{part}", f"应为 dict，实为 {type(sub).__name__}")
        for k, v in sub.items():
            total[k] = total.get(k, 0) + v
    invs = private.get("inventories")
    if invs is None:
        return total
    if not isinstance(invs, list):
        raise _bad(f"{where}.private.inventories",
                   f"应为 list，实为 {type(invs).__name__}")
    for i, sub in enumerate(invs):
        if sub is None:
            continue
        if not isinstance(sub, dict):
            raise _bad(f"{where}.private.inventories[{i}]",
                       f"应为 dict，实为 {type(sub).__name__}")
        for k, v in sub.items():
            total[k] = total.get(k, 0) + v
    return total


def _parse_entry(t: int, seat: int, entry: Any) -> Dict[str, Any]:
    where = f"steps[{t}][{seat}]"
    if not isinstance(entry, dict):
        raise _bad(where, f"应为 dict，实为 {type(entry).__name__}")
    if "action" not in entry:
        raise _missing(where, "action")
    if "observation" not in entry:
        raise _missing(where, "observation")
    action = entry["action"]
    if not isinstance(action, dict):
        raise _bad(f"{where}.action", f"应为 dict，实为 {type(action).__name__}")
    for key in ("farmer", "hands", "market"):
        if key not in action:
            raise _missing(f"{where}.action", key)
    obs = entry["observation"]
    if not isinstance(obs, dict):
        raise _bad(f"{where}.observation", f"应为 dict，实为 {type(obs).__name__}")
    for key in ("day", "hour", "farms", "private"):
        if key not in obs:
            raise _missing(f"{where}.observation", key)
    obs_step = obs.get("step")
    if obs_step is not None and obs_step != t:
        raise _bad(f"{where}.observation.step", f"={obs_step} 与记录序 {t} 不符")
    if not isinstance(obs["day"], int) or isinstance(obs["day"], bool):
        raise _bad(f"{where}.observation.day", f"应为 int，实为 {obs['day']!r}")
    if not isinstance(obs["hour"], int) or isinstance(obs["hour"], bool):
        raise _bad(f"{where}.observation.hour", f"应为 int，实为 {obs['hour']!r}")
    farms = obs["farms"]
    if not isinstance(farms, list) or len(farms) != _SEATS:
        raise _bad(f"{where}.observation.farms",
                   f"应为恰 {_SEATS} 场 list，实为 {farms!r:.40}")
    farm = farms[seat]
    farm_where = f"{where}.observation.farms[{seat}]"
    if not isinstance(farm, dict):
        raise _bad(farm_where, f"应为 dict，实为 {type(farm).__name__}")
    for key in ("money", "hands", "farmer", "tiles"):
        if key not in farm:
            raise _missing(farm_where, key)
    money = farm["money"]
    if isinstance(money, bool) or not isinstance(money, (int, float)):
        raise _bad(f"{farm_where}.money", f"应为数值，实为 {money!r}")
    if not isinstance(farm["hands"], list):
        raise _bad(f"{farm_where}.hands", f"应为 list，实为 {type(farm['hands']).__name__}")
    if not isinstance(farm["farmer"], list):
        raise _bad(f"{farm_where}.farmer", f"应为 list，实为 {type(farm['farmer']).__name__}")
    animals_grid, tiles_map = _extract_grids(f"{farm_where}.tiles", farm["tiles"])
    return {
        "step": t,
        "seat": seat,
        "day": obs["day"],
        "hour": obs["hour"],
        "action": action,
        "money": money,
        "hands": farm["hands"],
        "farmer": farm["farmer"],
        "animals_grid": animals_grid,
        "tiles": tiles_map,
        "inventory": _inventory(f"{where}.observation", obs["private"]),
    }


def parse_episode_states(replay_path: str) -> List[Dict[str, Any]]:
    """replay JSON → 逐步双席规范行数组（step 升序、席位 0→1：rows[2*t+seat]）。

    解析口径（分析22 考古实测校准，2026-09-25 对 /tmp/kagr22 六局灾难局
    replay 实物逐字段复核）：

    - **step 口径裁定：行 step = replay 原生序 si（steps 下标；= 席0
      observation.step，day=step//24、hour=step%24 与 observation.day/hour
      实物恒等）**。契约"磁带 step X ↔ replay si X+1"在本口径下即：磁带
      step X 的动作记录在 step=X+1 的行上（消费方按磁带步取动作需 +1 换算；
      d1 h0 等状态判据直接取 day==1,hour==0 即 step 24 行）。
    - 行内状态字段（money/hands/farmer/animals_grid/tiles/inventory）为该步
      执行后值；action 为该步执行的动作（由前一拍观测算出），原样透传
      {farmer,hands,market}，不求值语义（那是 verdict/count 的事）。
    - 字段映射（实物字段名）：action=steps[t][seat].action 原样；money=
      farms[seat].money；hands=farms[seat].hands（执行后位置表 [[x,y],…]）；
      farmer=farms[seat].farmer（执行后位置 [x,y]）；day/hour=observation.day/
      hour；inventory=observation.private 的 shed+seeds+随身 inventories 合计
      （分析22 tot_inv 口径，供 BUY_ANIMAL 成交判据）。
    - animals_grid：格上牲畜分布——farms[seat].tiles[y][x] 中带真值 animal
      的格 → {(x,y): {"type": cell["animal"], **其余观察子键}}；tiles：格上
      作物/建筑——全部 dict 格（含牲畜格的建筑面）→ {(x,y): {"type":
      cell["crop"] 或 cell["kind"], **其余观察子键}}。键 (x,y) 与 observation
      位置 [x,y] 同构（取法 tiles[y][x]，x=列、y=行；分析22/基座 _tile_at
      口径）。**观察字段有就带、没有就省略该子键**（不补默认值：如
      fed_today/consecutive_unfed 等随引擎版本可缺，缺即不出现在条目里）；
      identity 键（animal 或 crop 或 kind，取用者）改名为 type，其余观察子键
      原样带。animals_grid 的键恒为 tiles 的子集。
    - 双席约定：steps[t] 恰 2 席、observation.farms 恰 2 场（farms[seat]=该
      席农场，public 双席均可见）；observation.private 为该席私有（已实测两
      席互异）；observation.step 可缺（席1 实物全缺），在场必须 == 记录序。

    签名意图：输入: replay JSON 路径 / 输出: 逐步状态行数组 /
    错误: 格式不符/缺字段即抛 ValueError（消息含缺什么）；文件不存在→
    FileNotFoundError；JSON 解析失败→ValueError。
    """
    try:
        with open(replay_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise ValueError(f"replay JSON 解析失败：{exc}") from exc
    if not isinstance(data, dict):
        raise _bad("顶层", f"应为 dict，实为 {type(data).__name__}")
    if "steps" not in data:
        raise _missing("顶层", "steps")
    steps = data["steps"]
    if not isinstance(steps, list):
        raise _bad("steps", f"应为 list，实为 {type(steps).__name__}")
    rows: List[Dict[str, Any]] = []
    for t, pair in enumerate(steps):
        if not isinstance(pair, list) or len(pair) != _SEATS:
            raise _bad(f"steps[{t}]", f"应为恰 {_SEATS} 席 list")
        for seat in range(_SEATS):
            rows.append(_parse_entry(t, seat, pair[seat]))
    return rows
