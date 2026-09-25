# -*- coding: utf-8 -*-
"""build_r37（R19/R20 L1）+ 审计/打包子函数。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
以 orderbook_2965_adopt/a/main.py（r34a 在飞件字节）为底复制 →
inject_cash_guard_block + retape_sheep_timing + retape_tail_savings
三白名单改造 → audit_diff_vs_r34a → pack_r37；产物落 orderbook_r37/，
r34a/在飞件零改动。
"""
from __future__ import annotations

from typing import Any, Dict, Optional


def build_r37(r34a_main_path: str,
              out_dir: Optional[str] = None) -> Dict[str, Any]:
    """构建编排：三白名单改造→diff 审计恰=三件→确定性打包+manifest。

    签名意图：输入: r34a main 路径 / 输出: r37 main+manifest+变更集审计 /
    错误: 超白名单即抛。

    【实现方案留档（build 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录（orderbook_r37/build/，与 pack_r37 缺省同址），
      测试以 tmp_path 覆盖；首参与返回主键不变（返回含 main_path/
      main_sha256/manifest/diff_attribution）。
    - 编排流（责任契约 R19/R20）：读 r34a 文本→retape_sheep._decode_routes→
      retape_sheep_timing→retape_tail_savings→_encode_routes→尾块前写两行
      变更表注释→inject_cash_guard_block→audit_diff_vs_r34a→pack_r37。
      r34a 输入只读打开、全程零写回（测试钉字节不变）。
    - 变更表注释（pack 自证口径）：恰两行单行注释
      「# R37_SHEEP_CHANGE_TABLE: <json>」（retape_sheep_timing.change_table）
      与「# R37_TAIL_REMOVAL_LIST: <json>」（retape_tail_savings.removed），
      JSON=canonical（json.dumps sort_keys=True/ensure_ascii=False/紧凑分隔符
      →键序稳定），落位=尾块前（注释行随尾部追加块进 diff 归因区，行文本区
      口径 r37=r34a+恰一尾块成立）。
    - 失败面（不落半成品）：产物落盘前一切红（缺文件/解码红/手术红/注入红/
      审计红）只经 tempfile 暂存件中转，out 目录零触碰（不建目录不落文件）；
      审计过后才写 out/main.py 并 pack，写盘段任一异常即清本次三件产物
      （main.py/submission.tar.gz/build_manifest.json）再抛。
    - 返回：{"main_path", "main_sha256", "tar_sha256", "manifest",
      "diff_attribution", "block_sha", "sheep_change_table",
      "tail_removal_list", "r34a_main_path", "r34a_sha256"}（全 JSON 可序列化）。
    """
    import hashlib
    import os
    import sys
    import tempfile

    try:
        from orderbook_r37 import inject_guard as _ig
        from orderbook_r37 import retape_sheep as _rs
        from orderbook_r37 import retape_tail as _rt
    except ImportError:                      # 脚本态兜底（audit 组同款）
        _here = os.path.dirname(os.path.abspath(__file__))
        if _here not in sys.path:
            sys.path.insert(0, _here)
        import inject_guard as _ig           # type: ignore
        import retape_sheep as _rs           # type: ignore
        import retape_tail as _rt            # type: ignore

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r34a_main_path, str):
        raise TypeError("r34a_main_path must be str, got %s"
                        % type(r34a_main_path).__name__)
    if not isinstance(out_dir, (str, type(None))):
        raise TypeError("out_dir must be str or None, got %s"
                        % type(out_dir).__name__)
    if not r34a_main_path.strip():
        raise ValueError("r34a_main_path must not be empty/whitespace-only")

    with open(r34a_main_path, "rb") as fh:
        b34 = fh.read()                      # 缺文件→FileNotFoundError（落盘前）
    if not b34:
        raise ValueError("r34a main 文件为空：%s" % r34a_main_path)
    t34 = b34.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError（ValueError 子类）

    # ---- 1. 三白名单改造（写时复制链：输入包零改动） ----
    pkg0 = _rs._decode_routes(t34)
    sheep = _rs.retape_sheep_timing(pkg0)
    tail = _rt.retape_tail_savings(sheep["routes"])
    mid = _rs._encode_routes(t34, tail["routes"])

    # ---- 2. 变更表注释（canonical 单行 JSON，尾块前落位） ----
    import json
    sheep_table = sheep["change_table"]
    tail_list = tail["removed"]

    def _canon(o: Any) -> str:
        return json.dumps(o, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"))

    body = mid if mid.endswith("\n") else mid + "\n"
    body += "# R37_SHEEP_CHANGE_TABLE: " + _canon(sheep_table) + "\n"
    body += "# R37_TAIL_REMOVAL_LIST: " + _canon(tail_list) + "\n"
    inj = _ig.inject_cash_guard_block(body)
    r37_bytes = inj["main_text"].encode("utf-8")

    # ---- 3. diff 审计（恰=白名单三件；红即抛，暂存件中转零半成品） ----
    stage = None
    try:
        fd, stage = tempfile.mkstemp(prefix="r37_build_", suffix=".py")
        with os.fdopen(fd, "wb") as fh:
            fh.write(r37_bytes)
        attribution = audit_diff_vs_r34a(stage, r34a_main_path)
    finally:
        if stage is not None and os.path.exists(stage):
            os.remove(stage)

    # ---- 4. 落盘+确定性打包（写盘段红→清本次三件产物再抛） ----
    out = out_dir if out_dir is not None else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "build")
    os.makedirs(out, exist_ok=True)
    main_path = os.path.join(out, "main.py")
    try:
        with open(main_path, "wb") as fh:
            fh.write(r37_bytes)
        manifest = pack_r37(main_path, out_dir=out)
    except BaseException:
        for name in ("main.py", "submission.tar.gz", "build_manifest.json"):
            p = os.path.join(out, name)
            if os.path.exists(p):
                os.remove(p)
        raise

    return {
        "main_path": main_path,
        "main_sha256": manifest["main_sha256"],
        "tar_sha256": manifest["tar_sha256"],
        "manifest": manifest,
        "diff_attribution": attribution,
        "block_sha": inj["block_sha"],
        "sheep_change_table": sheep_table,
        "tail_removal_list": tail_list,
        "r34a_main_path": r34a_main_path,
        "r34a_sha256": hashlib.sha256(b34).hexdigest(),
    }


def audit_diff_vs_r34a(r37_main: str, r34a_main: str) -> Dict[str, Any]:
    """对底版逐字节 diff 审计——差异恰=白名单三件（尾部追加守卫块/羊步点
    变更表/尾盘删除清单），出现白名单外差异即红；输出差异归因表。

    签名意图：输入: r37 main+r34a main / 输出: 归因表 /
    错误: 白名单外差异即抛。

    【实现方案留档（audit 组测试钉住）】
    - 归因表：{"ok", "whitelist": {"tail_guard_block"/"sheep_retiming"/
      "tail_savings"}, "unattributed"}；unattributed 非空→ValueError（消息含
      首条未归因定位）。tail_guard_block={"present","bytes","sha256"}（追加块
      =r37 相对 r34a 的尾部多出字节，sha256 与 inject block_sha 同口径）；
      sheep_retiming={"present","n_moves","moves":[{"order","from","to"}]}；
      tail_savings={"present","n_removed","removed":[{"kind","item","at"}]}。
    - 判定：mask blob payload 后 r37 须=r34a+仅尾部一块（块含守卫锚行恰一次+
      单参入口行、r34a 无锚行），块外行文本零差异（首差定位进消息）；payload
      变更经 retape_sheep._decode_routes 解码两侧、按解码后动作集合差异归因
      （动作对按内容去重、路由下标共享按引用步聚合）：SHEEP 买单步点/槽位移动
      （移出=换 []/移入=尾部追加或空槽，内容多重集守恒）→ sheep_retiming；
      CARE/FEED 单元指令删除与闲置 HIRE 市场单删除→ tail_savings；其余（路由
      结构/shops/别类动作差/解码失败）→ unattributed。
    - 只抛不改；返回可直接进 manifest（全 JSON 可序列化）。
    """
    import hashlib
    import json
    import os
    import re
    import sys

    try:
        from orderbook_r37 import retape_sheep as _rs
    except ImportError:                      # 脚本态兜底（pack_r37 同款）
        _here = os.path.dirname(os.path.abspath(__file__))
        if _here not in sys.path:
            sys.path.insert(0, _here)
        import retape_sheep as _rs           # type: ignore

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r37_main, str):
        raise TypeError("r37_main must be str, got %s" % type(r37_main).__name__)
    if not isinstance(r34a_main, str):
        raise TypeError("r34a_main must be str, got %s" % type(r34a_main).__name__)
    if not r37_main.strip() or not r34a_main.strip():
        raise ValueError("路径不得为空/纯空白")

    with open(r37_main, "rb") as fh:
        b37 = fh.read()
    with open(r34a_main, "rb") as fh:
        b34 = fh.read()
    if not b37:
        raise ValueError("r37 main 文件为空：%s" % r37_main)
    if not b34:
        raise ValueError("r34a main 文件为空：%s" % r34a_main)
    t37 = b37.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError（ValueError 子类）
    t34 = b34.decode("utf-8")

    anchor_str = ("# ============ r37 现金保底守卫尾块（自动生成，勿手改） "
                  "============")
    entry = b"def _r37_agent(observation):"
    rx = re.compile(_rs._BLOB_RE.pattern.encode("utf-8"))
    m37 = list(rx.finditer(b37))
    m34 = list(rx.finditer(b34))

    unattributed: list = []

    def _first_diff(x: bytes, y: bytes) -> int:
        n = min(len(x), len(y))
        for i in range(n):
            if x[i] != y[i]:
                return i
        return n

    def _line(b: bytes, off: int) -> int:
        return b[:off].count(b"\n") + 1

    def _note(kind: str, where: str, detail: str) -> None:
        unattributed.append({"kind": kind, "where": where, "detail": detail[:120]})

    def _is_sheep_buy(o: Any) -> bool:
        return (isinstance(o, list) and len(o) >= 3 and o[0] == "BUY_ANIMAL"
                and o[1] == "SHEEP")

    def _is_hire(o: Any) -> bool:
        return isinstance(o, list) and len(o) >= 1 and o[0] == "HIRE"

    def _j(o: Any) -> str:
        return json.dumps(o, sort_keys=True, ensure_ascii=False)

    # ---- 1. blob 区定位（mask payload 后行文本区=前/后缀） ----
    pay37 = pay34 = b""
    masked37 = masked34 = None
    if len(m37) != len(m34) or len(m37) > 1:
        _note("blob_presence_mismatch" if len(m37) != len(m34)
              else "blob_not_unique", "_R108_DATA blob",
              "r37×%d r34a×%d（期望双方各恰 0/1 且相等）" % (len(m37), len(m34)))
    else:
        if m37:
            lo37, hi37 = m37[0].span(1)
            lo34, hi34 = m34[0].span(1)
            pay37, pay34 = b37[lo37:hi37], b34[lo34:hi34]
            masked37 = b37[:lo37] + b37[hi37:]
            masked34 = b34[:lo34] + b34[hi34:]
        else:
            masked37, masked34 = b37, b34

    # ---- 2. 行文本区零差异 + 尾部恰一块（守卫块识别） ----
    tail_block = {"present": False, "bytes": 0, "sha256": None}
    if masked37 is not None:
        if masked37 == masked34:
            chunk = b""
        elif masked37.startswith(masked34):
            chunk = masked37[len(masked34):]
        else:
            chunk = b""
            off = _first_diff(masked34, masked37)
            _note("line_text_diff",
                  "行文本 r34a 行%d/r37 行%d 字节%d" % (
                      _line(masked34, off), _line(masked37, off), off),
                  "r34a=%r r37=%r" % (masked34[off:off + 16],
                                      masked37[off:off + 16]))
        if chunk:
            if (t37.count(anchor_str) == 1 and t34.count(anchor_str) == 0
                    and entry in chunk):
                tail_block = {"present": True, "bytes": len(chunk),
                              "sha256": hashlib.sha256(chunk).hexdigest()}
            else:
                _note("tail_append_not_guard_block", "尾部追加块",
                      "锚行 r37×%d r34a×%d 入口行=%s 字节%d" % (
                          t37.count(anchor_str), t34.count(anchor_str),
                          entry in chunk, len(chunk)))

    # ---- 3. blob payload 语义归因（解码后动作集合差异分类） ----
    sheep_moves: list = []
    tail_removed: list = []
    n_moves = 0
    n_removed = 0
    if masked37 is not None and pay37 != pay34:
        try:
            pkg34 = _rs._decode_routes(t34)
            pkg37 = _rs._decode_routes(t37)
        except ValueError as exc:
            _note("blob_decode_failure", "_R108_DATA blob 解码", str(exc))
        else:
            want_keys = {"actions", "routes", "shops"}
            if set(pkg34) != want_keys or set(pkg37) != set(pkg34):
                _note("tape_shape", "磁带包键",
                      "r34a=%s r37=%s" % (sorted(pkg34), sorted(pkg37)))
            elif pkg34["shops"] != pkg37["shops"]:
                _note("shops_changed", "shops",
                      "两侧行数 %d/%d" % (len(pkg34["shops"]),
                                        len(pkg37["shops"])))
            else:
                r_a, r_b = pkg34["routes"], pkg37["routes"]
                if set(r_a) != set(r_b) or any(len(r_a[k]) != len(r_b[k])
                                               for k in r_a):
                    _note("route_structure", "routes",
                          "键数 r34a=%d r37=%d" % (len(r_a), len(r_b)))
                else:
                    # 按 (route,step) 解析共享下标逐引用步分类（动作池共享下标，
                    # 同一池件被多路由引用时按引用步各计一次）
                    rem: list = []
                    add: list = []
                    tail_hits: list = []
                    for rid in sorted(r_a, key=str):
                        for t, (ia, ib) in enumerate(zip(r_a[rid], r_b[rid])):
                            o = pkg34["actions"][ia]
                            c = pkg37["actions"][ib]
                            if o == c:
                                continue
                            where = "route %s step %d" % (rid, t)
                            if set(o) != set(c) or set(o) != {
                                    "farmer", "hands", "market"}:
                                _note("action_shape", where, "键 r34a=%s r37=%s"
                                      % (sorted(o), sorted(c)))
                                continue
                            bad = None
                            got = {"rem": [], "add": [], "hire": [],
                                   "del": []}
                            om, cm = o["market"], c["market"]
                            for j in range(max(len(om), len(cm))):
                                x = om[j] if j < len(om) else None
                                y = cm[j] if j < len(cm) else None
                                if x == y:
                                    continue
                                xe = x is None or x == []
                                ye = y is None or y == []
                                if ye and _is_sheep_buy(x):
                                    got["rem"].append((x, j))
                                elif ye and _is_hire(x):
                                    got["hire"].append((x, j))
                                elif xe and _is_sheep_buy(y):
                                    got["add"].append((y, j))
                                else:
                                    bad = "market[%d] %r→%r" % (j, x, y)
                                    break
                            if bad is None:
                                oh, ch = o["hands"], c["hands"]
                                if (not isinstance(oh, list)
                                        or not isinstance(ch, list)
                                        or len(oh) != len(ch)):
                                    bad = "hands 形态 %r→%r" % (oh, ch)
                                else:
                                    slots = [("F", o["farmer"], c["farmer"])]
                                    slots += [("h%d" % i, oh[i], ch[i])
                                              for i in range(len(oh))]
                                    for name, ou, nu in slots:
                                        if ou == nu:
                                            continue
                                        if (isinstance(ou, list) and ou
                                                and ou[0] in ("CARE", "FEED")
                                                and nu in ([], ["PASS"])):
                                            got["del"].append((ou, name))
                                        else:
                                            bad = "unit %s %r→%r" % (
                                                name, ou, nu)
                                            break
                            if bad is not None:
                                _note("action_delta_unclassified", where, bad)
                                continue
                            for x, j in got["rem"]:
                                rem.append({"order": x, "at": [rid, t, j]})
                            for y, j in got["add"]:
                                add.append({"order": y, "at": [rid, t, j]})
                            for x, slot in got["hire"]:
                                tail_hits.append({"kind": "HIRE", "item": x,
                                                  "at": [rid, t, slot]})
                            for ou, name in got["del"]:
                                tail_hits.append({"kind": ou[0], "item": ou,
                                                  "at": [rid, t, name]})
                    n_moves = len(rem)
                    n_removed = len(tail_hits)
                    # SHEEP 买单移动=内容多重集守恒；不守恒即非"移动"
                    bal: Dict[str, int] = {}
                    for e in rem:
                        bal[_j(e["order"])] = bal.get(_j(e["order"]), 0) - 1
                    for e in add:
                        bal[_j(e["order"])] = bal.get(_j(e["order"]), 0) + 1
                    if any(v != 0 for v in bal.values()):
                        _note("sheep_buy_not_conserved", "SHEEP 买单移动",
                              "移出%d 移入%d" % (len(rem), len(add)))
                    else:
                        by_o: Dict[str, Any] = {}
                        for e in rem:
                            by_o.setdefault(_j(e["order"]), {
                                "order": e["order"], "from": [],
                                "to": []})["from"].append(e["at"])
                        for e in add:
                            by_o[_j(e["order"])]["to"].append(e["at"])
                        sheep_moves = [by_o[k] for k in sorted(by_o)]
                    by_r: Dict[Any, Any] = {}
                    for e in tail_hits:
                        k = (e["kind"], _j(e["item"]))
                        by_r.setdefault(k, {"kind": e["kind"], "item": e["item"],
                                            "at": []})["at"].append(e["at"])
                    tail_removed = [by_r[k] for k in sorted(by_r)]
                    # 池件闭合：新侧未被任何路由引用的池件须为旧池件既有内容
                    # （写时复制残件），否则=白名单外私货
                    old_hit: Dict[str, int] = {}
                    for x in pkg34["actions"]:
                        old_hit[_j(x)] = old_hit.get(_j(x), 0) + 1
                    referenced: set = set()
                    for idxs in r_b.values():
                        referenced.update(idxs)
                    for i, act in enumerate(pkg37["actions"]):
                        if i not in referenced and old_hit.get(_j(act), 0) == 0:
                            _note("unreferenced_pool_addition",
                                  "actions[%d]" % i,
                                  "未被路由引用且非旧池件残件: %s" % _j(act)[:80])

    table = {
        "ok": not unattributed,
        "whitelist": {
            "tail_guard_block": tail_block,
            "sheep_retiming": {"present": bool(sheep_moves),
                               "n_moves": n_moves, "moves": sheep_moves},
            "tail_savings": {"present": bool(tail_removed),
                             "n_removed": n_removed, "removed": tail_removed},
        },
        "unattributed": unattributed,
    }
    if unattributed:
        first = unattributed[0]
        raise ValueError("白名单外差异 %d 处；首条未归因：%s（%s）%s"
                         % (len(unattributed), first["where"], first["kind"],
                            first["detail"]))
    return table


def pack_r37(r37_main: str, out_dir: Optional[str] = None) -> Dict[str, Any]:
    """确定性打包+manifest——沿 R16 配方（tarfile mtime0/uid0/gid0/mode644、
    gzip mtime0、双跑逐字节一致）；manifest=基底 sha 链（a16e0e9b→r34a→r37）、
    三白名单件 sha、双跑哈希、描述文案
    "public derivative with cash-floor guard and earlier flock schedule"。

    签名意图：输入: r37 main / 输出: submission.tar.gz+manifest /
    错误: 双跑不一致即抛。

    【实现方案留档（pack 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录，测试以 tmp_path 覆盖；首参与返回形态不变
      （返回=写盘 manifest 字典）。
    - 打包配方单一真源：复用 orderbook_2965_adopt.build_adopt.build_tar_bytes
      （R16/v48 配方零改动语义，不手抄第二份）——单成员 main.py、mtime0/
      uid0/gid0/mode644、gzip filename="" mtime0。双跑两次取字节逐字节比对，
      不等即 RuntimeError（fail-closed）；落盘前再验成员形态（names==['main.py']
      且 mode644/mtime0/uid0/gid0/size、内层 main 逐字节同输入），不符即
      RuntimeError。tar 与 build_manifest.json 落 out_dir。
    - manifest 字段（沿 R16/R17 命名习惯+R19/R20 增补）：schema
      "orderbook_r37_manifest/1.0"、generated（日期）、variant "r37"、
      description（文案原文）、main_sha256/main_bytes、tar_sha256/tar_bytes/
      tar_members/tar_rebuild_reproducible/tar_size_ok（≤100MiB）、
      base_sha_chain、whitelist_shas、whitelist_shas_complete、
      double_run_sha256={run1,run2}（双跑哈希，两值恒等）。
    - base_sha_chain 键=链节点（a16e0e9b→r34a→r37），值=完整 sha256：
      a16e0e9b=round-30 基座 main 钉死值（l1/l2/l3 构建链三方核对同值）；
      r34a=orderbook_2965_adopt/a/main.py 在飞件钉死值（其 build_manifest.json
      main_sha256 同值）；r37=本次输入重算。前两节点为字面钉死（pack 签名
      只见 r37 main，不外读盘）；漂移审计归 verify 体积身份链门。
    - 三白名单件 sha 方案（自洽选定：尾部块识别+内嵌变更表读取，尽力自证
      不造假）：
      ① guard_block=尾部块识别——块首标题行「# =+ r37 现金保底守卫尾块
        （自动生成，勿手改） =+」全文恰现一次且锚前恰两换行；块文本=锚前
        2 字节起至文件尾（恰=inject_cash_guard_block 追加载荷形态），sha256=
        块文本字节 sha（与 inject_cash_guard_block 返回 block_sha 同口径）；
        另验块内含单参入口行「def _r37_agent(observation):」。标题缺→null；
        标题多次/分隔畸形→ValueError。
      ② sheep_change_table/tail_removal_list=内嵌变更表读取——r37 main 恰
        一行注释携带 JSON：「# R37_SHEEP_CHANGE_TABLE: <json>」（
        retape_sheep_timing.change_table，由 build_r37 写入该形态）与
        「# R37_TAIL_REMOVAL_LIST: <json>」（retape_tail_savings.removed）；
        行位置任意、恰一行。sha256=规范 JSON 字节 sha（json.dumps
        sort_keys=True/ensure_ascii=False/紧凑分隔符）——对嵌入空白与键序
        不敏感。缺行→null；重复行/JSON 不可解析→ValueError。
      whitelist_shas_complete=三件全非 null（消费方可 fail-closed）。
    - 错误面：非 str→TypeError；空/纯空白路径→ValueError；空文件→ValueError；
      变更表重复/坏 JSON、锚畸形→ValueError；双跑不一致/成员形态不过→
      RuntimeError；路径不存在→FileNotFoundError。
    """
    import hashlib
    import io
    import json
    import os
    import re
    import tarfile
    import time

    try:
        from orderbook_2965_adopt import build_adopt as _ba
    except ImportError:                      # 脚本态兜底（build_r35 同款）
        import sys
        _adopt = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "orderbook_2965_adopt")
        if _adopt not in sys.path:
            sys.path.insert(0, _adopt)
        import build_adopt as _ba            # type: ignore

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r37_main, str):
        raise TypeError("r37_main must be str, got %s" % type(r37_main).__name__)
    if not r37_main.strip():
        raise ValueError("r37_main must not be empty/whitespace-only")

    with open(r37_main, "rb") as fh:
        main_bytes = fh.read()
    if not main_bytes:
        raise ValueError("r37 main 文件为空：%s" % r37_main)
    text = main_bytes.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError（ValueError 子类）

    # ---- 1. 三白名单件 sha（尾部块识别+内嵌变更表读取，尽力自证） ----
    anchor_re = re.compile(
        (r"^# =+ r37 现金保底守卫尾块（自动生成，勿手改） =+$").encode("utf-8"),
        re.M)
    anchors = list(anchor_re.finditer(main_bytes))
    guard_sha: Optional[str] = None
    if len(anchors) > 1:
        raise ValueError("守卫块锚行出现 %d 次（期望 0/1）" % len(anchors))
    if anchors:
        pos = anchors[0].start()
        if pos < 2 or main_bytes[pos - 2:pos] != b"\n\n":
            raise ValueError("守卫块锚行前分隔畸形（期望恰两换行）：%s" % r37_main)
        block = main_bytes[pos - 2:]
        if b"def _r37_agent(observation):" not in block:
            raise ValueError("尾部块缺单参入口 def _r37_agent(observation):")
        guard_sha = hashlib.sha256(block).hexdigest()

    def _table_sha(marker: str, label: str) -> Optional[str]:
        hits = [ln for ln in text.splitlines() if ln.startswith(marker)]
        if len(hits) > 1:
            raise ValueError("%s 标记行 %d（期望恰 0/1）" % (label, len(hits)))
        if not hits:
            return None
        payload = hits[0][len(marker):].strip()
        try:
            obj = json.loads(payload)
        except ValueError as exc:
            raise ValueError("%s 标记行 JSON 不可解析: %s" % (label, exc)) from exc
        canon = json.dumps(obj, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(canon).hexdigest()

    sheep_sha = _table_sha("# R37_SHEEP_CHANGE_TABLE:", "羊步点变更表")
    tail_sha = _table_sha("# R37_TAIL_REMOVAL_LIST:", "尾盘删除清单")
    whitelist = {
        "guard_block": guard_sha,
        "sheep_change_table": sheep_sha,
        "tail_removal_list": tail_sha,
    }
    complete = all(v is not None for v in whitelist.values())

    # ---- 2. 确定性打包：双跑逐字节（不等即抛）+成员形态校验 ----
    tar1 = _ba.build_tar_bytes(main_bytes)
    tar2 = _ba.build_tar_bytes(main_bytes)
    if tar1 != tar2:
        raise RuntimeError("tar 双跑不一致（非确定性，fail-closed）：%s" % r37_main)
    with tarfile.open(fileobj=io.BytesIO(tar1), mode="r:gz") as tar:
        members = tar.getmembers()
        names = [m.name for m in members]
        inner = tar.extractfile("main.py").read() if "main.py" in names else None
    shape_ok = (len(members) == 1 and members[0].name == "main.py"
                and members[0].mode == 0o644 and members[0].mtime == 0
                and members[0].uid == 0 and members[0].gid == 0
                and members[0].size == len(main_bytes))
    if names != ["main.py"] or inner != main_bytes or not shape_ok:
        raise RuntimeError("tar 成员形态校验失败（R16 配方钉死面）：%s" % names)

    out = out_dir if out_dir is not None else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "build")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "submission.tar.gz"), "wb") as fh:
        fh.write(tar1)

    # ---- 3. manifest（R16/R17 惯例键 + R19/R20 增补） ----
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    manifest = {
        "schema": "orderbook_r37_manifest/1.0",
        "generated": time.strftime("%Y-%m-%d"),
        "variant": "r37",
        "description": ("public derivative with cash-floor guard "
                        "and earlier flock schedule"),
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": hashlib.sha256(tar1).hexdigest(),
        "tar_bytes": len(tar1),
        "tar_members": names,
        "tar_rebuild_reproducible": True,
        "tar_size_ok": len(tar1) <= 100 * 1024 * 1024,
        "base_sha_chain": {
            "a16e0e9b": ("a16e0e9b40c489972630a0b9d04f30e9c1cab031"
                         "59fa78676db74277d84d82ab"),
            "r34a": ("51fc19dba2d0bcbf2d0a3720c26ff318541a0e6c"
                     "e5800873bc863f612451aa5b"),
            "r37": main_sha,
        },
        "whitelist_shas": whitelist,
        "whitelist_shas_complete": complete,
        "double_run_sha256": {"run1": hashlib.sha256(tar1).hexdigest(),
                              "run2": hashlib.sha256(tar2).hexdigest()},
    }
    with open(os.path.join(out, "build_manifest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return manifest
