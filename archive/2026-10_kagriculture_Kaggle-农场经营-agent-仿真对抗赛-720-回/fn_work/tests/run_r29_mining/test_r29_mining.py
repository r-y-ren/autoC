"""run_r29_mining 三件套真实测试（B49；R29 lint/registry/编排三组）。

覆盖（对齐 fn_docs/hybrid/responsibility.md【R29 增补】判据原文）：
① lint 组——四字段缺失逐项报错（entry/field 逐条钉住）；来源 URL 不在册 fail；
   抓取日期缺项 fail；禁区冲突度非法 fail（域={无,低,中,高,禁区同族}）；
   格式不可解析 fail（坏 markdown/坏 JSON/非 list/非 dict 条目）；markdown/JSON
   双形态过检；INDEX 不可读 fail-closed。
② registry 组——追加不改旧种子（旧字节前缀原样保留）；名录重复（同名同档）与
   冲突（同名异档）跳过并记录（含 roster 内部重复）；"对手换血"判定法+跨频道
   线索（nikital7/Nikita Lugovoy）入 SOP 留痕。
③ 编排组——检查不过不落盘（报告/INDEX/种子/SOP 一概不动）；检查过=报告落
   analyses/31-*.md+INDEX 登记+名录回灌三面落盘（tmp_path 夹具）。
确定性：全部产物无时间戳，同输入同输出。
"""

import json

import pytest

from run_r29_mining.check_reference_map import ALLOWED_RISK, check_reference_map
from run_r29_mining.register_opponent_pool_seeds import (
    CROSS_CHANNEL_LEADS,
    TURNOVER_RULE,
    register_opponent_pool_seeds,
)
from run_r29_mining.run_r29_mining import run_r29_mining

_URL = (
    "https://github.com/mooman0222/Kaggriculture-opencode/blob/main/"
    ".opencode/knowledge/refs/github-2026-09-27.md"
)
_URL2 = "https://www.kaggle.com/code/leoprovorov/kaggricult-man-reverse-engineering"

_INDEX_HEADER = (
    "# references INDEX\n\n"
    "| 路径 | 来源 URL | 抓取日期 | 用途 | 引用它的产物/任务 |\n"
    "|---|---|---|---|---|\n"
)


def _entry(**over):
    item = {
        "evidence": "github-2026-09-27.md L12-L40（r34l_v7 对战表）",
        "hook": "对手池种子定义（select_advanceable 视界面）",
        "expected_signal": "战后对手池覆盖率上升",
        "risk": "低",
        "source_url": _URL,
        "fetched_date": "2026-09-28",
    }
    item.update(over)
    return item


def _write_index(tmp_path, rows=("",)):
    index = tmp_path / "references" / "INDEX.md"
    index.parent.mkdir(parents=True, exist_ok=True)
    index.write_text(_INDEX_HEADER + "\n".join(rows) + "\n", encoding="utf-8")
    return index


# ---------------------------------------------------------------- lint 组
def test_check_reference_map_pass(tmp_path):
    """过检面：四字段齐+URL 在册+日期在场+风险域内→pass=True 且 missing 空。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",
                                         f"| b.md | {_URL2} | 2026-09-28 | x | y |"))
    result = check_reference_map([_entry(), _entry(source_url=_URL2, risk="无")], index_doc=index)
    assert result == {"pass": True, "missing": []}
    assert ALLOWED_RISK == frozenset({"无", "低", "中", "高", "禁区同族"})


def test_check_reference_map_four_fields_missing_each(tmp_path):
    """四字段缺失逐项报错：evidence/hook/expected_signal/risk 各自独立成条目。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",))
    result = check_reference_map(
        [_entry(evidence="", hook=" ", expected_signal=None, risk="")], index_doc=index
    )
    assert result["pass"] is False
    reported = {(m["entry"], m["field"]) for m in result["missing"]}
    assert reported == {(0, "evidence"), (0, "hook"), (0, "expected_signal"), (0, "risk")}
    assert all(m["entry"] == 0 for m in result["missing"])


def test_check_reference_map_url_not_registered(tmp_path):
    """URL 不在册 fail：in-册 URL 过、out-of-册 URL 逐条报 source_url。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",))
    result = check_reference_map(
        [_entry(), _entry(source_url="https://evil.example/not-registered")], index_doc=index
    )
    assert result["pass"] is False
    assert result["missing"] == [
        {"entry": 1, "field": "source_url", "reason": "来源 URL 不在 references INDEX 在册"}
    ]


def test_check_reference_map_fetched_date_missing(tmp_path):
    """抓取日期在场判据：缺日期独立报 fetched_date，不与四字段混报。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",))
    result = check_reference_map([_entry(fetched_date="")], index_doc=index)
    assert result["pass"] is False
    assert [(m["entry"], m["field"]) for m in result["missing"]] == [(0, "fetched_date")]


def test_check_reference_map_risk_domain(tmp_path):
    """禁区冲突度非法 fail：域内 5 值全过，域外值逐条报 risk。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",))
    ok = check_reference_map([_entry(risk=v) for v in sorted(ALLOWED_RISK)], index_doc=index)
    assert ok["pass"] is True
    bad = check_reference_map([_entry(risk="极高"), _entry(risk="禁区")], index_doc=index)
    assert bad["pass"] is False
    assert [(m["entry"], m["field"]) for m in bad["missing"]] == [(0, "risk"), (1, "risk")]
    assert all("取值非法" in m["reason"] for m in bad["missing"])


@pytest.mark.parametrize(
    "mapping",
    [
        "这不是表格也不是 JSON",
        "[{bad json",
        '{"not": "a list"}',
        "[1, 2, 3]",
        42,
        None,
        "",
    ],
)
def test_check_reference_map_unparseable_fails(tmp_path, mapping):
    """格式不可解析→fail：坏 markdown/坏 JSON/非 list/非 dict 条目/标量全打回。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",))
    result = check_reference_map(mapping, index_doc=index)
    assert result["pass"] is False
    assert result["missing"][0]["field"] == "format"


def test_check_reference_map_markdown_and_json_forms(tmp_path):
    """markdown 表/JSON 串双形态过检：与 list 主格式同判据。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",))
    md = (
        "| 证据 | 挂接面 | 预期信号 | 禁区冲突度 | 来源 URL | 抓取日期 |\n"
        "|---|---|---|---|---|---|\n"
        f"| L12-L40 | 对手池 | 覆盖率↑ | 低 | {_URL} | 2026-09-28 |\n"
    )
    assert check_reference_map(md, index_doc=index)["pass"] is True
    assert check_reference_map(json.dumps([_entry()]), index_doc=index)["pass"] is True


def test_check_reference_map_index_unreadable_fails(tmp_path):
    """INDEX 不可读→fail-closed：空清单也不放行。"""
    result = check_reference_map([], index_doc=tmp_path / "no-such-INDEX.md")
    assert result["pass"] is False
    assert result["missing"][0]["field"] == "index_doc"


# ------------------------------------------------------------- registry 组
def test_register_opponent_pool_seeds_appends_only(tmp_path):
    """追加不改旧种子：旧字节前缀原样保留+新种子尾随追加；重复（同名同档）跳过并记录。"""
    pool = tmp_path / "pool.md"
    sop = tmp_path / "sop.md"
    old = "# 对手池种子定义（追加式）\n- name=OLD | score_band=top | note=旧种子不动\n"
    pool.write_text(old, encoding="utf-8")
    roster = [
        {"name": "UMG", "score_band": "top", "note": "源码未公开"},
        {"name": "OLD", "score_band": "top", "note": "同名同档重复"},
    ]
    out = register_opponent_pool_seeds(roster, pool, sop)
    text = pool.read_text(encoding="utf-8")
    assert text.startswith(old)  # 旧种子一字不动
    assert text == out["definition"]
    assert out["added"] == ["UMG"]
    assert out["skipped"] == [{"name": "OLD", "reason": "重复（同名同档已有种子），跳过"}]
    assert "- name=UMG | score_band=top | note=源码未公开\n" in text
    assert text.count("- name=OLD") == 1  # 重复不二次入池
    assert "OLD" in out["record"] and "跳过" in out["record"]


def test_register_opponent_pool_seeds_conflict_and_inner_dup(tmp_path):
    """同名异档=冲突跳过；roster 内部重复同样跳过并记录。"""
    pool = tmp_path / "pool.md"
    sop = tmp_path / "sop.md"
    pool.write_text("- name=OLD | score_band=top | note=旧\n", encoding="utf-8")
    roster = [
        {"name": "OLD", "score_band": "mid", "reason": "x", "note": "异档"},
        {"name": "Majkel", "score_band": "top", "note": "首现"},
        {"name": "Majkel", "score_band": "top", "note": "roster 内重复"},
    ]
    out = register_opponent_pool_seeds(roster, pool, sop)
    assert out["added"] == ["Majkel"]
    assert out["skipped"][0]["name"] == "OLD" and "冲突" in out["skipped"][0]["reason"]
    assert out["skipped"][1]["name"] == "Majkel" and "重复" in out["skipped"][1]["reason"]
    assert pool.read_text(encoding="utf-8").count("- name=Majkel") == 1
    assert pool.read_text(encoding="utf-8").count("- name=OLD") == 1


def test_register_opponent_pool_seeds_sop_trace(tmp_path):
    """换血判定法+跨频道线索（nikital7/Nikita Lugovoy）入 SOP 留痕；SOP 追加不覆盖。"""
    pool = tmp_path / "pool.md"
    sop = tmp_path / "sop.md"
    sop.write_text("# 读数 SOP\n旧留痕不动\n", encoding="utf-8")
    out = register_opponent_pool_seeds(
        [{"name": "kuro", "score_band": "top", "note": "源码未公开"}], pool, sop
    )
    text = sop.read_text(encoding="utf-8")
    assert text.startswith("# 读数 SOP\n旧留痕不动\n")  # 追加写
    assert TURNOVER_RULE in text and TURNOVER_RULE in out["record"]
    for lead in CROSS_CHANNEL_LEADS:
        assert lead in text
    assert "nikital7" in text and "Nikita Lugovoy" in text
    assert "kuro 入池" in text


# --------------------------------------------------------------- 编排组
def test_run_r29_mining_check_fails_writes_nothing(tmp_path):
    """检查不过→打回不落盘：报告/INDEX/种子/SOP 四面零写入。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",))
    index_before = index.read_text(encoding="utf-8")
    corpus = {
        "candidates": [_entry(hook=""), _entry(source_url="https://evil.example/x")],
        "roster": [{"name": "UMG", "score_band": "top", "note": "n"}],
    }
    out = run_r29_mining(corpus, tmp_path)
    assert out["pass"] is False
    fields = {m["field"] for m in out["missing"]}
    assert {"hook", "source_url"} <= fields
    assert not (tmp_path / "analyses").exists()
    assert index.read_text(encoding="utf-8") == index_before
    assert not (tmp_path / "opponent_pool_seeds.md").exists()
    assert not (tmp_path / "readout_sop.md").exists()
    assert out["report_path"] is None and out["registry"] is None


def test_run_r29_mining_pass_lands_report_index_registry(tmp_path):
    """检查过=报告（analyses/31-*.md）+INDEX 登记+名录回灌三面落盘。"""
    index = _write_index(tmp_path, rows=(f"| a.md | {_URL} | 2026-09-28 | x | y |",
                                         f"| b.md | {_URL2} | 2026-09-27 | x | y |"))
    index_before = index.read_text(encoding="utf-8")
    corpus = {
        "candidates": [
            _entry(),
            _entry(),  # (source_url,hook) 重复→甄选去重
            _entry(source_url=_URL2, fetched_date="2026-09-27", selected=False),  # 显式剔除
            _entry(
                evidence="L1-L9 | 含竖线转义",
                hook="execution 面",
                expected_signal="成交价不降",
                risk="中",
                source_url=_URL2,
                fetched_date="2026-09-27",
            ),
        ],
        "roster": [{"name": "UMG", "score_band": "top", "note": "源码未公开"}],
    }
    out = run_r29_mining(corpus, tmp_path)
    assert out["pass"] is True and out["missing"] == []

    reports = list((tmp_path / "analyses").glob("31-*.md"))
    assert len(reports) == 1
    body = reports[0].read_text(encoding="utf-8")
    assert "只挖不改" in body and "不实施任何代码改动" in body
    assert body.count("\n| 1 |") == 1 and body.count("\n| 2 |") == 1  # 去重+剔除后恰 2 条
    assert "L1-L9 \\| 含竖线转义" in body  # 竖线转义保表完整

    index_text = index.read_text(encoding="utf-8")
    assert index_text.startswith(index_before)  # 登记=追加不改旧行
    assert "31-r29-reference-map.md" in index_text.splitlines()[-1]
    assert _URL in index_text.splitlines()[-1] and _URL2 in index_text.splitlines()[-1]

    pool = (tmp_path / "opponent_pool_seeds.md").read_text(encoding="utf-8")
    sop = (tmp_path / "readout_sop.md").read_text(encoding="utf-8")
    assert "- name=UMG | score_band=top | note=源码未公开" in pool
    assert TURNOVER_RULE in sop and "nikital7" in sop and "Nikita Lugovoy" in sop
    assert out["registry"]["added"] == ["UMG"]
    # 确定性：同输入二次编排仅追加、不改旧（INDEX 行新增一行，报告同文）
    out2 = run_r29_mining(corpus, tmp_path)
    assert out2["pass"] is True
    assert reports[0].read_text(encoding="utf-8") == body
    assert out2["registry"]["added"] == []  # 种子已存在→重复跳过
