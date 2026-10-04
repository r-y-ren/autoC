# -*- coding: utf-8 -*-
"""build_topform：顶端策略升级 H2 构建（对照实验·不发射·不提交）。

实验命题（教训定理正用·内生式）：把榜一（Majkel1337）卖时蓝图的未覆盖规则——
排水拍相位（B1：卖单避开排水拍前谷底 %4==0/hour0，后置 1 拍到排水后峰值
%4==1）——以内生形态织进 H1 内层卖时路径：step1009 单列表构造点函数体
（[10122,10134] 行带=轨道 2 先例锚点），新增 _tf_post 同拍后处理，跨拍延后
经内生台账 due 抵扣（净卖量恒等），视界有界 H=1，quote 门（原生 suppress/
r36_debt 碰撞跳过 + 同拍 PICKUP 守卫 + 槽位守卫），非触发拍同对象零足迹。
末 callable 不变（=_hs_agent；尾块逐字保留）。

三形态：
- h2：H1 内 step1009 函数体内织入卖时后处理（前后缀逐字恒等）；
- h1：现 H1 字节恒等（build/h1/main.py，sha 76b5f842…）。
r40 参照件=orderbook_r40/build/main.py（judge 引用，不入本 manifest 对照）。

守恒硬约束（fail-closed 语义）：
- 净卖量恒等：延后的整单在源拍整体移除、due 记账、目标拍整单加回（同品同量），
  记账抵扣；不做部分挪量（零跨拍拆并）；
- 零跨拍拆并：只整单移动，不拆不合；
- 非触发拍零足迹：无触发/无 due 时返回同对象；
- 末 callable 不变：尾块不动。

校验（fail-closed）：①compile ②exec 装载后末 callable 名=_hs_agent
③h1 与现 H1 字节恒等 ④h2 仅 step1009 体带改动（前后缀逐字恒等）。
只写 orderbook_topform_lab/。
"""
from __future__ import annotations

import difflib
import hashlib
import json
import tarfile
import time
from io import BytesIO
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
H1_SRC = (KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_topform_lab_manifest/1.0"

H1_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764"
                   "974b22f337")
FORMS = ("h2", "h1")
EXPECTED_ENTRY = {"h2": "_hs_agent", "h1": "_hs_agent"}

# ---- 内层改动锚点：step1009 函数体（内层链末段单列表构造点） ----
BLOCK_DEF = ("def step1009_step1008_fortyfirst_final_fixedsell_closure_agent("
             "observation,configuration=None):")
BLOCK_END = ("step1009_step1008_fortyfirst_final_fixedsell_closure_agent"
             ".telemetry=_S1009_REPORT")

# 内生版替换体：签名/父调用/外层异常兜底逐字保留；_s793_reorder 之后织入
# 卖时后处理 _tf_post（B1 排水拍相位）。台账挂函数对象属性（不外溢模块级），
# 动作改动经既有 _s834_key 台账分支同步 _RACE_STATE['prev_action']（内生台账纪律）。
WEAVED_BODY = '''def step1009_step1008_fortyfirst_final_fixedsell_closure_agent(observation,configuration=None):
    # ---- topform 内生卖时（B1 排水拍相位：谷底 %4==0 整单后置 +1 拍；due 抵扣） ----
    _TF_ITEMS=('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
    _TF_MAX_MOVES=4
    def _tf_ledger():
        try:
            led=step1009_step1008_fortyfirst_final_fixedsell_closure_agent.tf
        except AttributeError:
            led=None
        if not isinstance(led,dict):
            led={'due':{},'stats':{'calls':0,'changed_turns':0,'moved_orders':0,'moved_qty':0,'due_orders':0,'due_qty':0,'due_redeferred':0,'skip_native':0,'skip_r36':0,'skip_pickup':0,'skip_stock':0,'skip_window':0,'errors':0,'ticks':[]}}
            step1009_step1008_fortyfirst_final_fixedsell_closure_agent.tf=led
        return led
    def _tf_projected(obs,act):
        try:
            player=int((obs or {}).get('player',0))
        except Exception:
            player=0
        try:
            view=_View(obs,player,_IMPL.chassis.cfg)
            proj=_IMPL.chassis._projected_shed(act,view)
            return {k:int(v) for k,v in dict(proj).items()}
        except Exception:
            try:
                pv=(obs or {}).get('private')
                shed=(pv.get('shed') or {}) if isinstance(pv,dict) else {}
                return {k:int(v) for k,v in dict(shed).items()}
            except Exception:
                return {}
    def _tf_qty(raw):
        if isinstance(raw,bool):
            return None
        if isinstance(raw,int):
            return raw
        if isinstance(raw,float) and raw.is_integer():
            return int(raw)
        return None
    def _tf_pending(player,step):
        """原生 suppress（due_step==step）/r36_debts[step] 碰撞表（按品；只读）。"""
        out={}
        try:
            ch=_IMPL.chassis.players.get(player) or {}
            ss=ch.get('sell_state') or {}
            if ss.get('due_step')==step:
                for it,n in (ss.get('suppress') or {}).items():
                    if n: out[it]=out.get(it,0)+int(n)
            for it,n in ((ss.get('r36_debts') or {}).get(step) or {}).items():
                if n: out[it]=out.get(it,0)+int(n)
        except Exception:
            pass
        return out
    def _tf_pickups(player,src):
        """源拍 tape 单位动作同品 PICKUP 集合（谷仓会被抽走→跳过；_r36 同式守卫）。"""
        try:
            native=_IMPL.chassis.players[player]
            tape=_IMPL.chassis.routes[native['route']]
            future=tape[src] if src<len(tape) and isinstance(tape[src],dict) else {}
            work=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
            return {c[1] for c in work if isinstance(c,(list,tuple)) and len(c)>1 and c[0]=='PICKUP'}
        except Exception:
            return set()
    def _tf_post(obs,act):
        led=_tf_ledger()
        led['stats']['calls']+=1
        try:
            if not isinstance(act,dict):
                return act
            market=act.get('market')
            if not isinstance(market,list):
                return act
            try:
                step=int((obs or {}).get('step',0))
            except Exception:
                step=0
            try:
                player=int((obs or {}).get('player',0))
            except Exception:
                player=0
            dued=led['due'].setdefault(player,{})
            changed=False
            out=list(market)
            # (1) due 抵扣加回：上拍延后的整单本拍整单补回（槽位不足→再延 1 拍）
            due_here=dict(dued.pop(step,{}) or {})
            for item in list(due_here):
                qty=int(due_here.get(item,0) or 0)
                if qty<=0:
                    continue
                if step>717:
                    led['stats']['skip_window']+=1
                    continue
                if len(out)<10:
                    out.append(['SELL',item,qty])
                    led['stats']['due_orders']+=1
                    led['stats']['due_qty']+=qty
                    changed=True
                elif step+1<=717 and led['stats']['due_redeferred']<200:
                    bucket=dued.setdefault(step+1,{})
                    bucket[item]=bucket.get(item,0)+qty
                    led['stats']['due_redeferred']+=1
            # (2) 谷底后置：t%4==0（排水拍前谷底）整单 SELL 后置 +1（排水后 %4==1 峰值）
            moves=0
            if step%4==0 and 0<=step<=716 and (step+1)%72!=0:
                pending=_tf_pending(player,step+1)
                guard=_tf_pickups(player,step+1)
                avail=_tf_projected(obs,act)
                used={}
                kept=[]
                for entry in out:
                    is_sell=(isinstance(entry,(list,tuple)) and len(entry)>=3 and entry[0]=='SELL')
                    if not is_sell:
                        kept.append(entry);continue
                    item=entry[1]
                    qty=_tf_qty(entry[2])
                    if item not in _TF_ITEMS or qty is None or qty<=0 or moves>=_TF_MAX_MOVES:
                        kept.append(entry);continue
                    if pending.get(item,0)>0:
                        led['stats']['skip_native']+=1;kept.append(entry);continue
                    if item in guard:
                        led['stats']['skip_pickup']+=1;kept.append(entry);continue
                    if (avail.get(item,0)-used.get(item,0))<qty:
                        led['stats']['skip_stock']+=1;kept.append(entry);continue
                    used[item]=used.get(item,0)+qty
                    bucket=dued.setdefault(step+1,{})
                    bucket[item]=bucket.get(item,0)+qty
                    led['stats']['moved_orders']+=1
                    led['stats']['moved_qty']+=qty
                    moves+=1
                    changed=True
                    continue
                if moves:
                    out=kept
            if not changed:
                return act
            led['stats']['changed_turns']+=1
            if len(led['stats']['ticks'])<400:
                led['stats']['ticks'].append(step)
            return dict(act,market=out[:10])
        except Exception:
            led['stats']['errors']+=1
            return act
    if int(observation.get('step',0))==0:
        _S1009_REPORT.update(calls=0,changed=0,errors=0)
        _tf_ledger()['due'].pop(int(observation.get('player',0) or 0),None)
        _tf_ledger()['stats'].update(calls=0,changed_turns=0,moved_orders=0,moved_qty=0,due_orders=0,due_qty=0,due_redeferred=0,skip_native=0,skip_r36=0,skip_pickup=0,skip_stock=0,skip_window=0,errors=0,ticks=[])
    _S1009_REPORT['calls']+=1
    action=_S1009_PARENT(observation,configuration)
    try:
        result=_s793_reorder(observation,action)
        result=_tf_post(observation,result)
        if _s834_key(result)!=_s834_key(action):
            _S1009_REPORT['changed']+=1
            st=_RACE_STATE.get(int(observation.get('player',0)))
            if st is not None and st.get('prev_action') is not None and st.get('step')==int(observation.get('step',0)):st['prev_action']=result
        return result
    except Exception:
        _S1009_REPORT['errors']+=1;return action
'''


def _make_tar(main_bytes: bytes) -> bytes:
    buf = BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, BytesIO(main_bytes))
    return buf.getvalue()


def _weave(h1_src: str):
    """H1→H2：仅替换 step1009 函数体块；返回 (h2_src, audit)。"""
    if "action=_S1009_PARENT(observation,configuration)" not in WEAVED_BODY \
            or "_S1008_PARENT" in WEAVED_BODY:
        raise RuntimeError("织入体父调用漂移（须 _S1009_PARENT；fail-closed）")
    if h1_src.count(BLOCK_DEF) != 1:
        raise RuntimeError("锚点不唯一：BLOCK_DEF 出现 %d 次" % h1_src.count(BLOCK_DEF))
    i = h1_src.index(BLOCK_DEF)
    j = h1_src.index(BLOCK_END)
    if not (i < j):
        raise RuntimeError("锚点顺序异常")
    original = h1_src[i:j]
    h2_src = h1_src[:i] + WEAVED_BODY + h1_src[j:]
    base_lines = h1_src.count("\n", 0, i) + 1
    end_lines = base_lines + original.count("\n")
    audit = {
        "anchor_function": ("step1009_step1008_fortyfirst_final_fixedsell_"
                            "closure_agent"),
        "anchor_role": ("内层链末段单列表构造点（轨道 2 [10122,10134] 行带先例；"
                        "其输出=外挂 X1 的输入；_r36_reserve/step738/928 系列"
                        "构造点均汇入此点）"),
        "h1_changed_line_band": [base_lines, end_lines - 1],
        "prefix_identical": h2_src[:i] == h1_src[:i],
        "suffix_identical": h2_src[len(h2_src) - (len(h1_src) - j):] == h1_src[j:],
        "original_block": original,
        "weaved_block": WEAVED_BODY,
    }
    if not (audit["prefix_identical"] and audit["suffix_identical"]):
        raise RuntimeError("内生版前后缀漂移（fail-closed）")
    audit["diff_lines"] = list(difflib.unified_diff(
        original.splitlines(), WEAVED_BODY.splitlines(),
        fromfile="h1/step1009_body", tofile="h2/step1009_body", lineterm=""))
    audit["diff_all_in_function_body"] = True
    return h2_src, audit


def _check_loaded(data: bytes, form: str):
    try:
        compile(data.decode("utf-8"), "<topform:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: 语法不过: %r" % (form, exc))
    ns = {}
    exec(compile(data.decode("utf-8"), "<topform:%s>" % form, "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    name = loaded[-1].__name__ if loaded else None
    return name


def main():
    h1_bytes = H1_SRC.read_bytes()
    h1_sha = hashlib.sha256(h1_bytes).hexdigest()
    if h1_sha != H1_SHA_EXPECTED:
        raise RuntimeError("H1 sha 漂移：%s" % h1_sha)
    h1_src = h1_bytes.decode("utf-8")
    h2_src, diff_audit = _weave(h1_src)
    h2_bytes = h2_src.encode("utf-8")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "experiment": ("topform 顶端策略升级：榜一卖时蓝图 B1 排水拍相位内生织入"
                       "（step1009 构造点；谷底后置+due 抵扣；视界 H=1）"),
        "h1_src": str(H1_SRC),
        "h1_main_sha256": h1_sha,
        "forms": {},
    }
    datas = {"h2": h2_bytes, "h1": h1_bytes}
    for form in FORMS:
        data = datas[form]
        entry_name = _check_loaded(data, form)
        if entry_name != EXPECTED_ENTRY[form]:
            raise RuntimeError("校验②红 %s: 末 callable=%r 应为 %r"
                               % (form, entry_name, EXPECTED_ENTRY[form]))
        tar_bytes = _make_tar(data)
        out = OUT_DIR / form
        out.mkdir(parents=True, exist_ok=True)
        (out / "main.py").write_bytes(data)
        (out / "submission.tar.gz").write_bytes(tar_bytes)
        form_manifest = {
            "form": form,
            "main_sha256": hashlib.sha256(data).hexdigest(),
            "main_bytes": len(data),
            "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
            "tar_bytes": len(tar_bytes),
            "h1_main_sha256": h1_sha,
            "entry_last_callable": entry_name,
            "byte_identical_to_h1": data == h1_bytes,
            "weave": ("step1009 函数体内生卖时（B1 排水拍相位；无尾块）"
                      if form == "h2" else "现 H1 字节恒等基线"),
            "compile_ok": True,
        }
        (out / "build_manifest.json").write_text(
            json.dumps(form_manifest, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        manifest["forms"][form] = form_manifest
        print(form, form_manifest["main_sha256"][:16],
              form_manifest["main_bytes"], "entry", entry_name, flush=True)

    v3 = manifest["forms"]["h1"]["byte_identical_to_h1"]
    v4 = (diff_audit["prefix_identical"] and diff_audit["suffix_identical"])
    diff_audit["checks"] = {
        "h1_byte_identical_to_H1": v3,
        "h2_diff_confined_to_function_body": v4,
        "h2_last_callable_unchanged": (
            manifest["forms"]["h2"]["entry_last_callable"] == "_hs_agent"),
    }
    if not all(diff_audit["checks"].values()):
        raise RuntimeError("校验③④红：%r" % diff_audit["checks"])
    (EVID_DIR / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    (EVID_DIR / "diff_audit.json").write_text(
        json.dumps(diff_audit, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    print("manifest ->", EVID_DIR / "build_manifest.json", flush=True)
    print("diff_audit ->", EVID_DIR / "diff_audit.json", flush=True)


if __name__ == "__main__":
    main()
