# -*- coding: utf-8 -*-
"""build_r40 + audit_diff_r40_vs_r37 + pack_r40（R23 L1/L2）。

责任契约：r37 字节为底 → build_route_library 建续段库 → retape_sell_lots
卖单批量化手术 → inject_r40_block 注入运行时件链（续段选择器/选路接线/
竞速/补洞）→
audit → pack_r40；r37 零改动。
"""
from __future__ import annotations

from typing import Any, Dict, Optional

# 块锚行核心短语（与 inject_r40._BLOCK_CORE 同值，test 钉一致）。
_CORE = "r40 运行时尾块"

# 变更表注释单行标记（build_r40 内嵌单行=标记+" "+canonical json；audit/pack
# 按 startswith 认账，恰 0/1 行）。
_LOT_MARKER = "# R40_LOT_CHANGE_TABLE:"

# 库 sha 伴生行标记（pack 兜底认账，恰 0/1 行）。
_LIB_MARKER = "# R40_LIBRARY_SHA256:"

# base_sha_chain 前两节点字面（a16e0e9b=round-30 基座 main、r34a=orderbook_
# 2965_adopt/a/main.py 在飞件；pack 签名只见 r40 main 不外读盘，钉死常量）。
_A16 = ("a16e0e9b40c489972630a0b9d04f30e9c1cab031"
        "59fa78676db74277d84d82ab")
_R34A = ("51fc19dba2d0bcbf2d0a3720c26ff318541a0e6c"
         "e5800873bc863f612451aa5b")

# 建库语料（route_library_realrun 同配方）：top 回放两目录 + analysis24 败局
# 12 局（kagr23/kagr22/kagr24 定位，去重后 77 局 49 族=真库 0236c30e…）。
CORPUS_DIRS = ("/tmp/kagr23", "/tmp/kagr22")
LOSS_IDS = (113735225, 113817068, 113754147, 113852533, 113962831, 113724375,
            113837634, 113873625, 114064544, 113838925, 113764768, 113738419)
LOSS_SEARCH_DIRS = ("/tmp/kagr23", "/tmp/kagr22", "/tmp/kagr24")

# 四组件全集（①路由切换 ②卖单批量化 ③抢价 ④清坑）；components 配置参可选
# 子集（B32 修订批间登记）：缺省 None=全四件（历史字节稳）。
COMPONENTS = ("route_select", "sell_lots", "race_slots", "slot_hygiene")


def _resolve_components(components: Any) -> tuple:
    """components→启用组件元组（COMPONENTS 序）；None=全四件；非法即抛。

    至少启用一件运行时件（route_select/race_slots/slot_hygiene）——纯磁带件
    形态（sell_lots 单件）不在本管线（探针件 ablation_r40 自行组装）。
    """
    if components is None:
        return COMPONENTS
    if isinstance(components, (str, bytes)) or not isinstance(
            components, (list, tuple, set, frozenset)):
        raise ValueError("components 须为组件名序列或 None，得到 %r"
                         % (components,))
    want = set()
    for c in components:
        if c not in COMPONENTS:
            raise ValueError("components 未知组件 %r（仅 %s）"
                             % (c, sorted(COMPONENTS)))
        want.add(c)
    out = tuple(c for c in COMPONENTS if c in want)
    if not out:
        raise ValueError("components 不得为空")
    if not any(c in want for c in ("route_select", "race_slots",
                                   "slot_hygiene")):
        raise ValueError("components 至少启用一件运行时件"
                         "（route_select/race_slots/slot_hygiene）")
    return out


def build_r40(r37_main_path: str,
              out_dir: Optional[str] = None,
              components: Any = None) -> Dict[str, Any]:
    """构建编排：建续段库→卖单手术→注入运行时件链→审计→打包。

    签名意图：输入: r37 main 路径 / 输出: r40 main+manifest+变更集审计 /
    错误: 超白名单即抛。

    【实现方案留档（build 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录（orderbook_r40/build/，与 pack_r40 缺省同址），
      测试以 tmp_path 覆盖；首参与返回主键不变。
    - 签名微调登记（B32 修订批间）：新增第三参 components: Any=None——四组件
      （COMPONENTS=route_select/sell_lots/race_slots/slot_hygiene）开关，缺省
      None=全四件（历史字节稳，测试钉形态不变）；子集=只做所选件手术/注入
      （sell_lots 关=磁带零改动+变更表空登记注释行照落，manifest 三 sha 对账
      面不变；运行时件关=inject_r40_block 只抽所选件）；纯磁带件形态不在本
      管线（_resolve_components 拦）。
    - 编排流（责任契约 R23）：读 r37 文本（只读打开、全程零写回，测试钉字节
      不变）→ retape_sheep._decode_routes 解码磁带路由包 →
      retape_sell_lots 卖单批量化手术（写时复制、输入零改动；缺省参数
      max_orders_target=337/window=d21-28）→ _encode_routes 回写（四件自检
      链）→ 变更表注释内嵌单行「# R40_LOT_CHANGE_TABLE: <json>」（canonical
      json：sort_keys+紧凑分隔+ensure_ascii=False，单行落 base 尾部；
      sell_lots_change_sha256=该 JSON utf-8 字节 sha256）→
      build_route_library 建续段库（语料=CORPUS_DIRS 回放+LOSS_IDS 败局 12 局
      =77 局真库，记录 sha=build_audit.library_sha）→ inject_r40_block 注入
      运行时尾块（件链+内嵌库）→ audit_diff_r40_vs_r37（带 change_table，
      两类白名单）→ pack_r40。
    - 失败面（不落半成品，B18/B26 build 同款）：落盘前一切红（缺文件/解码红/
      手术红/建库红/注入红/审计红）只经 tempfile 暂存件中转，out 目录零触碰
      （不建目录不落文件）；审计过后才写 out/main.py 并 pack，写盘段任一异常
      即清本次三件产物（main.py/submission.tar.gz/build_manifest.json）再抛。
    - 写盘段 fail-closed 自检：audit/manifest 运行时块 sha==inject block_sha、
      manifest route_library_sha256==build_audit.library_sha、manifest
      sell_lots_change_sha256==audit sell_lots sha==变更表 canonical sha、
      manifest complete==True，任一不符即 RuntimeError（清三件再抛）。
    - 返回：{"main_path", "main_sha256", "tar_sha256", "manifest",
      "diff_attribution", "block_sha", "library_sha256",
      "sell_lots_change_sha256"}（全 JSON 可序列化）。
    """
    import hashlib
    import json
    import os
    import sys
    import tempfile

    try:
        from orderbook_r40 import inject_r40 as _ij
        from orderbook_r40 import retape_lots as _rt
        from orderbook_r40 import route_library as _rl
        from orderbook_r37 import retape_sheep as _rs
    except ImportError:                      # 脚本态兜底（B18 build 同款）
        _here = os.path.dirname(os.path.abspath(__file__))
        if _here not in sys.path:
            sys.path.insert(0, _here)
        import inject_r40 as _ij             # type: ignore
        import retape_lots as _rt            # type: ignore
        import route_library as _rl          # type: ignore
        _r37dir = os.path.join(os.path.dirname(_here), "orderbook_r37")
        if _r37dir not in sys.path:
            sys.path.insert(0, _r37dir)
        import retape_sheep as _rs           # type: ignore

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r37_main_path, str):
        raise TypeError("r37_main_path must be str, got %s"
                        % type(r37_main_path).__name__)
    if not isinstance(out_dir, (str, type(None))):
        raise TypeError("out_dir must be str or None, got %s"
                        % type(out_dir).__name__)
    if not r37_main_path.strip():
        raise ValueError("r37_main_path must not be empty/whitespace-only")
    comps = _resolve_components(components)

    with open(r37_main_path, "rb") as fh:
        b37 = fh.read()                      # 缺文件→FileNotFoundError（落盘前）
    if not b37:
        raise ValueError("r37 main 文件为空：%s" % r37_main_path)
    t37 = b37.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError（ValueError 子类）

    # ---- 1. 卖单批量化手术（写时复制，r37 零改动）→变更表注释内嵌单行 ----
    # components 关 sell_lots→磁带零改动、变更表空登记（注释行照落=manifest
    # 三 sha 对账面不变）。
    if "sell_lots" in comps:
        pkg = _rs._decode_routes(t37)
        # cross_step=False（B32 消融机制修正）：只同拍并单零时序移动——
        # 跨拍 run 合并落点=更早步点=提前抛售，单件 h2h 0.3667→0.875 实证。
        lot = _rt.retape_sell_lots(pkg, cross_step=False)
        change_table = lot["change_table"]
        t40 = _rs._encode_routes(t37, lot["routes"])
    else:
        change_table = []
        t40 = t37
    canon = json.dumps(change_table, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False)   # 变更表 canonical json（单行）
    comment = _LOT_MARKER + " " + canon + "\n"
    base_text = t40 if t40.endswith("\n") else t40 + "\n"
    base_text = base_text + comment
    lot_sha = hashlib.sha256(canon.encode("utf-8")).hexdigest()

    # ---- 2. 建续段库→注入运行时尾块（库数据随块内嵌；件集=components） ----
    built = _rl.build_route_library(_corpus_files(), None)   # 真库语料（契约钉）
    runtime_comps = tuple(c for c in comps if c != "sell_lots")
    inj = _ij.inject_r40_block(base_text, built, components=runtime_comps)
    r40_bytes = inj["main_text"].encode("utf-8")
    block_sha = inj["block_sha"]

    # ---- 3. diff 审计（两类白名单；红即抛，暂存件中转零半成品） ----
    stage = None
    try:
        fd, stage = tempfile.mkstemp(prefix="r40_build_", suffix=".py")
        with os.fdopen(fd, "wb") as fh:
            fh.write(r40_bytes)
        attribution = audit_diff_r40_vs_r37(stage, r37_main_path, change_table)
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
            fh.write(r40_bytes)
        manifest = pack_r40(main_path, out_dir=out)
        # fail-closed 自检：块 sha/库 sha/变更表 sha/complete 对账（不过即红）
        rb = attribution["whitelist"]["runtime_block"]
        sl = attribution["whitelist"]["sell_lots"]
        if (rb["sha256"] != block_sha
                or manifest["runtime_block"]["sha256"] != block_sha):
            raise RuntimeError(
                "块 sha 对账红：inject=%s audit=%s pack=%s"
                % (block_sha, rb["sha256"], manifest["runtime_block"]["sha256"]))
        lib_sha = built["build_audit"]["library_sha"]
        if manifest["route_library_sha256"] != lib_sha:
            raise RuntimeError(
                "库 sha 对账红：pack=%s build_audit=%s"
                % (manifest["route_library_sha256"], lib_sha))
        if (manifest["sell_lots_change_sha256"] != lot_sha
                or sl["sha256"] != lot_sha):
            raise RuntimeError(
                "sell_lots 变更表 sha 对账红：pack=%s audit=%s 变更表=%s"
                % (manifest["sell_lots_change_sha256"], sl["sha256"], lot_sha))
        if not manifest["complete"]:
            raise RuntimeError("manifest 自证不完整（complete=False）")
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
        "block_sha": block_sha,
        "library_sha256": manifest["route_library_sha256"],
        "sell_lots_change_sha256": lot_sha,
    }


def _corpus_files() -> list:
    """建库语料清单：CORPUS_DIRS 回放 + LOSS_IDS 败局 12 局（缺件跳过，
    语料不足交 build_route_library min_games 把关）。"""
    from pathlib import Path
    out = []
    seen = set()
    for d in CORPUS_DIRS:
        for p in sorted(Path(d).glob("episode-*-replay.json")):
            if p.name not in seen:
                seen.add(p.name)
                out.append(str(p))
    for eid in LOSS_IDS:
        name = "episode-%d-replay.json" % eid
        if name in seen:
            continue
        hit = next((Path(d) / name for d in LOSS_SEARCH_DIRS
                    if (Path(d) / name).exists()), None)
        if hit is not None:
            seen.add(name)
            out.append(str(hit))
    return out


def audit_diff_r40_vs_r37(r40_main: str, r37_main: str,
                          change_table: Any = None) -> Dict[str, Any]:
    """白名单两类审计——①尾部运行时块（含库）②磁带 sell_lots diff（变更表
    归因）；白名单外即抛；输出归因表。

    签名意图：输入: r40 main+r37 main+change_table / 输出: 归因表 /
    错误: 白名单外即抛。

    【实现方案留档（audit 组测试钉住）】
    - 签名微调登记（批间）：首两参=文件路径（B26 audit_diff_vs_r37 同规）；
      change_table=None=不许磁带差异与注释行的纯尾块形态（sell_lots 类零登记，
      任何磁带区差异=unattributed），list（可空）=两类白名单。
    - 白名单两类：①尾部运行时块（锚行识别只按核心短语「r40 运行时尾块」所在
      行识别，不钉 === 装饰；全文恰 r40 1/r37 0；锚行前恰两换行=B17 前置空行
      形态，块=该处至文件尾，bytes/sha 与 inject_r40_block.block_sha 同口径）
      ②磁带区 sell_lots diff（两侧 _R108_DATA blob 解码对比，差异恰=卖单
      批量化手术且逐条对应 change_table 登记→归类 sell_lots；其余 blob 差异/
      前缀破坏→unattributed 即抛）。
    - 归因表：{"ok", "whitelist": {"runtime_block": {"present","bytes",
      "sha256"}, "sell_lots": {"present","rows","changed_routes","sha256"}},
      "unattributed"}；unattributed 非空→ValueError（消息含首条定位，格式沿
      B26）。runtime_block=present 在场与否（零差异→False/bytes 0/sha None）；
      sell_lots=present（磁带区/注释差异在场）、rows（变更表条数）、
      changed_routes（登记路由升序，数字串按数值）、sha256（变更表 canonical
      json sha，ensure_ascii=False 口径=sell_lots_change_sha256 同源）。
    - 基座区形态：blob 前缀逐字节恒等；blob 后缀=r37 后缀+可选单行注释
      「# R40_LOT_CHANGE_TABLE: <json>」（build_r40 内嵌同口径；注释
      canonical sha 须==change_table 参数 canonical sha，不符/坏值/
      change_table=None 时在场→unattributed）。
    - 磁带区归因（sell_lots，B26 shear 归因同款双向对应）：
      结构面——shops/route 键集/route 步数恒等；动作池写时复制形态（被引用
      池件零改动、无主池件=actions[0] 内容=_pool_residue_sweep 池归一口径）；
      步内非卖单槽/单元指令恒等，卖单槽只许同品改量或清 []（空槽不填单）。
      登记面——change_table 逐行（kind=sell_lots）按行序对 (route,item,step)
      卖单状态机重放（同拍并单/跨拍批量化：落点=最早 (step,slot)、qty=登记
      合计、from_steps 含落点步且 to_step=min(from_steps)（只提前不推后）），
      重放终态⟺磁带实测卖单终态逐 (route,item,step,slot,qty) 双向恒等
      （登记格外差异/虚报登记/行形态坏→unattributed）。
    - 只抛不改；返回可直接进 manifest（全 JSON 可序列化）。
    """
    import hashlib
    import json
    import os
    import sys

    core = _CORE

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r40_main, str):
        raise TypeError("r40_main must be str, got %s" % type(r40_main).__name__)
    if not isinstance(r37_main, str):
        raise TypeError("r37_main must be str, got %s" % type(r37_main).__name__)
    if not isinstance(change_table, (list, type(None))):
        raise TypeError("change_table must be list or None, got %s"
                        % type(change_table).__name__)
    if not r40_main.strip() or not r37_main.strip():
        raise ValueError("路径不得为空/纯空白")

    with open(r40_main, "rb") as fh:
        b40 = fh.read()
    with open(r37_main, "rb") as fh:
        b37 = fh.read()
    if not b40:
        raise ValueError("r40 main 文件为空：%s" % r40_main)
    if not b37:
        raise ValueError("r37 main 文件为空：%s" % r37_main)
    t40 = b40.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError
    t37 = b37.decode("utf-8")

    un: list = []

    def _note(kind, where, detail):
        un.append({"kind": kind, "where": where, "detail": detail[:120]})

    def _fd(x, y):                      # 首差字符偏移
        n = min(len(x), len(y))
        for i in range(n):
            if x[i] != y[i]:
                return i
        return n

    def _ln(t, off):                    # 偏移→行号
        return t[:off].count("\n") + 1

    def _canon_sha(obj):
        blob = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    rows = list(change_table) if change_table is not None else []
    try:
        lot_sha = _canon_sha(rows)
    except Exception as exc:
        raise ValueError("变更表不可 canonical sha: %r" % exc) from exc

    # ---- 1. 尾部运行时块锚行识别（核心短语口径，不钉 === 装饰） ----
    tail_block = {"present": False, "bytes": 0, "sha256": None}
    base40 = t40
    n37, n40 = t37.count(core), t40.count(core)
    if n37 != 0:
        _note("anchor_in_base", "块锚行",
              "核心短语在 r37 底版出现 %d 次（期望 0）" % n37)
    if n40 > 1:
        _note("anchor_duplicate", "块锚行",
              "核心短语出现 %d 次（期望恰 1）" % n40)
    if n40 == 1:
        phrase_off = t40.find(core)
        anchor_start = t40.rfind("\n", 0, phrase_off) + 1
        if anchor_start < 2 or t40[anchor_start - 2:anchor_start] != "\n\n":
            _note("block_separator", "块锚行 偏移%d" % phrase_off,
                  "锚行前分隔畸形（期望恰两换行·B17 前置空行）")
        else:
            base40 = t40[:anchor_start - 2]
            chunk = t40[anchor_start - 2:]
            chunk_bytes = chunk.encode("utf-8")
            tail_block = {"present": True, "bytes": len(chunk_bytes),
                          "sha256": hashlib.sha256(chunk_bytes).hexdigest()}

    # ---- 2. 变更表登记面（行形态+路由升序 changed_routes） ----
    rows_by_route: Dict[str, list] = {}
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("kind") != "sell_lots":
            _note("lot_row", "变更表 行%d" % i,
                  "行非 kind=sell_lots 登记: %r" % (row,))
            continue
        rows_by_route.setdefault(str(row.get("route")), []).append(row)
    real_routes = sorted(rows_by_route,
                         key=lambda k: (0, int(k)) if k.isdigit() else (1, k))
    sell_lots = {"present": base40 != t37, "rows": len(rows),
                 "changed_routes": real_routes, "sha256": lot_sha}

    # ---- 3. 基座区归因：blob 前缀/后缀+变更表注释+两侧解码对比 ----
    pkg37 = pkg40 = None
    if base40 != t37:
        try:
            from orderbook_r37 import retape_sheep as _rs
        except ImportError:             # 脚本态兜底
            _here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            _r37dir = os.path.join(_here, "orderbook_r37")
            if _r37dir not in sys.path:
                sys.path.insert(0, _r37dir)
            import retape_sheep as _rs  # type: ignore
        m37 = list(_rs._BLOB_RE.finditer(t37))
        m40 = list(_rs._BLOB_RE.finditer(base40))
        if len(m37) != 1 or len(m40) != 1:
            _note("blob_span", "磁带区",
                  "blob 匹配数 r37=%d/r40=%d（期望各 1）" % (len(m37), len(m40)))
        else:
            lo37, hi37 = m37[0].span(1)
            lo40, hi40 = m40[0].span(1)
            if t37[:lo37] != base40[:lo40]:
                off = _fd(t37[:lo37], base40[:lo40])
                _note("prefix_broken",
                      "前缀 偏移%d（r37 行%d/r40 行%d）"
                      % (off, _ln(t37, off), _ln(base40, off)),
                      "r37=%r r40=%r" % (t37[off:off + 16], base40[off:off + 16]))
            suf37, suf40 = t37[hi37:], base40[hi40:]
            if suf40 == suf37:
                pass                    # 无变更表注释（注释可选）
            elif suf40.startswith(suf37):
                extra = suf40[len(suf37):]
                pad = "\n" if extra.startswith("\n") else ""
                rest = extra[len(pad):]
                if (rest.startswith(_LOT_MARKER) and rest.endswith("\n")
                        and "\n" not in rest[:-1]):
                    payload = rest[len(_LOT_MARKER):].strip()
                    if change_table is None:
                        _note("lot_comment", "变更表注释",
                              "注释在场但 change_table=None（零登记口径）")
                    else:
                        try:
                            obj = json.loads(payload)
                        except Exception as exc:   # noqa: BLE001
                            _note("lot_comment", "变更表注释",
                                  "注释行 JSON 解析失败: %r" % exc)
                        else:
                            try:
                                same = _canon_sha(obj) == lot_sha
                            except Exception as exc:   # noqa: BLE001
                                _note("lot_comment", "变更表注释",
                                      "注释不可 canonical sha: %r" % exc)
                            else:
                                if not same:
                                    _note("lot_comment", "变更表注释",
                                          "注释 canonical sha 与 change_table"
                                          " 参数不符")
                else:
                    _note("outside_block_bytes", "尾部追加区",
                          "变更表注释外 %d 字节 %r" % (len(extra), extra[:40]))
            else:
                off = _fd(suf37, suf40)
                _note("suffix_broken",
                      "blob 后缀 偏移%d（r37 行%d/r40 行%d）"
                      % (off, _ln(t37, hi37 + off), _ln(base40, hi40 + off)),
                      "r37=%r r40=%r" % (suf37[off:off + 16],
                                         suf40[off:off + 16]))
            try:
                pkg37 = _rs._decode_routes(t37)
                pkg40 = _rs._decode_routes(base40)
            except Exception as exc:    # noqa: BLE001
                _note("lot_decode", "磁带区", "解码失败: %r" % exc)
    else:
        # 磁带区零差异：变更表不得虚报登记（双向对应同则）
        for rk, rs in rows_by_route.items():
            if rs:
                _note("lot_no_diff", "路由%s" % rk,
                      "变更表登记 %d 条但磁带区零差异" % len(rs))

    if pkg37 is not None and pkg40 is not None:
        _attribute_sell_lots(pkg37, pkg40, rows, _note)

    table = {
        "ok": not un,
        "whitelist": {"runtime_block": tail_block, "sell_lots": sell_lots},
        "unattributed": un,
    }
    if un:
        first = un[0]
        raise ValueError("白名单外差异 %d 处；首条未归因：%s（%s）%s"
                         % (len(un), first["where"], first["kind"],
                            first["detail"]))
    return table


def _sell_of(o: Any):
    """SELL 单形态校验 → (item, qty)；非法形态返回 None（不入卖单状态机）。"""
    if isinstance(o, list) and o and o[0] == "SELL" and len(o) == 3 \
            and isinstance(o[1], str) and isinstance(o[2], int) \
            and not isinstance(o[2], bool) and o[2] >= 0:
        return o[1], o[2]
    return None


def _sell_state(pkg: Dict[str, Any]) -> Dict[Any, Any]:
    """磁带路由包 → 卖单状态 {route: {item: {step: [(slot, qty)…]}}}（slot 升序）。"""
    st: Dict[Any, Any] = {}
    for rid, ids in (pkg.get("routes") or {}).items():
        d: Dict[Any, Any] = {}
        if isinstance(ids, list):
            for s, i in enumerate(ids):
                try:
                    act = pkg["actions"][i]
                except Exception:       # noqa: BLE001
                    continue
                mkt = act.get("market") if isinstance(act, dict) else None
                if not isinstance(mkt, list):
                    continue
                for j, o in enumerate(mkt):
                    sv = _sell_of(o)
                    if sv is not None:
                        d.setdefault(sv[0], {}).setdefault(s, []).append(
                            (j, sv[1]))
        for item in d:
            for s in d[item]:
                d[item][s].sort()
        st[rid] = d
    return st


def _norm_state(st: Dict[Any, Any]) -> Dict[Any, Any]:
    """状态归一：丢空步键，得可深比形态。"""
    return {rid: {item: {s: v for s, v in steps.items() if v}
                  for item, steps in items.items()}
            for rid, items in st.items()}


def _attribute_sell_lots(pkg37: Dict[str, Any], pkg40: Dict[str, Any],
                         rows: list, _note) -> None:
    """磁带区 sell_lots 归因（B26 shear 归因同款双向对应）：结构面恒等+
    变更表逐行状态机重放终态⟺实测卖单终态；越界即 _note。"""
    a37, a40 = pkg37.get("actions") or [], pkg40.get("actions") or []
    r37m, r40m = pkg37.get("routes") or {}, pkg40.get("routes") or {}

    # ---- 结构面 ----
    if pkg37.get("shops") != pkg40.get("shops"):
        _note("lot_structure", "磁带区 shops", "手术外 shops 不一致")
    if set(r37m) != set(r40m):
        _note("lot_structure", "磁带区 routes", "路由键集不一致")
    refd40 = set()
    for ids in r40m.values():
        if isinstance(ids, list):
            refd40.update(i for i in ids if isinstance(i, int))
    residue = a37[0] if a37 else None
    for i in range(min(len(a40), len(a37))):
        if a40[i] == a37[i]:
            continue
        if i in refd40:
            _note("lot_pool", "池件%d" % i,
                  "被引用池件被改动（非写时复制形态）")
        elif a40[i] != residue:
            _note("lot_pool", "池件%d" % i,
                  "无主池件未按池归一口径（=actions[0] 内容）")
    for i in range(len(a37), len(a40)):
        if i not in refd40 and a40[i] != residue:
            _note("lot_pool", "池件%d" % i,
                  "新增无主池件未按池归一口径（=actions[0] 内容）")

    # ---- 步内面：非卖单槽/单元指令恒等，卖单槽只许同品改量/清 [] ----
    # 掩码=卖单槽（含清坑 [] 槽）置 None（其内容差异全由卖单状态机重放核对：
    # 清 []/同品改量放行，空槽填单/卖单改品由终态恒等定罪），非卖单槽逐位恒等。
    def _mask(mkt):
        return [None if (_sell_of(o) is not None or o == []) else o
                for o in (mkt or [])]

    for rid in sorted(set(r37m) & set(r40m),
                      key=lambda k: (0, int(k)) if str(k).isdigit()
                      else (1, str(k))):
        ids37, ids40 = r37m[rid], r40m[rid]
        where = "路由%s" % rid
        if not (isinstance(ids37, list) and isinstance(ids40, list)
                and len(ids37) == len(ids40)):
            _note("lot_structure", where, "路由步数/形态不一致")
            continue
        for s, (i37, i40) in enumerate(zip(ids37, ids40)):
            if i37 == i40:
                continue
            try:
                a_old, a_new = a37[i37], a40[i40]
            except Exception:           # noqa: BLE001
                _note("lot_action", "%s 步%d" % (where, s), "动作下标越界")
                continue
            if not (isinstance(a_old, dict) and isinstance(a_new, dict)):
                _note("lot_action", "%s 步%d" % (where, s), "动作形态非法")
                continue
            bad_key = None
            for k in set(a_old) | set(a_new):
                if k == "market":
                    continue
                if a_old.get(k) != a_new.get(k):
                    bad_key = k
                    break
            if bad_key is not None:
                _note("lot_action", "%s 步%d" % (where, s),
                      "单元指令/结构键 %r 被改动" % bad_key)
                continue
            omkt, nmkt = a_old.get("market"), a_new.get("market")
            if not isinstance(omkt, list) or not isinstance(nmkt, list) \
                    or len(omkt) != len(nmkt):
                _note("lot_action", "%s 步%d" % (where, s),
                      "market 槽位数/形态被改动")
                continue
            if _mask(omkt) != _mask(nmkt):
                _note("lot_action", "%s 步%d" % (where, s),
                      "非卖单槽被改动/卖单改品/空槽填单")

    # ---- 登记面：变更表逐行状态机重放（双向对应） ----
    state = _sell_state(pkg37)
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            continue                       # 形态坏已在登记面记账
        rid, item = row.get("route"), row.get("item")
        f_steps, t_step, qty = (row.get("from_steps"), row.get("to_step"),
                                row.get("qty"))
        tag = "变更表 行%d" % i
        if not (isinstance(item, str) and isinstance(f_steps, list) and f_steps
                and all(isinstance(x, int) and not isinstance(x, bool)
                        for x in f_steps)):
            _note("lot_row", tag, "行形态非法（item/from_steps）")
            continue
        if f_steps != sorted(f_steps):
            _note("lot_row", tag, "from_steps 非升序")
            continue
        if t_step != f_steps[0]:
            _note("lot_row", tag,
                  "to_step=%r != min(from_steps)（只提前不推后破）" % (t_step,))
            continue
        if isinstance(qty, bool) or not isinstance(qty, int) or qty < 0:
            _note("lot_row", tag, "qty 形态非法: %r" % (qty,))
            continue
        d = state.get(rid)
        if d is None:
            _note("lot_row", tag, "登记路由 %r 不在磁带路由表" % (rid,))
            continue
        counts: Dict[int, int] = {}
        for s in f_steps:
            counts[s] = counts.get(s, 0) + 1
        take: Dict[int, list] = {}
        bad = False
        for s in sorted(counts):
            lst = (d.get(item) or {}).get(s) or []
            if len(lst) != counts[s]:
                _note("lot_row", tag,
                      "步%d 在册卖单 %d 条 != 登记 %d 条" % (s, len(lst), counts[s]))
                bad = True
                break
            take[s] = list(lst)
        if bad:
            continue
        total = sum(q for s in take for (_slot, q) in take[s])
        if total != qty:
            _note("lot_row", tag, "登记 qty %r != 在册合计 %d" % (qty, total))
        land_slot = take[f_steps[0]][0][0]      # 落点=最早 (step,slot)
        for s in sorted(counts):
            d.setdefault(item, {})[s] = []
        d[item].setdefault(f_steps[0], []).append((land_slot, qty))
        d[item][f_steps[0]].sort()

    exp = _norm_state(state)
    obs = _norm_state(_sell_state(pkg40))
    if exp != obs:
        n_diff = 0
        first = None
        for rid in sorted(set(exp) | set(obs), key=str):
            em, om = exp.get(rid) or {}, obs.get(rid) or {}
            for item in sorted(set(em) | set(om), key=str):
                es, os_ = em.get(item) or {}, om.get(item) or {}
                for s in sorted(set(es) | set(os_)):
                    if es.get(s) != os_.get(s):
                        n_diff += 1
                        if first is None:
                            first = "路由%s %s 步%d 登记=%r 实测=%r" % (
                                rid, item, s, es.get(s), os_.get(s))
        _note("lot_state", "磁带区 卖单终态",
              "重放终态⟺实测终态不恒等：%d 处；首处 %s" % (n_diff, first))


def pack_r40(r40_main: str, out_dir: Optional[str] = None) -> Dict[str, Any]:
    """确定性打包+manifest 沿 R16 配方；sha 链（…→r37→r40）+库 sha+
    变更表 sha+描述 "public derivative with route library and late-season
    sell execution"。

    签名意图：输入: r40 main / 输出: submission.tar.gz+manifest /
    错误: 双跑不一致即抛。

    【实现方案留档（pack 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录（orderbook_r40/build/，与 pack_r39 缺省同规），
      测试以 tmp_path 覆盖；首参与返回形态不变（返回=写盘 manifest 字典）。
    - 打包配方单一真源：复用 orderbook_2965_adopt.build_adopt.build_tar_bytes
      （R16 配方零改动语义，不手抄第二份）——单成员 main.py、mtime0/uid0/
      gid0/mode644、gzip filename="" mtime0。双跑两次取字节逐字节比对，不等
      即 RuntimeError（fail-closed，产物不落盘）；落盘前再验成员形态
      （names==['main.py'] 且 mode644/mtime0/uid0/gid0/size、内层 main 逐字节
      同输入），不符即 RuntimeError。tar 与 build_manifest.json 落 out_dir。
    - manifest 字段（沿 orderbook_r39_manifest/1.0 惯例裁形）：schema
      "orderbook_r40_manifest/1.0"、generated（日期）、variant "r40"、
      description（文案原文 "public derivative with route library and
      late-season sell execution"）、main_sha256/main_bytes、tar_sha256/
      tar_bytes/tar_members、double_run_sha256={run1,run2}（双跑哈希恒等）、
      base_sha_chain、runtime_block、route_library_sha256、
      sell_lots_change_sha256、complete（自证完整旗）。
    - base_sha_chain 键=a16e0e9b/r34a/r37/r40：前两节点字面钉死（pack 签名
      只见 r40 main，不外读盘）；r37=剥块重算（块前恰两换行为界，块前字节
      sha——r40 含卖单手术时该节点为「r37 底版经 sell_lots+变更表注释」的块前
      字节，原始 r37 sha 由 build_r40 evidence 另证；manifest 自证链口径=块前
      字节可复算）；r40=输入重算。运行时块缺→r37 节点记 null 不造假。
    - runtime_block 识别（尽力自证，锚行口径同 audit_diff_r40_vs_r37：只按核心
      短语「r40 运行时尾块」所在行识别，不钉 === 装饰）：全文恰 0/1 次
      （多现→ValueError）；锚行行首前须恰两换行（B17 追加载荷前置空行形态），
      否则 ValueError。块文本=锚前 2 字节起至文件尾（恰=inject_r40_block
      追加载荷形态，含前置空行分隔，sha 与 inject_r40_block.block_sha 同
      口径），字段={present, bytes, sha256}；缺件→{"present": False,
      "bytes": 0, "sha256": None} 不造假。
    - route_library_sha256=块内 _R40_LIBRARY 的 canonical json sha（json.dumps
      sort_keys=True/ensure_ascii=False/紧凑分隔符）：先从块文本 AST 解析
      _R40_LIBRARY 赋值字面量重算（主链，==build_audit.library_sha 真库
      0236c30e… 口径）；解析不出→伴生 manifest 行「# R40_LIBRARY_SHA256:
      <hex64>」兜底认账（重复行/坏值→ValueError）；仍解析不出→null 不造假。
    - sell_lots_change_sha256=变更表注释单行「# R40_LOT_CHANGE_TABLE: <json>」
      的 canonical json sha（主链=文本自证；全文恰 0/1 行，多现/坏值→
      ValueError）；缺行→null 不造假。
    - complete=块 sha+库 sha+r37 链节点+变更表 sha 四件全非 null（消费方可
      fail-closed）。
    - 错误面：非 str→TypeError；空/纯空白路径→ValueError；空文件→ValueError；
      锚多现/锚前分隔畸形/伴生行重复或坏值→ValueError；双跑不一致/成员形态
      不过→RuntimeError；路径不存在→FileNotFoundError。
    """
    import ast
    import hashlib
    import io
    import json
    import os
    import re
    import sys
    import tarfile
    import time

    try:
        from orderbook_2965_adopt import build_adopt as _ba
    except ImportError:                      # 脚本态兜底（pack_r39 同款）
        _adopt = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "orderbook_2965_adopt")
        if _adopt not in sys.path:
            sys.path.insert(0, _adopt)
        import build_adopt as _ba            # type: ignore

    core = _CORE.encode("utf-8")     # 块锚行核心短语（同 audit 口径）

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r40_main, str):
        raise TypeError("r40_main must be str, got %s" % type(r40_main).__name__)
    if not isinstance(out_dir, (str, type(None))):
        raise TypeError("out_dir must be str or None, got %s"
                        % type(out_dir).__name__)
    if not r40_main.strip():
        raise ValueError("r40_main must not be empty/whitespace-only")

    with open(r40_main, "rb") as fh:
        main_bytes = fh.read()
    if not main_bytes:
        raise ValueError("r40 main 文件为空：%s" % r40_main)
    main_text = main_bytes.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError

    # ---- 1. 运行时块识别+库 sha+变更表 sha（尽力自证，缺件不造假） ----
    runtime: Dict[str, Any] = {"present": False, "bytes": 0, "sha256": None}
    r37_sha: Optional[str] = None
    block_text: Optional[str] = None
    hits = [m.start() for m in re.finditer(re.escape(core), main_bytes)]
    if len(hits) > 1:
        raise ValueError("r40 运行时块锚行核心短语出现 %d 次（期望 0/1）" % len(hits))
    if hits:
        anchor_start = main_bytes.rfind(b"\n", 0, hits[0]) + 1
        if anchor_start < 2 or main_bytes[anchor_start - 2:anchor_start] != b"\n\n":
            raise ValueError("r40 运行时块锚行前分隔畸形（期望恰两换行·B17 前置空行）：%s"
                             % r40_main)
        block = main_bytes[anchor_start - 2:]
        runtime = {"present": True, "bytes": len(block),
                   "sha256": hashlib.sha256(block).hexdigest()}
        r37_sha = hashlib.sha256(main_bytes[:anchor_start - 2]).hexdigest()
        block_text = block.decode("utf-8")

    lib_sha: Optional[str] = None
    if block_text is not None:
        obj: Any = None
        try:
            for node in ast.walk(ast.parse(block_text)):
                if (isinstance(node, ast.Assign)
                        and any(isinstance(t, ast.Name)
                                and t.id == "_R40_LIBRARY"
                                for t in node.targets)):
                    obj = ast.literal_eval(node.value)
                elif (isinstance(node, ast.AnnAssign)
                      and isinstance(node.target, ast.Name)
                      and node.target.id == "_R40_LIBRARY"
                      and node.value is not None):
                    obj = ast.literal_eval(node.value)
        except Exception:                    # noqa: BLE001（解析不出走兜底）
            obj = None
        if obj is not None:
            try:
                canon = json.dumps(obj, sort_keys=True, ensure_ascii=False,
                                   separators=(",", ":")).encode("utf-8")
            except (TypeError, ValueError):
                canon = None
        else:
            canon = None
        if canon is not None:
            lib_sha = hashlib.sha256(canon).hexdigest()
        else:
            marks = [ln for ln in block_text.splitlines()
                     if ln.startswith(_LIB_MARKER)]
            if len(marks) > 1:
                raise ValueError("R40_LIBRARY_SHA256 伴生行 %d（期望恰 0/1）"
                                 % len(marks))
            if marks:
                payload = marks[0][len(_LIB_MARKER):].strip()
                if not re.fullmatch(r"[0-9a-f]{64}", payload):
                    raise ValueError("R40_LIBRARY_SHA256 伴生行值非 sha256 hex: %r"
                                     % payload[:24])
                lib_sha = payload

    lot_sha: Optional[str] = None
    smarks = [ln for ln in main_text.splitlines() if ln.startswith(_LOT_MARKER)]
    if len(smarks) > 1:
        raise ValueError("R40_LOT_CHANGE_TABLE 伴生行 %d（期望恰 0/1）"
                         % len(smarks))
    if smarks:
        spayload = smarks[0][len(_LOT_MARKER):].strip()
        try:
            sobj = json.loads(spayload)
            scanon = json.dumps(sobj, sort_keys=True, ensure_ascii=False,
                                separators=(",", ":")).encode("utf-8")
        except Exception as exc:             # noqa: BLE001
            raise ValueError("R40_LOT_CHANGE_TABLE 伴生行值坏: %r" % exc) from exc
        lot_sha = hashlib.sha256(scanon).hexdigest()

    complete = bool(runtime["sha256"] and lib_sha and r37_sha and lot_sha)

    # ---- 2. 确定性打包：双跑逐字节（不等即抛）+成员形态校验 ----
    tar1 = _ba.build_tar_bytes(main_bytes)
    tar2 = _ba.build_tar_bytes(main_bytes)
    if tar1 != tar2:
        raise RuntimeError("tar 双跑不一致（非确定性，fail-closed）：%s" % r40_main)
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

    # ---- 3. manifest（R16/R17 惯例键 + R23 增补） ----
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    manifest = {
        "schema": "orderbook_r40_manifest/1.0",
        "generated": time.strftime("%Y-%m-%d"),
        "variant": "r40",
        "description": ("public derivative with route library and "
                        "late-season sell execution"),
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": hashlib.sha256(tar1).hexdigest(),
        "tar_bytes": len(tar1),
        "tar_members": names,
        "double_run_sha256": {"run1": hashlib.sha256(tar1).hexdigest(),
                              "run2": hashlib.sha256(tar2).hexdigest()},
        "base_sha_chain": {
            "a16e0e9b": _A16,
            "r34a": _R34A,
            "r37": r37_sha,
            "r40": main_sha,
        },
        "runtime_block": runtime,
        "route_library_sha256": lib_sha,
        "sell_lots_change_sha256": lot_sha,
        "complete": complete,
    }
    with open(os.path.join(out, "build_manifest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return manifest
