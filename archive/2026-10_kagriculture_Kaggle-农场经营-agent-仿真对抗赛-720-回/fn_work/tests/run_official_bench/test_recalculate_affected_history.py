"""recalculate_affected_history 真实行为测试（G1 重算台账）。

覆盖（对齐 fn_docs/responsibility.md run_official_bench 块该节核验命令
"台账存在+键完整"）：
① 合成小清单+合成回放（生成方式复刻 test_rollout_with_replay_opponent
   ——引擎固定种子 20260921，seat0=恒 PASS→3000.0、seat1=每 5 回合买
   1 包 WHEAT 种子→1570.0）→ 台账含 RECALC 条目，双口径字段齐：
   原值（错位口径 [1570.0,3000.0] 伪影）/ 重算值（seated 口径
   [3000.0,1570.0] 真值）/ 翻转标记随两值关系翻转。
② 数据缺失路径 → SKIP(replay_data_missing) 且批不中断（缺失条目前后
   夹正常条目，三者均入台账）。
③ 台账 schema 键完整（结论标识/局号/原值/重算值/翻转/状态列头齐 +
   行 dict 键齐；另覆盖 persona_missing SKIP 留因）。测试全程 tmp_path
   重定向台账路径，不写真实 fn_docs。
"""

import json

import pytest

from kaggle_environments import make

from run_official_bench.recalculate_affected_history import (
    LEDGER_COLUMNS,
    LEDGER_ENTRY_KEYS,
    recalculate_affected_history,
)

SEED = 20260921
EPISODE_STEPS = 720

# 合成回放终局真值 / 旧错位通道伪影（与 test_rollout 冻结口径一致）
FROZEN_SEATED_FINAL = [3000.0, 1570.0]
FROZEN_MISSEATED_FINAL = [1570.0, 3000.0]


def _pass_bot(obs):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _seed_buyer_bot():
    """状态无关脚本：每第 5 个决策买 1 包 WHEAT 种子（与回放生成同源）。"""
    counter = [0]

    def bot(obs):
        counter[0] += 1
        if counter[0] % 5 == 0:
            return {"farmer": ["PASS"], "hands": [],
                    "market": [["BUY_SEED", "WHEAT", 1]]}
        return {"farmer": ["PASS"], "hands": [], "market": []}

    return bot


def _to_plain(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if isinstance(obj, dict):
        return {key: _to_plain(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_plain(value) for value in obj]
    return obj


@pytest.fixture(scope="module")
def synthetic_replay():
    """经引擎生成合成回放（module 级共享；复刻 test_rollout 生成方式）。"""
    env = make("kaggriculture",
               configuration={"episodeSteps": EPISODE_STEPS, "seed": SEED,
                              "actTimeout": 60},
               debug=True)
    env.run([_pass_bot, _seed_buyer_bot()])
    final = env.steps[-1]
    assert [s["status"] for s in final] == ["DONE", "DONE"]
    replay = {
        "configuration": _to_plain(env.configuration),
        "info": {"seed": SEED},
        "steps": _to_plain(env.steps),
        "rewards": [float(s["reward"]) for s in final],
    }
    assert replay["rewards"] == FROZEN_SEATED_FINAL
    return replay


def _write_replay(tmp_path, name, replay):
    """合成回放落 tmp 文件（台账引擎按路径装载 json 回放）。"""
    path = tmp_path / name
    path.write_text(json.dumps(replay), encoding="utf-8")
    return path


def _seated_entry(entry_id, replay_path, original_value):
    """合成结论条目：me_seat=1 + 同源 persona 复刻 → seated 真值。"""
    return {"id": entry_id, "original_value": original_value,
            "episodes": [{"episode": 1, "replay_path": str(replay_path),
                          "me_seat": 1}],
            "injection_point": 0,
            "agent_factory": _seed_buyer_bot,
            "aggregate": lambda rows: rows[0]["seated_final"]}


def _missing_entry(entry_id, tmp_path):
    return {"id": entry_id, "original_value": "5/9",
            "episodes": [{"episode": 9,
                          "replay_path": str(tmp_path / f"{entry_id}.json"),
                          "me_seat": 0}],
            "agent_callable": _pass_bot}


# ---------------------------------------------------------------------------
# ① 合成清单 + 合成回放 → RECALC 条目（双口径字段齐）
# ---------------------------------------------------------------------------

def test_recalc_entries_dual_channel_fields(synthetic_replay, tmp_path):
    """两条合成结论（原值分别为错位伪影/已是真值序）→ 均 RECALC：重算值
    恒 seated 真值 [3000.0,1570.0]，是否翻转随原值口径（伪影原值→是、
    真值原值→否）；台账文件含两口径列值与 RECALC 态。"""
    replay_path = _write_replay(tmp_path, "episode-1-replay.json",
                                synthetic_replay)
    entries = [
        _seated_entry("cf:misseated_artifact", replay_path,
                      FROZEN_MISSEATED_FINAL),
        _seated_entry("cf:already_seated", replay_path,
                      FROZEN_SEATED_FINAL),
    ]
    out = recalculate_affected_history(
        entries, ledger_path=tmp_path / "ledger.md")

    assert out["n_entries"] == 2
    assert out["n_recalc"] == 2 and out["n_skip"] == 0
    row_artifact, row_seated = out["entries"]

    assert row_artifact["status"] == "RECALC"
    # 双口径字段齐：原值（错位口径）与重算值（seated 口径）各就各位
    assert row_artifact["original_value"] == FROZEN_MISSEATED_FINAL
    assert row_artifact["recalc_value"] == FROZEN_SEATED_FINAL
    assert row_artifact["flipped"] is True

    assert row_seated["status"] == "RECALC"
    assert row_seated["original_value"] == FROZEN_SEATED_FINAL
    assert row_seated["recalc_value"] == FROZEN_SEATED_FINAL
    assert row_seated["flipped"] is False

    ledger = (tmp_path / "ledger.md").read_text(encoding="utf-8")
    assert "cf:misseated_artifact" in ledger and "cf:already_seated" in ledger
    assert "RECALC" in ledger
    # 台账渲染两口径数值（JSON 紧凑形态）
    assert "[3000.0,1570.0]" in ledger and "[1570.0,3000.0]" in ledger


# ---------------------------------------------------------------------------
# ② 数据缺失 → SKIP(replay_data_missing)，批不中断
# ---------------------------------------------------------------------------

def test_missing_replay_skips_without_breaking_batch(synthetic_replay,
                                                     tmp_path):
    """[缺失, 正常, 缺失] 三条一批：两条 SKIP(replay_data_missing) 留缺失
    路径明细，正常条不受前后失败影响照常 RECALC——整批完成、台账完整。"""
    replay_path = _write_replay(tmp_path, "episode-1-replay.json",
                                synthetic_replay)
    entries = [
        _missing_entry("m1", tmp_path),
        _seated_entry("cf:good", replay_path, FROZEN_MISSEATED_FINAL),
        _missing_entry("m2", tmp_path),
    ]
    out = recalculate_affected_history(
        entries, ledger_path=tmp_path / "ledger.md")

    assert out["n_entries"] == 3
    assert out["n_recalc"] == 1 and out["n_skip"] == 2
    m1, good, m2 = out["entries"]
    assert m1["status"] == "SKIP(replay_data_missing)"
    assert m2["status"] == "SKIP(replay_data_missing)"
    assert "m1.json" in (m1["detail"] or "")
    assert good["status"] == "RECALC"
    assert good["recalc_value"] == FROZEN_SEATED_FINAL
    # SKIP 条目双口径占位：重算值/翻转记空
    assert m1["recalc_value"] is None and m1["flipped"] is None

    ledger = (tmp_path / "ledger.md").read_text(encoding="utf-8")
    assert "SKIP(replay_data_missing)" in ledger
    assert "SKIP 详情" in ledger and "m1.json" in ledger


# ---------------------------------------------------------------------------
# ③ 台账 schema 键完整（无引擎，纯快路径）
# ---------------------------------------------------------------------------

def test_ledger_schema_keys_complete(tmp_path):
    """六列表头齐（结论标识/局号/原值（错位口径）/重算值（seated 口径）/
    是否翻转/状态）+ 行 dict 键=LEDGER_ENTRY_KEYS；头部含口径定义与重跑
    前提；persona 缺失条目 SKIP(persona_missing) 留 persona_note。"""
    replay_path = _write_replay(tmp_path, "ghost.json", {"steps": [[{}]]})
    entries = [
        _missing_entry("m1", tmp_path),
        {"id": "p1", "original_value": "7/13",
         "episodes": [{"episode": 3, "replay_path": str(replay_path),
                       "me_seat": 0}],
         "persona_note": "v3 运行点 base 臂 persona（原脚本同源）"},
    ]
    ledger_path = tmp_path / "ledger.md"
    out = recalculate_affected_history(entries, ledger_path=ledger_path)

    assert out["n_skip"] == 2
    for row in out["entries"]:
        assert set(LEDGER_ENTRY_KEYS) <= set(row)
    statuses = {r["id"]: r["status"] for r in out["entries"]}
    assert statuses["m1"] == "SKIP(replay_data_missing)"
    assert statuses["p1"] == "SKIP(persona_missing)"
    assert "v3 运行点 base 臂 persona" in (
        next(r for r in out["entries"] if r["id"] == "p1")["detail"])

    text = ledger_path.read_text(encoding="utf-8")
    assert "| " + " | ".join(LEDGER_COLUMNS) + " |" in text
    assert "口径定义" in text and "重跑前提" in text
    assert "SKIP(persona_missing)" in text
