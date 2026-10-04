# -*- coding: utf-8 -*-
"""build_behavsel：行为选择器 v2 构建线（D3；判决先行·不发射·不提交·不改既有代码）。

责任口径（任务 D3）：基底=orderbook_oppcond_lab/build/oc_c3（画像器+C3 已在，
sha 3f8b57fd…）零改动读入；纯增量尾块追加＝行为选择器（按画像族切换行为，
≤3 条件行为）：
  bs_gap   idle-seller 缺口放量（gap 线索的量/品项版）：对手流缺口拍（近 3 拍
           该品对手流和≤2）∧ 品项=对手稳态出货品（24 拍窗累计对手出货 argmax）
           → 追加/合并单量翻倍（帽内=projected 可售−同品他单；不缩水不幻影）；
           非缺口拍照旧。
  bs_slot  镜像族响应（画像=h1_mirror）：卖时相位微错——同拍内首个自由 SELL
           （竞速品、无同品 BUY 腿）提前一槽（单次相邻交换；slot 饱和已证
           不全错位只微调）；护栏=零跨拍（仅同拍列表内置换，量/单数不变）。
  bs_c3    WFR/攻击族：C3 已有（保留＝不动基座换表件）；r37/2965 族沿矩阵
           已证优势面零动作（安全）。
画像不确定（unknown）→ 全部照旧（零足迹）；所有臂 step≥144（画像锁存）后才
激活 → 开局冻结（turn1-4 字节一致，D5 条款 2）。臂 1 不加价峰择时门（D5 条款
3）。D5 第四臂（产线响应 GOOSE/SHEEP 预设档）**跳过**：H1 产线层深埋 tape/圈
层规划非尾块可动，且 D5 自适应证据为 B 级且未控 seed，预算 400 已排满——见
evidence arms.skipped。
形态（逐件消融）：bs2=三臂全开；bs2_nogap/bs2_noslot/bs2_noc3=逐臂关闭。
校验（fail-closed 不产出）：①语法 ②末 callable=_hs_agent ③基底字节前缀恒等
④画像探针 7/7（profiler_core 同源）⑤臂语义探针（gap/量/帽/槽/洗仓腿跳过）
⑥零足迹探针（unknown/r37 类→动作对象恒等）⑦c3 消融标记 ⑧反提取封印
（尾块剥离→逐字节=oc_c3 源）。
用法：python3 build_behavsel.py
只写 orderbook_behavsel_lab/。不改既有代码。不发射。
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_oppcond_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_oppcond_lab"))

from profiler_core import probe_expected  # noqa: E402  同源字节复用（只读）

RECORD_VERSION = "behavsel-build/1.0"
BASE_MAIN = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
BASE_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d39"
                     "ba9bd23d")
BUILD_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
ENTRY_NAME = "_hs_agent"
REVEAL_STEP = 144

FORMS = {
    "bs2": {"gap": True, "slot": True, "c3": True},
    "bs2_nogap": {"gap": False, "slot": True, "c3": True},
    "bs2_noslot": {"gap": True, "slot": False, "c3": True},
    "bs2_noc3": {"gap": True, "slot": True, "c3": False},
}


# ------------------------------------------------------------ 尾块 --
def build_tail(flags: dict) -> str:
    return (
        "\n# ===== behavsel layer v2（行为选择器；oc_c3 尾块后追加；"
        "基底零改动前缀恒等） =====\n"
        "_BS_PARENT = _hs_agent\n"
        "del _hs_agent\n"
        "_BS_FLAGS = {'gap': %r, 'slot': %r, 'c3': %r}\n"
        "_BS_REPORT = dict(calls=0, gap_evals=0, gap_fire=0, gap_units=0,\n"
        "                  slot_moves=0, censored_lo=0, errors=0)\n"
        "_BS_WIN = 3\n"
        "_BS_GAP_MAX = 2\n"
        "_BS_HIST = 24\n"
        "_BS_FLOW = {}\n"
        "_BS_PREV = {}\n\n\n"
        "def _bs_reset():\n"
        "    _BS_REPORT.update(calls=0, gap_evals=0, gap_fire=0, gap_units=0,\n"
        "                      slot_moves=0, censored_lo=0, errors=0)\n"
        "    _BS_FLOW.clear()\n"
        "    _BS_PREV.clear()\n\n\n"
        "def _bs_update(observation, action):\n"
        "    \"\"\"R28 删失口径对手出货流窗（racegap 同式）：\n"
        "    d=inv'−inv+town_draw(t−1)−prev_own；0 删失；24 拍滚动。\"\"\"\n"
        "    try:\n"
        "        step = int((observation or {}).get('step', 0))\n"
        "        player = int((observation or {}).get('player', 0))\n"
        "        inv = (((observation or {}).get('market') or {})"
        ".get('inventory') or {})\n"
        "        shops = list((((observation or {}).get('town') or {})"
        ".get('unlocked_shops') or []))\n"
        "        own = _oc_own_sells(action)\n"
        "        flow = _BS_FLOW.setdefault(player, {})\n"
        "        prev = _BS_PREV.get(player)\n"
        "        if prev and prev.get('step') == step - 1:\n"
        "            try:\n"
        "                draw = _oc_town_draw(prev.get('shops') or shops,"
        " step - 1) or {}\n"
        "            except Exception:\n"
        "                draw = {}\n"
        "            for item in _OC_RACE_ITEMS:\n"
        "                try:\n"
        "                    d = (int(inv.get(item, 0))"
        " - int(prev['inv'].get(item, 0))\n"
        "                         + int(draw.get(item, 0))"
        " - int(prev['own'].get(item, 0)))\n"
        "                except Exception:\n"
        "                    continue\n"
        "                if d < 0:\n"
        "                    _BS_REPORT['censored_lo'] += 1\n"
        "                row = flow.setdefault(item, [])\n"
        "                row.append(max(0, d))\n"
        "                if len(row) > _BS_HIST:\n"
        "                    del row[:len(row) - _BS_HIST]\n"
        "        _BS_PREV[player] = {\n"
        "            'step': step,\n"
        "            'inv': {i: int(inv.get(i, 0)) for i in _OC_RACE_ITEMS},\n"
        "            'own': own, 'shops': shops}\n"
        "    except Exception:\n"
        "        _BS_REPORT['errors'] += 1\n\n\n"
        "def _bs_steady(player):\n"
        "    \"\"\"对手稳态出货品=24 拍窗累计对手出货 argmax（平局取表序；"
        "无正流出→None）。\"\"\"\n"
        "    flow = _BS_FLOW.get(int(player)) or {}\n"
        "    best, best_q = None, 0\n"
        "    for item in _OC_RACE_ITEMS:\n"
        "        q = sum(flow.get(item) or [])\n"
        "        if q > best_q:\n"
        "            best, best_q = item, q\n"
        "    return best\n\n\n"
        "def _bs_gap_ok(item, player):\n"
        "    \"\"\"近 _BS_WIN 拍该品对手流和≤_BS_GAP_MAX → 缺口拍 True；"
        "窗未满→False（照旧）。\"\"\"\n"
        "    row = (_BS_FLOW.get(int(player)) or {}).get(str(item)) or []\n"
        "    if len(row) < _BS_WIN:\n"
        "        return False\n"
        "    _BS_REPORT['gap_evals'] += 1\n"
        "    return sum(row[-_BS_WIN:]) <= _BS_GAP_MAX\n\n\n"
        "def _bs_double(action, observation, item):\n"
        "    \"\"\"追加单量翻倍（帽内）：同品首单 SELL q→min(2q, "
        "projected 可售−同品他单)；不缩水。\"\"\"\n"
        "    try:\n"
        "        market = [list(o) if isinstance(o, (list, tuple)) else o\n"
        "                  for o in (action.get('market') or [])]\n"
        "        idx = [i for i, o in enumerate(market)\n"
        "               if isinstance(o, list) and len(o) >= 3"
        " and o[0] == 'SELL'\n"
        "               and str(o[1]) == str(item) and int(o[2]) > 0]\n"
        "        if not idx:\n"
        "            return action\n"
        "        try:\n"
        "            proj = projected_shed(action, FarmView(observation)) or {}\n"
        "            cap_total = int(proj.get(item, 0) or 0)\n"
        "        except Exception:\n"
        "            cap_total = 0\n"
        "        others = sum(int(market[i][2]) for i in idx[1:])\n"
        "        q = int(market[idx[0]][2])\n"
        "        q2 = min(2 * q, max(q, cap_total - others))\n"
        "        if q2 <= q:\n"
        "            return action\n"
        "        market[idx[0]][2] = q2\n"
        "        _BS_REPORT['gap_fire'] += 1\n"
        "        _BS_REPORT['gap_units'] += q2 - q\n"
        "        return dict(action, market=market)\n"
        "    except Exception:\n"
        "        _BS_REPORT['errors'] += 1\n"
        "        return action\n\n\n"
        "def _bs_slot(action):\n"
        "    \"\"\"同拍微错：首个自由 SELL（竞速品、无同品 BUY 腿）提前一槽"
        "（单次相邻交换）；零跨拍。\"\"\"\n"
        "    try:\n"
        "        market = [list(o) if isinstance(o, (list, tuple)) else o\n"
        "                  for o in (action.get('market') or [])]\n"
        "        if len(market) < 2:\n"
        "            return action\n"
        "        bought = set()\n"
        "        for o in market:\n"
        "            if (isinstance(o, list) and len(o) >= 2\n"
        "                    and str(o[0]) in ('BUY_PRODUCT', 'BUY_SEED',"
        " 'BUY_ANIMAL')):\n"
        "                bought.add(str(o[1]))\n"
        "        for i in range(1, len(market)):\n"
        "            o = market[i]\n"
        "            if not (isinstance(o, list) and len(o) >= 3"
        " and o[0] == 'SELL'):\n"
        "                continue\n"
        "            if str(o[1]) not in _OC_RACE_ITEMS or str(o[1]) in bought:\n"
        "                continue\n"
        "            if int(o[2]) <= 0:\n"
        "                continue\n"
        "            market[i - 1], market[i] = market[i], market[i - 1]\n"
        "            _BS_REPORT['slot_moves'] += 1\n"
        "            return dict(action, market=market)\n"
        "        return action\n"
        "    except Exception:\n"
        "        _BS_REPORT['errors'] += 1\n"
        "        return action\n\n\n"
        % (bool(flags.get("gap")), bool(flags.get("slot")),
           bool(flags.get("c3")))
        + ("# 臂3 消融：C3 换表件惰性化（基座 wrapper 经全局名晚绑定命中）\n"
           "def _oc_c3_swap(observation, step):\n"
           "    return None\n"
           "_oc_c3_swap._bs_noop = True\n\n\n"
           if not flags.get("c3") else "")
        + "# ---- 入口包（官方 last-callable 语义；名保持 _hs_agent） ----\n"
          "_BS_PARENT_REF = _BS_PARENT\n\n\n"
          "def _hs_agent(observation, configuration=None):\n"
          "    try:\n"
          "        step = int((observation or {}).get('step', 0))\n"
          "    except Exception:\n"
          "        step = 0\n"
          "    if step == 0:\n"
          "        _bs_reset()\n"
          "    action = _BS_PARENT_REF(observation, configuration)\n"
          "    try:\n"
          "        _BS_REPORT['calls'] += 1\n"
          "        cls = _oc_cls(observation, step)\n"
          "        if step >= %d and cls == 'h1_mirror':\n"
          "            if _BS_FLAGS.get('gap'):\n"
          "                p = int((observation or {}).get('player', 0))\n"
          "                item = _bs_steady(p)\n"
          "                if item is not None and _bs_gap_ok(item, p):\n"
          "                    action = _bs_double(action, observation, item)\n"
          "            if _BS_FLAGS.get('slot'):\n"
          "                action = _bs_slot(action)\n"
          "        _bs_update(observation, action)\n"
          "    except Exception:\n"
          "        _BS_REPORT['errors'] += 1\n"
          "    return action\n"
          "_hs_agent.telemetry = _BS_REPORT\n" % REVEAL_STEP
    )


# ------------------------------------------------------------ 校验探针 --
def _mk_obs(step, player=0):
    return {"step": step, "player": player, "day": step // 24, "hour": step % 24,
            "town": {"unlocked_shops": []},
            "farms": [{"money": 1000.0}, {"money": 1000.0}],
            "market": {"inventory": {}, "prices": {}, "params": {}}}


def verify_form(text, base_src, flags, form):
    # ①语法
    try:
        compile(text, "<behavsel:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: %r" % (form, exc))
    # ③基底字节前缀恒等
    if not text.startswith(base_src):
        raise RuntimeError("校验③红 %s: 基底前缀漂移" % form)
    # ⑧反提取封印：尾块剥离→逐字节=oc_c3 源
    if text[:len(base_src)] != base_src:
        raise RuntimeError("校验⑧红 %s: 反提取失败" % form)
    ns: dict = {}
    exec(compile(text, "<behavsel:%s>" % form, "exec"), ns)
    # ②末 callable
    loaded = [v for v in ns.values() if callable(v)]
    if not loaded or loaded[-1].__name__ != ENTRY_NAME:
        raise RuntimeError("校验②红 %s: 末 callable=%r" % (
            form, loaded[-1].__name__ if loaded else None))
    # ④画像探针（profiler_core 同源）
    rows = []
    for row in probe_expected():
        got, why = ns["_oc_decide"]({
            "cashdiff1": row["features"][0],
            "rival_money1": row["features"][1],
            "sim_max": row["features"][2],
            "sim_seen": 1,
            "rival_animals_143": {"SHEEP": row["features"][3]},
        })
        rows.append({"expect": row["expect"], "got": got,
                     "match": got == row["expect"]})
    if not all(r["match"] for r in rows):
        raise RuntimeError("校验④红 %s: 画像探针 %s" % (form, rows))
    # ⑤臂语义探针
    arm_rows = []
    ns["_BS_FLOW"][0] = {"MILK": [5, 0, 0]}
    r1 = ns["_bs_gap_ok"]("MILK", 0) is False          # 高流→非缺口
    ns["_BS_FLOW"][0] = {"MILK": [0, 0, 1]}
    r2 = ns["_bs_gap_ok"]("MILK", 0) is True           # 缺口→放量
    ns["_BS_FLOW"][0] = {"MILK": [1, 1]}
    r3 = ns["_bs_gap_ok"]("MILK", 0) is False          # 窗未满→照旧
    ns["_BS_FLOW"][0] = {"MILK": [3, 1, 2], "WOOL": [9, 9, 9]}
    r4 = ns["_bs_steady"](0) == "WOOL"                 # 稳态品=累计 argmax
    obs = _mk_obs(200)
    act = {"market": [["SELL", "MILK", 2], ["HIRE"]]}
    ns["projected_shed"] = lambda a, v: {"MILK": 10}
    ns["FarmView"] = lambda o: None
    out = ns["_bs_double"](act, obs, "MILK")
    r5 = out["market"][0][2] == 4                      # 翻倍
    ns["projected_shed"] = lambda a, v: {"MILK": 3}
    out2 = ns["_bs_double"](act, obs, "MILK")
    r6 = out2["market"][0][2] == 3                     # 帽内
    ns["projected_shed"] = lambda a, v: {"MILK": 1}
    out3 = ns["_bs_double"](act, obs, "MILK")
    r7 = out3["market"][0][2] == 2                     # 不缩水
    a4 = {"market": [["HIRE"], ["SELL", "CARROT", 2], ["SELL", "WOOL", 1]]}
    o4 = ns["_bs_slot"](a4)
    r8 = (o4["market"][0] == ["SELL", "CARROT", 2]
          and o4["market"][1] == ["HIRE"]
          and o4["market"][2] == ["SELL", "WOOL", 1])  # 一槽+同品组保序
    a5 = {"market": [["BUY_PRODUCT", "CARROT", 1], ["SELL", "CARROT", 1]]}
    r9 = ns["_bs_slot"](a5) is a5                      # 洗仓腿跳过
    a6 = {"market": [["BUY_SEED", "WHEAT", 1], ["SELL", "WHEAT", 1]]}
    r10 = ns["_bs_slot"](a6) is a6                     # 非竞速品跳过
    arm_rows = [{"gap_high_flow": r1, "gap_hit": r2, "gap_window_short": r3,
                 "steady_argmax": r4, "double": r5, "cap": r6,
                 "no_shrink": r7, "slot_one": r8, "wash_skip": r9,
                 "nonrace_skip": r10}]
    if not all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]):
        raise RuntimeError("校验⑤红 %s: 臂探针 %s" % (form, arm_rows))
    # ⑥零足迹探针（unknown→动作对象恒等；h1_mirror+缺口→改动）
    ns["_BS_PARENT_REF"] = lambda o, c=None: {"market": [["HIRE"],
                                                         ["SELL", "MILK", 2]]}
    ns["_OC_STATE"].clear()
    st = ns["_oc_state_for"]({"player": 0})
    st.update({"cls": "unknown", "locked": True})
    ns["_BS_FLOW"].clear()
    ns["_BS_PREV"].clear()
    sentinel = ns["_hs_agent"](_mk_obs(200), None)
    r11 = sentinel["market"] == [["HIRE"], ["SELL", "MILK", 2]]
    ns["_OC_STATE"].clear()
    st = ns["_oc_state_for"]({"player": 0})
    st.update({"cls": "h1_mirror", "locked": True})
    ns["_BS_FLOW"].clear()
    ns["_BS_PREV"].clear()
    # 稳态品=MILK（累计 2）且近 3 拍流和 0≤2 → 缺口拍；gap 或 slot 至少一臂改动
    ns["_BS_FLOW"][0] = {"MILK": [2, 0, 0, 0, 0, 0]}
    ns["projected_shed"] = lambda a, v: {"MILK": 10}
    ns["FarmView"] = lambda o: None
    fired = ns["_hs_agent"](_mk_obs(200), None)
    r12 = fired["market"] != [["HIRE"], ["SELL", "MILK", 2]]
    zero_rows = [{"unknown_identity": r11, "mirror_fires": r12}]
    if not (r11 and (r12 or not (flags.get("gap") or flags.get("slot")))):
        raise RuntimeError("校验⑥红 %s: 零足迹探针 %s" % (form, zero_rows))
    # ⑦c3 消融标记
    noop = getattr(ns["_oc_c3_swap"], "_bs_noop", False)
    r13 = (noop is True) if not flags.get("c3") else (noop is False)
    if not r13:
        raise RuntimeError("校验⑦红 %s: c3 消融标记 %r" % (form, noop))
    return {"probe_core": rows, "probe_arm": arm_rows,
            "probe_zero_footprint": zero_rows,
            "probe_c3_noop": {"expected_noop": not flags.get("c3"),
                              "got_noop": bool(noop), "match": r13}}


def _make_tar(main_bytes):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    return buf.getvalue()


def build_form(name, flags, base_bytes, base_src):
    tail = build_tail(flags)
    text = base_src + tail
    data = text.encode("utf-8")
    probes = verify_form(text, base_src, flags, name)
    out_dir = BUILD_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)
    tar_bytes = _make_tar(data)
    (out_dir / "main.py").write_bytes(data)
    (out_dir / "submission.tar.gz").write_bytes(tar_bytes)
    manifest = {
        "schema": "orderbook_behavsel_manifest/1.0",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "form": name, "flags": dict(flags),
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "main_sha256": hashlib.sha256(data).hexdigest(),
        "main_bytes": len(data), "tar_sha256": hashlib.sha256(tar_bytes)
        .hexdigest(),
        "tar_bytes": len(tar_bytes), "tar_members": ["main.py"],
        "append_only_prefix_identical": True, "entry": ENTRY_NAME,
        "entry_last_callable": True,
        "layers": ["profiler", "c3_wool_phase"]
        + (["bs_gap_volume"] if flags.get("gap") else [])
        + (["bs_slot_micro"] if flags.get("slot") else []),
        "reverse_extract_byte_identical_to_oc_c3": True,
        "compile_ok": True, "probes": probes,
    }
    (out_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("built", name, manifest["main_sha256"][:16], manifest["main_bytes"],
          "bytes layers", manifest["layers"], flush=True)
    return manifest


def main():
    t0 = time.perf_counter()
    base_bytes = BASE_MAIN.read_bytes()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("构建底 sha 不符（oc_c3 漂移）：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("基底不以换行收尾（fail-closed）")
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    forms = {name: build_form(name, flags, base_bytes, base_src)
             for name, flags in FORMS.items()}
    out = {
        "version": RECORD_VERSION,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_main": str(BASE_MAIN), "base_main_sha256": base_sha,
        "byte_zero_change_on_base": True,
        "design": "画像→行为选择器（按族切换）：h1_mirror→bs_gap+bs_slot；"
                  "wfr→C3 保留；r37_2965→零动作；unknown→零足迹；"
                  "全部臂 step≥144 后激活（开局冻结）",
        "d5_fourth_arm": {
            "action": "skipped",
            "reason": "产线响应（画像族→GOOSE/SHEEP 占比预设档）构建成本高："
                      "H1 产线层深埋 tape/圈层规划非尾块可安全改写；D5 自适应"
                      "证据 B 级且未控 seed（市场 vs 对手自适应未分离）；"
                      "预算 400 局次已排满（面板+消融+认证）",
        },
        "forms": {k: {"flags": v["flags"], "main_sha256": v["main_sha256"],
                      "main_bytes": v["main_bytes"], "layers": v["layers"]}
                  for k, v in forms.items()},
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    (EVID_DIR / "build.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("DONE", out["elapsed_s"], "s", flush=True)
    return out


if __name__ == "__main__":
    main()
