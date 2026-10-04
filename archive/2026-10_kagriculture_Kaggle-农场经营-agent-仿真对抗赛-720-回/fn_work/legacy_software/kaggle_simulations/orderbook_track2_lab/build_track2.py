# -*- coding: utf-8 -*-
"""build_track2：track2 内生重构对照实验三形态构建（对照实验·不发射·不提交）。

实验命题（教训定理正用）：外挂层重复基座内生机制必负（R28/I2/K1 同型），
正解=做进内层。对照：把 X1 卫生层（同拍碎单合并+幻影死单清理）从外挂尾块
改写为内生版——融入 H1 内层卖单构造路径的末段单列表构造点
（step1009_step1008_fortyfirst_final_fixedsell_closure_agent 的函数体，
该函数是内层链最后一个组装 market 列表/槽位的构造点，其输出即外挂 X1 的
输入；_r36_reserve/step738/928 系列构造点均汇入此点）。

三形态：
- h1_outer：现 H1 字节恒等（build/h1/main.py，sha 76b5f842…=haodou V82+
  外挂 X1 卫生层尾块）；
- h1_inner：内生版——基座内 step1009 函数体内织入 X1 同语义卫生
  （同拍碎单并最早槽/幻影死单清理/零跨拍），卫生成为内层链原生一步
  （改动落在内层函数体；末 callable 不变=pet_any_demand_agent；无尾块）；
- h1_base：无卫生（haodou V82 采纳件字节，sha bdb82117…）。

内生版语义=X1 同：同拍合并量守恒/幻影清理（qty<=0 死单、超库存 clamp）/
零跨拍挪量；触发窗 step>=624（窗外同对象零足迹）；异常吞掉回退。
内生版的机制差：卫生改动走基座内生 _RACE_STATE['prev_action'] 台账同步
（外挂 X1 在宿主返回后改动作、不同步台账=账本脱钩；内生版同拍同步）。

校验（fail-closed）：①三形态 compile ②exec 装载后末 callable 名符合
（inner/base=pet_any_demand_agent 不变，outer=_hs_agent）③outer 与现 H1
字节恒等 ④base 与采纳件字节恒等 ⑤inner=base 仅 step1009 体带改动
（diff 全部落在内层函数体行带；块外前后缀逐字恒等）。
只写 orderbook_track2_lab/。
"""
from __future__ import annotations

import difflib
import hashlib
import io
import json
import tarfile
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
ADOPT_DIR = KSIM_DIR / "orderbook_haodou_adopt"
BASE_TAR = ADOPT_DIR / "submission.tar.gz"
H1_OUTER_SRC = (KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1"
                / "main.py")
OUT_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"
SCHEMA = "orderbook_track2_lab_manifest/1.0"

BASE_SHA_EXPECTED = ("bdb821178ca73c0e8480f06c1887e20921caea0438398a5edb68bd9"
                     "ad20b1de8")
OUTER_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764"
                      "974b22f337")
FORMS = ("h1_outer", "h1_inner", "h1_base")

# ---- 内层改动锚点：step1009 函数体（内层链末段单列表构造点） ----
BLOCK_DEF = ("def step1009_step1008_fortyfirst_final_fixedsell_closure_agent("
             "observation,configuration=None):")
BLOCK_END = ("step1009_step1008_fortyfirst_final_fixedsell_closure_agent"
             ".telemetry=_S1009_REPORT")

# 内生版替换体：签名/父调用/外层异常兜底逐字保留；_s793_reorder 之后织入
# X1 同语义卫生（_hy_post），卫生改动经既有 _s834_key 台账分支同步
# _RACE_STATE['prev_action']（内生台账纪律）。辅助函数以嵌套函数收进函数体
# （改动不外溢模块级）。计量口径与 layer_x1._X1_REPORT 同名同义。
WEAVED_BODY = '''def step1009_step1008_fortyfirst_final_fixedsell_closure_agent(observation,configuration=None):
    # ---- track2 内生 X1 卫生（同拍碎单并最早槽 + 幻影死单清理；零跨拍） ----
    def _hy_qty(raw):
        if isinstance(raw,bool):
            return None
        if isinstance(raw,int):
            return raw
        if isinstance(raw,float) and raw.is_integer():
            return int(raw)
        return None
    def _hy_projected(obs,act):
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
                shed=((obs or {}).get('private') or {}).get('shed') or {}
                return {k:int(v) for k,v in dict(shed).items()}
            except Exception:
                return {}
    def _hy_post(obs,act):
        _h=_S1009_REPORT.setdefault('hyg',dict(calls=0,changed_turns=0,dropped_dead=0,clamped_orders=0,clamped_qty=0,merged_fragments=0,merged_qty=0,unparsed_kept=0,window_out=0,errors=0,ticks=[]))
        _h['calls']+=1
        try:
            if not isinstance(act,dict):
                return act
            market=act.get('market')
            if not isinstance(market,list) or not market:
                return act
            try:
                step=int((obs or {}).get('step',0))
            except Exception:
                step=0
            if step<624:
                _h['window_out']+=1
                return act
            avail=dict(_hy_projected(obs,act))
            kept=[]
            changed=False
            for entry in market:
                is_sell=(isinstance(entry,(list,tuple)) and len(entry)>=3 and entry[0]=='SELL')
                if not is_sell:
                    kept.append(['other',entry])
                    if isinstance(entry,(list,tuple)) and len(entry)>=3 and entry[0] in ('BUY_PRODUCT','BUY_ANIMAL'):
                        q=_hy_qty(entry[2])
                        if q is not None and q>0:
                            avail[entry[1]]=avail.get(entry[1],0)+q
                    continue
                item=entry[1]
                qty=_hy_qty(entry[2])
                if qty is None:
                    kept.append(['other',entry])
                    _h['unparsed_kept']+=1
                    continue
                if qty<=0:
                    changed=True
                    _h['dropped_dead']+=1
                    continue
                have=avail.get(item,0)
                n=qty if qty<=have else have
                if n<qty:
                    changed=True
                    _h['clamped_orders']+=1
                    _h['clamped_qty']+=qty-n
                if n<=0:
                    changed=True
                    _h['dropped_dead']+=1
                    continue
                avail[item]=have-n
                target=-1
                for i,rec in enumerate(kept):
                    if rec[0]=='sell' and rec[1][1]==item:
                        target=i
                        break
                if target>=0:
                    cross_buy=any(rec[0]=='other' and isinstance(rec[1],(list,tuple)) and len(rec[1])>=3 and rec[1][0] in ('BUY_PRODUCT','BUY_ANIMAL') and rec[1][1]==item for rec in kept[target+1:])
                    if not cross_buy:
                        kept[target][1]=['SELL',item,_hy_qty(kept[target][1][2])+n]
                        changed=True
                        _h['merged_fragments']+=1
                        _h['merged_qty']+=n
                        continue
                if n==qty:
                    kept.append(['sell',entry])
                else:
                    kept.append(['sell',['SELL',item,n]])
            out=[rec[1] for rec in kept][:10]
            if not changed:
                return act
            _h['changed_turns']+=1
            if len(_h['ticks'])<400:
                _h['ticks'].append(step)
            return dict(act,market=out)
        except Exception:
            _h['errors']+=1
            return act
    if int(observation.get('step',0))==0:_S1009_REPORT.update(calls=0,changed=0,errors=0,hyg=dict(calls=0,changed_turns=0,dropped_dead=0,clamped_orders=0,clamped_qty=0,merged_fragments=0,merged_qty=0,unparsed_kept=0,window_out=0,errors=0,ticks=[]))
    _S1009_REPORT['calls']+=1
    action=_S1009_PARENT(observation,configuration)
    try:
        result=_s793_reorder(observation,action)
        result=_hy_post(observation,result)
        if _s834_key(result)!=_s834_key(action):
            _S1009_REPORT['changed']+=1
            st=_RACE_STATE.get(int(observation.get('player',0)))
            if st is not None and st.get('prev_action') is not None and st.get('step')==int(observation.get('step',0)):st['prev_action']=result
        return result
    except Exception:
        _S1009_REPORT['errors']+=1;return action
'''


def _read_base_from_tar():
    with tarfile.open(fileobj=io.BytesIO(BASE_TAR.read_bytes()),
                      mode="r:gz") as tar:
        member = tar.extractfile("main.py")
        if member is None:
            raise RuntimeError("submission.tar.gz 内无 main.py")
        return member.read()


def _make_tar(main_bytes):
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name="main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    return buf.getvalue()


def _weave(base_src):
    """基座→内生版：仅替换 step1009 函数体块；返回 (inner_src, audit)。"""
    if "action=_S1009_PARENT(observation,configuration)" not in WEAVED_BODY \
            or "_S1008_PARENT" in WEAVED_BODY:
        raise RuntimeError("织入体父调用漂移（须 _S1009_PARENT；fail-closed）")
    if base_src.count(BLOCK_DEF) != 1:
        raise RuntimeError("锚点不唯一：BLOCK_DEF 出现 %d 次"
                           % base_src.count(BLOCK_DEF))
    i = base_src.index(BLOCK_DEF)
    j = base_src.index(BLOCK_END)
    if not (i < j):
        raise RuntimeError("锚点顺序异常")
    original = base_src[i:j]
    inner_src = base_src[:i] + WEAVED_BODY + base_src[j:]
    base_lines = base_src.count("\n", 0, i) + 1
    end_lines = base_lines + original.count("\n")
    audit = {
        "anchor_function": "step1009_step1008_fortyfirst_final_fixedsell_closure_agent",
        "anchor_role": ("内层链末段单列表构造点（_s793_reorder 组装 market 列表/"
                        "槽位；其输出=外挂 X1 的输入；_r36_reserve/step738/928 "
                        "系列构造点均汇入此点）"),
        "base_changed_line_band": [base_lines, end_lines - 1],
        "prefix_identical": inner_src[:i] == base_src[:i],
        "suffix_identical": inner_src[len(inner_src) - (len(base_src) - j):]
                            == base_src[j:],
        "original_block": original,
        "weaved_block": WEAVED_BODY,
    }
    if not (audit["prefix_identical"] and audit["suffix_identical"]):
        raise RuntimeError("内生版前后缀漂移（fail-closed）")
    diff = list(difflib.unified_diff(original.splitlines(),
                                     WEAVED_BODY.splitlines(),
                                     fromfile="base/step1009_body",
                                     tofile="inner/step1009_body", lineterm=""))
    audit["diff_lines"] = diff
    audit["diff_all_in_function_body"] = True
    return inner_src, audit


def _check_loaded(data, form):
    """校验①②：compile + exec 装载后末 callable 名。"""
    try:
        compile(data.decode("utf-8"), "<track2:%s>" % form, "exec")
    except Exception as exc:
        raise RuntimeError("校验①红 %s: 语法不过: %r" % (form, exc))
    ns = {}
    exec(compile(data.decode("utf-8"), "<track2:%s>" % form, "exec"), ns)
    loaded = [v for v in ns.values() if callable(v)]
    name = loaded[-1].__name__ if loaded else None
    return name, ns


def main():
    base_bytes = _read_base_from_tar()
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != BASE_SHA_EXPECTED:
        raise RuntimeError("基座 sha 漂移：%s" % base_sha)
    base_src = base_bytes.decode("utf-8")
    if not base_src.endswith("\n"):
        raise RuntimeError("基座不以换行收尾（fail-closed）")
    outer_bytes = H1_OUTER_SRC.read_bytes()
    outer_sha = hashlib.sha256(outer_bytes).hexdigest()
    if outer_sha != OUTER_SHA_EXPECTED:
        raise RuntimeError("现 H1 sha 漂移：%s" % outer_sha)
    inner_src, diff_audit = _weave(base_src)
    inner_bytes = inner_src.encode("utf-8")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    expected_entry = {
        "h1_outer": "_hs_agent",
        "h1_inner": "pet_any_demand_agent",
        "h1_base": "pet_any_demand_agent",
    }
    manifest = {
        "schema": SCHEMA,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "experiment": ("track2 内生 vs 外挂对照：X1 卫生层（同拍碎单合并+幻影"
                       "死单清理）内生版=织入 step1009 单列表构造点函数体"),
        "base_tar": str(BASE_TAR),
        "base_main_sha256": base_sha,
        "outer_src": str(H1_OUTER_SRC),
        "outer_main_sha256": outer_sha,
        "forms": {},
    }
    datas = {"h1_outer": outer_bytes, "h1_inner": inner_bytes,
             "h1_base": base_bytes}
    for form in FORMS:
        data = datas[form]
        entry_name, _ = _check_loaded(data, form)
        if entry_name != expected_entry[form]:
            raise RuntimeError("校验②红 %s: 末 callable=%r 应为 %r"
                               % (form, entry_name, expected_entry[form]))
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
            "base_main_sha256": base_sha,
            "outer_main_sha256": outer_sha,
            "entry_last_callable": entry_name,
            "byte_identical_to_H1_outer": data == outer_bytes,
            "byte_identical_to_base": data == base_bytes,
            "weave": "step1009 函数体内生卫生（无尾块）" if form == "h1_inner"
                     else ("外挂 X1 尾块（字节恒等现 H1）" if form == "h1_outer"
                           else "无卫生基座（字节恒等采纳件）"),
            "compile_ok": True,
        }
        (out / "build_manifest.json").write_text(
            json.dumps(form_manifest, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        manifest["forms"][form] = form_manifest
        print(form, form_manifest["main_sha256"][:16],
              form_manifest["main_bytes"], "entry", entry_name, flush=True)

    # ---- 校验③④⑤：outer/base 字节恒等 + inner diff 圈禁 ----
    v3 = manifest["forms"]["h1_outer"]["byte_identical_to_H1_outer"]
    v4 = manifest["forms"]["h1_base"]["byte_identical_to_base"]
    v5 = (diff_audit["prefix_identical"] and diff_audit["suffix_identical"])
    diff_audit["checks"] = {
        "outer_byte_identical_to_H1": v3,
        "base_byte_identical_to_adopt": v4,
        "inner_diff_confined_to_function_body": v5,
        "inner_last_callable_unchanged": (
            manifest["forms"]["h1_inner"]["entry_last_callable"]
            == "pet_any_demand_agent"),
    }
    if not all(diff_audit["checks"].values()):
        raise RuntimeError("校验③④⑤红：%r" % diff_audit["checks"])
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
