# ===========================================================================
# 【中文·模块导览】planner/twin.py —— 脱离框架的快速数字孪生引擎（Track-B P1）
# ---------------------------------------------------------------------------
# 目的：为"bot 内嵌引擎副本做整季前瞻规划"提供地基——
#   1) 从官方回放 JSON 的任意中间步重建双席完整引擎状态（含 private
#      shed/seeds/随身），绕开 kaggle_environments 框架的 env.step 慢路径
#      （框架路径 ~0.787ms/步 vs 解释器直驱 ~0.02-0.1ms/步）；
#   2) 直接驱动 vendored 场景解释器（kaggriculture.interpreter）逐步推进，
#      语义与官方框架逐步等价（core.py 中与本场景相关的簿记只涉及
#      obs0.step 自增与终局 DONE/reward，均在 step() 内镜像）。
# 引擎来源（fail-closed 指纹链）：vendored wheel
#   software/vendor/kaggle_environments-1.32.7+nodeps-py3-none-any.whl，
#   从中抽取场景两文件（kaggriculture.py/.json）到运行时缓存目录并逐一
#   校验 sha256；wheel 或任一文件指纹不符即拒绝加载。场景解释器本体零修改。
# 状态表示：纯 dict/list + 轻量属性视图（Seat/Observation/Struct），无
#   structify 全量深拷贝——这正是快路径的来源。farms/market/town 在孪生内
#   是单一共享对象（解释器每步末尾本就重新别名同步，等价框架语义）。
# 公开接口（P2 planner_offline_bench 将按"给定注入状态 + 双席策略回调"调用）：
#   load_engine()                        -> EngineBundle（interpreter + 指纹）
#   build_state_from_replay(replay, t)   重建回放第 t 步完整双席状态
#   rebuild_snapshots(replay, steps)     单次前向走子、多点快照（等价逐点重建）
#   step(state, actions_both_seats)      推进一步（原地变更，返回同 state）
#   run_to_end(state, action_source)     rollout 至终局（可迭代或回调）
#   final_money(state)                   -> [float, float] 双席资金
#   clone_state(state)                   -> 独立副本（手写快克隆，禁 deepcopy）
#   state_to_canonical(state)            -> 与回放可逐位比对的纯 JSON 投影
#   replay_canonical(replay, t)          -> 回放第 t 步的同构投影
#   states_bit_equal / first_difference  -> 规范投影逐位比对与差异定位
# 随机性：仅杂草 p=0.005/格/天与商店解锁抽取，由 env.info["seed"] 按日重播种
#   Random((seed*1000003)^day) 驱动——回放 info.seed 即真值种子（引擎事实表
#   §7），种子缺失的回放无法复现这两处随机（保真门中单列豁免）。
# 纪律：stdlib-only、确定性（无集合迭代序依赖）、不改 vendored 引擎一个字节。
# ===========================================================================

import hashlib
import importlib.util
import json
import os
import struct
import sys
import types
import zipfile

# --------------------------------------------------------------------------
# 指纹链（fail-closed）：vendored wheel 与场景两文件的 sha256。
# 建立于 2026-09-19（P1），wheel 与 site-packages 副本逐文件核对一致。
# --------------------------------------------------------------------------
WHEEL_NAME = "kaggle_environments-1.32.7+nodeps-py3-none-any.whl"
WHEEL_SHA256 = "be693e837bcb0f81bad7d6509f2737f29986fe66b12296e9990b0aa88f287465"
SCENE_PY_SHA256 = "bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e"
SCENE_JSON_SHA256 = "a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867"
_SCENE_ZIP_MEMBERS = {
    "py": "kaggle_environments/envs/kaggriculture/kaggriculture.py",
    "json": "kaggle_environments/envs/kaggriculture/kaggriculture.json",
}

_HERE = os.path.dirname(os.path.abspath(__file__))
_SOFTWARE = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
DEFAULT_WHEEL = os.path.join(_SOFTWARE, "vendor", WHEEL_NAME)
# 运行时缓存落 gitignored 的探针目录（exports/probes/* 已 gitignore）。
DEFAULT_CACHE_DIR = os.path.join(
    _SOFTWARE, "exports", "probes", "twin_fidelity", "engine_cache")


class TwinFingerprintError(RuntimeError):
    """引擎指纹校验失败（wheel/场景文件与 P1 登记值不符）——拒绝加载。"""


class Struct(dict):
    """dict+属性双视图（对齐 kaggle_environments.utils.structify.Struct 的
    读取语义；场景解释器以 get(cfg,...)/cfg.episodeSteps 两种方式读配置）。"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class Observation:
    """单席观测视图：解释器要求属性访问（obs0.farms / obs0.step ...）。"""

    __slots__ = ("farms", "market", "town", "day", "hour", "step",
                 "player", "private", "remainingOverageTime")


class Seat:
    """框架 state[i] 的最小等价物：observation/action/status/reward。"""

    __slots__ = ("observation", "action", "status", "reward")

    def __init__(self, observation, player):
        self.observation = observation
        self.action = None
        self.status = "ACTIVE"
        self.reward = None
        observation.player = player


class TwinEnv:
    """解释器所需的 env 形状：configuration（属性可读）、info（含 seed）、
    done（镜像 core.py：所有席位非 ACTIVE 即 done）、interpreter（直驱入口）。"""

    __slots__ = ("configuration", "info", "_state", "interpreter")

    def __init__(self, configuration, seed, state, interpreter):
        self.configuration = configuration
        self.info = {"seed": seed}
        self._state = state
        self.interpreter = interpreter

    @property
    def done(self):
        return all(s.status != "ACTIVE" for s in self._state.seats)


class TwinState:
    """孪生世界：seats 列表（解释器的 state 参数）+ 反向引用的 env。"""

    __slots__ = ("seats", "env")

    def __init__(self, seats, env):
        self.seats = seats
        self.env = env


class EngineBundle:
    """加载好的场景解释器 + 指纹（供保真报告登记）。"""

    __slots__ = ("interpreter", "module", "fingerprint")

    def __init__(self, interpreter, module, fingerprint):
        self.interpreter = interpreter
        self.module = module
        self.fingerprint = fingerprint


# --------------------------------------------------------------------------
# 引擎加载（vendored wheel -> 指纹校验 -> 缓存抽取 -> import）
# --------------------------------------------------------------------------
_BUNDLE = None


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _import_scene_module(py_path):
    """把场景解释器按受控模块名导入（指纹校验由调用方负责）。导入期
    `from kaggle_environments.utils import resolve_episode_seed` 的 stub
    处理与 wheel 路径一致（有真包用真包，无包临时挂最小 stub 后拆除）。"""
    mod_name = f"_kaggriculture_twin_scene_{WHEEL_SHA256[:12]}"
    added_modules = _ensure_scene_importable()
    try:
        if mod_name in sys.modules:
            return sys.modules[mod_name]
        spec = importlib.util.spec_from_file_location(mod_name, py_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
    finally:
        for key in added_modules:
            if key in sys.modules:
                del sys.modules[key]
    return sys.modules[mod_name]


def _ensure_scene_importable():
    """场景模块 import 时会 `from kaggle_environments.utils import
    resolve_episode_seed`（仅 _initialize 用，孪生重建路径不触发）。
    有真包用真包；无包则临时挂最小 stub 并在导入后拆除（不污染进程）。"""
    try:
        import kaggle_environments.utils  # noqa: F401
        return []
    except ImportError:
        pkg = types.ModuleType("kaggle_environments")
        pkg.__path__ = []
        sub = types.ModuleType("kaggle_environments.utils")

        def _resolve_episode_seed(env, *, config_key="seed", fallback=None):
            info = getattr(env, "info", None) or {}
            seed = info.get("seed")
            if seed is None and fallback is not None:
                seed = fallback()
            if seed is None:
                seed = 0
            info["seed"] = seed
            return seed

        sub.resolve_episode_seed = _resolve_episode_seed
        sys.modules["kaggle_environments"] = pkg
        sys.modules["kaggle_environments.utils"] = sub
        return ["kaggle_environments", "kaggle_environments.utils"]


def load_engine(wheel_path=None, cache_dir=None, force_reload=False):
    """加载 vendored 场景解释器（进程内缓存）。指纹不符即抛
    TwinFingerprintError——fail-closed，绝不静默降级。"""
    global _BUNDLE
    if _BUNDLE is not None and not force_reload:
        return _BUNDLE

    wheel_path = wheel_path or DEFAULT_WHEEL
    cache_dir = cache_dir or DEFAULT_CACHE_DIR
    if not os.path.isfile(wheel_path):
        raise TwinFingerprintError(f"vendored wheel 不存在: {wheel_path}")
    wheel_sha = _sha256_file(wheel_path)
    if wheel_sha != WHEEL_SHA256:
        raise TwinFingerprintError(
            f"wheel sha256 漂移: {wheel_sha} != {WHEEL_SHA256}")

    py_path = os.path.join(cache_dir, "kaggriculture.py")
    json_path = os.path.join(cache_dir, "kaggriculture.json")
    prov_path = os.path.join(cache_dir, "_provenance.json")
    need_extract = True
    if os.path.isfile(py_path) and os.path.isfile(json_path) \
            and os.path.isfile(prov_path):
        try:
            with open(prov_path, encoding="utf-8") as f:
                prov = json.load(f)
            need_extract = not (
                prov.get("wheel_sha256") == wheel_sha
                and prov.get("scene_py_sha256") == SCENE_PY_SHA256
                and prov.get("scene_json_sha256") == SCENE_JSON_SHA256
                and _sha256_file(py_path) == SCENE_PY_SHA256
                and _sha256_file(json_path) == SCENE_JSON_SHA256)
        except (OSError, ValueError):
            need_extract = True
    if need_extract:
        os.makedirs(cache_dir, exist_ok=True)
        with zipfile.ZipFile(wheel_path) as z:
            py_data = z.read(_SCENE_ZIP_MEMBERS["py"])
            json_data = z.read(_SCENE_ZIP_MEMBERS["json"])
        if hashlib.sha256(py_data).hexdigest() != SCENE_PY_SHA256 \
                or hashlib.sha256(json_data).hexdigest() != SCENE_JSON_SHA256:
            raise TwinFingerprintError(
                "wheel 内场景文件 sha256 与登记值不符（引擎被改动？）")
        with open(py_path, "wb") as f:
            f.write(py_data)
        with open(json_path, "wb") as f:
            f.write(json_data)
        with open(prov_path, "w", encoding="utf-8") as f:
            json.dump({
                "wheel": os.path.basename(wheel_path),
                "wheel_sha256": wheel_sha,
                "scene_py_sha256": SCENE_PY_SHA256,
                "scene_json_sha256": SCENE_JSON_SHA256,
                "extracted_at": "P1-2026-09-19",
            }, f, ensure_ascii=False, indent=1)

    module = _import_scene_module(py_path)

    bundle = EngineBundle(
        interpreter=module.interpreter,
        module=module,
        fingerprint={
            "wheel": os.path.basename(wheel_path),
            "wheel_sha256": wheel_sha,
            "scene_py_sha256": SCENE_PY_SHA256,
            "scene_json_sha256": SCENE_JSON_SHA256,
            "module_version": "1.32.7+nodeps",
        })
    _BUNDLE = bundle
    return bundle


def load_engine_from_scene(scene_py, scene_json, source="scene"):
    """从（提交包内置的）场景两文件直接加载解释器——零磁盘写路径。

    指纹纪律与 load_engine 相同（fail-closed）：两文件 sha256 必须逐一
    等于 P1 登记值（SCENE_PY_SHA256 / SCENE_JSON_SHA256），否则抛
    TwinFingerprintError，绝不静默降级。提交包内 vendored wheel 不存在，
    build.py 在打包期从 wheel 抽取并校验后以 planner/scene/ 成员入包，
    运行期本函数绕过抽取直接加载。"""
    global _BUNDLE
    if _BUNDLE is not None:
        return _BUNDLE
    for path in (scene_py, scene_json):
        if not os.path.isfile(path):
            raise TwinFingerprintError(f"内置场景文件缺失: {path}")
    if _sha256_file(scene_py) != SCENE_PY_SHA256 \
            or _sha256_file(scene_json) != SCENE_JSON_SHA256:
        raise TwinFingerprintError(
            "内置场景文件 sha256 与 P1 登记值不符（打包漂移？拒绝加载）")
    module = _import_scene_module(scene_py)
    bundle = EngineBundle(
        interpreter=module.interpreter,
        module=module,
        fingerprint={
            "source": source,
            "scene_py_sha256": SCENE_PY_SHA256,
            "scene_json_sha256": SCENE_JSON_SHA256,
            "module_version": "1.32.7+nodeps",
        })
    _BUNDLE = bundle
    return bundle


# --------------------------------------------------------------------------
# 状态构造 / 推进 / 克隆
# --------------------------------------------------------------------------
def _copy_tile(tile):
    if tile is None or tile == "LOCKED":
        return tile
    return dict(tile)


def _copy_farm(farm):
    return {
        "money": farm["money"],
        "tiles": [[_copy_tile(t) for t in row] for row in farm["tiles"]],
        "farmer": list(farm["farmer"]),
        "hands": [list(p) for p in farm.get("hands", [])],
        "unlocked_quadrants": list(farm["unlocked_quadrants"]),
        "hires_today": farm["hires_today"],
    }


def _copy_private(private):
    return {
        "shed": dict(private.get("shed", {})),
        "seeds": dict(private.get("seeds", {})),
        "inventories": [dict(inv) for inv in private.get("inventories", [{}])],
    }


def clone_state(state):
    """手写深克隆（P2 rollout 热路径；禁用 copy.deepcopy 的全图遍历）。
    action 只读共享（解释器从不写 action）。"""
    seats = []
    for seat in state.seats:
        obs = seat.observation
        nobs = Observation()
        nobs.farms = obs.farms if obs.player == 0 else None  # 稍后统一别名
        nobs.market = None
        nobs.town = None
        nobs.private = _copy_private(obs.private)
        nobs.day = obs.day
        nobs.hour = obs.hour
        nobs.step = obs.step
        nobs.remainingOverageTime = obs.remainingOverageTime
        nseat = Seat(nobs, obs.player)
        nseat.action = seat.action
        nseat.status = seat.status
        nseat.reward = seat.reward
        seats.append(nseat)
    obs0 = seats[0].observation
    obs0.farms = [_copy_farm(f) for f in obs0.farms]
    market = state.seats[0].observation.market
    obs0.market = {
        "inventory": dict(market["inventory"]),
        "prices": dict(market["prices"]),
    }
    if "params" in market:
        obs0.market["params"] = {
            item: dict(p) for item, p in market["params"].items()}
    obs0.town = {"unlocked_shops": list(state.seats[0].observation.town
                                        ["unlocked_shops"])}
    for i in range(1, len(seats)):
        o = seats[i].observation
        o.farms = obs0.farms
        o.market = obs0.market
        o.town = obs0.town
    env = TwinEnv(state.env.configuration, state.env.info.get("seed", 0),
                  None, state.env.interpreter)
    new_state = TwinState(seats, env)
    env._state = new_state
    return new_state


def _make_configuration(replay):
    cfg = dict(replay.get("configuration") or {})
    cfg.setdefault("episodeSteps", 720)
    return Struct(cfg)


def new_state_from_replay_head(replay, bundle=None):
    """从回放 steps[0]（框架 _initialize 之后的初态）构造孪生状态。
    farms/market/town 取 seat0 观测（框架语义的共享正本），private 逐席取。"""
    bundle = bundle or load_engine()
    steps = replay.get("steps") or []
    if not steps:
        raise ValueError("replay 无 steps")
    head = steps[0]
    obs0_raw = (head[0] or {}).get("observation") or {}
    privates, statuses = [], []
    for seat in range(len(head)):
        entry = head[seat] or {}
        obs = entry.get("observation") or {}
        privates.append(obs.get("private") or {})
        statuses.append(entry.get("status") or "ACTIVE")

    market_raw = obs0_raw.get("market") or {}
    town_raw = obs0_raw.get("town") or {}
    seats = []
    for i in range(len(head)):
        obs = Observation()
        obs.private = _copy_private(privates[i])
        obs.day = int(obs0_raw.get("day", 0) or 0)
        obs.hour = int(obs0_raw.get("hour", 0) or 0)
        obs.step = int(obs0_raw.get("step", 0) or 0) if i == 0 else None
        obs.remainingOverageTime = None
        seat = Seat(obs, i)
        seat.status = statuses[i]
        seats.append(seat)

    obs0 = seats[0].observation
    obs0.farms = [_copy_farm(f) for f in obs0_raw["farms"]]
    obs0.market = {
        "inventory": dict(market_raw.get("inventory", {})),
        "prices": dict(market_raw.get("prices", {})),
    }
    if "params" in market_raw:
        obs0.market["params"] = {
            item: dict(p) for item, p in market_raw["params"].items()}
    obs0.town = {"unlocked_shops": list(town_raw.get("unlocked_shops", []))}
    for i in range(1, len(seats)):
        o = seats[i].observation
        o.farms = obs0.farms
        o.market = obs0.market
        o.town = obs0.town
        o.day = obs0.day
        o.hour = obs0.hour

    env = TwinEnv(_make_configuration(replay),
                  (replay.get("info") or {}).get("seed", 0), None,
                  bundle.interpreter)
    state = TwinState(seats, env)
    env._state = state
    return state


# 线上 obs 视角的孪生初态合成参数（P3 runtime 用；与
# scripts/planner_flagoff_golden.synthetic_season_head 的合成季配置逐键
# 同源——episodeSteps=720=官方整季、weedSpawnChance=0.005 等引擎默认值）。
DEFAULT_TWIN_CONFIGURATION = {
    "episodeSteps": 720, "actTimeout": 1, "boardSize": 10,
    "startingMoney": 3000, "maxMarketOrdersPerTurn": 10, "turnsPerDay": 24,
    "shedCapacity": 100, "weedSpawnChance": 0.005,
    "townShopUnlockInterval": 3, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "seed": None, "farmHandCostMult": 1,
    "marketParams": {},
}


def _obs_get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def synth_opponent_private(module):
    """合成对手 private（线上不可观测席的悲观口径）：
    棚仓按产品满仓合成——对应 PessimisticFill 的登记前提"假定对手持有
    等量倾销库存"（opponents.py 模块头），风格池的 daily_sell_cap 卖出
    也由此供货；种子仓空、随身空。990/项 不可达棚仓帽（100）只约束
    DEPOSIT 不约束 SELL（引擎 _commit_unit 语义），故卖出侧永不断货。"""
    shed = {item: 990 for item in list(module.PRODUCTS) + list(module.ANIMALS)}
    return {"shed": shed, "seeds": dict.fromkeys(module.CROPS, 0),
            "inventories": [{}]}


def new_state_from_obs(obs, player=0, seed=1, bundle=None,
                       configuration=None):
    """从线上我方席观测构造孪生状态（P3 bot 内规划入口；与
    new_state_from_replay_head 平行的第二入口）。

    可见性口径（诚实声明）：
      * 公开区 farms/market/town 双席共享正本（框架语义同源）；
      * 我方 private 直取（obs.private 本席可见）；
      * 对手 private 不可观测——synth_opponent_private 的满仓合成
        （悲观压力测试口径，非估计）。
    seed：线上真种子对 agent 不可观测（info.seed 是环境侧），孪生内
    杂草/商店解锁随机按伪种子（缺省 1）确定性驱动——逐局与真值可能
    不同，但同一伪种子下规划器自身确定。"""
    bundle = bundle or load_engine()
    module = bundle.module
    farms_raw = _obs_get(obs, "farms") or []
    market_raw = _obs_get(obs, "market") or {}
    town_raw = _obs_get(obs, "town") or {}
    day = int(_obs_get(obs, "day", 0) or 0)
    hour = int(_obs_get(obs, "hour", 0) or 0)
    step = int(_obs_get(obs, "step", 0) or 0) or day * 24 + hour
    n = max(2, len(farms_raw))

    seats = []
    for i in range(n):
        obs_i = Observation()
        if i == int(player):
            obs_i.private = _copy_private(_obs_get(obs, "private") or {})
        else:
            obs_i.private = synth_opponent_private(module)
        obs_i.day = day
        obs_i.hour = hour
        obs_i.step = step if i == 0 else None
        obs_i.remainingOverageTime = float(
            _obs_get(obs, "remainingOverageTime", 60) or 60)
        seat = Seat(obs_i, i)
        seat.status = "ACTIVE"
        seats.append(seat)

    obs0 = seats[0].observation
    obs0.farms = [_copy_farm(f) for f in farms_raw]
    obs0.market = {
        "inventory": dict(market_raw.get("inventory", {})),
        "prices": dict(market_raw.get("prices", {})),
    }
    if "params" in market_raw:
        obs0.market["params"] = {
            item: dict(p) for item, p in market_raw["params"].items()}
    obs0.town = {"unlocked_shops": list(town_raw.get("unlocked_shops", []))}
    for i in range(1, len(seats)):
        o = seats[i].observation
        o.farms = obs0.farms
        o.market = obs0.market
        o.town = obs0.town
        o.day = obs0.day

    cfg = dict(DEFAULT_TWIN_CONFIGURATION)
    if configuration:
        cfg.update(configuration)
    cfg["seed"] = None                      # 种子只进 info（引擎事实表 §7）
    env = TwinEnv(Struct(cfg), int(seed), None, bundle.interpreter)
    state = TwinState(seats, env)
    env._state = state
    return state


def step(state, actions_both_seats):
    """推进一步（原地变更并返回 state）。actions_both_seats: [a0, a1]，
    可含 None（等价框架对非 ACTIVE 席传 None -> 解释器按 {} 处理）。
    镜像 core.py：解释器读 obs0.step（推进前值），框架随后写 step+1。"""
    if len(actions_both_seats) != len(state.seats):
        raise ValueError("actions 数与席位数不一致")
    for seat, action in zip(state.seats, actions_both_seats):
        seat.action = action
    state.env._state = state
    state.env.interpreter(state.seats, state.env)
    obs0 = state.seats[0].observation
    obs0.step = obs0.step + 1
    return state


def run_to_end(state, action_source, max_steps=None):
    """rollout 至终局。action_source 二选一：
      - 可迭代：逐转移产出 [a0, a1]（如回放动作流）；
      - 可回调：callable(state) -> [a0, a1]（P2 双席策略回调用法）。
    终止：env.done（全席非 ACTIVE，含解释器 step>=episodeSteps-2 置 DONE）
    或动作源耗尽或 max_steps 用尽。返回 state。"""
    if max_steps is None:
        max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    callable_source = callable(action_source)
    it = None if callable_source else iter(action_source)
    taken = 0
    while not state.env.done and taken < max_steps:
        actions = action_source(state) if callable_source else next(it, None)
        if actions is None:
            break
        step(state, actions)
        taken += 1
    return state


def final_money(state):
    """双席终局资金（解释器 reward 语义 = float(farms.money)）。"""
    return [float(f["money"]) for f in state.seats[0].observation.farms]


# --------------------------------------------------------------------------
# 回放 -> 孪生：状态重建
# --------------------------------------------------------------------------
def replay_transition_actions(replay):
    """动作流：steps[t] 记录的 action 驱动 t-1 -> t 转移（框架约定，与
    observer_v0_validator 同款解读）。返回列表，长度 = len(steps) - 1。"""
    steps = replay.get("steps") or []
    out = []
    for t in range(1, len(steps)):
        out.append([(steps[t][0] or {}).get("action"),
                    (steps[t][1] or {}).get("action")])
    return out


def build_state_from_replay(replay, step_index, bundle=None):
    """从回放第 0 步起按官方动作流前向重演至 step_index，返回该步的
    完整双席状态（等价于回放 steps[step_index] 的引擎态）。"""
    bundle = bundle or load_engine()
    if step_index < 0:
        raise ValueError("step_index 必须 >= 0")
    state = new_state_from_replay_head(replay, bundle)
    if step_index == 0:
        return state
    actions = replay_transition_actions(replay)
    if step_index > len(actions):
        raise ValueError(
            f"step_index={step_index} 超出可重演范围 {len(actions)}")
    for t in range(step_index):
        step(state, actions[t])
    return state


def rebuild_snapshots(replay, step_indices, bundle=None):
    """单次前向走子、多点快照（等价于对每点单独 build_state_from_replay，
    但只走一遍）。返回 {step_index: TwinState}（深克隆，互不影响）。"""
    bundle = bundle or load_engine()
    wanted = sorted(set(int(s) for s in step_indices))
    if not wanted:
        return {}
    state = new_state_from_replay_head(replay, bundle)
    actions = replay_transition_actions(replay)
    snapshots = {}
    cursor = 0
    for target in wanted:
        if target > len(actions):
            raise ValueError(
                f"step_index={target} 超出可重演范围 {len(actions)}")
        while cursor < target:
            step(state, actions[cursor])
            cursor += 1
        snapshots[target] = clone_state(state)
    return snapshots


# --------------------------------------------------------------------------
# 规范投影（与回放逐位比对的纯 JSON 形态）
# --------------------------------------------------------------------------
def _canon_tile(tile):
    if tile is None or tile == "LOCKED":
        return tile
    return {k: tile[k] for k in sorted(tile)}


def _canon_farm(farm):
    return {
        "money": float(farm["money"]),
        "tiles": [[_canon_tile(t) for t in row] for row in farm["tiles"]],
        "farmer": list(farm["farmer"]),
        "hands": [list(p) for p in farm.get("hands", [])],
        "unlocked_quadrants": list(farm["unlocked_quadrants"]),
        "hires_today": int(farm["hires_today"]),
    }


def _canon_private(private):
    private = private or {}
    return {
        "shed": {k: int(private.get("shed", {}).get(k, 0))
                 for k in sorted(private.get("shed", {}))},
        "seeds": {k: int(private.get("seeds", {}).get(k, 0))
                  for k in sorted(private.get("seeds", {}))},
        "inventories": [
            {k: int(v) for k, v in sorted(inv.items())}
            for inv in private.get("inventories", [])
        ],
    }


def _canon_market(market):
    market = market or {}
    out = {
        "inventory": {k: int(market["inventory"][k])
                      for k in sorted(market.get("inventory", {}))},
        "prices": {k: int(market["prices"][k])
                   for k in sorted(market.get("prices", {}))},
    }
    if "params" in market:
        out["params"] = {k: dict(sorted(market["params"][k].items()))
                         for k in sorted(market["params"])}
    return out


def state_to_canonical(state):
    """孪生状态的回放可比投影：共享态取 obs0 视角 + 双席 private。
    不含框架簿记字段（remainingOverageTime / status / reward / player）。"""
    obs0 = state.seats[0].observation
    return {
        "step": int(obs0.step),
        "day": int(obs0.day),
        "hour": int(obs0.hour),
        "farms": [_canon_farm(f) for f in obs0.farms],
        "market": _canon_market(obs0.market),
        "town": {"unlocked_shops": list(obs0.town["unlocked_shops"])},
        "private": [_canon_private(s.observation.private) for s in state.seats],
    }


def replay_canonical(replay, t):
    """回放第 t 步的同构投影（与 state_to_canonical 逐位可比）。
    step 取 seat0 观测（框架只写 seat0 的 obs.step；seat1 无该字段）。"""
    steps = replay.get("steps") or []
    obs0 = ((steps[t][0] or {}).get("observation")) or {}
    obs1 = ((steps[t][1] or {}).get("observation")) or {}
    market = obs0.get("market") or {}
    town = obs0.get("town") or {}
    canon = {
        "step": int(obs0.get("step", t) or t),
        "day": int(obs0.get("day", 0) or 0),
        "hour": int(obs0.get("hour", 0) or 0),
        "farms": [_canon_farm(f) for f in obs0["farms"]],
        "market": _canon_market(market),
        "town": {"unlocked_shops": list(town.get("unlocked_shops", []))},
        "private": [
            _canon_private(obs0.get("private")),
            _canon_private(obs1.get("private")),
        ],
    }
    if "params" in market:
        canon["market"]["params"] = {
            k: dict(sorted(market["params"][k].items()))
            for k in sorted(market["params"])}
    return canon


def _strict_equal(a, b):
    """型别敏感的深度相等（bool != int、int != float、3000 != 3000.0）。"""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        if len(a) != len(b):
            return False
        for key, val in a.items():
            if key not in b or not _strict_equal(val, b[key]):
                return False
        return True
    if isinstance(a, list):
        if len(a) != len(b):
            return False
        return all(_strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def first_difference(a, b, path="", limit=8):
    """两规范投影的型别敏感深度比对，返回前 limit 处差异
    [{path, twin, replay}, ...]；完全一致返回 []。"""
    diffs = []
    queue = [(a, b, path)]
    while queue and len(diffs) < limit:
        cur_a, cur_b, cur_path = queue.pop(0)
        if type(cur_a) is not type(cur_b):
            diffs.append({"path": cur_path or "<root>",
                          "twin": _short(cur_a), "replay": _short(cur_b)})
            continue
        if isinstance(cur_a, dict):
            for key in sorted(set(cur_a) | set(cur_b)):
                sub_path = f"{cur_path}.{key}"
                if key not in cur_a or key not in cur_b:
                    diffs.append({"path": sub_path,
                                  "twin": _short(cur_a.get(key)),
                                  "replay": _short(cur_b.get(key))})
                    if len(diffs) >= limit:
                        break
                else:
                    queue.append((cur_a[key], cur_b[key], sub_path))
        elif isinstance(cur_a, list):
            if len(cur_a) != len(cur_b):
                diffs.append({"path": f"{cur_path}#len",
                              "twin": len(cur_a), "replay": len(cur_b)})
                continue
            for i, (x, y) in enumerate(zip(cur_a, cur_b)):
                queue.append((x, y, f"{cur_path}[{i}]"))
        else:
            if cur_a != cur_b:
                diffs.append({"path": cur_path or "<root>",
                              "twin": _short(cur_a), "replay": _short(cur_b)})
    return diffs


def _short(value, width=90):
    try:
        text = json.dumps(value, sort_keys=True, default=repr)
    except (TypeError, ValueError):
        text = repr(value)
    return text if len(text) <= width else text[:width] + "..."


def states_bit_equal(state, replay, t):
    """孪生状态与回放第 t 步是否逐位一致（型别敏感）。
    返回 (ok, diffs)。diffs 为 first_difference 的规范投影差异。"""
    twin = state_to_canonical(state)
    truth = replay_canonical(replay, t)
    if _strict_equal(twin, truth):
        return True, []
    return False, first_difference(twin, truth)


def canonical_json(canon):
    """规范投影的确定性序列化（台账/快照比对辅助）。"""
    return json.dumps(canon, sort_keys=True, ensure_ascii=False)


# --------------------------------------------------------------------------
# 回放口径杂项（供 harness / P2 复用）
# --------------------------------------------------------------------------
def replay_final_rewards(replay):
    """回放终局真值：优先顶层 rewards，退化取末步 reward。"""
    rewards = replay.get("rewards")
    if rewards is not None:
        return list(rewards)
    last = (replay.get("steps") or [None])[-1]
    if not last:
        return []
    return [(last[seat] or {}).get("reward") for seat in range(len(last))]


def money_bit_hex(value):
    """float 的位型（逐位相等台账用）。"""
    return struct.pack(">d", float(value)).hex()
