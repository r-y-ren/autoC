"""verify_replay_fidelity（L1，R2）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

金标准：库内每条路由经 v48 回放语义逐步回放 = 源轨迹动作**逐字节**。

* 回放语义（v48 载入路径同构）：v21 replay_policy——step t → 深拷贝
  actions[t]（索引钳位 [0, len-1]）；v23 safe_action——缺省补
  {farmer:["PASS"], hands:[], market:[]}。
* 对齐口径（T1/deep-read 实证）：route[t] == 源席回放 steps[t+1].action
  （T1 轨迹库 actions[t] 即该步的规范形态，故对库逐字节比对即对源逐字节）。
* 逐路由语义：default 路由 = 骨干源全 719 步逐字节；分叉路由
  （嵌缀拼接，v48 磁带同构）= [0,f) 逐字节= 骨干源、[f,719) 逐字节
  = 分叉成员源（payload 以 prefix_actions/actions 分别给出两段源）。

比对为规范 JSON 逐字节（sort_keys+紧排，与 T1 seat_action_blob 同式）；
任一步失配即 fidelity 失败（fail-closed，由顶层拒绝出库）。
"""

from __future__ import annotations

import copy

from mine_trajectories.extract_and_filter_seats import seat_action_blob


def safe_action(action):
    """v23 policy_library.safe_action 同义实现（v48 载入路径的缺省补全）。"""
    result = copy.deepcopy(action) if isinstance(action, dict) else {}
    result.setdefault("farmer", ["PASS"])
    result.setdefault("hands", [])
    market = result.get("market")
    result["market"] = list(market) if isinstance(market, (list, tuple)) \
        else []
    return result


def replay_step(route, step: int) -> dict:
    """v21 replay_policy 同义实现：step t -> 深拷贝 route[t]（索引钳位）。"""
    t = min(max(0, int(step)), len(route) - 1)
    return copy.deepcopy(route[t] or {"farmer": ["PASS"], "hands": [],
                                      "market": []})


def verify_replay_fidelity(payload=None):
    """意图级签名；真值在责任文档。

    payload：{routes: {名: 719 步}, sources: {名: {"actions": 源流,
    "aligned_from": f, "prefix_actions": 骨干源流（f>0 时必给）}}}。
    逐路由对齐语义：t < f 逐字节=骨干源（prefix_actions），t ≥ f 逐字节
    =本源（actions）；f=0 即全步对本源。
    返回 {fidelity: {名: {checked_steps, mismatches, first_mismatch,
    aligned_from, ok}}, all_ok}；比对经 replay_step+safe_action 回放
    语义后与源规范 JSON 逐字节。
    """
    payload = dict(payload or {})
    routes = payload.get("routes") or {}
    sources = payload.get("sources") or {}
    if not routes or not sources:
        raise ValueError("verify_replay_fidelity needs routes and sources "
                         "(fail-closed)")

    fidelity = {}
    all_ok = True
    for name in sorted(routes):
        route = routes[name]
        spec = sources.get(name)
        if not spec or not spec.get("actions"):
            fidelity[name] = {"error": "missing source stream"}
            all_ok = False
            continue
        source = spec["actions"]
        aligned_from = int(spec.get("aligned_from") or 0)
        prefix = spec.get("prefix_actions") or source
        mismatches = []
        for t in range(len(route)):
            reference = prefix[t] if t < aligned_from else source[t]
            replayed = safe_action(replay_step(route, t))
            if seat_action_blob(replayed) != seat_action_blob(reference):
                mismatches.append(t)
                if len(mismatches) >= 5:
                    break
        entry = {
            "checked_steps": len(route),
            "aligned_from": aligned_from,
            "mismatches": len(mismatches),
            "first_mismatch": mismatches[0] if mismatches else None,
            "ok": not mismatches,
        }
        fidelity[name] = entry
        if mismatches:
            all_ok = False
    return {"fidelity": fidelity, "all_ok": all_ok}
