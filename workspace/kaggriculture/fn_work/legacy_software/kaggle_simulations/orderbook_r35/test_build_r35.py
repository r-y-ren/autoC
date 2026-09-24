# -*- coding: utf-8 -*-
"""R17 测试面：build_r35（白名单合并构建+diff 审计+打包）。"""
import glob
import json
import os

import pytest

from orderbook_r35 import build_r35 as B


R34A_FIXTURE = '''_V92_P_EVERY = 2
_CA_MARGIN = -15.0
_CA_DROP = 0.0
_OR2_SLOT_MARGIN = 8.0
V9_RACE_DEFAULT = 40
V9_RACE_DEFAULT = 44
_V93_ROUTE_BY_RIVAL = {(229.0, 9989): 128}


def agent(o, c=None):
    return {'farmer': ['PASS']}


def _v233_arm(obs, initial, state):
    extra=([['BUY_LAND'],['BUY_ANIMAL','SHEEP',6]] if initial else [])+[['BUY_PRODUCT','WHEAT',6],['HIRE'],['HIRE']]
    incoming=6+6*initial
    budget=7000*initial+6*(int(obs['market']['prices']['WHEAT'])+10)
    if not 0<shortage<=6 or state.get('rescue_today',0)+shortage>6:return action
    if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) for x in range(5,8)):return False
    if state:
        funded='SE' in farm['unlocked_quadrants'] and (not pending['initial'] or private['shed'].get('SHEEP',0)>=6)
        if True:
            if True:
                for i in range(2):state['workers'][pending['first']+i]=[(x,5+i) for x in range(5,8)]
    return incoming + budget + funded


CROP_MIN_PRICE=70


def _v219_qualifies(obs):
    farm = obs['farm']
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    return True


def e402_agent(o, c=None):
    return {'farmer': ['PASS']}


def _ig_standard():
    return None


def _cxd_agent(o, c=None):
    return {'farmer': ['PASS']}
'''

SRC2965_FIXTURE = '''def _cxd_agent(o, c=None):
    return {'farmer': ['PASS']}
kaggle_submission_agent = _cxd_agent
_HR_PARENT = agent
_HR_REPORT = {'changed': 0, 'extra_units': 0, 'errors': 0}


def agent(observation, configuration=None):
    action = _HR_PARENT(observation, configuration)
    step = int(observation['step'])
    if not 192 <= step < 696:
        return action
    command = action.get('farmer') or ['PASS']
    if command[:2] != ['PICKUP', 'WHEAT']:
        return action
    try:
        requested = int(command[2]) if len(command) >= 3 else 1
        extra = min(2, max(0, 2 - requested))
        if extra:
            _HR_REPORT['changed'] += 1
            return dict(action, farmer=['PICKUP', 'WHEAT', requested + extra])
    except Exception:
        _HR_REPORT['errors'] += 1
    return action


kaggle_submission_agent = agent
'''


def _write_fixture(tmp_path, adopt, with_2965=True):
    r34a = tmp_path / "r34a_main.py"
    r34a.write_text(R34A_FIXTURE)
    src2965 = tmp_path / "main2965.py"
    src2965.write_text(SRC2965_FIXTURE)
    monkey_fetch = {"path": str(src2965), "sha256": "0" * 64, "source": "fixture"}
    return r34a, src2965, monkey_fetch


def test_extract_hr_block_and_ledger_exclusion(tmp_path):
    src2965 = tmp_path / "s.py"
    src2965.write_text(SRC2965_FIXTURE.replace(
        "_HR_PARENT = agent",
        "_NEW_PARENT = _cxd_agent\n_NEW_REPORT = {}\nsubmission_v57 = agent\n"
        "_HR_PARENT = agent"))
    block, audit = B.extract_hr_block(str(src2965))
    assert block[0] == "_HR_PARENT = agent"
    assert block[-1] == "kaggle_submission_agent = agent"
    assert audit["lines"] >= 20
    plain = tmp_path / "plain.py"
    plain.write_text(SRC2965_FIXTURE)
    block2, _ = B.extract_hr_block(str(plain))
    assert block2 == block


def test_extract_hr_block_rejects_telemetry(tmp_path):
    src2965 = tmp_path / "s.py"
    src2965.write_text(SRC2965_FIXTURE.replace(
        "_HR_REPORT = {'changed': 0, 'extra_units': 0, 'errors': 0}",
        "_HR_REPORT = {'changed': 0}\n_LEDGER_PARENT = agent"))
    with pytest.raises(B.BuildR35Error):
        B.extract_hr_block(str(src2965))


def test_build_change_one_only(tmp_path, monkeypatch):
    """adopt={} → 恰改 1（CA −25 + _HR 尾块）；末 callable=agent。"""
    r34a, src2965, fetch = _write_fixture(tmp_path, {})
    monkeypatch.setattr(B._ba, "fetch_2965_source", lambda: fetch)
    out = tmp_path / "out"
    summary = B.build_r35({}, str(r34a), str(out))
    assert summary["ok"] is True
    assert summary["adopted"] == {"ca_margin": True, "hr_tail": True}
    text = (out / "main.py").read_text()
    assert "_CA_MARGIN = -25.0" in text and "_CA_MARGIN = -15.0" not in text
    assert "_HR_PARENT = _cxd_agent" in text
    assert text.rstrip().endswith("_r35_agent = agent")
    assert "_NEW_PARENT" not in text and "_LEDGER" not in text
    assert summary["diff_attribution"] == {
        "ca_margin_true_value(-25, 2965 tail)": 1,
        "hr_tail_append(_HR group-feeding, _LEDGER excluded)": 1}
    manifest = json.loads((out / "build_manifest.json").read_text())
    assert manifest["schema"] == "orderbook_r35_manifest/1.0"
    assert manifest["description"] == B.DESCRIPTION
    tar1 = (out / "submission.tar.gz").read_bytes()
    assert B.build_tar_bytes((out / "main.py").read_bytes()) == tar1


def test_build_all_adopted(tmp_path, monkeypatch):
    """三项条件项全并入 → diff 审计恰五类；装载/常数/符号校验过。"""
    r34a, src2965, fetch = _write_fixture(tmp_path, {})
    monkeypatch.setattr(B._ba, "fetch_2965_source", lambda: fetch)
    out = tmp_path / "out"
    adopt = {"sheep": {"adopt": True, "params": {"sheep_buy": 8}},
             "tomato": {"adopt": True,
                        "params": {"CROP_MIN_PRICE": 90, "money_gate": 9000}},
             "route": {"adopt": True, "params": {"_V93_ROUTE_BY_RIVAL":
                                                 {"(900.0, 9989)": 5}}}}
    summary = B.build_r35(adopt, str(r34a), str(out))
    text = (out / "main.py").read_text()
    assert "'SHEEP',8]]" in text and "'WHEAT',8]" in text
    assert "incoming=8+8*initial" in text
    assert "budget=8000*initial+8*(" in text
    assert "shortage<=8" in text and "range(5,9)" in text
    assert "CROP_MIN_PRICE=90" in text and "farm['money'] < 9000 or" in text
    assert "_V93_ROUTE_BY_RIVAL = {(229.0, 9989): 128, (900.0, 9989): 5}" in text
    assert summary["adopted"]["sheep_6to8"] is True
    assert summary["adopted"]["tomato_gate"] is True
    assert summary["adopted"]["route_table"] is True
    assert set(summary["diff_attribution"]) == {
        "ca_margin_true_value(-25, 2965 tail)",
        "hr_tail_append(_HR group-feeding, _LEDGER excluded)",
        "sheep_6to8(day-11 arm)", "tomato_gate_params(scan winner)",
        "route_table_entries(expansion)"}


def test_build_route_only_additions(tmp_path, monkeypatch):
    """路由表改写既有项值 → 拒（只加表项纪律）。"""
    r34a, src2965, fetch = _write_fixture(tmp_path, {})
    monkeypatch.setattr(B._ba, "fetch_2965_source", lambda: fetch)
    adopt = {"route": {"adopt": True, "params": {"_V93_ROUTE_BY_RIVAL":
                                                 {"(229.0, 9989)": 7}}}}
    with pytest.raises(B.BuildR35Error):
        B.build_r35(adopt, str(r34a), str(tmp_path / "out2"))


def test_build_rejects_stray_diff(tmp_path, monkeypatch):
    """白名单外差异（构造层注入杂散行）→ diff 审计红（fail-closed）。"""
    r34a, src2965, fetch = _write_fixture(tmp_path, {})
    monkeypatch.setattr(B._ba, "fetch_2965_source", lambda: fetch)
    real_change_one = B.apply_change_one

    def change_one_plus_stray(text, path):
        out, audit = real_change_one(text, path)
        return out + "_STRAY_LINE = 1\n", audit

    monkeypatch.setattr(B, "apply_change_one", change_one_plus_stray)
    with pytest.raises(B.BuildR35Error):
        B.build_r35({}, str(r34a), str(tmp_path / "out3"))


def test_audit_diff_vs_r34a_classification(tmp_path):
    r34a = tmp_path / "a.py"
    r35 = tmp_path / "b.py"
    r34a.write_text("x = 1\ny = 2\n")
    r35.write_text("x = 1\n_STRAY_LINE = 1\n")
    audit = B.audit_diff_vs_r34a(str(r34a), str(r35))
    assert audit["ok"] is False and audit["attribution"] == {"UNATTRIBUTED": 1}


_REAL_BASE = (glob.glob("/mnt/data/Code/autoC/workspace/kag*iculture/fn_work/"
                        "legacy_software/kaggle_simulations/"
                        "orderbook_2965_adopt/a/main.py") or [None])[0]


@pytest.mark.skipif(_REAL_BASE is None
                    or not os.path.isfile("/tmp/2965decoded/main2965.py"),
                    reason="真基座/2965 缓存不在场（集成面跳过）")
def test_build_integration_real_base(tmp_path):
    """真 r34a+真 2965 缓存：仅改 1 构建（轻量冒烟，全量走 S3）。"""
    summary = B.build_r35({}, _REAL_BASE, str(tmp_path / "real"))
    assert summary["ok"] and summary["last_callable"] == "agent"
    assert summary["diff_attribution"]["hr_tail_append(_HR group-feeding, "
                                       "_LEDGER excluded)"] == 1
