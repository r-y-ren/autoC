# -*- coding: utf-8 -*-
"""build_r38（R21 L1）+ 审计/打包子函数。

责任契约（fn_docs/hybrid/responsibility.md【R21 增补】）：
以 r37 在飞件字节为底 → build_sellflow_library 建库 → inject_predict_block
注入预测块（库数据随块内嵌）→ audit_diff_vs_r37 → pack_r38；r37/在飞件
零改动。
"""
from __future__ import annotations

from typing import Any, Dict, Optional


def build_r38(r37_main_path: str,
              out_dir: Optional[str] = None) -> Dict[str, Any]:
    """构建编排：建库→注入预测块→审计→打包。

    签名意图：输入: r37 main 路径 / 输出: r38 main+manifest+变更集审计 /
    错误: 超白名单即抛。

    【实现方案留档（build 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录（orderbook_predict/build/，与 pack_r38 缺省
      同址），测试以 tmp_path 覆盖；首参与返回主键不变。
    - 编排流（责任契约 R21）：读 r37 文本（只读打开、全程零写回，测试钉字节
      不变）→ sellflow.build_sellflow_library("/tmp/r33audit")（真库语料=
      86 局 158 键）→ inject_predict.inject_predict_block 注入预测块（库数据
      随块内嵌；block_sha=追加载荷整体字节含前置两空行分隔）→
      audit_diff_vs_r37（白名单恰一类=predict_block 尾块）→ pack_r38。
    - 变更表注释：本件改动集=纯尾块，不设 SHEEP 式内嵌变更行——manifest 已
      自证（predict_block sha/library_sha256/base_sha_chain r37=剥块重算）；
      pack 的库 sha 走块内 _PREDICT_LIBRARY AST 解析主链，「# R38_LIBRARY_
      SHA256」伴生行仅兜底（正常路不写），写盘段 fail-closed 自检保证链通。
    - 失败面（不落半成品，B18 build_r37 同款）：落盘前一切红（缺文件/建库红/
      注入红/审计红）只经 tempfile 暂存件中转，out 目录零触碰（不建目录不落
      文件）；审计过后才写 out/main.py 并 pack，写盘段任一异常即清本次三件
      产物（main.py/submission.tar.gz/build_manifest.json）再抛。
    - 写盘段 fail-closed 三件套自检：audit/manifest 块 sha==inject block_sha、
      manifest library_sha256==build_audit.sha256_of_library、manifest
      complete==True，任一不符即 RuntimeError（清三件再抛）。
    - 返回：{"main_path", "main_sha256", "tar_sha256", "manifest",
      "diff_attribution", "block_sha", "library_sha256", "build_audit",
      "r37_main_path", "r37_sha256"}（全 JSON 可序列化）。
    """
    import hashlib
    import os
    import sys
    import tempfile

    try:
        from orderbook_predict import inject_predict as _ip
        from orderbook_predict import sellflow as _sf
    except ImportError:                      # 脚本态兜底（B18 build_r37 同款）
        _here = os.path.dirname(os.path.abspath(__file__))
        if _here not in sys.path:
            sys.path.insert(0, _here)
        import inject_predict as _ip        # type: ignore
        import sellflow as _sf              # type: ignore

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r37_main_path, str):
        raise TypeError("r37_main_path must be str, got %s"
                        % type(r37_main_path).__name__)
    if not isinstance(out_dir, (str, type(None))):
        raise TypeError("out_dir must be str or None, got %s"
                        % type(out_dir).__name__)
    if not r37_main_path.strip():
        raise ValueError("r37_main_path must not be empty/whitespace-only")

    with open(r37_main_path, "rb") as fh:
        b37 = fh.read()                      # 缺文件→FileNotFoundError（落盘前）
    if not b37:
        raise ValueError("r37 main 文件为空：%s" % r37_main_path)
    t37 = b37.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError（ValueError 子类）

    # ---- 1. 建库→注入预测块（写时复制链：r37/在飞件零写回） ----
    built = _sf.build_sellflow_library("/tmp/r33audit")   # 真库语料（契约钉）
    inj = _ip.inject_predict_block(t37, built)            # 库数据随块内嵌
    r38_bytes = inj["main_text"].encode("utf-8")
    block_sha = inj["block_sha"]

    # ---- 2. diff 审计（恰=白名单一类；红即抛，暂存件中转零半成品） ----
    stage = None
    try:
        fd, stage = tempfile.mkstemp(prefix="r38_build_", suffix=".py")
        with os.fdopen(fd, "wb") as fh:
            fh.write(r38_bytes)
        attribution = audit_diff_vs_r37(stage, r37_main_path)
    finally:
        if stage is not None and os.path.exists(stage):
            os.remove(stage)

    # ---- 3. 落盘+确定性打包（写盘段红→清本次三件产物再抛） ----
    out = out_dir if out_dir is not None else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "build")
    os.makedirs(out, exist_ok=True)
    main_path = os.path.join(out, "main.py")
    try:
        with open(main_path, "wb") as fh:
            fh.write(r38_bytes)
        manifest = pack_r38(main_path, out_dir=out)
        # fail-closed 三件套自检：块 sha/库 sha/complete 对账（不过即红）
        pb = attribution["whitelist"]["predict_block"]
        if (pb["sha256"] != block_sha
                or manifest["predict_block"]["sha256"] != block_sha):
            raise RuntimeError(
                "块 sha 对账红：inject=%s audit=%s pack=%s"
                % (block_sha, pb["sha256"], manifest["predict_block"]["sha256"]))
        lib_sha = built["build_audit"]["sha256_of_library"]
        if manifest["library_sha256"] != lib_sha:
            raise RuntimeError(
                "库 sha 对账红：pack=%s build_audit=%s"
                % (manifest["library_sha256"], lib_sha))
        if not manifest["complete"]:
            raise RuntimeError("manifest 自证不完整（complete=False，库 sha 兜底链断）")
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
        "library_sha256": manifest["library_sha256"],
        "build_audit": built["build_audit"],
        "r37_main_path": r37_main_path,
        "r37_sha256": hashlib.sha256(b37).hexdigest(),
    }


def audit_diff_vs_r37(r38_main: str, r37_main: str) -> Dict[str, Any]:
    """对底版逐字节 diff 审计——差异恰=白名单一类（尾部追加预测块含库数据；
    磁带区零改动），白名单外差异即抛；输出归因表。

    签名意图：输入: r38 main+r37 main / 输出: 归因表 / 错误: 白名单外差异即抛。

    【实现方案留档（audit 组测试钉住）】
    - 归因表：{"ok", "whitelist": {"predict_block": {"present","bytes",
      "sha256"}}, "unattributed"}；unattributed 非空→ValueError（消息含首条
      定位）。predict_block=尾部追加预测块：present=在场与否（同文本零差异
      →False/bytes 0/sha256 None）、bytes=尾部块字节数、sha256=尾部块字节
      sha（与 inject_predict_block.block_sha 同口径：追加载荷整体字节，含
      B17 前置空行分隔）。
    - 判定：r38 以 r37 为逐字节前缀、仅尾部多一块——块锚行=
      「# ============ r38 对手预测尾块（自动生成，勿手改） ============」，
      核心短语「r38 对手预测尾块」恰现一次（r38 全文恰 1、r37 全文 0；兼容
      装饰差异——识别只按核心短语所在行，不钉 === 装饰）；锚行须落在追加区
      且其行首不越过追加起点（末行不许被接长），追加区锚行前只许换行分隔
      （B17 追加载荷前置空行形态）——此外任何字节=块外多字节，白名单外即抛。
      前缀破坏（原文任何字节变/少）→unattributed 即抛（首差字节+两侧行号
      进消息）；磁带区零改动由前缀性质直接覆盖。
    - 只抛不改；返回可直接进 manifest（全 JSON 可序列化）。
    """
    import hashlib

    core = "r38 对手预测尾块".encode("utf-8")   # 块锚行核心短语（与注入件约定）

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r38_main, str):
        raise TypeError("r38_main must be str, got %s" % type(r38_main).__name__)
    if not isinstance(r37_main, str):
        raise TypeError("r37_main must be str, got %s" % type(r37_main).__name__)
    if not r38_main.strip() or not r37_main.strip():
        raise ValueError("路径不得为空/纯空白")

    with open(r38_main, "rb") as fh:
        b38 = fh.read()
    with open(r37_main, "rb") as fh:
        b37 = fh.read()
    if not b38:
        raise ValueError("r38 main 文件为空：%s" % r38_main)
    if not b37:
        raise ValueError("r37 main 文件为空：%s" % r37_main)

    unattributed: list = []

    def _note(kind: str, where: str, detail: str) -> None:
        unattributed.append({"kind": kind, "where": where,
                             "detail": detail[:120]})

    def _first_diff(x: bytes, y: bytes) -> int:
        n = min(len(x), len(y))
        for i in range(n):
            if x[i] != y[i]:
                return i
        return n

    def _line(b: bytes, off: int) -> int:
        return b[:off].count(b"\n") + 1

    tail_block = {"present": False, "bytes": 0, "sha256": None}

    if b38 == b37:
        pass                                    # ④同文本零差异：白名单件不在场
    elif not b38.startswith(b37):
        off = _first_diff(b37, b38)             # 前缀破坏=白名单外（首差定位）
        _note("prefix_broken",
              "前缀 字节%d（r37 行%d/r38 行%d）" % (off, _line(b37, off),
                                                 _line(b38, off)),
              "r37=%r r38=%r" % (b37[off:off + 16], b38[off:off + 16]))
    else:
        chunk = b38[len(b37):]                  # 尾部追加块字节（唯一白名单候选）
        n37, n38 = b37.count(core), b38.count(core)
        if n37 != 0:
            _note("anchor_in_base", "块锚行",
                  "核心短语在 r37 底版出现 %d 次（期望 0）" % n37)
        if n38 == 0:
            _note("anchor_missing", "块锚行",
                  "核心短语缺失（追加块 %d 字节）" % len(chunk))
        elif n38 > 1:
            _note("anchor_duplicate", "块锚行",
                  "核心短语出现 %d 次（期望恰 1）" % n38)
        if n37 == 0 and n38 == 1:
            phrase_off = b38.find(core)         # 恰一次 → find 即唯一定位
            anchor_start = b38.rfind(b"\n", 0, phrase_off) + 1   # 锚行行首
            head = b38[len(b37):anchor_start]   # 锚行前追加字节
            if anchor_start < len(b37):
                _note("anchor_not_at_tail", "块锚行 字节%d" % phrase_off,
                      "锚行行首 %d 在底版区（追加起点 %d）" % (anchor_start,
                                                          len(b37)))
            elif head.strip(b"\n"):
                _note("outside_block_bytes",
                      "尾部追加区 字节%d（行%d）" % (len(b37),
                                                 _line(b38, len(b37))),
                      "锚行前 %d 块外字节 %r" % (len(head), head[:40]))
            else:
                tail_block = {"present": True, "bytes": len(chunk),
                              "sha256": hashlib.sha256(chunk).hexdigest()}

    table = {
        "ok": not unattributed,
        "whitelist": {"predict_block": tail_block},
        "unattributed": unattributed,
    }
    if unattributed:
        first = unattributed[0]
        raise ValueError("白名单外差异 %d 处；首条未归因：%s（%s）%s"
                         % (len(unattributed), first["where"], first["kind"],
                            first["detail"]))
    return table


def pack_r38(r38_main: str, out_dir: Optional[str] = None) -> Dict[str, Any]:
    """确定性打包+manifest——沿 R16 配方（mtime0/uid0/gid0/mode644/gzip
    mtime0/双跑逐字节）；manifest=sha 链（…→r37→r38）+预测块 sha+库 sha+
    描述文案 "public derivative with opponent sell prediction (front-run + dodge)"。

    签名意图：输入: r38 main / 输出: submission.tar.gz+manifest /
    错误: 双跑不一致即抛。

    【实现方案留档（pack 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录（orderbook_predict/build/，与 pack_r37 缺省
      同规），测试以 tmp_path 覆盖；首参与返回形态不变（返回=写盘 manifest
      字典）。
    - 打包配方单一真源：复用 orderbook_2965_adopt.build_adopt.build_tar_bytes
      （R16 配方零改动语义，不手抄第二份）——单成员 main.py、mtime0/uid0/
      gid0/mode644、gzip filename="" mtime0。双跑两次取字节逐字节比对，不等
      即 RuntimeError（fail-closed，产物不落盘）；落盘前再验成员形态
      （names==['main.py'] 且 mode644/mtime0/uid0/gid0/size、内层 main 逐字节
      同输入），不符即 RuntimeError。tar 与 build_manifest.json 落 out_dir。
    - manifest 字段（沿 orderbook_r37_manifest/1.0 惯例裁形）：schema
      "orderbook_r38_manifest/1.0"、generated（日期）、variant "r38"、
      description（文案原文）、main_sha256/main_bytes、tar_sha256/tar_bytes/
      tar_members、double_run_sha256={run1,run2}（双跑哈希恒等）、
      base_sha_chain、predict_block、library_sha256、complete（自证完整旗）。
    - base_sha_chain 键=a16e0e9b/r34a/r37/r38：前两节点字面钉死（a16e0e9b=
      round-30 基座 main、r34a=orderbook_2965_adopt/a/main.py 在飞件，同
      pack_r37 口径——pack 签名只见 r38 main，不外读盘）；r37=剥预测块重算
      （块前恰两换行为界，块前字节即 r37 底版字节，manifest 自证）；r38=
      输入重算。预测块缺→r37 节点记 null 不造假。
    - predict_block 识别（尽力自证，锚行口径同 audit_diff_vs_r37：只按核心
      短语所在行识别，不钉 === 装饰）：锚行=含核心短语「r38 对手预测尾块」
      的行，全文恰 0/1 次（多现→ValueError）；锚行行首前须恰两换行
      （B17 追加载荷前置空行形态），否则 ValueError。块文本=锚前 2 字节起至
      文件尾（恰=注入件追加载荷形态，含前置空行分隔，sha 与
      inject_predict_block.block_sha 同口径），字段={present, bytes, sha256}；
      缺件→{"present": False, "bytes": 0, "sha256": None} 不造假。
    - library_sha256=块内 _PREDICT_LIBRARY 的 canonical json sha（json.dumps
      sort_keys=True/ensure_ascii=False/紧凑分隔符，对键序/嵌入空白不敏感）：
      先从块文本 AST 解析 _PREDICT_LIBRARY 赋值字面量重算；解析不出→伴生
      manifest 行「# R38_LIBRARY_SHA256: <hex64>」兜底认账（重复行/坏值→
      ValueError）；仍解析不出→null 不造假。
    - complete=块 sha+库 sha+r37 链节点三件全非 null（消费方可 fail-closed）。
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
    except ImportError:                      # 脚本态兜底（pack_r37 同款）
        _adopt = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "orderbook_2965_adopt")
        if _adopt not in sys.path:
            sys.path.insert(0, _adopt)
        import build_adopt as _ba            # type: ignore

    core = "r38 对手预测尾块".encode("utf-8")   # 块锚行核心短语（同 audit 口径）

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r38_main, str):
        raise TypeError("r38_main must be str, got %s" % type(r38_main).__name__)
    if not isinstance(out_dir, (str, type(None))):
        raise TypeError("out_dir must be str or None, got %s"
                        % type(out_dir).__name__)
    if not r38_main.strip():
        raise ValueError("r38_main must not be empty/whitespace-only")

    with open(r38_main, "rb") as fh:
        main_bytes = fh.read()
    if not main_bytes:
        raise ValueError("r38 main 文件为空：%s" % r38_main)
    main_bytes.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError（ValueError 子类）

    # ---- 1. 预测块识别+库 sha（尽力自证，缺件不造假） ----
    predict: Dict[str, Any] = {"present": False, "bytes": 0, "sha256": None}
    r37_sha: Optional[str] = None
    block_text: Optional[str] = None
    hits = [m.start() for m in re.finditer(re.escape(core), main_bytes)]
    if len(hits) > 1:
        raise ValueError("预测块锚行核心短语出现 %d 次（期望 0/1）" % len(hits))
    if hits:
        anchor_start = main_bytes.rfind(b"\n", 0, hits[0]) + 1
        if anchor_start < 2 or main_bytes[anchor_start - 2:anchor_start] != b"\n\n":
            raise ValueError("预测块锚行前分隔畸形（期望恰两换行·B17 前置空行）：%s"
                             % r38_main)
        block = main_bytes[anchor_start - 2:]
        predict = {"present": True, "bytes": len(block),
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
                                and t.id == "_PREDICT_LIBRARY"
                                for t in node.targets)):
                    obj = ast.literal_eval(node.value)
                elif (isinstance(node, ast.AnnAssign)
                      and isinstance(node.target, ast.Name)
                      and node.target.id == "_PREDICT_LIBRARY"
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
            marker = "# R38_LIBRARY_SHA256:"
            marks = [ln for ln in block_text.splitlines()
                     if ln.startswith(marker)]
            if len(marks) > 1:
                raise ValueError("R38_LIBRARY_SHA256 伴生行 %d（期望恰 0/1）"
                                 % len(marks))
            if marks:
                payload = marks[0][len(marker):].strip()
                if not re.fullmatch(r"[0-9a-f]{64}", payload):
                    raise ValueError("R38_LIBRARY_SHA256 伴生行值非 sha256 hex: %r"
                                     % payload[:24])
                lib_sha = payload

    complete = bool(predict["sha256"] and lib_sha and r37_sha)

    # ---- 2. 确定性打包：双跑逐字节（不等即抛）+成员形态校验 ----
    tar1 = _ba.build_tar_bytes(main_bytes)
    tar2 = _ba.build_tar_bytes(main_bytes)
    if tar1 != tar2:
        raise RuntimeError("tar 双跑不一致（非确定性，fail-closed）：%s" % r38_main)
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

    # ---- 3. manifest（R16/R17 惯例键 + R21 增补） ----
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    manifest = {
        "schema": "orderbook_r38_manifest/1.0",
        "generated": time.strftime("%Y-%m-%d"),
        "variant": "r38",
        "description": ("public derivative with opponent sell prediction "
                        "(front-run + dodge)"),
        "main_sha256": main_sha,
        "main_bytes": len(main_bytes),
        "tar_sha256": hashlib.sha256(tar1).hexdigest(),
        "tar_bytes": len(tar1),
        "tar_members": names,
        "double_run_sha256": {"run1": hashlib.sha256(tar1).hexdigest(),
                              "run2": hashlib.sha256(tar2).hexdigest()},
        "base_sha_chain": {
            "a16e0e9b": ("a16e0e9b40c489972630a0b9d04f30e9c1cab031"
                         "59fa78676db74277d84d82ab"),
            "r34a": ("51fc19dba2d0bcbf2d0a3720c26ff318541a0e6c"
                     "e5800873bc863f612451aa5b"),
            "r37": r37_sha,
            "r38": main_sha,
        },
        "predict_block": predict,
        "library_sha256": lib_sha,
        "complete": complete,
    }
    with open(os.path.join(out, "build_manifest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return manifest
