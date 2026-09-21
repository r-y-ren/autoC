# ===========================================================================
# test_decide_macro_mode.py —— 迁移件真实测试（B12）
# ---------------------------------------------------------------------------
# 覆盖（fn_docs/responsibility.md run_submission_agent · decide_macro_mode）：
#   ① 关键符号在场（20 件，含阶段寄存器/容量门/轮作规划全家）；
#   ② R10/R20 登记面——R20 三处注释漂移修正后正文与旧源在"剥 docstring 的
#      AST"上完全同构（机械证明"行为不变仅注释修正"）；漂移旧文案零残留；
#      VOLUME_ANTICIPATED_ENTRY 两侧同值 True；stage_* 四键保留轴在旗关恒回
#      STAGE_* 冻结值、旗开可被计划覆盖（轴未被丢）；
#   ③ 纯函数等值抽查——_wheat_cap/_herd_target/_stage_of/_decide_mode/
#      _field_alloc/_macro_plan 同输入下旧新 exec 输出 repr 逐字节一致；
#   ④ 文件头迁移登记（源路径+源 sha256+剥离清单=无+保留轴显式化注记）。
# 装置：种子 imports + 旧树 constants/observer/market 为共同依赖基座（隔离
#   本件 diff），再分别 exec 旧 strategy.py / 新 decide_macro_mode.py。
# ===========================================================================

import ast
import hashlib
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

_ROOTS = discover_campaign_roots(Path(__file__))
OLD_SRC = _ROOTS["software_root"] / "kaggle_simulations" / "agent" / "src"
NEW_FILE = Path(__file__).resolve().parent.parent.parent / "src" / \
    "run_submission_agent" / "decide_macro_mode.py"
OLD_FILE = OLD_SRC / "strategy.py"
_SEED_IMPORTS = "import copy\nimport math\nimport json\nimport hashlib\n"


def _exec_into(ns, path):
    exec(compile(Path(path).read_text(encoding="utf-8"), str(path), "exec"), ns)


def _namespace(use_migrated, **patches):
    ns = {}
    exec(_SEED_IMPORTS, ns)
    for dep in ("constants", "observer", "market"):
        _exec_into(ns, OLD_SRC / (dep + ".py"))
    _exec_into(ns, NEW_FILE if use_migrated else OLD_FILE)
    ns.update(patches)
    return ns


FARM = {
    "unlocked_quadrants": ["NW"], "money": 1234.5, "farmer": [1, 1],
    "tiles": [
        [None,
         {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 9,
          "yield_units": 2, "max_lifespan_step": 300},
         {"kind": "WEED"}],
        [{"animal": "COW", "placed_day": 2, "yield_units": 3,
          "fed_today": True},
         None,
         {"kind": "PLANT", "crop": "WHEAT", "planted_day": 5,
          "yield_units": 1}],
        [None, None,
         {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 11,
          "consecutive_unwatered": 1, "yield_units": 0}],
    ],
    "hands": [[1, 1], [2, 2]],
}
PRICES = {"STRAWBERRY": 120, "WHEAT": 25, "MILK": 160, "WOOL": 200,
          "MELON": 250, "FERTILIZER": 100}
OBS = {
    "player": 0, "day": 8, "hour": 5, "step": 200,
    "market": {"prices": PRICES},
    "town": {"unlocked_shops": ["SMOOTHIE_SHOP", "FARMERS_MARKET"]},
    "farms": [FARM, dict(FARM, money=800)],
}


# --------------------------------------------------------------------------
# ① 关键符号在场
# --------------------------------------------------------------------------

def test_key_symbols_present_after_exec():
    ns = _namespace(use_migrated=True)
    symbols = [
        "_wheat_farm_plan", "_wheat_farm_entry_ok", "_wheat_cap",
        "_herd_target", "_hands_target", "_crew_target", "_animal_pace",
        "_npv_herd_decision", "_plan_rollout", "_decide_mode", "_macro_plan",
        "_stage_of", "_classify_opponent_opening", "_capacity_gate",
        "_curve_gate_ok", "_cash_gate_ok", "_d6_checkpoint", "_stage_plan",
        "_fuse_check", "_field_alloc", "_PLAN_MEM", "_STAGE_MEM",
    ]
    missing = [s for s in symbols if s not in ns]
    assert not missing, f"迁移件 exec 后缺失符号: {missing}"


# --------------------------------------------------------------------------
# ② R20 注释漂移修正的同构性与 R10 保留轴
# --------------------------------------------------------------------------

def _ast_sans_docstrings(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:]
    return ast.dump(tree)


def test_ast_identical_modulo_docstrings():
    # 三处修正全部是注释/docstring：剥掉 docstring 后旧新 AST 完全同构。
    assert (_ast_sans_docstrings(OLD_FILE) == _ast_sans_docstrings(NEW_FILE))


def test_r20_drift_texts_gone_and_flag_true():
    body = NEW_FILE.read_text(encoding="utf-8").split('"""', 2)[2]
    assert "DISABLED by the" not in body
    assert "VOLUME_ANTICIPATED_ENTRY = False" not in body
    assert "已被 r5-P5 消融禁用" not in body
    old, new = _namespace(False), _namespace(True)
    assert old["VOLUME_ANTICIPATED_ENTRY"] is True
    assert new["VOLUME_ANTICIPATED_ENTRY"] is True


def test_stage_axes_retained_and_knob_wired():
    # R10 保留轴：stage_* 四键显式保留——旗关恒回 STAGE_* 冻结值（6/14/21/27），
    # 旗开可被计划覆盖（发射已接线），且旧新行为一致。
    old, new = _namespace(False), _namespace(True)
    for ns in (old, new):
        stages = [ns["_stage_of"](d) for d in range(31)]
        assert stages == ["P0"] + ["P1"] * 5 + ["P2"] * 9 + ["P3"] * 7 \
            + ["P4"] * 6 + ["P5"] * 3
    enabled = {"PLANNER_ENABLED": True,
               "PLANNER_OVERRIDES": {"stage_p2_freeze": 10, "stage_p3_end": 17,
                                     "stage_p4_end": 20}}
    old_on = _namespace(False, **dict(enabled))
    new_on = _namespace(True, **dict(enabled))
    got_old = [old_on["_stage_of"](d) for d in range(31)]
    got_new = [new_on["_stage_of"](d) for d in range(31)]
    assert got_old == got_new
    assert got_new[9] == "P2" and got_new[10] == "P2"   # freeze 14→10（d≤10 皆 P2）
    assert got_new[11] == "P3"                          # p3_end 21→17
    assert got_new[19] == "P4" and got_new[21] == "P5"  # p4_end 27→20


# --------------------------------------------------------------------------
# ③ 纯函数等值抽查
# --------------------------------------------------------------------------

def test_planning_formula_family_equivalent():
    old, new = _namespace(False), _namespace(True)
    wheat = [repr(old["_wheat_cap"](d, p))
             for d in range(0, 30, 3) for p in (25, 35, 42, 50)]
    wheat_n = [repr(new["_wheat_cap"](d, p))
               for d in range(0, 30, 3) for p in (25, 35, 42, 50)]
    assert wheat == wheat_n
    herd = [repr(old["_herd_target"](d, c))
            for d in (0, 3, 6, 10, 20) for c in (4, 10, 18)]
    herd_n = [repr(new["_herd_target"](d, c))
              for d in (0, 3, 6, 10, 20) for c in (4, 10, 18)]
    assert herd == herd_n
    crew = [repr(old["_crew_target"](d, h, w, q, pl))
            for d in (2, 8, 16) for h in (0, 9, 14) for w in (0, 6) for q in (1, 3)
            for pl in (None, old["_DEFENSIVE_PLAN"], old["_VOLUME_PLAN"])]
    crew_n = [repr(new["_crew_target"](d, h, w, q, pl))
              for d in (2, 8, 16) for h in (0, 9, 14) for w in (0, 6) for q in (1, 3)
              for pl in (None, new["_DEFENSIVE_PLAN"], new["_VOLUME_PLAN"])]
    assert crew == crew_n


def test_decide_mode_and_field_alloc_equivalent():
    old, new = _namespace(False), _namespace(True)
    for day, prev in ((8, None), (12, "VOLUME_CROP"), (20, "SCALE_RANCH"),
                      (1, None)):
        assert (repr(old["_decide_mode"](OBS, day, prev))
                == repr(new["_decide_mode"](OBS, day, prev)))
    for day in (0, 10, 20, 28):
        for plan in (None, old["_DEFENSIVE_PLAN"], old["_VOLUME_PLAN"]):
            assert (repr(old["_field_alloc"](FARM, day, PRICES,
                                             plan if plan is None
                                             else dict(plan)))
                    == repr(new["_field_alloc"](FARM, day, PRICES,
                                                plan if plan is None
                                                else dict(plan))))
    # 每日缓存计划（含阶段寄存器/熔断接线）两席两日同值
    for ns_idx, ns in enumerate((old, new)):
        ns["_macro_plan"](0, OBS, 8)
    assert repr(old["_macro_plan"](1, OBS, 8)) == \
        repr(new["_macro_plan"](1, OBS, 8))


def test_rollout_evaluator_equivalent():
    old, new = _namespace(False), _namespace(True)
    scan = old["_farm_scan"](FARM)
    demand = old["_town_daily_demand"](OBS["town"]["unlocked_shops"])
    for plan in (old["_DEFENSIVE_PLAN"], old["_VOLUME_PLAN"]):
        assert (repr(old["_plan_rollout"](8, scan, plan, PRICES, demand, 120))
                == repr(new["_plan_rollout"](8, scan, plan, PRICES, demand,
                                             120)))


# --------------------------------------------------------------------------
# ④ 文件头迁移登记
# --------------------------------------------------------------------------

def test_header_docstring_registration():
    head = NEW_FILE.read_text(encoding="utf-8").split('"""')[1]
    old_sha = hashlib.sha256(OLD_FILE.read_bytes()).hexdigest()
    assert "源文件: software/kaggle_simulations/agent/src/strategy.py" in head
    assert f"源 sha256: {old_sha}" in head
    assert "剥离清单" in head and "无死码剥离项" in head
    assert "保留轴显式化注记" in head and "stage_p4_end" in head
    assert "R20 注释漂移修正（3 处" in head
