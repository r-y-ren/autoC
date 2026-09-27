# -*- coding: utf-8 -*-
"""build_r39 + pack_r39（R22 L1/L2）：构建编排与打包。

责任契约（fn_docs/hybrid/responsibility.md【R22 增补】）：
以 r37 在飞件字节为底 → retape_shear_phase 毛期手术 → 变更表注释内嵌 →
build_sellflow_library[改造] 建新库（top-30 新鲜重采）→ inject_predict_block
[改造] 注入 v2 块（含克隆检测+credit 账）→ audit_diff_vs_r37[改造]（两类
白名单）→ pack_r39；r37 零改动。
"""
from __future__ import annotations

from typing import Any, Dict, Optional


def build_r39(r37_main_path: str,
              out_dir: Optional[str] = None) -> Dict[str, Any]:
    """构建编排：毛期手术→变更表注释→建库→注入 v2 块→审计→打包。

    签名意图：输入: r37 main 路径 / 输出: r39 main+manifest+变更集审计 /
    错误: 超白名单即抛。

    【实现方案留档（build 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录（orderbook_predict/build/，与 pack_r39 缺省
      同址），测试以 tmp_path 覆盖；首参与返回主键不变。
    - 编排流（责任契约 R22）：读 r37 文本（只读打开、全程零写回，测试钉字节
      不变）→ retape_sheep._decode_routes 解码磁带路由包 →
      retape_shear_phase（offset 缺省 +2）毛期手术（写时复制、输入零改动）→
      _encode_routes 回写（四件自检链）→ 变更表注释内嵌单行「#
      R39_SHEAR_CHANGE_TABLE: <json>」（canonical json：sort_keys+紧凑分隔+
      ensure_ascii=False，单行落 base 尾部；shear_change_sha256=该 JSON utf-8
      字节 sha256）→ build_sellflow_library("/tmp/kagr23") 建 v2 库（top-30
      新鲜重采，旧 86 局走 SELLFLOW_AUX_REPLAY_DIR 缺省 /tmp/r33audit 降辅助）
      → inject_predict_block 注入 v2 尾块（库数据随块内嵌）→
      audit_diff_vs_r37（带 change_table，两类白名单）→ pack_r39。
    - 失败面（不落半成品，B18 build_r37 同款）：落盘前一切红（缺文件/解码红/
      手术红/建库红/注入红/审计红）只经 tempfile 暂存件中转，out 目录零触碰
      （不建目录不落文件）；审计过后才写 out/main.py 并 pack，写盘段任一异常
      即清本次三件产物（main.py/submission.tar.gz/build_manifest.json）再抛。
    - 写盘段 fail-closed 自检：audit/manifest 块 sha==inject block_sha、
      manifest library_sha256==build_audit.sha256_of_library、manifest
      shear_change_sha256==audit shear sha==变更表 canonical sha、manifest
      complete==True，任一不符即 RuntimeError（清三件再抛）。
    - 返回：{"main_path", "main_sha256", "tar_sha256", "manifest",
      "diff_attribution", "block_sha", "library_sha256",
      "shear_change_sha256"}（全 JSON 可序列化）。
    """
    import hashlib
    import json
    import os
    import sys
    import tempfile

    try:
        from orderbook_predict import inject_predict as _ip
        from orderbook_predict import retape_shear_phase as _sp
        from orderbook_predict import sellflow as _sf
        from orderbook_predict.build_r38 import audit_diff_vs_r37 as _audit
        from orderbook_r37 import retape_sheep as _rs
    except ImportError:                      # 脚本态兜底（B18 build_r37 同款）
        _here = os.path.dirname(os.path.abspath(__file__))
        if _here not in sys.path:
            sys.path.insert(0, _here)
        import inject_predict as _ip         # type: ignore
        import retape_shear_phase as _sp     # type: ignore
        import sellflow as _sf               # type: ignore
        from build_r38 import audit_diff_vs_r37 as _audit   # type: ignore
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

    with open(r37_main_path, "rb") as fh:
        b37 = fh.read()                      # 缺文件→FileNotFoundError（落盘前）
    if not b37:
        raise ValueError("r37 main 文件为空：%s" % r37_main_path)
    t37 = b37.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError（ValueError 子类）

    # ---- 1. 毛期手术（写时复制，r37 零改动）→变更表注释内嵌单行 ----
    pkg = _rs._decode_routes(t37)
    sheared = _sp.retape_shear_phase(pkg)     # offset 缺省 +2
    change_table = sheared["change_table"]
    t39 = _rs._encode_routes(t37, sheared["routes"])
    canon = json.dumps(change_table, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False)   # 变更表 canonical json（单行）
    comment = "# R39_SHEAR_CHANGE_TABLE: " + canon + "\n"
    base_text = t39 if t39.endswith("\n") else t39 + "\n"
    base_text = base_text + comment
    shear_sha = hashlib.sha256(canon.encode("utf-8")).hexdigest()

    # ---- 2. 建 v2 库→注入 v2 尾块（库数据随块内嵌） ----
    built = _sf.build_sellflow_library("/tmp/kagr23")   # 真库语料（契约钉）
    inj = _ip.inject_predict_block(base_text, built)
    r39_bytes = inj["main_text"].encode("utf-8")
    block_sha = inj["block_sha"]

    # ---- 3. diff 审计（两类白名单；红即抛，暂存件中转零半成品） ----
    stage = None
    try:
        fd, stage = tempfile.mkstemp(prefix="r39_build_", suffix=".py")
        with os.fdopen(fd, "wb") as fh:
            fh.write(r39_bytes)
        attribution = _audit(stage, r37_main_path, change_table)
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
            fh.write(r39_bytes)
        manifest = pack_r39(main_path, out_dir=out)
        # fail-closed 自检：块 sha/库 sha/shear sha/complete 对账（不过即红）
        pb = attribution["whitelist"]["predict_block"]
        sh = attribution["whitelist"]["shear_phase"]
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
        if (manifest["shear_change_sha256"] != shear_sha
                or sh["sha256"] != shear_sha):
            raise RuntimeError(
                "shear 变更表 sha 对账红：pack=%s audit=%s 变更表=%s"
                % (manifest["shear_change_sha256"], sh["sha256"], shear_sha))
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
        "library_sha256": manifest["library_sha256"],
        "shear_change_sha256": shear_sha,
    }


def pack_r39(r39_main: str, out_dir: Optional[str] = None) -> Dict[str, Any]:
    """确定性打包+manifest——沿 R16 配方（mtime0/uid0/gid0/mode644/gzip
    mtime0/双跑逐字节）；manifest=orderbook_r39_manifest/1.0，sha 链
    （a16e0e9b→51fc19db(r34a)→r37 剥块重算→r39=输入）+预测块 sha+库 sha+
    shear 变更表 sha+描述文案 "public derivative with throttled opponent
    sell prediction (v2) and anti-counter schedule"。

    签名意图：输入: r39 main / 输出: submission.tar.gz+manifest /
    错误: 双跑不一致即抛。

    【实现方案留档（pack 组测试钉住）】
    - 签名微调登记（批间）：新增第二参 out_dir: Optional[str]=None——默认
      None 落本包 build/ 目录（orderbook_predict/build/，与 pack_r38 缺省
      同规），测试以 tmp_path 覆盖；首参与返回形态不变（返回=写盘 manifest
      字典）。
    - 打包配方单一真源：复用 orderbook_2965_adopt.build_adopt.build_tar_bytes
      （R16 配方零改动语义，不手抄第二份）——单成员 main.py、mtime0/uid0/
      gid0/mode644、gzip filename="" mtime0。双跑两次取字节逐字节比对，不等
      即 RuntimeError（fail-closed，产物不落盘）；落盘前再验成员形态
      （names==['main.py'] 且 mode644/mtime0/uid0/gid0/size、内层 main 逐字节
      同输入），不符即 RuntimeError。tar 与 build_manifest.json 落 out_dir。
    - manifest 字段（沿 orderbook_r38_manifest/1.0 惯例裁形）：schema
      "orderbook_r39_manifest/1.0"、generated（日期）、variant "r39"、
      description（文案原文）、main_sha256/main_bytes、tar_sha256/tar_bytes/
      tar_members、double_run_sha256={run1,run2}（双跑哈希恒等）、
      base_sha_chain、predict_block、library_sha256、shear_change_sha256、
      complete（自证完整旗）。
    - base_sha_chain 键=a16e0e9b/r34a/r37/r39：前两节点字面钉死（a16e0e9b=
      round-30 基座 main、r34a=orderbook_2965_adopt/a/main.py 在飞件，同
      pack_r38 口径——pack 签名只见 r39 main，不外读盘）；r37=剥块重算（块前
      恰两换行为界，块前字节 sha——r39 含毛期手术时该节点为「r37 底版经
      shear+变更表注释」的块前字节，原始 r37 sha 由 build_r39 evidence 另证；
      manifest 自证链口径=块前字节可复算）；r39=输入重算。预测块缺→r37 节点
      记 null 不造假。
    - predict_block 识别（尽力自证，锚行口径同 audit_diff_vs_r37：只按核心
      短语「r38 对手预测尾块」所在行识别，不钉 === 装饰）：全文恰 0/1 次
      （多现→ValueError）；锚行行首前须恰两换行（B17 追加载荷前置空行形态），
      否则 ValueError。块文本=锚前 2 字节起至文件尾（恰=inject_predict_block
      追加载荷形态，含前置空行分隔，sha 与 inject_predict_block.block_sha 同
      口径），字段={present, bytes, sha256}；缺件→{"present": False,
      "bytes": 0, "sha256": None} 不造假。
    - library_sha256=块内 _PREDICT_LIBRARY 的 canonical json sha（json.dumps
      sort_keys=True/ensure_ascii=False/紧凑分隔符，对键序/嵌入空白不敏感）：
      先从块文本 AST 解析 _PREDICT_LIBRARY 赋值字面量重算（主链）；解析不出
      →伴生 manifest 行「# R39_LIBRARY_SHA256: <hex64>」兜底认账（重复行/坏值
      →ValueError）；仍解析不出→null 不造假。
    - shear_change_sha256=变更表注释单行「# R39_SHEAR_CHANGE_TABLE: <json>」
      的 canonical json sha（主链=文本自证；全文恰 0/1 行，多现/坏值→
      ValueError）；缺行→null 不造假。
    - complete=块 sha+库 sha+r37 链节点+shear sha 四件全非 null（消费方可
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
    except ImportError:                      # 脚本态兜底（pack_r38 同款）
        _adopt = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "orderbook_2965_adopt")
        if _adopt not in sys.path:
            sys.path.insert(0, _adopt)
        import build_adopt as _ba            # type: ignore

    core = "r38 对手预测尾块".encode("utf-8")   # 块锚行核心短语（同 audit 口径）

    # ---- 0. 输入预检（非 str/空即抛，先于一切 IO） ----
    if not isinstance(r39_main, str):
        raise TypeError("r39_main must be str, got %s" % type(r39_main).__name__)
    if not isinstance(out_dir, (str, type(None))):
        raise TypeError("out_dir must be str or None, got %s"
                        % type(out_dir).__name__)
    if not r39_main.strip():
        raise ValueError("r39_main must not be empty/whitespace-only")

    with open(r39_main, "rb") as fh:
        main_bytes = fh.read()
    if not main_bytes:
        raise ValueError("r39 main 文件为空：%s" % r39_main)
    main_text = main_bytes.decode("utf-8")   # 非法 utf-8→UnicodeDecodeError

    # ---- 1. 预测块识别+库 sha/shear sha（尽力自证，缺件不造假） ----
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
                             % r39_main)
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
            marker = "# R39_LIBRARY_SHA256:"
            marks = [ln for ln in block_text.splitlines()
                     if ln.startswith(marker)]
            if len(marks) > 1:
                raise ValueError("R39_LIBRARY_SHA256 伴生行 %d（期望恰 0/1）"
                                 % len(marks))
            if marks:
                payload = marks[0][len(marker):].strip()
                if not re.fullmatch(r"[0-9a-f]{64}", payload):
                    raise ValueError("R39_LIBRARY_SHA256 伴生行值非 sha256 hex: %r"
                                     % payload[:24])
                lib_sha = payload

    shear_sha: Optional[str] = None
    smarker = "# R39_SHEAR_CHANGE_TABLE:"
    smarks = [ln for ln in main_text.splitlines() if ln.startswith(smarker)]
    if len(smarks) > 1:
        raise ValueError("R39_SHEAR_CHANGE_TABLE 伴生行 %d（期望恰 0/1）"
                         % len(smarks))
    if smarks:
        spayload = smarks[0][len(smarker):].strip()
        try:
            sobj = json.loads(spayload)
            scanon = json.dumps(sobj, sort_keys=True, ensure_ascii=False,
                                separators=(",", ":")).encode("utf-8")
        except Exception as exc:             # noqa: BLE001
            raise ValueError("R39_SHEAR_CHANGE_TABLE 伴生行值坏: %r" % exc) from exc
        shear_sha = hashlib.sha256(scanon).hexdigest()

    complete = bool(predict["sha256"] and lib_sha and r37_sha and shear_sha)

    # ---- 2. 确定性打包：双跑逐字节（不等即抛）+成员形态校验 ----
    tar1 = _ba.build_tar_bytes(main_bytes)
    tar2 = _ba.build_tar_bytes(main_bytes)
    if tar1 != tar2:
        raise RuntimeError("tar 双跑不一致（非确定性，fail-closed）：%s" % r39_main)
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

    # ---- 3. manifest（R16/R17 惯例键 + R22 增补） ----
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    manifest = {
        "schema": "orderbook_r39_manifest/1.0",
        "generated": time.strftime("%Y-%m-%d"),
        "variant": "r39",
        "description": ("public derivative with throttled opponent sell "
                        "prediction (v2) and anti-counter schedule"),
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
            "r39": main_sha,
        },
        "predict_block": predict,
        "library_sha256": lib_sha,
        "shear_change_sha256": shear_sha,
        "complete": complete,
    }
    with open(os.path.join(out, "build_manifest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return manifest
