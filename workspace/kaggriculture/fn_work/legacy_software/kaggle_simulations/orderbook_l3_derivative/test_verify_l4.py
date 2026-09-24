"""test_verify_l4：门④形态扩展矩阵 + R13 四门编排 fail-closed 矩阵。

不真跑全量（四门真跑=对局+lineage+重演+发射引擎面，留给 verify 编排正式
跑批）：
① 门④形态扩展——gate_launch_l3._l3_truncation_form 直测（L1 严格口径红、
   L3 扩展集绿）+ 经 _extended_form 换装驱动 L1 门 _truncation_only_diff
   （monkeypatch 装载器/verbatim 路径，合成 719-obs 序列）：减量对绿/整单
   消失+SELL 变化绿/空槽归一步绿（S6 伪差异形态）/步界 570<576 红/净增单与
   非 market 槽位漂移红；run 的换装-还原接线（形态判定+layer_s_block
   _CXS_FROM 步界进程内参数化 576/还原，monkeypatch L1 门 run 为探针）。
② 编排矩阵——verify_l13_gates 四门全 monkeypatch 假件：全绿→overall 真；
   任一门红→overall 假但四门全跑不短路；任一门抛异常→executed=False 门红
   其余门照跑；门② evidence 落点改指本包（复用不覆写 L1 包真台账）且跑后
   还原；mode 从 build_manifest.json 读取（缺失→None）；CLI 参数解析与退出
   码；verify_summary.json 结构（环境戳+三 main sha+mode+evidence 五件清单）。"""

import hashlib
import json
import os
import platform
import re

import pytest

import gate_launch_l3                    # noqa: E402  (自带 L1_DIR sys.path 自举)
import gate_launch_fourgate_l1 as _l1g   # noqa: E402
import verify_l13_gates as vlg           # noqa: E402

# ---------------------------------------------------------------------------
# ① 门④形态扩展矩阵
# ---------------------------------------------------------------------------
def _norm(a):
    return json.dumps(a, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def test_l3_form_extends_l1_strict_form():
    # L1 严格口径：减量对=红（整单消失保序子序列判据不认改量单）；
    # L3 扩展集：同品项 disappear(8)≥appear(3) 同步 → 绿。
    base = {"market": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 8]]}
    cand = {"market": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 3]]}
    assert _l1g._seed_drop_form(base, cand, _norm)[0] is False
    ok, detail = gate_launch_l3._l3_truncation_form(base, cand, _norm)
    assert ok is True and "CARROT 8->3" in detail

    # 直测扩展集矩阵：整单消失绿 / SELL 变化绿 / 减量对+SELL 同步绿；
    # 净增单红 / 跨品项顶替红 / 非 market 槽位漂移红 / 槽位重排红 /
    # 非 BUY_SEED/SELL 订单差异红 / 键集差红 / action 非 dict 红。
    assert gate_launch_l3._l3_truncation_form(
        {"market": [["BUY_SEED", "WHEAT", 2]]},
        {"market": []}, _norm) == (True, "BUY_SEED 整单消失 WHEATx2")
    ok, detail = gate_launch_l3._l3_truncation_form(
        {"market": [["SELL", "CARROT", 5]]},
        {"market": [["SELL", "CARROT", 4]]}, _norm)
    assert ok is True and "SELL 变化" in detail
    ok, detail = gate_launch_l3._l3_truncation_form(
        {"market": [["BUY_SEED", "CARROT", 8], ["SELL", "CARROT", 5]]},
        {"market": [["BUY_SEED", "CARROT", 1], ["SELL", "CARROT", 4]]}, _norm)
    assert ok is True and "CARROT 8->1" in detail and "SELL 变化" in detail
    # 净增单（出现 8 > 消失 3）→ 红
    ok, detail = gate_launch_l3._l3_truncation_form(
        {"market": [["BUY_SEED", "CARROT", 3]]},
        {"market": [["BUY_SEED", "CARROT", 8]]}, _norm)
    assert ok is False and "净增单" in detail
    # 跨品项顶替（CARROT 消失/WHEAT 出现）→ 红
    assert gate_launch_l3._l3_truncation_form(
        {"market": [["BUY_SEED", "CARROT", 8]]},
        {"market": [["BUY_SEED", "WHEAT", 3]]}, _norm)[0] is False
    # 非 market 槽位漂移（farmer 单位动作）→ 红
    assert gate_launch_l3._l3_truncation_form(
        {"market": [], "farmer": ["PASS"]},
        {"market": [], "farmer": ["PLANT", "CARROT"]}, _norm)[0] is False
    # 槽位重排（多重集同而序变）→ 红（fail-closed 不放过不可归因差）
    assert gate_launch_l3._l3_truncation_form(
        {"market": [["SELL", "WHEAT", 1], ["BUY_SEED", "CARROT", 2]]},
        {"market": [["BUY_SEED", "CARROT", 2], ["SELL", "WHEAT", 1]]},
        _norm)[0] is False
    # 非 BUY_SEED/SELL 订单差异（HIRE）→ 红
    assert gate_launch_l3._l3_truncation_form(
        {"market": [["HIRE", "x"]]}, {"market": []}, _norm)[0] is False
    # 键集差 / action 非 dict → 红
    assert gate_launch_l3._l3_truncation_form(
        {"market": []}, {"hands": []}, _norm)[0] is False
    assert gate_launch_l3._l3_truncation_form(
        [], {"market": []}, _norm)[0] is False


def test_l3_form_empty_slot_normalization():
    # 空槽归一（R13 修订一轮）：[]/None 占位数量差=伪差异 → 归一后恒等绿；
    # 剔空槽后实质差异照常分类；非空 len<3 畸形单仍红（fail-closed 不变）。
    ok, detail = gate_launch_l3._l3_truncation_form(
        {"market": [["SELL", "CARROT", 1], [], []]},
        {"market": [["SELL", "CARROT", 1], [], [], []]}, _norm)
    assert ok is True and "空槽" in detail
    # None 与 [] 跨形占位
    assert gate_launch_l3._l3_truncation_form(
        {"market": [["BUY_SEED", "CARROT", 2], None]},
        {"market": [["BUY_SEED", "CARROT", 2], []]}, _norm)[0] is True
    # 空槽剔除后实质差异（减量对）照常判绿并携带形态摘要
    ok, detail = gate_launch_l3._l3_truncation_form(
        {"market": [["BUY_SEED", "CARROT", 8], []]},
        {"market": [["BUY_SEED", "CARROT", 3], []]}, _norm)
    assert ok is True and "CARROT 8->3" in detail
    # 非空 len<3 畸形单不是空槽 → 红（other 卷不对称 / 结构异常）
    for malformed in (["BUY_SEED"], ["BUY_SEED", "CARROT"]):
        assert gate_launch_l3._l3_truncation_form(
            {"market": [malformed]}, {"market": []}, _norm)[0] is False
    assert gate_launch_l3._l3_truncation_form(
        {"market": [["BUY_SEED", "CARROT", "x"]]},
        {"market": []}, _norm)[0] is False


class _FakeCheck:
    """L1 门 _truncation_only_diff 的 check 假件（norm_action 同源口径）。"""

    DERIV_MAIN = "/fake/l3pkg/main.py"

    @staticmethod
    def norm_action(a):
        return _norm(a)


def _run_truncation(monkeypatch, base_by_step, cand_by_step):
    """合成 719-obs 序列驱动 L1 门 _truncation_only_diff（L3 扩展形态已换装）。

    base/cand 按步取动作（obs 序列 steps 0..718，含键集 {"step","market"}）；
    装载器与 verbatim 路径均 monkeypatch 为假件（不发引擎）。"""
    def fake_load(path):
        if path == _FakeCheck.DERIV_MAIN:
            def _cxs_agent(obs):
                return cand_by_step[obs.step]
            return _cxs_agent

        def _cxd_agent(obs):
            return base_by_step[obs.step]
        return _cxd_agent

    monkeypatch.setattr(_l1g, "_load_last_callable", fake_load)
    monkeypatch.setattr(_l1g, "VERBATIM_MAIN", "/fake/verbatim/main.py")
    obs_series = [{"step": t, "market": []} for t in range(719)]
    with gate_launch_l3._extended_form():
        return _l1g._truncation_only_diff(_FakeCheck(), obs_series)


def test_truncation_diff_reduce_pair_green(monkeypatch):
    # 减量对（步 700，CARROT 8→3）绿：ok 真、唯一差异步、明细带减量对形态。
    base = {t: {"market": []} for t in range(719)}
    cand = {t: dict(base[t]) for t in range(719)}
    base[700] = {"market": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 8]]}
    cand[700] = {"market": [["SELL", "WHEAT", 2], ["BUY_SEED", "CARROT", 3]]}
    got = _run_truncation(monkeypatch, base, cand)
    assert got["ok"] is True
    assert got["n_divergent"] == 1 and got["divergent_steps"] == [700]
    assert got["min_divergent_step"] == 700
    assert got["form_violations"] == []
    assert "CARROT 8->3" in got["dropped_detail"][0]["form"]


def test_truncation_diff_whole_disappear_and_sell_change_green(monkeypatch):
    # 整单消失 + SELL 变化同局绿（步 576 恰在界内：≥576 含端=day24 包络界）。
    base = {t: {"market": []} for t in range(719)}
    cand = {t: dict(base[t]) for t in range(719)}
    base[576] = {"market": [["BUY_SEED", "WHEAT", 2], ["SELL", "CARROT", 5]]}
    cand[576] = {"market": [["SELL", "CARROT", 4]]}
    got = _run_truncation(monkeypatch, base, cand)
    assert got["ok"] is True
    assert got["divergent_steps"] == [576]
    assert got["all_divergent_steps_ge_threshold"] is True
    assert got["threshold"] == 576                      # day24 包络（进程内参数化）
    assert got["dropped_detail"][0]["form"].startswith("BUY_SEED 整单消失")


def test_truncation_diff_empty_slot_only_step_green(monkeypatch):
    # 空槽归一接线：纯空槽数量差步（S6 伪差异形态）→ 步计入 divergent 但
    # 形态绿（归一后恒等）、零 form_violations。
    base = {t: {"market": []} for t in range(719)}
    cand = {t: dict(base[t]) for t in range(719)}
    base[670] = {"market": [["SELL", "CARROT", 1], [], []]}
    cand[670] = {"market": [["SELL", "CARROT", 1], [], [], []]}
    got = _run_truncation(monkeypatch, base, cand)
    assert got["ok"] is True
    assert got["divergent_steps"] == [670]
    assert got["form_violations"] == []
    assert "空槽" in got["dropped_detail"][0]["form"]


def test_truncation_diff_step_boundary_red(monkeypatch):
    # 步界红：差异步 570 < 576 → ok 假（all_divergent_steps_ge_threshold 假；
    # 形态本身合法——红在步界面非形态面）。
    base = {t: {"market": []} for t in range(719)}
    cand = {t: dict(base[t]) for t in range(719)}
    base[570] = {"market": [["BUY_SEED", "CARROT", 8]]}
    cand[570] = {"market": [["BUY_SEED", "CARROT", 3]]}
    got = _run_truncation(monkeypatch, base, cand)
    assert got["ok"] is False
    assert got["min_divergent_step"] == 570
    assert got["all_divergent_steps_ge_threshold"] is False
    assert got["form_violations"] == []               # 形态面无 violation


@pytest.mark.parametrize("base_step,cand_step", [
    # 异常形红①：净增单（出现 8 > 消失 3，步 700 界内）。
    ({700: [["BUY_SEED", "CARROT", 3]]}, {700: [["BUY_SEED", "CARROT", 8]]}),
    # 异常形红②：非 market 槽位漂移（farmer 单位动作变化，步 700 界内）。
    ({700: []}, {700: []}),
])
def test_truncation_diff_abnormal_form_red(base_step, cand_step, monkeypatch):
    base = {t: {"market": []} for t in range(719)}
    cand = {t: dict(base[t]) for t in range(719)}
    for step, market in base_step.items():
        base[step] = {"market": market}
    for step, market in cand_step.items():
        cand[step] = {"market": market}
    if base_step == {700: []}:                        # ② 非 market 槽位注入
        base[700] = {"market": [], "farmer": ["PASS"]}
        cand[700] = {"market": [], "farmer": ["PLANT", "CARROT"]}
    got = _run_truncation(monkeypatch, base, cand)
    assert got["ok"] is False
    assert got["form_violations"] and got["form_violations"][0]["step"] == 700


def test_launch_run_installs_and_restores_form(tmp_path, monkeypatch):
    # run 接线：调用期间 L1 门模块形态判定已换为 L3 扩展件（进程内），且
    # layer_s_block._CXS_FROM 参数化改指 576（day24 包络）；返回后原样还原；
    # 返回契约沿 L1 门+form_extension 摘要（evidence 增记面不触假件
    # evidence_path=None 的路径分支）。
    import layer_s_block
    seen = {}
    original = _l1g._seed_drop_form
    original_from = layer_s_block._CXS_FROM
    payload = {"gates": {"load": True, "full_episodes": True,
                         "determinism": True, "package": True},
               "truncation_only_diff": {"ok": True,
                                        "divergent_steps": [700]},
               "passed": True, "evidence_path": None}

    def probe_run(pkg_path=None, evidence_path=None):
        seen["form_is_l3"] = (_l1g._seed_drop_form
                              is gate_launch_l3._l3_truncation_form)
        seen["cxs_from"] = layer_s_block._CXS_FROM
        seen["evidence_path"] = evidence_path
        return dict(payload)

    monkeypatch.setattr(_l1g, "run", probe_run)
    result = gate_launch_l3.run(str(tmp_path))
    assert seen["form_is_l3"] is True
    assert seen["cxs_from"] == 576                     # 步界进程内参数化生效
    assert _l1g._seed_drop_form is original            # try/finally 还原
    assert layer_s_block._CXS_FROM == original_from    # L1 原值还原（648）
    assert result["passed"] is True
    assert result["gates"] == payload["gates"]
    ext = result["form_extension"]
    assert ext["step_boundary"]["threshold"] == 576
    assert set(ext["kinds"]) == {"buy_seed_whole_disappear",
                                 "buy_seed_reduce_pair", "sell_order_change"}
    assert ext["empty_slot_normalization"]["applied"] is True


def test_launch_run_augments_evidence_protocol(tmp_path, monkeypatch):
    # evidence 增记面：L1 门真写 evidence 后 run 增记 l3_form_extension 并升
    # 协议 orderbook-l3-launch-fourgate/1.1（只增键不删四门字段）。
    ev = tmp_path / "launch_check_evidence.json"
    ev.write_text(json.dumps({"protocol": "orderbook-l1-launch-fourgate/1.0",
                              "gates": {"load": True}}), encoding="utf-8")
    monkeypatch.setattr(_l1g, "run", lambda pkg_path=None, evidence_path=None: {
        "gates": {"load": True}, "truncation_only_diff": {"ok": True,
                                                           "divergent_steps": []},
        "passed": True, "evidence_path": str(ev)})
    result = gate_launch_l3.run(str(tmp_path))
    with open(ev, encoding="utf-8") as fh:
        evidence = json.load(fh)
    assert evidence["protocol"] == "orderbook-l3-launch-fourgate/1.1"
    assert evidence["gates"] == {"load": True}        # 原字段不删改
    assert evidence["l3_form_extension"]["step_boundary"]["threshold"] == 576
    assert result["form_extension"]["kinds"] == evidence[
        "l3_form_extension"]["kinds"]


# ---------------------------------------------------------------------------
# ② 编排矩阵（四门全假件）
# ---------------------------------------------------------------------------
_CONTRACT_KEYS = {"overall", "h2h", "lineage", "equivalence", "launch",
                  "evidence_dir", "started", "finished"}
_GATE_ORDER = ["h2h", "lineage", "equivalence", "launch"]

# 假件 payload：只携带编排要摘取的裁决面字段（per_game 等重台账本就不进 summary）。
_H2H_PAYLOAD = {"n": 16, "wins": 10, "rate": 0.625, "passed": True,
                "ref_face": {"n": 8, "wins": 5, "losses": 3, "ties": 0,
                             "rate": 0.625, "gating": False,
                             "evidence_path": "/fake/h2h_ref_evidence.json"},
                "evidence_path": "/fake/h2h_evidence.json"}
_LINEAGE_PAYLOAD = {
    "per_opponent": {
        "v48-pure": {"n": 8, "wins": 5, "losses": 0, "ties": 3,
                     "all_done": True, "per_game": []},
        "v4b": {"n": 8, "wins": 6, "losses": 0, "ties": 2,
                "all_done": True, "per_game": []},
        "hybrid-v2": {"n": 8, "wins": 4, "losses": 0, "ties": 4,
                      "all_done": True, "per_game": []},
    },
    "evidence_path": "/fake/lineage_evidence.json",
}
_EQUIV_PAYLOAD = {"form_face": {"ok": True, "appear_total": 1},
                  "result_face": {"ok": True, "dead_seeds_total_value": 120,
                                  "starve_free": True},
                  "subset": True, "cases": True, "n_errors": 0,
                  "evidence_path": "/fake/equivalence_evidence.json"}
_LAUNCH_PAYLOAD = {
    "gates": {"load": True, "full_episodes": True,
              "determinism": True, "package": True},
    "truncation_only_diff": {"ok": True, "divergent_steps": [576, 700]},
    "form_extension": {"kinds": ["buy_seed_whole_disappear",
                                 "buy_seed_reduce_pair", "sell_order_change"],
                       "step_boundary": {"threshold": 576}},
    "evidence_path": "/fake/launch_check_evidence.json",
}
_PAYLOADS = {"h2h": _H2H_PAYLOAD, "lineage": _LINEAGE_PAYLOAD,
             "equivalence": _EQUIV_PAYLOAD, "launch": _LAUNCH_PAYLOAD}
_GATE_MODULES = {"h2h": vlg.gate_h2h_vs_l1,
                 "lineage": vlg.gate_lineage_strength,
                 "equivalence": vlg.gate_equivalence_l3,
                 "launch": vlg.gate_launch_l3}


@pytest.fixture
def pkg(tmp_path):
    """临时包（gate 门均为假件，main.py/build_manifest.json 只需存在）。"""
    root = tmp_path / "orderbook_l3_candidate"
    root.mkdir(parents=True)
    (root / "main.py").write_text("def _cxs_agent(obs):\n    return {}\n",
                                  encoding="utf-8")
    (root / "build_manifest.json").write_text(
        json.dumps({"schema": "orderbook_l3_derivative_manifest/1.0",
                    "mode": "fine"}), encoding="utf-8")
    return root


def _install_fakes(monkeypatch, outcomes=None, calls=None):
    """四门全装假件。outcomes：{门名: True/False/异常实例}（异常即抛），缺省全
    绿；calls：列表，按完成序记录 (门名, args, kwargs)。"""
    outcomes = dict(outcomes or {})

    def _make(label):
        def run(*args, **kwargs):
            if calls is not None:
                calls.append((label, args, kwargs))
            outcome = outcomes.get(label, True)
            if isinstance(outcome, BaseException):
                raise outcome
            payload = dict(_PAYLOADS[label])
            if outcome is False:                      # 红门时裁决面同红
                if label == "lineage":
                    payload["per_opponent"] = {
                        name: dict(summ, losses=1)
                        for name, summ in payload["per_opponent"].items()}
                if label == "equivalence":
                    payload["form_face"] = {"ok": False, "appear_total": 3}
                    payload["result_face"] = {
                        "ok": False, "dead_seeds_total_value": 1000,
                        "starve_free": False}
            return dict(payload, passed=bool(outcome))

        return run

    for label, module in _GATE_MODULES.items():
        monkeypatch.setattr(module, "run", _make(label))


def test_verify_l3_orchestration(pkg, monkeypatch):
    # 编排矩阵①：全绿→overall 真、四门 executed、跑序=门序全跑不短路。
    calls = []
    _install_fakes(monkeypatch, None, calls)
    result = vlg.verify(str(pkg))
    assert set(result) == _CONTRACT_KEYS
    assert result["overall"] is True
    assert [c[0] for c in calls] == _GATE_ORDER       # 四门全跑
    for gate in _GATE_ORDER:
        entry = result[gate]
        assert entry["passed"] is True and entry["executed"] is True
        assert entry["error"] is None and entry["wall_s"] >= 0
    assert result["h2h"]["ref_face"]["gating"] is False
    assert result["h2h"]["rate"] == 0.625
    assert set(result["lineage"]["per_opponent"]) == {
        "v48-pure", "v4b", "hybrid-v2"}
    assert result["equivalence"]["form_face"] is True
    assert result["equivalence"]["dead_seeds_total_value"] == 120
    assert result["equivalence"]["starve_free"] is True
    assert result["launch"]["truncation_only_diff"]["n_divergent"] == 2
    assert result["launch"]["form_extension"]["step_boundary"]["threshold"] == 576
    assert result["evidence_dir"] == str(pkg / "evidence")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
                        result["started"])
    assert result["finished"] >= result["started"]

    # 编排矩阵②：任一门红→overall 假但四门照跑（fail-closed 不短路）。
    for broken in _GATE_ORDER:
        calls = []
        _install_fakes(monkeypatch, {broken: False}, calls)
        red = vlg.verify(str(pkg))
        assert red["overall"] is False
        assert red[broken]["passed"] is False and red[broken]["executed"] is True
        assert [c[0] for c in calls] == _GATE_ORDER   # 红门不拦其余门

    # 编排矩阵③：任一门抛异常→executed=False 门红整体红，其余门照跑
    # （异常门的调用也已尝试并记账，四门调用序完整）。
    calls = []
    _install_fakes(monkeypatch, {"launch": RuntimeError("boom-launch")}, calls)
    exc = vlg.verify(str(pkg))
    assert exc["overall"] is False
    assert exc["launch"]["executed"] is False
    assert exc["launch"]["passed"] is False
    assert "RuntimeError: boom-launch" in exc["launch"]["error"]
    assert [c[0] for c in calls] == _GATE_ORDER
    for gate in ("h2h", "lineage", "equivalence"):
        assert exc[gate]["executed"] is True


def test_verify_gate_arguments_passed_through(pkg, monkeypatch):
    # 四门实参：l3 main=<pkg>/main.py、L1/verbatim 相对推导、门② 8 局缺省、
    # 门③/④ evidence 落 <pkg>/evidence/ 五件名。
    calls = []
    _install_fakes(monkeypatch, None, calls)
    epdir = pkg.parent / "replays"
    epdir.mkdir()
    vlg.verify(str(pkg), str(epdir))
    by_call = {c[0]: c for c in calls}
    l3_main = str(pkg / "main.py")
    h2h_args, h2h_kwargs = by_call["h2h"][1:3]
    assert h2h_args == (l3_main, vlg.L1_MAIN, vlg.VERBATIM_MAIN)
    assert h2h_kwargs == {"evidence_path": str(
        pkg / "evidence" / "h2h_evidence.json")}
    lin_args, lin_kwargs = by_call["lineage"][1:3]
    assert lin_args == (l3_main, vlg.OPPONENTS)
    assert lin_kwargs == {"per_opponent_n": 8}
    eq_args, eq_kwargs = by_call["equivalence"][1:3]
    assert eq_args == (str(epdir), l3_main, vlg.L1_MAIN, vlg.VERBATIM_MAIN)
    assert eq_kwargs == {"evidence_path": str(
        pkg / "evidence" / "equivalence_evidence.json")}
    launch_args, launch_kwargs = by_call["launch"][1:3]
    assert launch_args == (str(pkg),)
    assert launch_kwargs == {"evidence_path": str(
        pkg / "evidence" / "launch_check_evidence.json")}


def test_verify_l3_orchestration_lineage_redirect(pkg, monkeypatch):
    # 门②复用证据纪律：L1 门②落点是 L1 包内模块常量——编排须改指本包
    # evidence/lineage_evidence.json（跑后还原模块常量），防覆写 L1 真台账。
    gs = vlg.gate_lineage_strength
    original_dir, original_path = gs.EVIDENCE_DIR, gs.EVIDENCE_PATH

    def probe_run(*args, **kwargs):
        os.makedirs(gs.EVIDENCE_DIR, exist_ok=True)
        with open(gs.EVIDENCE_PATH, "w", encoding="utf-8") as fh:
            json.dump({"note": "redirect probe"}, fh)
        return dict(_LINEAGE_PAYLOAD, passed=True,
                    evidence_path=gs.EVIDENCE_PATH)

    _install_fakes(monkeypatch)
    monkeypatch.setattr(gs, "run", probe_run)
    result = vlg.verify(str(pkg))
    assert result["overall"] is True
    probe = pkg / "evidence" / "lineage_evidence.json"
    assert probe.is_file()                            # 落本包 evidence/
    assert json.loads(probe.read_text(encoding="utf-8"))["note"] == \
        "redirect probe"
    assert result["lineage"]["evidence_path"] == str(probe)
    assert (gs.EVIDENCE_DIR, gs.EVIDENCE_PATH) == (original_dir, original_path)


def test_verify_summary_structure_and_mode(pkg, monkeypatch):
    # verify_summary.json：契约键+协议+mode（build_manifest 读取）+环境戳+
    # 三 main sha256+evidence 五件清单；红门留痕。
    _install_fakes(monkeypatch, {"equivalence": False})   # 红门留痕
    result = vlg.verify(str(pkg))
    path = pkg / "evidence" / "verify_summary.json"
    assert path.is_file()
    summary = json.loads(path.read_text(encoding="utf-8"))
    assert _CONTRACT_KEYS <= set(summary)
    assert set(summary) == _CONTRACT_KEYS | {
        "protocol", "pkg_path", "episodes_dir", "mode", "gates_passed",
        "evidence_files", "environment", "mains"}
    assert summary["protocol"] == "verify-l13-gates/1.0"
    assert summary["pkg_path"] == str(pkg)
    assert summary["episodes_dir"] == vlg.EPISODES_DIR_DEFAULT
    assert summary["mode"] == "fine"                  # build_manifest.json 读取
    assert summary["overall"] is False and result["overall"] is False
    assert summary["gates_passed"] == {"h2h": True, "lineage": True,
                                       "equivalence": False, "launch": True}
    env = summary["environment"]
    assert env["python_version"] == platform.python_version()
    assert env["python_full"] and env["platform"]
    assert summary["started"] == result["started"]
    assert summary["finished"] == result["finished"]
    mains = summary["mains"]
    assert mains["l3_main"] == str(pkg / "main.py")
    assert mains["l1_main"] == vlg.L1_MAIN
    assert mains["verbatim_main"] == vlg.VERBATIM_MAIN
    assert mains["sha256"]["l3_main"] == hashlib.sha256(
        (pkg / "main.py").read_bytes()).hexdigest()
    assert mains["sha256"]["l1_main"] == hashlib.sha256(
        open(vlg.L1_MAIN, "rb").read()).hexdigest()
    assert mains["sha256"]["verbatim_main"] == hashlib.sha256(
        open(vlg.VERBATIM_MAIN, "rb").read()).hexdigest()
    assert summary["evidence_files"] == {
        "h2h": str(pkg / "evidence" / "h2h_evidence.json"),
        "h2h_ref": str(pkg / "evidence" / "h2h_ref_evidence.json"),
        "lineage": str(pkg / "evidence" / "lineage_evidence.json"),
        "equivalence": str(pkg / "evidence" / "equivalence_evidence.json"),
        "launch": str(pkg / "evidence" / "launch_check_evidence.json"),
    }
    for gate in _GATE_ORDER:
        assert summary[gate]["executed"] is True
        assert summary[gate]["error"] is None


def test_verify_mode_reading_variants(tmp_path, monkeypatch):
    # mode 读取三级回退：顶层 mode → change_set.mode → candidate.mode（dict）；
    # 缺失/畸形 manifest → None（戳面不拦裁决）。
    _install_fakes(monkeypatch)

    def _pkg_with(manifest_text):
        root = tmp_path / f"pkg_{abs(hash(manifest_text)) % 10**8}"
        root.mkdir()
        (root / "main.py").write_text("def _cxs_agent(obs):\n"
                                      "    return {}\n", encoding="utf-8")
        if manifest_text is not None:
            (root / "build_manifest.json").write_text(manifest_text,
                                                      encoding="utf-8")
        return root

    for manifest, want in (
            (json.dumps({"mode": "coarse"}), "coarse"),
            (json.dumps({"change_set": {"mode": "fine"}}), "fine"),
            (json.dumps({"candidate": {"mode": "coarse"}}), "coarse"),
            (json.dumps({"candidate": "some string"}), None),
            (json.dumps({"main_sha256": "x"}), None),
            ("{not json", None),
            (None, None)):
        root = _pkg_with(manifest)
        result = vlg.verify(str(root))
        summary = json.loads((root / "evidence" / "verify_summary.json")
                             .read_text(encoding="utf-8"))
        assert summary["mode"] == want, (manifest, want)
        assert result["overall"] is True               # mode 面不拦裁决


def test_verify_pkg_default(monkeypatch, tmp_path):
    # pkg_path 缺省=HERE（本编排所在包）；episodes 缺省=相对推导语料目录。
    p = tmp_path / "self_pkg"
    p.mkdir()
    (p / "main.py").write_text("def _cxs_agent(obs):\n    return {}\n",
                               encoding="utf-8")
    calls = []
    _install_fakes(monkeypatch, None, calls)
    monkeypatch.setattr(vlg, "HERE", str(p))
    result = vlg.verify()
    assert result["evidence_dir"] == str(p / "evidence")
    eq_args = [c for c in calls if c[0] == "equivalence"]
    assert all(c[1][0] == vlg.EPISODES_DIR_DEFAULT for c in eq_args)
    assert os.path.isdir(vlg.EPISODES_DIR_DEFAULT)     # 语料真实在场
    assert (p / "evidence" / "verify_summary.json").is_file()


def test_cli_usage_errors(capsys):
    assert vlg.main([]) == 2                           # 缺 pkg_dir
    assert vlg.main(["a", "b", "c"]) == 2              # 参数过多
    err = capsys.readouterr().err
    assert vlg.USAGE in err


def test_cli_exit_code_follows_overall(pkg, monkeypatch):
    _install_fakes(monkeypatch)
    assert vlg.main([str(pkg)]) == 0                   # 四门全绿
    _install_fakes(monkeypatch, {"equivalence": False})
    assert vlg.main([str(pkg)]) == 1                   # 任一门红
    _install_fakes(monkeypatch, {"h2h": ValueError("no engine")})
    assert vlg.main([str(pkg)]) == 1                   # 门不可执行=红


def test_cli_passes_args_through(pkg, tmp_path, monkeypatch):
    epdir = tmp_path / "replays"
    epdir.mkdir()
    calls = []
    _install_fakes(monkeypatch, None, calls)
    assert vlg.main([str(pkg), str(epdir)]) == 0
    by_call = {c[0]: c for c in calls}
    assert by_call["equivalence"][1][0] == str(epdir)
    assert by_call["launch"][1][0] == str(pkg)
