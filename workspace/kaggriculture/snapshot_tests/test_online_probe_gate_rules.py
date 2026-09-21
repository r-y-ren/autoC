# test_online_probe_gate_rules.py —— 线上采样台账门 fail-closed 规则固化（R1 基线）
# ===========================================================================
# 钉什么：kgenv/online_probe.py 的 fail-closed 门行为（SOP 唯一门，
#   行为清单 §2 "online_probe.py：采样台账 fail-closed 门"）：
#   * build_sampling_payload 拒绝本地自对局源（replays_are_local_selfplay）；
#   * build_sampling_payload 拒绝零可用对局；
#   * next_round_gate：无台账 / 缺 COMPLETE 采样 / status=PENDING /
#     自对局源 / 台账-采样 submission_ref 不匹配 → 一律 pass=False 且
#     带明确 reasons；合法布局 → pass=True + sampled_rounds 登记。
# 台账/采样目录布局用 tmp_path 合成（不触碰 exports/ 真实台账）。
# 回放对象为合成最小 dict（720 步骨架 + TeamNames/statuses/rewards），
#   classify_replay/integrity 全链照跑。
# 冻结值 2026-09-21 实测固化。
# ===========================================================================

import json

import pytest

from kgenv import online_probe as op

ROUND_NO = 20          # >= FIRST_SAMPLING_ROUND(20)，门才检查采样记录
SUBMISSION_REF = 56400478


def _synthetic_replay(episode_id, opponent, our_reward, opp_reward,
                      me_seat=0):
    teams = (["renyxin", opponent] if me_seat == 0
             else [opponent, "renyxin"])
    rewards = ([our_reward, opp_reward] if me_seat == 0
               else [opp_reward, our_reward])
    return {"info": {"TeamNames": teams, "EpisodeId": episode_id},
            "statuses": ["DONE", "DONE"],
            "steps": [{}, {}] * 360,       # 720 步骨架（金额/动作缺省=0）
            "rewards": rewards}


@pytest.fixture()
def classified_games():
    return [op.classify_replay(_synthetic_replay(9001, "opp_alpha",
                                                 9000.0, 4000.0)),
            op.classify_replay(_synthetic_replay(9002, "opp_beta",
                                                 5000.0, 4800.0)),
            op.classify_replay(_synthetic_replay(9003, "opp_alpha",
                                                 7000.0, 6500.0))]


@pytest.fixture()
def launch_ledger():
    return {"candidate": {"submission_ref": SUBMISSION_REF,
                          "label": "v48-derivative",
                          "pkg_sha256": "0" * 64, "git_ref": "abc1234"},
            "status": "PENDING"}


@pytest.fixture()
def complete_payload(classified_games, launch_ledger):
    return op.build_sampling_payload(
        round_no=ROUND_NO, submission_ref=SUBMISSION_REF,
        launch_ledger=launch_ledger, games=classified_games,
        public_score=5.0, source={"channel": "kaggle-cli"},
        captured_at_utc="2026-09-21T00:00:00+00:00")


def _layout(tmp_path, ledger=None, payload=None):
    ledger_dir = op.launch_ledger_dir(tmp_path)
    sampling_dir = op.sampling_dir(tmp_path)
    ledger_dir.mkdir(parents=True, exist_ok=True)
    sampling_dir.mkdir(parents=True, exist_ok=True)
    if ledger is not None:
        (ledger_dir / f"round{ROUND_NO}_ledger.json").write_text(
            json.dumps(ledger), encoding="utf-8")
    if payload is not None:
        (sampling_dir / f"round{ROUND_NO}_sampling.json").write_text(
            json.dumps(payload), encoding="utf-8")
    return tmp_path


def test_synthetic_games_classify_public_pass(classified_games):
    assert [g["kind"] for g in classified_games] == ["public"] * 3
    assert all(g["integrity"] == "PASS" for g in classified_games)
    assert [g["won"] for g in classified_games] == [True] * 3


def test_payload_shape_and_validate_ok(complete_payload):
    assert complete_payload["schema"] == "online-probe-sampling/1.0"
    assert complete_payload["status"] == "COMPLETE"
    assert complete_payload["submission_ref"] == SUBMISSION_REF
    assert complete_payload["public_sampling"]["public_games"] == 3
    assert complete_payload["public_sampling"]["record"] == "3W-0L"
    assert complete_payload["source"]["replays_are_local_selfplay"] is False
    assert op.validate_sampling(complete_payload) == []


def test_build_rejects_local_selfplay_source(classified_games,
                                             launch_ledger):
    with pytest.raises(op.OnlineProbeError,
                       match="local self-play cannot complete"):
        op.build_sampling_payload(
            round_no=ROUND_NO, submission_ref=SUBMISSION_REF,
            launch_ledger=launch_ledger, games=classified_games,
            public_score=None,
            source={"replays_are_local_selfplay": True},
            captured_at_utc="2026-09-21T00:00:00+00:00")


def test_build_rejects_no_usable_games(launch_ledger):
    with pytest.raises(op.OnlineProbeError, match="no usable official games"):
        op.build_sampling_payload(
            round_no=ROUND_NO, submission_ref=SUBMISSION_REF,
            launch_ledger=launch_ledger, games=[], public_score=None,
            source={}, captured_at_utc="x")


def test_gate_empty_root_fails_closed(tmp_path):
    report = op.next_round_gate(tmp_path)
    # 早退分支的冻结形态：只有三键（无 rule/sampled/missing——本身就是
    # 一个被固化的行为面）。
    assert report == {"pass": False, "latest_round": None,
                      "reasons": ["no launch ledgers found"]}


def test_gate_missing_sampling_fails_closed(tmp_path, launch_ledger):
    root = _layout(tmp_path, ledger=launch_ledger, payload=None)
    report = op.next_round_gate(root)
    assert report["pass"] is False
    assert report["latest_round"] == ROUND_NO
    assert any("still has no sampling record" in reason
               for reason in report["reasons"])
    assert any("latest launch round" in reason
               for reason in report["reasons"])


def test_gate_valid_layout_passes(tmp_path, launch_ledger,
                                  complete_payload):
    root = _layout(tmp_path, ledger=launch_ledger, payload=complete_payload)
    report = op.next_round_gate(root)
    assert report["pass"] is True
    assert report["reasons"] == []
    assert report["sampled_rounds"] == [ROUND_NO]
    assert report["missing_rounds"] == []


def test_gate_rejects_pending_status(tmp_path, launch_ledger,
                                     complete_payload):
    stale = dict(complete_payload, status="PENDING")
    root = _layout(tmp_path, ledger=launch_ledger, payload=stale)
    report = op.next_round_gate(root)
    assert report["pass"] is False
    assert any("status=PENDING" in reason for reason in report["reasons"])


def test_gate_rejects_local_selfplay_sampling(tmp_path, launch_ledger,
                                              complete_payload):
    forged = json.loads(json.dumps(complete_payload))
    forged["source"]["replays_are_local_selfplay"] = True
    root = _layout(tmp_path, ledger=launch_ledger, payload=forged)
    report = op.next_round_gate(root)
    assert report["pass"] is False
    assert any("local self-play" in reason for reason in report["reasons"])


def test_gate_rejects_ref_mismatch(tmp_path, launch_ledger,
                                    complete_payload):
    mismatched = dict(complete_payload, submission_ref=111)
    root = _layout(tmp_path, ledger=launch_ledger, payload=mismatched)
    report = op.next_round_gate(root)
    assert report["pass"] is False
    assert any("sampling ref 111 != launch ref 56400478" in reason
               for reason in report["reasons"])


def test_validate_sampling_min_public_threshold(complete_payload):
    """最新一轮需 >=3 public 对局：2 局 → 明确 issue。"""
    trimmed = json.loads(json.dumps(complete_payload))
    trimmed["public_sampling"]["public_games"] = 2
    issues = op.validate_sampling(trimmed, min_public=3)
    assert "public_games=2 < 3" in issues


def test_assert_next_round_allowed_raises_or_passes(tmp_path, launch_ledger,
                                                    complete_payload):
    root = _layout(tmp_path, ledger=launch_ledger, payload=None)
    with pytest.raises(op.OnlineProbeError, match="no sampling record"):
        op.assert_next_round_allowed(root)
    _layout(tmp_path, payload=complete_payload)
    report = op.assert_next_round_allowed(root)
    assert report["pass"] is True
