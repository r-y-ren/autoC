"""test_build（继承 R10 验收④装载门）：注入校验组 + build 收口组。

注入校验组（既有四用例）：
① test_inject_only_appends：注入后文件=基座原件+块（前缀逐字节恒等+后缀恰为
   分隔+块文本），基座原件 sha 注入前后不变；
② test_last_callable_is_cxs_agent：真 exec（整个测试文件仅此一次，~1MB 文件；
   120s 超时预算——环境无 pytest-timeout，以耗时断言落实）装载注入后文件，
   globals 最后 callable=_cxs_agent 且宿主捕获=_cxd_agent；
③ test_reinject_rejected：对已含块的文件再 inject → 抛错而非二次追加；
④ test_injected_block_matches_layer_file：防漂移——注入块与盘上 layer_s_block.py
   逐字节一致（注入块 sha == 层文件 sha）。

build 收口组（S2，build_layer_s_candidate；全文件恰真跑一次 build）：
⑤ test_build_full_chain_produces_artifacts：build() 全链实跑产出三件产物
   （main.py/submission.tar.gz/build_manifest.json 落盘保留=候选包本体），
   manifest 字段齐且与盘上真值逐项一致（注入 append-only 形态复核+身份链断言）；
⑥ test_build_tar_rebuild_matches_disk：独立复核确定性——以盘上注入版 main.py
   重建一次 tar（配方函数直调，不重跑 build），与盘上包逐字节+sha 一致；
⑦ test_build_tar_members_match_round30：tar 成员清单==round-30 同款
   （../orderbook_derivative/submission.tar.gz 成员名集合，恰 ["main.py"]）；
⑧ test_build_description_and_manifest_keys：描述文案==R10 要求
   "public derivative with seed-truncation layer"；manifest 必备键全部在位。"""

import hashlib
import json
import re
import shutil
import tarfile
import time
from pathlib import Path

import pytest

import append_layer_s_block
import build_layer_s_candidate

_HERE = Path(__file__).resolve().parent
_BASE = _HERE.parent / "orderbook_derivative" / "main.py"
_BASE_TAR = _HERE.parent / "orderbook_derivative" / "submission.tar.gz"
_BLOCK = _HERE / "layer_s_block.py"
_BASE_SHA256 = "a16e0e9b40c489972630a0b9d04f30e9c1cab03159fa78676db74277d84d82ab"
_BASE_TAR_SHA256 = "2838cc66e5d3f719569108fa553c9cf9acf8190d0662f8d991856560e6e9641c"

# 超时预算：注入四校验（py_compile+AST+整卷 exec）对 ~1MB 文件实测亚秒级，预算 120s。
_EXEC_BUDGET_SECONDS = 120.0

# build 全链预算：复制+注入（含整卷 exec）+双跑打包，预算 180s（实测见报告）。
_BUILD_BUDGET_SECONDS = 180.0

# manifest 必备键（S2 收口契约：schema/身份链/占位门/描述文案）。
_REQUIRED_MANIFEST_KEYS = {
    "schema", "candidate", "generated", "description",
    "main_sha256", "main_bytes", "tar_sha256", "tar_bytes",
    "block_sha256", "block_bytes", "provenance_chain",
    "four_gates", "h2h_2026_09_23",
}


@pytest.fixture(scope="module")
def injected(tmp_path_factory):
    """一次性完成真注入（inject 内部四条校验含真 exec）：返回 (main_path, report)。"""
    main_path = tmp_path_factory.mktemp("l1") / "main.py"
    shutil.copyfile(_BASE, main_path)
    report = append_layer_s_block.inject(main_path)
    return main_path, report


def test_inject_only_appends(injected):
    # ① 注入后文件=原件+块：前缀逐字节恒等（既有行零改动），后缀恰为"两空行分隔+块文本"。
    main_path, report = injected
    base_bytes = _BASE.read_bytes()
    block_bytes = _BLOCK.read_bytes()
    assert hashlib.sha256(base_bytes).hexdigest() == _BASE_SHA256  # 基座原件指纹前置断言
    got = main_path.read_bytes()
    assert got.startswith(base_bytes)  # 前缀恒等：diff 无既有行改动
    assert got[len(base_bytes):] == append_layer_s_block._SEPARATOR + block_bytes  # 后缀恰为块
    assert report["injected_main_sha256"] == hashlib.sha256(got).hexdigest()
    # 基座原件注入后仍逐字节未动（不落任何对原文件的改动）
    assert hashlib.sha256(_BASE.read_bytes()).hexdigest() == _BASE_SHA256


def test_last_callable_is_cxs_agent(injected):
    # ② 真 exec（本文件唯一一次）装载注入后文件：globals 最后 callable=_cxs_agent
    #    （官方入口装载门桌面版）；块首 _CXS_HOST 捕获=基座尾部 _cxd_agent（层 D 先例同构）。
    main_path, _ = injected
    src = main_path.read_bytes()
    ns: dict = {}
    t0 = time.perf_counter()
    exec(compile(src, str(main_path), "exec"), ns)  # noqa: S102 - 验收④装载门桌面版
    elapsed = time.perf_counter() - t0
    assert elapsed < _EXEC_BUDGET_SECONDS, f"装载 exec 超预算: {elapsed:.1f}s >= 120s"
    last = [v for v in ns.values() if callable(v)][-1]
    assert last.__name__ == "_cxs_agent"
    assert ns["_CXS_HOST"] is not None and ns["_CXS_HOST"].__name__ == "_cxd_agent"


def test_reinject_rejected(injected):
    # ③ 重复注入幂等拒绝：对已含块的文件再 inject → 抛错（sentinel/块字节判重），
    #    而非二次追加（文件逐字节不变）。
    main_path, _ = injected
    before = main_path.read_bytes()
    with pytest.raises(ValueError, match="already injected"):
        append_layer_s_block.inject(main_path)
    assert main_path.read_bytes() == before  # 未发生二次追加


def test_injected_block_matches_layer_file(injected):
    # ④ 防漂移断言：注入块=layer_s_block.py 当前盘上文本逐字节一致（注入块 sha==层文件 sha），
    #    且 report 的块审计字段与盘上真值一致。
    main_path, report = injected
    base_bytes = _BASE.read_bytes()
    block_bytes = _BLOCK.read_bytes()
    tail = main_path.read_bytes()[len(base_bytes) + len(append_layer_s_block._SEPARATOR):]
    assert tail == block_bytes
    assert hashlib.sha256(tail).hexdigest() == hashlib.sha256(block_bytes).hexdigest()
    assert report["block_sha256"] == hashlib.sha256(block_bytes).hexdigest()
    assert report["block_bytes"] == len(block_bytes)


# ---------------------------------------------------------------------------
# build 收口组（S2）：真跑一次 build_layer_s_candidate.build()（out_dir 默认=本目录），
# 三件产物落盘并保留（它就是候选包本体）；全文件 build 恰跑一次（耗时纪律）。

@pytest.fixture(scope="module")
def built():
    """一次性真跑 build()：返回 (manifest, elapsed_seconds)；产物留盘。"""
    t0 = time.perf_counter()
    manifest = build_layer_s_candidate.build()
    elapsed = time.perf_counter() - t0
    return manifest, elapsed


def test_build_full_chain_produces_artifacts(built):
    # ⑤ 全链实跑：三件产物落盘；manifest 字段齐且与盘上真值逐项一致。
    manifest, elapsed = built
    assert elapsed < _BUILD_BUDGET_SECONDS, f"build 全链超预算: {elapsed:.1f}s >= 180s"
    main_p = _HERE / "main.py"
    tar_p = _HERE / "submission.tar.gz"
    mf_p = _HERE / "build_manifest.json"
    assert main_p.is_file() and tar_p.is_file() and mf_p.is_file()
    main_bytes = main_p.read_bytes()
    assert manifest["schema"] == "orderbook_l1_derivative_manifest/1.0"
    assert _REQUIRED_MANIFEST_KEYS <= set(manifest)
    assert manifest["main_sha256"] == hashlib.sha256(main_bytes).hexdigest()
    assert manifest["main_bytes"] == len(main_bytes)
    assert manifest["tar_sha256"] == hashlib.sha256(tar_p.read_bytes()).hexdigest()
    assert manifest["tar_bytes"] == tar_p.stat().st_size
    assert manifest["block_sha256"] == hashlib.sha256(_BLOCK.read_bytes()).hexdigest()
    assert manifest["block_bytes"] == _BLOCK.stat().st_size
    # 注入形态复核：main.py == 基座全文+两空行分隔+layer_s_block.py 全文（append-only）
    base_bytes = _BASE.read_bytes()
    assert main_bytes == base_bytes + append_layer_s_block._SEPARATOR + _BLOCK.read_bytes()
    # 盘上 manifest 文件与 build() 返回 dict 逐项一致
    assert json.loads(mf_p.read_text(encoding="utf-8")) == manifest
    # 身份链：基座 a16e0e9b/2838cc66 + 注入块 sha + 双跑一致声明 + S3 占位
    chain = "\n".join(manifest["provenance_chain"])
    assert _BASE_SHA256 in chain
    assert _BASE_TAR_SHA256 in chain
    assert manifest["block_sha256"] in chain
    assert "double-build byte-identical" in chain
    assert "pending S3" in manifest["four_gates"]
    assert "pending S3" in manifest["h2h_2026_09_23"]
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", manifest["generated"])
    # 基座原件在 build 全链后仍逐字节未动（零改动纪律）
    assert hashlib.sha256(base_bytes).hexdigest() == _BASE_SHA256
    assert hashlib.sha256(_BASE_TAR.read_bytes()).hexdigest() == _BASE_TAR_SHA256


def test_build_tar_rebuild_matches_disk(built):
    # ⑥ 独立复核确定性：以盘上注入版 main.py 重建一次 tar（配方函数直调，不重跑
    #    build），与盘上 submission.tar.gz 逐字节一致、sha 等于 manifest 记录值。
    manifest, _ = built
    rebuilt = build_layer_s_candidate._pack_tar_gz((_HERE / "main.py").read_bytes())
    assert rebuilt == (_HERE / "submission.tar.gz").read_bytes()
    assert hashlib.sha256(rebuilt).hexdigest() == manifest["tar_sha256"]


def test_build_tar_members_match_round30(built):
    # ⑦ 成员清单==round-30 同款：与本仓 ../orderbook_derivative/submission.tar.gz
    #    成员名逐项相同，且恰为 ["main.py"]（Kaggle 提交布局）。
    with tarfile.open(_HERE / "submission.tar.gz") as tf:
        ours = tf.getnames()
    with tarfile.open(_BASE_TAR) as tf:
        r30 = tf.getnames()
    assert ours == r30 == ["main.py"]


def test_build_description_and_manifest_keys(built):
    # ⑧ 描述文案精确==R10 要求；manifest 必备键全部在位（不缺键）。
    manifest, _ = built
    assert manifest["description"] == "public derivative with seed-truncation layer"
    assert _REQUIRED_MANIFEST_KEYS <= set(manifest)
