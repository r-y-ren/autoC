"""Win rate against the engine's built-in agents, measured in the real engine.

The simulator only models policy-driven opponents (see docs/DESIGN.md), so the
`starter` / `pass` / `random` benchmark deliberately runs against
kaggle_environments itself. Every seed is played in both seats, so seat bias
cannot flatter the result -- unless `--seats 1` says otherwise, which is only
sound on a board where the seat cannot change the outcome (a pinned
`--with-town` replay).
"""
import argparse, atexit, contextlib, csv, json, os, re, shutil, sys, tarfile, tempfile, time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, "src")
# Appended, not prepended: the only thing this entry serves is the sibling
# `plan_stats` import below, whose name is unique to this repo, and a
# scripts/ directory at sys.path[0] would shadow any stdlib or site-packages
# module that happens to share a name with a file in it.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import plan_stats

_SRC = os.path.abspath("src")

from kagg3 import spec

THETA_PATH = os.path.join("artifacts", "theta.npy")

#: `--csv` columns. `scripts/paired_ci.py` reads them by name off this header.
#: `moves`..`quads` are the engine-replay half of section 7's operational
#: metrics; `--stats` appends the planner-side half (`plan_stats.FIELDS`).
CSV_HEADER = ("seed", "opponent", "seat", "mine", "theirs",
              "moves", "move_turns", "noops", "unsold", "quads")

#: Unit actions that spend a turn walking. `moves` sums them over the seat's
#: units, `move_turns` counts the turns in which at least one unit walked --
#: section 7's "walking turns" is the latter (a turn is the resource; eleven
#: units walking in one turn is one walking turn, not eleven).
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")

#: `unsold` sums only the nine market products. The engine's `private.shed`
#: also carries GOOSE/COW/SHEEP, which are livestock the shed stores and not
#: terminal inventory that failed to sell; FERTILIZER *is* a product and stays.
PRODUCT_NAMES = frozenset(spec.PRODUCTS)


#: The stride between one opponent's seed base and the next under
#: `--seed-per-opponent`. A prime well clear of `--games` so that no two
#: opponents' bases can coincide, and so that the bases of `--seed-base` and
#: `--seed-base + 1` (the real gate's replicate pair) stay disjoint too.
SEED_STRIDE = 1000003


def seed_lists(seed_base, games, n_opponents, per_opponent=False):
    """The seed list each `--opponents` member is played on, in that order.

    Off (the default), every opponent gets *the same* list -- the draw this
    script has always made -- so a run is byte-identical to the one before the
    flag existed.

    On, opponent `i` (0-based) draws from `seed_base + SEED_STRIDE * (i + 1)`,
    which is deterministic in both, distinct per opponent, and -- because the
    offset starts at one stride, not zero -- never the legacy list. A leg of
    `k` opponents then samples `games * k` distinct seeds instead of `games`:
    the per-seed paired win difference between two thetas has an sd of ~0.165
    across seeds and correlates only weakly across opponents (r 0.1-0.4), so
    9 opponents x 12 seeds x 2 seats carries +/-4.8 points of seed noise while
    sampling twelve seeds, and +/-1.6 while sampling 108 of them. Same games,
    same wall clock.
    """
    legacy = np.random.default_rng(seed_base).integers(0, 2 ** 31 - 1, games)
    if not per_opponent:
        return [legacy] * n_opponents
    return [np.random.default_rng(seed_base + SEED_STRIDE * (i + 1))
            .integers(0, 2 ** 31 - 1, games)
            for i in range(n_opponents)]


def opponent_episode_id(opponent):
    """Return the episode id embedded in an opponent-tape path, if any."""
    match = re.search(r"opponent_tape_(\d+)(?:/|$)", str(opponent))
    return match.group(1) if match else None


def seeds_from_file(path, opponents, games):
    """Read exact per-opponent seeds from ``KEY SEED`` lines.

    KEY is normally the episode id embedded in ``opponent_tape_<id>/main.py``;
    an exact opponent string is also accepted, which makes the interface useful
    for built-in agents and small tests.  A seed file describes one live board
    per opponent, so it deliberately refuses ``--games`` other than one.
    Extra keys are allowed: gates can take a prefix/subset of a canonical live
    sidecar without rewriting it.
    """
    if games != 1:
        raise ValueError("--seed-file requires --games 1 (one recorded seed per episode)")
    mapping = {}
    with open(path) as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.partition("#")[0].strip()
            if not line:
                continue
            fields = line.split()
            if len(fields) != 2:
                raise ValueError(f"{path}:{lineno}: expected KEY SEED")
            key, value = fields
            if key in mapping:
                raise ValueError(f"{path}:{lineno}: duplicate seed key {key}")
            try:
                seed = int(value)
            except ValueError as exc:
                raise ValueError(f"{path}:{lineno}: invalid seed {value!r}") from exc
            if not 0 <= seed < 2 ** 31:
                raise ValueError(f"{path}:{lineno}: seed outside [0, 2**31): {seed}")
            mapping[key] = seed

    out = []
    missing = []
    for opponent in opponents:
        episode = opponent_episode_id(opponent)
        keys = ([episode] if episode is not None else []) + [str(opponent)]
        found = [mapping[key] for key in keys if key in mapping]
        if not found:
            missing.append(episode or str(opponent))
        elif len(set(found)) != 1:
            raise ValueError(f"{path}: conflicting seeds for opponent {opponent}")
        else:
            out.append(np.asarray([found[0]], dtype=np.int64))
    if missing:
        raise ValueError(f"{path}: missing seeds for {', '.join(missing[:5])}")
    return out


def _is_file_agent(a):
    return isinstance(a, str) and a.endswith(".py")


#: What `package_submission.py` writes, and what the Kaggle upload wants: a
#: gzipped tar with `main.py` at its root. The engine loader cannot read one.
ARCHIVE_SUFFIXES = (".tar.gz", ".tgz", ".tar")


def _unpack_agent(path):
    """The `main.py` the engine can exec for the `--me` argument.

    A string agent is handed to `kaggle_environments` verbatim, and its loader
    reads *any* existing path as Python source. Point it at a `.tar.gz` and the
    gzip bytes fail to compile; `build_agent` swallows the SyntaxError inside
    the per-turn wrapper and falls back to returning the raw string, which the
    engine records as no action at all -- status stays DONE, `step.action` is
    not a dict, and the seat finishes the game on its untouched starting 3000
    coins. Measured 2026-09-04 with `dist/submission_flow58_g450_pump.tar.gz`,
    a package that was live on Kaggle at the time: every seed came back
    3000 vs 3000, against every opponent, at any `--workers`.

    So unpack the archive here -- once, in the parent, before the jobs are
    built -- and seat the `main.py` inside it. That is also what makes
    `_is_file_agent` recognise a packaged agent at all, and with it the whole
    `_vendored_imports` guard: a `.tar.gz` matched none of it either.

    A plain `main.py` path is returned unchanged. Anything else that is neither
    is refused loudly rather than quietly scoring 3000.
    """
    if path.endswith(ARCHIVE_SUFFIXES):
        d = tempfile.mkdtemp(prefix="eval_me_")
        atexit.register(shutil.rmtree, d, True)
        with tarfile.open(path) as tf:
            tf.extractall(d)
        main = os.path.join(d, "main.py")
        if not os.path.isfile(main):
            raise SystemExit(f"--me: {path} has no main.py at its root")
        path = main
    if not _is_file_agent(path) or not os.path.isfile(path):
        raise SystemExit(f"--me: {path} is neither a main.py nor a "
                         + "/".join(ARCHIVE_SUFFIXES) + " package")
    return path


#: Prefix of the environment variables this repo's agent code reads. Only
#: `KAGG3_OPENING` today (`kagg3/agent/opening.py`), but the rule is the
#: namespace, not the one name: a packaged agent's configuration and ours must
#: not see each other, whatever gets added next.
ENV_PREFIX = "KAGG3_"


def _kagg3_path_entries(path):
    """The `path` entries a plain `import kagg3` could resolve to.

    `_SRC` is the usual one and used to be assumed the only one, but the
    editable install writes the *checkout's* `src` into site-packages as a
    `.pth`, so inside a git worktree there are two: the worktree's `src` at
    `sys.path[0]` and the main checkout's, which an `abspath(p) != _SRC`
    comparison happily keeps. Ask the question the import system asks instead.
    """
    hidden = set()
    for p in path:
        d = os.path.join(p or os.curdir, "kagg3")
        if os.path.abspath(p) == _SRC or os.path.isdir(d) or os.path.isfile(d + ".py"):
            hidden.add(p)
    return hidden


@contextlib.contextmanager
def _vendored_imports(active):
    """Hide this repo's `kagg3` -- modules, path and environment -- for the
    duration of a game that seats a packaged agent.

    Three things have to be swapped out and put back, because a packaged
    submission is a whole second copy of this repo and every channel between
    the two images corrupts a measurement in one direction or the other.

    `sys.modules`. A packaged `main.py` puts its own directory on `sys.path`
    and then does a plain `from kagg3 import ...`. If this process has already
    imported the working tree's `kagg3` -- and it has, `plan_stats` does it at
    import -- that import is a no-op and the packaged agent silently runs the
    *current* planner against its own frozen theta. Measured, not theorised:
    the Phase-1 submission scores 11,979 coins on seed 2104521678 with the
    tree's `kagg3` loaded and 28,431 with its own. Dropping the modules for the
    length of the game makes the packaged agent's import resolve next to its
    `main.py`; agents already built here keep working, because they hold module
    objects rather than re-importing (nothing under `kagg3/agent` or
    `kagg3/core` imports lazily).

    `sys.path`. Dropping the modules is not enough on its own. The engine
    loader *appends* the agent's directory to `sys.path` while it execs
    `main.py`, and the packaged `main.py` only prepends its own directory when
    it is not already there -- so with a `kagg3` still importable from this
    process's path, the packaged `from kagg3 import ...` resolved to the
    working tree again (caught 2026-08-30: a pre-DROP package emitted DROP).
    Hide every entry a `kagg3` would come from, so the only one importable
    during the game is the one beside `main.py`.

    `os.environ`. A packaged agent that ships an opening tape reaches the
    splice through a variable, not an import: `package_submission.py` emits
    `os.environ.setdefault("KAGG3_OPENING", <its own tape>)` at the top of
    `main.py`, because the spec has to land before the agent object is built.
    That write outlived the game, and the *next* game the worker played built
    our seat through `runtime.make_agent` -> `opening.from_env`, which read it
    and spliced the opponent's opening in front of the candidate theta (caught
    2026-09-03: with `panel_opp/open16_pkg` in `--opponents`, our seed-479691604
    row went 66,609 -> 149,629 coins and the panel's win rate went 17% -> 100%).
    The same variable travels the other way too -- an opening we set for our own
    seat would win the packaged agent's `setdefault` and replace the tape it
    ships. So `KAGG3_*` is cleared on the way in and the whole environment is
    put back on the way out: the packaged agent plays as shipped, and nothing
    it configures survives the game.

    Our own seat is unaffected by all three, whichever way they are set: `_play`
    builds it before this context opens.
    """
    if not active:
        yield
        return
    ours = {k: v for k, v in sys.modules.items() if k == "kagg3" or k.startswith("kagg3.")}
    path = list(sys.path)
    env = dict(os.environ)
    for k in ours:
        del sys.modules[k]
    hidden = _kagg3_path_entries(path)
    sys.path[:] = [p for p in path if p not in hidden]
    for k in [k for k in os.environ if k.startswith(ENV_PREFIX)]:
        del os.environ[k]
    try:
        yield
    finally:
        for k in [k for k in sys.modules if k == "kagg3" or k.startswith("kagg3.")]:
            del sys.modules[k]
        sys.modules.update(ours)
        sys.path[:] = path
        # Touch only what the game actually changed: `os.environ` writes go
        # through `putenv`, and a blanket rewrite would churn every variable in
        # the process once per game for nothing.
        for k in [k for k in os.environ if k not in env]:
            del os.environ[k]
        for k, v in env.items():
            if os.environ.get(k) != v:
                os.environ[k] = v


def _replay_metrics(steps, seat):
    """(moves, move_turns, noops, unsold, quads) for one seat of a finished game.

    `moves` counts MOVE ops summed over the seat's units; `move_turns` counts
    the turns in which at least one of them walked, which is section 7's
    "walking turns" as a resource.

    The engine reports nothing about rejected *orders* -- illegal unit actions
    are documented silent no-ops and `info` stays empty -- so a wasted turn is
    read off the replay instead: the seat asked for something (a non-PASS unit
    action or a market order) and neither its farm nor its private state moved
    between the two recorded steps. That is a floor, not an exact count: an
    end-of-day tick or a plant decaying on the same turn masks the no-op.

    A whole action the engine refused is a different case and is counted
    exactly: `step.action` is then not a dict at all (`None`), which is what
    the engine records for status INVALID / ERROR / TIMEOUT. That turn asked
    for a day's worth of work and got none of it, so it counts as a no-op --
    and it walked nowhere, so it adds nothing to `moves` or `move_turns`.
    """
    moves = move_turns = noops = 0
    for t in range(1, len(steps)):
        prev, cur = steps[t - 1][seat], steps[t][seat]
        if not isinstance(cur.action, dict):
            noops += 1
            continue
        act = cur.action
        units = [act.get("farmer") or []] + list(act.get("hands") or [])
        walked = sum(1 for u in units if u and u[0] in MOVES)
        moves += walked
        move_turns += 1 if walked else 0
        asked = (act.get("market") or []) or [u for u in units if u and u[0] != "PASS"]
        if asked and (cur.observation["farms"][seat] == prev.observation["farms"][seat]
                      and cur.observation["private"] == prev.observation["private"]):
            noops += 1
    last = steps[-1][seat].observation
    unsold = sum(int(v) for k, v in last["private"]["shed"].items() if k in PRODUCT_NAMES)
    return (moves, move_turns, noops, unsold,
            len(last["farms"][seat]["unlocked_quadrants"]))


def _write_replay(env, out_dir, seed, seat, opponent):
    """Dump a finished game as Kaggle-replay-shaped JSON for `replay_profile.py`.

    Two deltas from `env.toJSON()`, both so the profiler can read the file
    straight off disk. `specification` goes, because it is a constant schema
    blob no reader here looks at. And `info.TeamNames` is filled in, because
    that is how the profiler names the seats and the engine leaves `info`
    holding nothing but the seed -- our seat is `ours`, whichever seat it is,
    so `--ours ours` finds it in both halves of a seed pair.
    """
    j = env.toJSON()
    j.pop("specification", None)
    names = ["ours", opponent] if seat == 0 else [opponent, "ours"]
    j["info"] = dict(j.get("info") or {}, TeamNames=names)
    with open(os.path.join(out_dir, f"{int(seed)}_{seat}.json"), "w") as fh:
        json.dump(j, fh, separators=(",", ":"))


def arm_residual(head_npz, head_py=None):
    """Arm the residual action head on the evaluated seat [ACTIONRL/ESHEAD].

    `--residual` is the `--theta` seat's half of what the SUBMISSION does:
    `package_submission.py` writes `_plan.RESIDUAL_ON = True` and
    `_plan.RESIDUAL_HEAD = <archive>/residual_head.npz` into the package's
    `main.py`, so a theta judged without this flag is judged as a DIFFERENT
    agent than the one the tarball ships.  `plan.residual_on()` is called here,
    in the worker's own process and BEFORE any game starts, for two reasons:
    it fails loudly at arming time if the head is missing or the wrong width,
    and `_vendored_imports` strips the `KAGG3_*` environment for the duration
    of a game -- so the lazy `KAGG3_RESIDUAL_HEAD_PY` lookup inside
    `plan._residual_head_module` must already have happened.

    The opponent is untouched: a packaged file agent plans inside its own
    module image (`_vendored_imports`), so this working tree's `plan` module
    is our seat and our seat alone.
    """
    from kagg3.core import plan as _plan
    if head_py:
        os.environ["KAGG3_RESIDUAL_HEAD_PY"] = os.path.abspath(head_py)
    _plan.RESIDUAL_ON = True
    _plan.RESIDUAL_HEAD = os.path.abspath(head_npz)
    _plan.RESIDUAL_FN = None                      # rebuild, never inherit one
    if not _plan.residual_on():
        raise SystemExit(f"--residual {head_npz}: the head did not arm")


def _assert_town_prefix(steps, schedule):
    """Fail if any recorded observation differs from an explicitly pinned town."""
    table, unlocked = {}, []
    for day, shop in sorted(schedule, key=lambda row: int(row[0])):
        unlocked = unlocked + [str(shop)]
        table[int(day)] = list(unlocked)
    for step in steps:
        for state in step:
            obs = state.observation
            day = int(obs.get("day", int(obs.get("step", 0)) // 24))
            keys = [d for d in table if d <= day]
            want = table[max(keys)] if keys else []
            got = list((obs.get("town") or {}).get("unlocked_shops", []))
            if got != want:
                raise AssertionError(
                    f"town prefix mismatch at day {day}: got {got!r}, want {want!r}")


def _play(args):
    if len(args) == 7:
        seed, opponent, seat, theta_path, want_stats, me_path, replay_dir = args
        town_schedule = None
    else:
        (seed, opponent, seat, theta_path, want_stats, me_path, replay_dir,
         town_schedule) = args
    from kaggle_environments import make

    # Opt-in, off unless `KAGG3_TOWN_SCHEDULE` names a file: pin the engine's
    # end-of-day town unlock to a recorded schedule instead of letting it draw.
    # Nothing under site-packages is edited -- `town_inject` rebinds the
    # engine module's `_end_of_day` name and overwrites `unlocked_shops` after
    # the original has run, so the RNG cursor, the weeds and every other rule
    # are untouched. Scoring is not involved either way. It has to happen here,
    # before `_vendored_imports` clears the `KAGG3_*` namespace for the game,
    # and it is keyed on the opponent so one run can play several tapes each
    # under its own town. See scripts/town_inject.py.
    import town_inject
    town_inject.install_from_env(opponent)
    if town_schedule is not None:
        town_inject.install(town_schedule)

    days = []
    if me_path:
        # A packaged submission, handed to the engine as a file agent (the same
        # way the opponents are). It plans inside its own module image, so
        # there is no DayView here to replay and the planner-side columns stay
        # empty -- the engine-replay columns are read off the steps as usual.
        me = me_path
    else:
        # Imported here, not at module scope: a packaged file agent runs inside
        # its own module image (`_vendored_imports`) and never touches this
        # runtime, and importing it eagerly would pull the working tree's
        # `kagg3.agent` into every worker for nothing.
        from kagg3.agent import runtime
        macro = plan_stats.make_macro(np.load(theta_path).astype(np.float32))
        if want_stats:
            macro = plan_stats.collect(macro, days)
        me = runtime.make_agent(macro, pass_prev_mkt_inv=True)

    env = make("kaggriculture", configuration={"seed": int(seed)})
    agents = [me, opponent] if seat == 0 else [opponent, me]
    with _vendored_imports(any(_is_file_agent(a) for a in agents)):
        env.run(agents)
    if town_schedule is not None:
        _assert_town_prefix(env.steps, town_schedule)
    if replay_dir:
        _write_replay(env, replay_dir, seed, seat, opponent)
    money = [f["money"] for f in env.steps[-1][0].observation["farms"]]
    mine, theirs = (money[0], money[1]) if seat == 0 else (money[1], money[0])
    win = 1.0 if mine > theirs else (0.5 if mine == theirs else 0.0)
    stats = () if not want_stats else (("", "", "") if me_path else plan_stats.totals(days))
    return (win, mine, theirs) + _replay_metrics(env.steps, seat) + stats


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theta", default=None,
                    help=f"policy checkpoint for the evaluated seat (default {THETA_PATH})")
    ap.add_argument("--me", help="run a packaged agent as the evaluated seat instead of "
                                 "--theta -- either a submission " + "/".join(ARCHIVE_SUFFIXES)
                                 + " or the main.py inside one; the planner-side --stats "
                                   "columns are then empty")
    ap.add_argument("--games", type=int, default=40, help="seeds per opponent (x --seats)")
    ap.add_argument("--seats", type=int, choices=(1, 2), default=2,
                    help="how many seats of every seed to play. 2 (default) "
                         "is the run this script always did: each seed is "
                         "played once in seat 0 and once in seat 1, so seat "
                         "bias cancels within the pair. 1 plays seat 0 only, "
                         "which halves the wall clock and is only sound when "
                         "the seat cannot change the outcome -- a pinned "
                         "--with-town replay (KAGG3_TOWN_SCHEDULE), where the "
                         "board is deterministic and both seats return the "
                         "same coins, so the second one is a re-measurement.")
    ap.add_argument("--residual", default=None, metavar="HEAD_NPZ",
                    help="arm the residual action head on the --theta seat, "
                         "exactly as the packaged submission arms it "
                         "(package_submission.py --residual). Without this "
                         "flag a theta trained with a head is judged as a "
                         "different agent than the tarball ships.")
    ap.add_argument("--residual-head-py", default=None, metavar="HEAD_PY",
                    help="the head module to import (default: the checkout's "
                         "S/actionrl/head.py, via KAGG3_RESIDUAL_HEAD_PY)")
    ap.add_argument("--opponents", nargs="*", default=["starter", "random", "pass"])
    ap.add_argument("--workers", type=int, default=os.cpu_count() // 2)
    ap.add_argument("--csv", help="write one row per game: " + ",".join(CSV_HEADER))
    ap.add_argument("--replay-dir",
                    help="also dump every finished game's engine JSON to "
                         "DIR/<seed>_<seat>.json, in the shape "
                         "scripts/replay_profile.py reads")
    # The discovery seeds are this default's draws; a held-out set is another
    # base (section 7 wants the two disjoint).
    ap.add_argument("--seed-base", type=int, default=20260821)
    ap.add_argument("--seed-per-opponent", action="store_true",
                    help="draw a SEPARATE seed list per opponent (seed_base + "
                         + str(SEED_STRIDE) + "*(i+1) for the i-th "
                         "--opponents entry) instead of playing every opponent "
                         "on the same --games seeds. A leg of k opponents then "
                         "samples games*k distinct seeds rather than games, "
                         "which is where its noise comes from; the games, the "
                         "wall clock and the CSV shape are unchanged. Off by "
                         "default: two CSVs are only paired on (seed, seat) if "
                         "they were drawn the same way.")
    ap.add_argument("--seed-file", metavar="PATH",
                    help="use the exact recorded seed for each opponent from "
                         "KEY SEED lines (KEY is the episode id in an "
                         "opponent_tape_<id> path). Requires --games 1 and "
                         "replaces --seed-base/--seed-per-opponent.")
    ap.add_argument("--stats", action="store_true",
                    help="also collect the planner-side metrics ("
                         + ",".join(plan_stats.FIELDS)
                         + "); needs --csv or --print-stats to go anywhere")
    ap.add_argument("--print-stats", action="store_true",
                    help="print the per-opponent means of the --stats metrics")
    args = ap.parse_args()

    # The two ways to seat our own agent are exclusive; a file agent wins,
    # because naming one is the more specific request.
    if args.me and args.theta:
        print(f"note: --me {args.me} overrides --theta {args.theta}")
    theta = None if args.me else (args.theta or THETA_PATH)
    # The label stays the path the user typed; the workers get the `main.py`.
    label = args.me or theta
    me = _unpack_agent(args.me) if args.me else None

    # Collecting the planner-side metrics replays `build_day_stats` for every
    # planned day inside the game loop and costs about 30% of the wall clock,
    # so it is paid only when something actually reads it.
    want_stats = args.stats and (bool(args.csv) or args.print_stats)
    if args.stats and not want_stats:
        print("note: --stats has no reader (no --csv, no --print-stats); not collecting")

    if args.replay_dir:
        os.makedirs(args.replay_dir, exist_ok=True)

    if args.seed_file and args.seed_per_opponent:
        ap.error("--seed-file replaces --seed-per-opponent; do not pass both")
    try:
        per_opponent = (seeds_from_file(args.seed_file, args.opponents, args.games)
                        if args.seed_file else
                        seed_lists(args.seed_base, args.games, len(args.opponents),
                                   args.seed_per_opponent))
    except (OSError, ValueError) as exc:
        ap.error(str(exc))
    jobs = [(s, o, seat, theta, want_stats, me, args.replay_dir)
            for o, seeds in zip(args.opponents, per_opponent)
            for s in seeds for seat in range(args.seats)]

    # `--residual`: arm every worker at start-up (an initializer, so the flag
    # is sound under `fork` and under `spawn` alike), and the parent too, so a
    # broken head raises here rather than 2 x --games games later.
    init, initargs = None, ()
    if args.residual:
        if args.me:
            raise SystemExit("--residual applies to the --theta seat; --me is "
                             "a packaged agent that already carries its own")
        arm_residual(args.residual, args.residual_head_py)
        init, initargs = arm_residual, (args.residual, args.residual_head_py)
        print(f"residual: head {args.residual} armed on the --theta seat",
              flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(args.workers, initializer=init,
                             initargs=initargs) as ex:
        res = list(ex.map(_play, jobs))

    if args.csv:
        with open(args.csv, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(CSV_HEADER + (plan_stats.FIELDS if want_stats else ()))
            for (seed, opponent, seat, *_), r in zip(jobs, res):
                w.writerow([int(seed), opponent, seat, *r[1:]])

    print(f"{len(jobs)} games in {time.time()-t0:.0f}s  agent={label}")
    # Column order after (win, mine, theirs): `_replay_metrics`'s five, then
    # `plan_stats.FIELDS` when they were collected.
    n_head = 3
    replay_names = CSV_HEADER[5:]
    i = 0
    for o in args.opponents:
        n = args.games * args.seats
        chunk = res[i:i + n]; i += n
        w = np.mean([c[0] for c in chunk])
        margin = np.mean([c[1] - c[2] for c in chunk])
        mine = np.mean([c[1] for c in chunk])
        diffs = np.array([c[1] - c[2] for c in chunk])
        print(f"  vs {o:8s}  win {w*100:5.1f}%   mean coins {mine:9.0f}   "
              f"mean margin {margin:+9.0f}   sd {diffs.std():6.0f}   "
              f"worst {diffs.min():+8.0f}   (n={n})")
        if args.print_stats:
            cols = list(replay_names) + (list(plan_stats.FIELDS) if want_stats else [])
            means = []
            for k, name in enumerate(cols):
                vals = [c[n_head + k] for c in chunk]
                if any(v == "" for v in vals):      # a packaged --me agent leaves them blank
                    means.append(f"{name}=-")
                else:
                    means.append(f"{name}={np.mean([float(v) for v in vals]):.1f}")
            print("            " + "  ".join(means))
